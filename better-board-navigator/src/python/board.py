import json

import geometryObjects as gobj
import component as comp
from abstractShape import Shape

class Board:
    def __init__(self):
        self.area = []
        self.outlines = []
        self.components = {}
        self.nets = []
        self.sideGroupedComponents = {}
        self.commonTypeGroupedComponents = {}
        self.mostCommonPrefix = ''
    
    def setArea(self, bottomLeftPoint:gobj.Point, topRightPoint:gobj.Point):
        x0, y0 = bottomLeftPoint.getXY()
        x1, y1 = topRightPoint.getXY()       

        bottomRightPoint = gobj.Point(x1, y0)
        topLeftPoint = gobj.Point(x0, y1)
        self.area = [bottomLeftPoint, bottomRightPoint, topRightPoint, topLeftPoint]

    def getArea(self) -> list[gobj.Point]:
        bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
        bottomLeftPoint, topRightPoint = gobj.updateBottomLeftTopRightPoints([bottomLeftPoint, topRightPoint], self.area)
        return [bottomLeftPoint, topRightPoint]

    def getWidthHeight(self) -> list[float|int, float|int]:
        xBL, yBL, xTR, yTR = Shape.getAreaAsXYXY(self.getArea())
        return abs(xTR - xBL), abs(yTR - yBL)
    
    def setOutlines(self, outlinesList:list[gobj.Point|gobj.Arc]):
        self.outlines = outlinesList

    def getOutlines(self) -> list[gobj.Point|gobj.Arc]:
        return self.outlines
    
    def setComponents(self, componentsDict:dict):
        self.components = componentsDict
    
    def getComponents(self) -> dict:
        return self.components
    
    def removeComponent(self, componentName:str):
        self.components.pop(componentName, None)
    
    def setNets(self, netsDict:dict):
        self.nets = netsDict
    
    def getNets(self) -> dict:
        return self.nets
    
    def addComponent(self, name:str, componentInstance:comp.Component):
        self.components[name] = componentInstance
    
    def getElementByName(self, groupName:str, elementName:str):
        matchDict = {'components':self.components, 'nets':self.nets}
        return matchDict[groupName].get(elementName, None)
    
    def setGroups(self, sideGroupedComponents:dict, commonTypeGroupedComponents:dict):
        self.sideGroupedComponents = sideGroupedComponents
        self.commonTypeGroupedComponents = commonTypeGroupedComponents

        countedPrefixes = {}
        for sideGroups in commonTypeGroupedComponents.values():
            for prefixGroupName, prefixGroupElements in sideGroups.items():
                countedPrefixes.setdefault(prefixGroupName, 0)
                countedPrefixes[prefixGroupName] += len(prefixGroupElements)
        
        self.mostCommonPrefix = max(countedPrefixes, key=countedPrefixes.get)

    def getSideGroupedComponents(self) -> dict:
        return self.sideGroupedComponents
    
    def getCommonTypeGroupedComponents(self) -> dict:
        return self.commonTypeGroupedComponents
    
    def getMostCommonPrefix(self) -> str:
        return self.mostCommonPrefix
    
    def calculateAreaFromComponents(self) -> tuple[gobj.Point, gobj.Point]:
        bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
        for componentInstance in self.components.values():
            for point in componentInstance.getArea():
                bottomLeftPoint, topRightPoint = gobj.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, point)
        
        return bottomLeftPoint, topRightPoint
    
    def calculateAreaFromOutlines(self) -> tuple[gobj.Point, gobj.Point]:
        bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
        for shape in self.outlines:
            bottomLeftPoint, topRightPoint = gobj.updateBottomLeftTopRightPoints([bottomLeftPoint, topRightPoint], list(shape.getPoints()))
        return bottomLeftPoint, topRightPoint
    
    def translateRotateScaleBoard(self, functionName:str, *args):
        '''
        Calls translateInPlace, rotateInPlace or scaleInPlace on area, shapes and components.
        functionName must be: translateInPlace, rotateInPlace or scaleInPlace
        Arguments for functions:
            translateInPlace -> moveVector:list[int|float, int|float]
            rotateInPlace -> rotationPoint:geometryObjects.Point, angleDeg:int|float
            scaleInPlace -> factor:int|float
        '''
        components = [componentInstance for componentInstance in self.components.values()]
        objList = self.area + self.outlines + components

        for obj in objList:
            func = getattr(obj, functionName)
            func(*args)
    
    def findComponentByCoords(self, clickedPoint:gobj.Point, side:str) -> list[str]:
        result = []
        componentNames = self.sideGroupedComponents[side]
        for componentName in componentNames:
            componentInstance = self.getElementByName('components', componentName)
            shape = componentInstance.getShapeData()
            if shape.checkIfPointInside(clickedPoint):
                result.append(componentName)
        return result


    def toDict(self) -> dict:
        def serializeShape(obj):
            if obj is None:
                return None
            if isinstance(obj, gobj.Point):
                return {'x': obj.x, 'y': obj.y}
            elif isinstance(obj, gobj.Line):
                return {'type': 'Line', 'start': serializeShape(obj.startPoint), 'end': serializeShape(obj.endPoint)}
            elif isinstance(obj, gobj.Arc):
                center, radius, start_angle, end_angle = obj.getAsCenterRadiusAngles()
                return {'type': 'Arc', 'center': serializeShape(center), 'radius': radius, 'startAngle': start_angle, 'endAngle': end_angle}
            elif isinstance(obj, gobj.Circle):
                return {'type': 'Circle', 'center': serializeShape(obj.centerPoint), 'radius': obj.radius}
            elif isinstance(obj, gobj.Rectangle):
                return {'type': 'Rectangle', 'points': [serializeShape(p) for p in obj.getPoints()]}
            return None

        def serializePin(p):
            return {
                'name': getattr(p, 'name', ''),
                'net': getattr(p, 'net', None),
                'shapeType': getattr(p, 'shape', 'RECT'),
                'shapeData': serializeShape(getattr(p, 'shapeData', None)),
                'coords': serializeShape(getattr(p, 'coords', None))
            }

        def serializeComponent(c):
            pinsDict = getattr(c, 'pins', {})
            return {
                'name': getattr(c, 'name', ''),
                'side': getattr(c, 'side', 'T'),
                'angle': getattr(c, 'angle', 0),
                'mountingType': getattr(c, 'mountingType', 'SMT'),
                'shapeType': getattr(c, 'shape', ''),
                'shapeData': serializeShape(getattr(c, 'shapeData', None)),
                'coords': serializeShape(getattr(c, 'coords', None)),
                'pins': {pinName: serializePin(pinObj) for pinName, pinObj in pinsDict.items()}
            }

        simplifiedNets = {}
        for netName, compDict in self.nets.items():
            simplifiedNets[netName] = {
                compName: {'pins': data.get('pins', [])} 
                for compName, data in compDict.items()
            }

        return {
            'boardDimensions': self.getWidthHeight(),
            'area': [serializeShape(p) for p in self.getArea()],
            'outlines': [serializeShape(shape) for shape in self.outlines],
            'components': {name: serializeComponent(c) for name, c in self.components.items()},
            'nets': simplifiedNets,
            'mostCommonPrefix': self.mostCommonPrefix
        }

    def toJson(self) -> str:
        return json.dumps(self.toDict())