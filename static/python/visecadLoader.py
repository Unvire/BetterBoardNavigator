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
        root = self._parseXMLFromFileLines(fileLines)
        outlinesLayers = self._getOutlinesLayers(root)
        padsID = self._processNetsTag(root, self.boardData)
        
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
    
    def _getOutlinesLayers(self, root:ET) -> list[str]:
        layersXML = root.find('Layers')

        outlineLayers = []
        for child in layersXML:
            if 'OUTLINE' in child.attrib['name'].upper():
                outlineLayers.append(child.attrib['num'])
        return outlineLayers

    def _processNetsTag(self, root:ET, boardInstance:board.Board) -> None:
        try:
            filesXML = root.find('Files').find('File').find('Nets')
        except AttributeError:
            return
        
        componentsDict = {}
        shapesIDDict = {}
        netsDict = {}
        for netXML in filesXML:
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

if __name__ == '__main__':
    def openSchematicFile() -> str:        
        from tkinter import filedialog
        filePath = filedialog.askopenfile(mode='r', filetypes=[('*', '*')])
        return filePath.name

    filePath = openSchematicFile()

    loader = VisecadLoader()
    fileLines = loader.loadFile(filePath)
    loader.processFileLines(fileLines)