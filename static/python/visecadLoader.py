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
        self._processNetsTag(root, self.boardData)
        
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
        
        componentDict = {}
        for netXML in filesXML:
            netName = netXML.attrib['name']
            for compPinXML in netXML:
                pinID = compPinXML.attrib['pin']
                pinX = compPinXML.attrib['x']
                pinY = compPinXML.attrib['y']
                newPin = self._createPin(pinID, pinX, pinY)

                pinAngle = compPinXML.attrib['rotation']
                padShapeID = compPinXML.attrib['padstackGeomNum']
                
                componentName = compPinXML.attrib['comp']
                mountingType = self._getComponentMountingType(compPinXML)
                newComponent = self._createComponent(componentName, mountingType)




                print(compPinXML.attrib['comp'], compPinXML.attrib['pin'])
        
    def _getComponentMountingType(self, attribRootXML:ET) -> str:
        mountDict = {'SMD': 'SMT', 'SMT':'SMT', 'THRU':'TH', 'TH':'TH'}
        for child in attribRootXML:
            if child.tag == 'Attrib' and 'val' in child.attrib and child.attrib['val'].upper() in mountDict:
                val = child.attrib['val']
                return mountDict[val]
    
    def _createPin(self, pinName:str, pinX:str, pinY:str) -> pin.Pin:
        pinX = gobj.floatOrNone(pinX)
        pinY = gobj.floatOrNone(pinY)
        coordsPoint = gobj.Point(pinX, pinY)
        
        newPin = pin.Pin(pinName)
        newPin.setCoords(coordsPoint)
        return newPin
    
    def _createComponent(self, componentName:str, mountingType:str) -> comp.Component:
        newComponent = comp.Component(componentName)
        newComponent.setMountingType(mountingType)
        return newComponent

if __name__ == '__main__':
    def openSchematicFile() -> str:        
        from tkinter import filedialog
        filePath = filedialog.askopenfile(mode='r', filetypes=[('*', '*')])
        return filePath.name

    filePath = openSchematicFile()

    loader = VisecadLoader()
    fileLines = loader.loadFile(filePath)
    loader.processFileLines(fileLines)