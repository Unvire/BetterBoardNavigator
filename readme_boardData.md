board = {
    ## defines working area
    area: [
        bottomLeftPoint: geometryObjects.Point, 
        topRightPoint: geometryObjects.Point
        ] 

    ## defines board outlines as a list of Lines and Arcs 
    shape: [
        geometryObjects.Line,
        geometryObjects.Arc
        ]

    ## defines components as dict of  key=name, val=componentInstance
    components:{
        name:str : component.Component
        }

    ##
    nets:{
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
    areaType: str
    componentArea = [
        bottomLeftPoint: geometryObjects.Point, 
        topRightPoint: geometryObjects.Point
    ]
    mountingType: str ('SMT' or 'TH')
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