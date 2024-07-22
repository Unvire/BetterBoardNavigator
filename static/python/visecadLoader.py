import xml.etree.ElementTree as ET
from zipfile import ZipFile
import math, copy
import geometryObjects as gobj
import component as comp
import board, pin

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
        self._getBoardArea(self.boardData)
        shapesIDToComponentDict = self._updateComponents(pcbXML, self.boardData)
        shapesDict = self._calculateBaseShapes(shapesXMLDict)
        padstackIDDict = self._getPadstackShapeID(padstackXMLDict, shapesDict)
        self._addShapesToPins(shapesIDToPinAngleDict, padstackIDDict)
        self._addShapesToComponents(shapesIDToComponentDict, padstackIDDict)
        
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
    
    def _getBoardArea(self, boardInstance:board.Board):        
        bottomLeftPoint, topRightPoint = boardInstance.calculateAreaFromOutlines()
        boardInstance.setArea(bottomLeftPoint, topRightPoint)

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

    def _calculateBaseShapes(self, shapesXMLDict:dict) -> dict:
        shapesDict = {}
        for shapeID, child in shapesXMLDict.items():
            sizeA = gobj.floatOrNone(child.attrib['sizeA'])
            sizeB = gobj.floatOrNone(child.attrib['sizeB'])
            if sizeB > 0:
                bottomLeftPoint = gobj.Point(-sizeA / 2, -sizeB / 2)
                topRightPoint = gobj.Point(sizeA / 2, sizeB / 2)
                shapeInstance = gobj.Rectangle(bottomLeftPoint, topRightPoint)
            else:
                centerPoint = gobj.Point(0, 0)
                radius = sizeA / 2
                shapeInstance = gobj.Circle(centerPoint, radius)
            shapesDict[shapeID] = shapeInstance
        return shapesDict

    def _getPadstackShapeID(self, padstackXMLDict:dict, shapesDict:dict) -> dict:
        padstackShapeIDDict = {}
        padstacksSecondIterationMatchList = []
        
        for padstackID, child in padstackXMLDict.items():
            datasXML = child.find('Datas')
            polyStructsXML = datasXML.findall('PolyStruct')
            insertsXML = datasXML.findall('Insert')

            if not polyStructsXML and not insertsXML: 
                continue
            
            if not polyStructsXML and insertsXML:
                insertPadstackID = insertsXML[0].attrib['geomNum']
                if insertPadstackID in shapesDict:
                    padstackShapeIDDict[insertPadstackID] = shapesDict[insertPadstackID]
                else:
                    padstacksSecondIterationMatchList.append([padstackID, insertPadstackID])
                continue
            
            rectangle = self._getRectangleFromPolyStruct(polyStructsXML[0])
            padstackShapeIDDict[padstackID] = rectangle
            numberOfPins = len(insertsXML)
            for insertXML in insertsXML:
                insertPadstackID = insertXML.attrib['geomNum']
                if insertPadstackID in shapesDict:
                    padstackShapeIDDict[insertPadstackID] = shapesDict[insertPadstackID]
                else:
                    rectBLPoint, _, rectTRPoint, _ = rectangle.getPoints()
                    scaleFactor = 1 / numberOfPins
                    scaledRectangle = gobj.Rectangle(gobj.Point.scale(rectBLPoint, scaleFactor), 
                                                    gobj.Point.scale(rectTRPoint, scaleFactor))
                    padstackShapeIDDict[insertPadstackID] = scaledRectangle
        
        for padstackID, insertPadstackID in padstacksSecondIterationMatchList:
            padstackShapeIDDict[padstackID] = padstackShapeIDDict[insertPadstackID]
        
        for key in padstackShapeIDDict:
            if key not in shapesDict:
                shapesDict[key] = padstackShapeIDDict[key]
        return shapesDict
    
    def _addShapesToPins(self, shapesIDToPinAngleDict:dict, padstackIDDict:dict):
        for shapeID, pinsAnglesList in shapesIDToPinAngleDict.items():
            for pinInstance, angle in pinsAnglesList:     
                shapeInstance = copy.deepcopy(padstackIDDict[shapeID]) 
                self._setInstanceShape(pinInstance, shapeInstance)
                self._setInstanceAreaDimensionsAndShapeData(pinInstance, shapeInstance)

                pinInstance.rotateInPlaceAroundCoords(math.degrees(float(angle)))

    def _addShapesToComponents(self, shapesIDToComponentDict:dict, padstackIDDict:dict):
        for shapeID, componentsList in shapesIDToComponentDict.items():
            for componentInstance in componentsList:
                shapeInstance = copy.deepcopy(padstackIDDict[shapeID])
                self._setInstanceShape(componentInstance, shapeInstance)
                self._setInstanceAreaDimensionsAndShapeData(componentInstance, shapeInstance)

                angle = componentInstance.getAngle()
                componentInstance.rotateInPlaceAroundCoords(angle)
    
    def _setInstanceShape(self, instance:pin.Pin|comp.Component, shapeInstance:gobj.Rectangle|gobj.Circle):
        if shapeInstance.type == 'Circle':
            instance.setShape('CIRCLE')
    
    def _setInstanceAreaDimensionsAndShapeData(self, instance:pin.Pin|comp.Component, shapeInstance:gobj.Rectangle|gobj.Circle):
        def moveAreaToCoords(shapeInstance:pin.Pin|comp.Component, moveVector:list[float, float]) -> tuple[gobj.Point, gobj.Point]:
            bottomLeftPoint, topRightPoint = shapeInstance.calculateArea()
            bottomLeftPoint.translateInPlace(moveVector)
            topRightPoint.translateInPlace(moveVector)
            return bottomLeftPoint, topRightPoint

        bottomLeftPoint, topRightPoint = moveAreaToCoords(shapeInstance, instance.getCoordsAsTranslationVector())
        bottomLeftPoint, topRightPoint = instance.makeAreaNotLinear(bottomLeftPoint, topRightPoint)
        instance.setArea(bottomLeftPoint, topRightPoint)
        instance.calculateDimensionsFromArea()
        instance.caluclateShapeData()

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
    
    def _getRectangleFromPolyStruct(self, polyStructXML:ET.ElementTree) -> gobj.Rectangle:
        pointsXML = polyStructXML.find('Poly').findall('Pnt')
        bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
        for pointXML in pointsXML:
            if 'bulge' in pointXML.attrib:
                continue
            x = gobj.floatOrNone(pointXML.attrib['x'])
            y = gobj.floatOrNone(pointXML.attrib['y'])
            point = gobj.Point(x, y)
            bottomLeftPoint, topRightPoint = gobj.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, point)
        
        xBL, yBL = bottomLeftPoint.getXY()
        xTR, yTR = topRightPoint.getXY()
        midX = 0.5 * (abs(xBL) + abs(xTR))   
        midY = 0.5 * (abs(yBL) + abs(yTR))
        return gobj.Rectangle(gobj.Point(-midX, -midY), gobj.Point(midX, midY))

if __name__ == '__main__':
    def openSchematicFile() -> str:        
        from tkinter import filedialog
        filePath = filedialog.askopenfile(mode='r', filetypes=[('*', '*')])
        return filePath.name

    filePath = openSchematicFile()

    loader = VisecadLoader()
    fileLines = loader.loadFile(filePath)
    loader.processFileLines(fileLines)