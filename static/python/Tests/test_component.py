import pytest
import pin
import component as comp
import geometryObjects as gobj

@pytest.fixture
def componentForPinsCalculation():
    testedComponent = comp.Component('1')
    pad1 = pin.Pin('1') 
    pad2 = pin.Pin('2')
    pad3 = pin.Pin('3')
    pad4 = pin.Pin('4')

    pad1.setCoords(gobj.Point(-1, -1))
    pad2.setCoords(gobj.Point(3, 2))
    pad3.setCoords(gobj.Point(-1, 1))
    pad4.setCoords(gobj.Point(2, 0))

    testedComponent.addPin('1', pad1)
    testedComponent.addPin('2', pad2)
    testedComponent.addPin('3', pad3)
    testedComponent.addPin('4', pad4)
    return testedComponent

@pytest.fixture
def componentForRotateTranslate():
    testedComponent = comp.Component('test')
    testedComponent.setCoords(gobj.Point(0, 0))
    testedComponent.setArea(gobj.Point(-4, -2), gobj.Point(4, 2))    
    testedComponent.setShape('RECT')
    testedComponent.caluclateShapeData()

    pad1 = pin.Pin('1')
    pad1.setCoords(gobj.Point(-2, -1)) 
    pad1.setDimensions(1, 1)
    pad1.calculateAreaFromWidthHeightCoords()
    pad1.setShape('RECT')
    pad1.caluclateShapeData()

    pad2 = pin.Pin('2')
    pad2.setCoords(gobj.Point(2, 1))
    pad2.setDimensions(1, 1)
    pad2.calculateAreaFromWidthHeightCoords()    
    pad2.setShape('RECT')
    pad2.caluclateShapeData()

    testedComponent.addPin('1', pad1)
    testedComponent.addPin('2', pad2)
    return testedComponent

@pytest.mark.parametrize('input, expected', [((None, None), False), ((2, 3), True), ((None, 2), False)])
def test_isCoordsValid(input, expected):
    x, y = input
    point = gobj.Point(x, y)
    testedComponent = comp.Component('1')
    testedComponent.setCoords(point)
    assert testedComponent.isCoordsValid() == expected

def test_calculateHitBoxFromPins(componentForPinsCalculation):
    point1, point2 = componentForPinsCalculation.calculateHitBoxFromPins()
    assert point1 == gobj.Point(-1, -1)
    assert point2 == gobj.Point(3, 2)

def test_calculateCenterFromPins(componentForPinsCalculation):    
    componentForPinsCalculation.calculateCenterFromPins()
    assert componentForPinsCalculation.coords.x == 1 and componentForPinsCalculation.coords.y == 0.5

def test_calculatePackageFromPins(componentForPinsCalculation):
    componentForPinsCalculation.calculateAreaFromPins()
    point1, point2 = componentForPinsCalculation.getArea()
    assert point1 == gobj.Point(-0.95, -0.95)
    assert point2 == gobj.Point(2.85, 1.9)

def test__makeAreaNotLinear():
    instance = comp.Component('1')
    
    bottomLeftPoint, topRightPoint = gobj.Point(-1, 0), gobj.Point(1, 0)
    bottomLeftPoint, topRightPoint = instance._makeAreaNotLinear(bottomLeftPoint, topRightPoint)
    assert [bottomLeftPoint, topRightPoint] == [gobj.Point(-1, -0.2), gobj.Point(1, 0.2)]

    bottomLeftPoint, topRightPoint = gobj.Point(0, -1), gobj.Point(0, 1)
    bottomLeftPoint, topRightPoint = instance._makeAreaNotLinear(bottomLeftPoint, topRightPoint)
    assert [bottomLeftPoint, topRightPoint] == [gobj.Point(-0.2, -1), gobj.Point(0.2, 1)]
    

