board = {
    ## defines working area
    area: [
        bottomLeftPoint: geometryObjects.Point, 
        topRightPoint: geometryObjects.Point
        ] 

    ## defines board outlines as a list of Lines and Arcs 
    outlines: [
        geometryObjects.Line,
        geometryObjects.Arc
        ]

    ## defines components as dict of  key=name, val=componentInstance
    components:{
        name:str : component.Component
        }

    ## defines nets as a dict
    nets:{
        netName: str:{
            componentName: str:{
                'componentInstance': component.Component (reference to component listed in 'COMPONENTS')
                'pins': list[str]
                }
            }
        }
    
    ## defines tracks as a dict of nets -> sides
    tracks:{
        netName:str :{
            'T': [
                geometryObjects.Line,
                geometryObjects.Arc,
                geometryObjects.Rectangle,
                geometryObjects.Circle
            ],
            'B': [
                geometryObjects.Line,
                geometryObjects.Arc,
                geometryObjects.Rectangle,
                geometryObjects.Circle
            ]

        }
    }

}
#######################################################################################################################
parent class for component and pin classes
shape = {
    name: str,
    shape = 'RECT' or 'CIRCLE'
    shapeData:list : [geometryObjects.Point, geometryObjects.Point, geometryObjects.Point, geometryObjects.Point] 
                     or
                     [geometryObjects.Point]
    coords: geometryObjects.Point,
    area = [
        bottomLeftPoint: geometryObjects.Point, 
        topRightPoint: geometryObjects.Point
    ]
}

#######################################################################################################################
Component inherits shape's parameter

component = {
    pins: {
        pinName:str :{
            pin: pin.Pin
        }
    }
    side: str ('T' or 'B')
    angle: float
    mountingType: str ('SMT' or 'TH')
}

#######################################################################################################################
Pin inherits shape's parameter 
pin = {
    net: str
}

#######################################################################################################################
Processing of a cad file

file --> format factory (loaderSelectorFactory) --> loader (camcadLoader, gencadLoader, odbPlusPlusLoader, viseCadLoader, ...) --> board instance (Board) --> board instance normalized (boardWrapper) --> pygameDrawBoard

All methods with "_" in name are private.
General purpose functions can be found in geometry objects as functions in a Point as static methods in AbstractShape as static methods.
All methods for drawing a frame in DrawBoardEngine have "Interface" as last word
