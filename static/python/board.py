import geometryObjects as gobj
import component as comp

class Board:
    def __init__(self):
        self.area = []
        self.outlines = []
        self.components = {}
        self.nets = []
        self.tracks = {}
        self.sideGroupedComponents = {}
        self.commonTypeGroupedComponents = {}
        self.hitMap = {}
    
    def setArea(self, bottomLeftPoint:gobj.Point, topRightPoint:gobj.Point):
        self.area = [bottomLeftPoint, topRightPoint]
    
    def getArea(self) -> list[gobj.Point]:
        return self.area
    
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
    
    def setTracks(self, tracksDict:dict):
        self.tracks = tracksDict
    
    def getTracks(self) -> dict:
        return self.tracks
    
    def getTrack(self, side:str, netName:str) -> list['gobj.Line|gobj.Rectangle|gobj.Arc|gobj.Circle']:
        return self.tracks[netName][side]
    
    def setGroups(self, sideGroupedComponents:dict, commonTypeGroupedComponents:dict, hitMap:dict):
        self.sideGroupedComponents = sideGroupedComponents
        self.commonTypeGroupedComponents = commonTypeGroupedComponents
        self.hitMap = hitMap

    def getSideGroupedComponents(self) -> dict:
        return self.sideGroupedComponents
    
    def getCommonTypeGroupedComponents(self) -> dict:
        return self.commonTypeGroupedComponents

    def getHitMap(self) -> dict:
        return self.hitMap
    
    def calculateAreaFromComponents(self) -> tuple[gobj.Point, gobj.Point]:
        bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
        for _, componentInstance in self.components.items():
            for point in componentInstance.getArea():
                bottomLeftPoint, topRightPoint = gobj.Point.minXY_maxXYCoords(bottomLeftPoint, topRightPoint, point)
        return bottomLeftPoint, topRightPoint
    
    def scaleBoard(self, factor:int|float):
        for _, componentInstance in self.components:
            componentInstance.scaleInPlace(factor)
        
        for shape in self.outlines:
            shape.scaleInPlace(factor)
