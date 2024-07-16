import xml.etree.ElementTree as ET
from zipfile import ZipFile
import math
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
        shapesIDToPinAngleDict = self._processNetsTag(rootXML, self.boardData)
        shapesXMLDict, padstackXMLDict, pcbXML = self._processGeometriesTag(rootXML)
        self._getBoardOutlines(pcbXML, self.boardData, outlinesLayers)
        shapesIDToComponentDict = self._updateComponents(pcbXML, self.boardData)
        
        return self.boardData
    
    def _getFileLines(self, filePath:str) -> list[str]:
        fileLines = []
        with ZipFile(filePath, 'r') as zippedFile:
            xmlFileName = zippedFile.namelist()[0]
            with zippedFile.open(xmlFileName) as xmlFile:
                fileLines = [line.decode('utf-8') for line in xmlFile.readlines()]
        return fileLines

    def _parseXMLFromFileLines(self, fileLines:list[str]) -> ET.ElementTree:
        return ET.fromstring(''.join(fileLines))
    
    def _getOutlinesLayers(self, rootXML:ET) -> list[str]:
        layersXML = rootXML.find('Layers')

        outlineLayers = []
        for child in layersXML:
            if 'OUTLINE' in child.attrib['name'].upper():
                outlineLayers.append(child.attrib['num'])
        return outlineLayers

    def _processNetsTag(self, rootXML:ET.ElementTree, boardInstance:board.Board) -> dict:
        try:
            filesXML = rootXML.find('Files').find('File').find('Nets')
        except AttributeError:
            return
        
        componentsDict = {}
        shapesIDToPinAngleDict = {}
        netsDict = {}
        
        for netXML in filesXML.findall('Net'):
            netName = netXML.attrib['name']
            netsDict[netName] = {}

            for compPinXML in netXML:
                try:
                    pinInstance = self._createPin(compPinXML)
                except KeyError:
                    continue
                
                self._getPinPadstackAngleInPlace(compPinXML, pinInstance, shapesIDToPinAngleDict)
                componentInstance = self._processComponentDataInNets(compPinXML, componentsDict, pinInstance)
                componentName = componentInstance.name

                if not componentName in netsDict[netName]:
                    netsDict[netName][componentName] = {'componentInstance': None, 'pins':[]}
                netsDict[netName][componentName]['componentInstance'] = componentInstance
                netsDict[netName][componentName]['pins'].append(pinInstance.name)

        boardInstance.setNets(netsDict)
        boardInstance.setComponents(componentsDict)
        return shapesIDToPinAngleDict

    def _processGeometriesTag(self, rootXML:ET.ElementTree) -> tuple[dict, dict, ET.ElementTree]:
        geometriesXML = rootXML.find('Geometries')
        
        shapesXMLDict = {}
        padstackXMLDict = {}
        pcbXML = ET.fromstring("<Init><Datas></Datas></Init>")
        for child in geometriesXML.findall('Geometry'):
            branchID = child.attrib['num']
            if 'sizeA' in child.attrib:
                shapesXMLDict[branchID] = child
            elif len(child) > 0:
                if len(child.find('Datas')) > len(pcbXML.find('Datas')):
                    pcbXML = child
                padstackXMLDict[branchID] = child
        
        padstackXMLDict.pop(pcbXML.attrib['num'])
        return shapesXMLDict, padstackXMLDict, pcbXML

    def _getBoardOutlines(self, pcbXML:ET.ElementTree, boardInstance:board.Board, outlinesLayers:list[str]):
        polyStructsXML = [child for child in pcbXML.find('Datas').findall('PolyStruct') if child.attrib['layer'] in outlinesLayers]

        outlinesList = []
        for polyStructXML in polyStructsXML:
            outlinesList += self._processPolyStruct(polyStructXML)
        boardInstance.setOutlines(outlinesList)
    
    def _updateComponents(self, pcbXML:ET.ElementTree, boardInstance:board.Board) -> dict:
        components = boardInstance.getComponents()
        insertsXML = [child for child in pcbXML.find('Datas').findall('Insert') if child.attrib['refName'] != '']

        shapesIDToComponentDict = {}
        for child in insertsXML:
            componentName = child.attrib['refName']
            shapeID = child.attrib['geomNum']
            x = gobj.floatOrNone(child.attrib['x'])
            y = gobj.floatOrNone(child.attrib['y'])
            angle = child.attrib['angle']
            side = 'B' if child.attrib['placeBottom'] == '1' else 'T'

            if componentName in components:
                componentInstance = components[componentName]
                componentInstance.setCoords(gobj.Point(x, y))
                componentInstance.setAngle(math.degrees(float(angle)))
                componentInstance.setSide(side)
                if not shapeID in shapesIDToComponentDict:
                    shapesIDToComponentDict[shapeID] = []
                shapesIDToComponentDict[shapeID].append(componentInstance)
        return shapesIDToComponentDict

    def _createPin(self, rootXML:ET.ElementTree) -> pin.Pin:
        pinID = rootXML.attrib['pin']

        pinX = gobj.floatOrNone(rootXML.attrib['x'])
        pinY = gobj.floatOrNone(rootXML.attrib['y'])
        coordsPoint = gobj.Point(pinX, pinY)

        newPin = pin.Pin(pinID)
        newPin.setCoords(coordsPoint)
        return newPin
    
    def _getPinPadstackAngleInPlace(self, rootXML:ET.ElementTree, pinInstance:pin.Pin, shapesIDToPinAngleDict:dict):
        pinAngle = rootXML.attrib['rotation']
        padShapeID = rootXML.attrib['padstackGeomNum']

        if padShapeID not in shapesIDToPinAngleDict:
            shapesIDToPinAngleDict[padShapeID] = []
        shapesIDToPinAngleDict[padShapeID].append([pinInstance, pinAngle])
    
    def _processComponentDataInNets(self, rootXML:ET.ElementTree, componentsDict:dict, pinInstance:pin.Pin) -> comp.Component:
        componentName = rootXML.attrib['comp']
        if componentName not in componentsDict:
            self._createComponentInPlace(rootXML, componentName, componentsDict)

        componentInstance = componentsDict[componentName]
        componentInstance.addPin(pinInstance.name, pinInstance)
        return componentInstance
    
    def _createComponentInPlace(self, rootXML:ET.ElementTree,  componentName:str, componentsDict:dict):
        mountingType = self._getComponentMountingType(rootXML)
        newComponent = comp.Component(componentName)
        newComponent.setMountingType(mountingType)
        componentsDict[componentName] = newComponent

    def _getComponentMountingType(self, attribRootXML:ET.ElementTree) -> str:
        mountDict = {'SMD': 'SMT', 'SMT':'SMT', 'THRU':'TH', 'TH':'TH'}
        for child in attribRootXML:
            if child.tag == 'Attrib' and 'val' in child.attrib and child.attrib['val'].upper() in mountDict:
                val = child.attrib['val']
                return mountDict[val]
    
    def _processPolyStruct(self, polyStructXML:ET.ElementTree) -> list[gobj.Line|gobj.Arc]:
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