def test_translateInPlace(componentForRotateTranslate):
    componentForRotateTranslate.translateInPlace([10, 10])

    assert componentForRotateTranslate.getCoords() == gobj.Point(10, 10)
    assert componentForRotateTranslate.getArea() == [gobj.Point(6, 8), gobj.Point(14, 12)]
    assert componentForRotateTranslate.getShapePoints() == [gobj.Point(6, 8), gobj.Point(14, 8), gobj.Point(14, 12), gobj.Point(6, 12)]

    pin1 = componentForRotateTranslate.getPinByName('1')
    assert pin1.getCoords() == gobj.Point(8, 9)
    assert pin1.getArea() == [gobj.Point(7.5, 8.5), gobj.Point(8.5, 9.5)] # before translation: (-2.5, -1.5), (-1.5, 0.5)
    assert pin1.getShapePoints() == [gobj.Point(7.5, 8.5), gobj.Point(8.5, 8.5), gobj.Point(8.5, 9.5), gobj.Point(7.5, 9.5)]

    pin2 = componentForRotateTranslate.getPinByName('2')
    assert pin2.getCoords() == gobj.Point(12, 11)
    assert pin2.getArea() == [gobj.Point(11.5, 10.5), gobj.Point(12.5, 11.5)] # before translation: (1.5, 0.5), (2.5, 1.5)
    assert pin2.getShapePoints() == [gobj.Point(11.5, 10.5), gobj.Point(12.5, 10.5), gobj.Point(12.5, 11.5), gobj.Point(11.5, 11.5)]

def test_rotateInPlace(componentForRotateTranslate):
    gobj.Point.DECIMAL_POINT_PRECISION = 3    
    componentForRotateTranslate.rotateInPlace(gobj.Point(1, 1), 30)

    assert componentForRotateTranslate.getCoords() == gobj.Point(0.634, -0.366)
    assert componentForRotateTranslate.getArea() == [gobj.Point(-3.830, -4.098), gobj.Point(5.098, 3.366)]
    assert componentForRotateTranslate.getShapePoints() == [gobj.Point(-1.830, -4.098), gobj.Point(5.098, -0.098), 
                                                            gobj.Point(3.098, 3.366), gobj.Point(-3.830, -0.634)]

    pin1 = componentForRotateTranslate.getPinByName('1')
    assert pin1.getCoords() == gobj.Point(-0.598, -2.232)
    assert pin1.getArea() == [gobj.Point(-0.781, -2.915), gobj.Point(-0.415, -1.549)] # before translation: (-2.5, -1.5), (-1.5, -0.5)
    assert pin1.getShapePoints() == [gobj.Point(-0.781, -2.915), gobj.Point(0.085, -2.415), gobj.Point(-0.415, -1.549), gobj.Point(-1.281, -2.049)]

    pin2 = componentForRotateTranslate.getPinByName('2')
    assert pin2.getCoords() == gobj.Point(1.866, 1.500)
    assert pin2.getArea() == [gobj.Point(1.683, 0.817), gobj.Point(2.049, 2.183)] # before translation: (1.5, 0.5), (2.5, 1.5)
    assert pin2.getShapePoints() == [gobj.Point(1.683, 0.817), gobj.Point(2.549, 1.317), gobj.Point(2.049, 2.183), gobj.Point(1.183, 1.683)]

def test_getPinByName(componentForPinsCalculation):
    testPin = componentForPinsCalculation.getPinByName('1')
    assert testPin == componentForPinsCalculation.pins['1']

    testPin = componentForPinsCalculation.getPinByName('13')
    assert testPin == None

def test_scaleInPlace(componentForRotateTranslate):
    gobj.Point.DECIMAL_POINT_PRECISION = 3    
    componentForRotateTranslate.scaleInPlace(100)

    assert componentForRotateTranslate.getCoords() == gobj.Point(0, 0)
    assert componentForRotateTranslate.getArea() == [gobj.Point(-400, -200), gobj.Point(400, 200)]
    assert componentForRotateTranslate.getShapePoints() == [gobj.Point(-400, -200), gobj.Point(400, -200), 
                                                            gobj.Point(400, 200), gobj.Point(-400, 200)]

    pin1 = componentForRotateTranslate.getPinByName('1')
    assert pin1.getCoords() == gobj.Point(-200, -100)
    assert pin1.getArea() == [gobj.Point(-250, -150), gobj.Point(-150, -50)]
    assert pin1.getShapePoints() == [gobj.Point(-250, -150), gobj.Point(-150, -150), gobj.Point(-150, -50), gobj.Point(-250, -50)]

    pin2 = componentForRotateTranslate.getPinByName('2')
    assert pin2.getCoords() == gobj.Point(200, 100)
    assert pin2.getArea() == [gobj.Point(150, 50), gobj.Point(250, 150)]
    assert pin2.getShapePoints() == [gobj.Point(150, 50), gobj.Point(250, 50), gobj.Point(250, 150), gobj.Point(150, 150)]