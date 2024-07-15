import xml.etree.ElementTree as ET
from zipfile import ZipFile
import geometryObjects as gobj
import component as comp
import board, pin
from abstractShape import Shape

class VisecadLoader():
    def __init__(self):
        self.boardData = board.Board()

    def loadFile(self, filePath:str) -> list[str]:
        fileLines = self._getFileLines(filePath)
        return fileLines
    
    def processFileLines(self, fileLines:list[str]) -> board.Board:
        rootXML = self._parseXMLFromFileLines(fileLines)
        outlinesLayers = self._getOutlinesLayers(rootXML)
        pinsAngleShapesIDDict = self._processNetsTag(rootXML, self.boardData)
        shapesDict, padstackDict, pcbXML = self._processGeometriesTag(rootXML)
        self._getBoardOutlines(pcbXML, self.boardData, outlinesLayers)
        
        return self.boardData
    
    def _getFileLines(self, filePath:str) -> list[str]:
        fileLines = []
        with ZipFile(filePath, 'r') as zippedFile:
            xmlFileName = zippedFile.namelist()[0]
            with zippedFile.open(xmlFileName) as xmlFile:
                fileLines = [line.decode('utf-8') for line in xmlFile.readlines()]
        return fileLines

    def _parseXMLFromFileLines(self, fileLines:list[str]) -> 'xml.etree.ElementTree':
        return ET.fromstring(''.join(fileLines))
    
    def _getOutlinesLayers(self, rootXML:ET) -> list[str]:
        layersXML = rootXML.find('Layers')

        outlineLayers = []
        for child in layersXML:
            if 'OUTLINE' in child.attrib['name'].upper():
                outlineLayers.append(child.attrib['num'])
        return outlineLayers

    def _processNetsTag(self, rootXML:ET, boardInstance:board.Board) -> None:
        try:
            filesXML = rootXML.find('Files').find('File').find('Nets')
        except AttributeError:
            return
        
        componentsDict = {}
        shapesIDDict = {}
        netsDict = {}
        
        for netXML in filesXML.findall('Net'):
            netName = netXML.attrib['name']
            netsDict[netName] = {}

            for compPinXML in netXML:
                try:
                    pinInstance = self._createPin(compPinXML)
                except KeyError:
                    continue
                
                self._getPinPadstackAngleInPlace(compPinXML, pinInstance, shapesIDDict)
                componentInstance = self._processComponentDataInNets(compPinXML, componentsDict, pinInstance)
                componentName = componentInstance.name

                if not componentName in netsDict[netName]:
                    netsDict[netName][componentName] = {'componentInstance': None, 'pins':[]}
                netsDict[netName][componentName]['componentInstance'] = componentInstance
                netsDict[netName][componentName]['pins'].append(pinInstance.name)

        boardInstance.setNets(netsDict)
        boardInstance.setComponents(componentsDict)
        return shapesIDDict

    def _processGeometriesTag(self, rootXML:ET) -> tuple[dict, dict, 'xml.etree.ElementTree']:
        geometriesXML = rootXML.find('Geometries')
        
        shapesXMLDict = {}
        padstackDict = {}
        pcbXML = ET.fromstring("<Init><Datas></Datas></Init>")
        for child in geometriesXML.findall('Geometry'):
            branchID = child.attrib['num']
            if 'sizeA' in child.attrib:
                shapesXMLDict[branchID] = child
            elif len(child) > 0:
                if len(child.find('Datas')) > len(pcbXML.find('Datas')):
                    pcbXML = child
                padstackDict[branchID] = child
        
        padstackDict.pop(pcbXML.attrib['num'])
        return shapesXMLDict, padstackDict, pcbXML

    def _getBoardOutlines(self, pcbXML:ET, boardInstance:board.Board, outlinesLayers:list[str]):
        polyStructsXML = [child for child in pcbXML.find('Datas').findall('PolyStruct') if child.attrib['layer'] in outlinesLayers]

        outlinesList = []
        for polyStructXML in polyStructsXML:
            outlinesList += self._processPolyStruct(polyStructXML)
        boardInstance.setOutlines(outlinesList)

    def _createPin(self, rootXML:ET) -> pin.Pin:
        pinID = rootXML.attrib['pin']

        pinX = gobj.floatOrNone(rootXML.attrib['x'])
        pinY = gobj.floatOrNone(rootXML.attrib['y'])
        coordsPoint = gobj.Point(pinX, pinY)

        newPin = pin.Pin(pinID)
        newPin.setCoords(coordsPoint)
        return newPin
    
    def _getPinPadstackAngleInPlace(self, rootXML:ET, pinInstance:pin.Pin, shapesIDDict:dict):
        pinAngle = rootXML.attrib['rotation']
        padShapeID = rootXML.attrib['padstackGeomNum']

        if padShapeID not in shapesIDDict:
            shapesIDDict[padShapeID] = []
        shapesIDDict[padShapeID].append([pinInstance, pinAngle])
    
    def _processComponentDataInNets(self, rootXML:ET, componentsDict:dict, pinInstance:pin.Pin) -> comp.Component:
        componentName = rootXML.attrib['comp']
        if componentName not in componentsDict:
            self._createComponentInPlace(rootXML, componentName, componentsDict)

        componentInstance = componentsDict[componentName]
        componentInstance.addPin(pinInstance.name, pinInstance)
        return componentInstance
    
    def _createComponentInPlace(self, rootXML:ET,  componentName:str, componentsDict:dict):
        mountingType = self._getComponentMountingType(rootXML)
        newComponent = comp.Component(componentName)
        newComponent.setMountingType(mountingType)
        componentsDict[componentName] = newComponent

    def _getComponentMountingType(self, attribRootXML:ET) -> str:
        mountDict = {'SMD': 'SMT', 'SMT':'SMT', 'THRU':'TH', 'TH':'TH'}
        for child in attribRootXML:
            if child.tag == 'Attrib' and 'val' in child.attrib and child.attrib['val'].upper() in mountDict:
                val = child.attrib['val']
                return mountDict[val]
    
    def _processPolyStruct(self, polyStructXML:ET) -> list[gobj.Line|gobj.Arc]:
        pointsXML = polyStructXML.find('Poly').findall('Pnt')
        previousPoint = None
        shapesList = []
        for pointXML in pointsXML:
            if 'bulge' in pointXML.attrib:
                continue
            x = gobj.floatOrNone(pointXML.attrib['x'])
            y = gobj.floatOrNone(pointXML.attrib['y'])
            currentPoint = gobj.Point(x, y)
            
            if previousPoint:
                shapesList.append(gobj.Line(previousPoint, currentPoint))
            previousPoint = currentPoint
        return shapesList


if __name__ == '__main__':
    def openSchematicFile() -> str:        
        from tkinter import filedialog
        filePath = filedialog.askopenfile(mode='r', filetypes=[('*', '*')])
        return filePath.name

    filePath = openSchematicFile()

    loader = VisecadLoader()
    fileLines = loader.loadFile(filePath)
    loader.processFileLines(fileLines)