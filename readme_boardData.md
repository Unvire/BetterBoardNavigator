boardData = {
    ## defines working area
    'AREA': [
        bottomLeftPoint: geometryObjects.Point, 
        topRightPoint: geometryObjects.Point
        ] 

    ## defines board outlines as a list of Lines and Arcs 
    'SHAPE': [
        geometryObjects.Line,
        geometryObjects.Arc
        ]

    ## defines components as dict of  key=name, val=componentInstance
    'COMPONENTS':{
        name:str : component.Component
        }

    ##
    'NETS':{
        netName: str:{
            componentName: str:{
                'instance': component.Component (reference to component listed in 'COMPONENTS')
                'pinName': str
                }
            }
        }

}

#######################################################################################################################

component = {
    name: str,
    pins: {
        pinName:str :{
            pin: pin.Pin
        }
    }
    coords: geometryObjects.Point
    side: str ('T' or 'B')
    angle: float
    partNumber: str
    componentArea = [
        bottomLeftPoint: geometryObjects.Point, 
        topRightPoint: geometryObjects.Point
    ]
    packageType: str ('SMT' or 'TH')
}

#######################################################################################################################

pin = {
    name: str
    shape: str ('RECT' or 'CIRCLE')
    coords = geometryObjects.Point
    pinArea = [
        bottomLeftPoint: geometryObjects.Point, 
        topRightPoint: geometryObjects.Point
    ]
    net: str
    width: float
    height: float
}