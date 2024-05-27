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
    
    def setArea(self, bottomLeftPoint:gobj.Point, topRightPoint:gobj.Point):
        self.area = [bottomLeftPoint, topRightPoint]
    
    def getArea(self) -> list[gobj.Point]:
        return self.area

    def getWidthHeight(self) -> list[float|int, float|int]:
        xBL, yBL, xTR, yTR = Shape.getAreaAsXYXY(self.area)
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

    def getSideGroupedComponents(self) -> dict:
        return self.sideGroupedComponents
    
    def getCommonTypeGroupedComponents(self) -> dict:
        return self.commonTypeGroupedComponents
    
    def calculateAreaFromComponents(self) -> tuple[gobj.Point, gobj.Point]:
        bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
        for _, componentInstance in self.components.items():
            for point in componentInstance.getArea():
                bottomLeftPoint, topRightPoint = gobj.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, point)
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
        components = [componentInstance for _, componentInstance in self.components.items()]
        objList = self.area + self.outlines + components
        for obj in objList:
            func = getattr(obj, functionName)
            func(*args)
        
        if functionName == 'rotateInPlace':
            bottomLeftPoint, topRightPoint = self.normalizeArea(self.area)
            self.setArea(bottomLeftPoint, topRightPoint)
    
    def normalizeArea(self, area:list[gobj.Point, gobj.Point]) -> list[gobj.Point, gobj.Point]:
        bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
        bottomLeftPoint, topRightPoint = gobj.updateBottomLeftTopRightPoints([bottomLeftPoint, topRightPoint], area)
        return bottomLeftPoint, topRightPoint
    
    def findComponentByCoords(self, clickedPoint:gobj.Point, side:str) -> str:
        componentNames = self.sideGroupedComponents[side]
        for componentName in componentNames:
            componentInstance = self.getElementByName('components', componentName)
            shape = componentInstance.getShapeData()
            if shape.checkIfPointInside(clickedPoint):
                return componentName
        return ''