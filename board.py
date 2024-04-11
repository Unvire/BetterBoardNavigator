import pin
import geometryObjects as gobj
import component as comp

class Board:
    def __init__(self):
        self.area = []
        self.outlines = []
        self.components = {}
        self.nets = []
        self.tracks = {}
    
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
    
    def getTrack(self, side:str, netName:str) -> list[gobj.Line|gobj.Rectangle|gobj.Arc|gobj.Circle]:
        return self.tracks[netName][side]