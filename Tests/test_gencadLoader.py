import pytest
from Loaders.gencadLoader import GenCadLoader
import geometryObjects as gobj 

@pytest.fixture
def sectionsRangeTest():
    fileLinesMock = [
        '$BOARD',
        '$ENDBOARD',
        '$PADS',        
        'PIN',
        '$ENDPADS',
        '$SHAPES',
        '$ENDSHAPES',
        '$COMPONENTS',
        '$ENDCOMPONENTS',
        '$SIGNALS',
        '$ENDSIGNALS',
        '$ROUTES',
        '$ENDROUTES',
        '$MECH',
        '$ENDMECH',
    ]
    return fileLinesMock

@pytest.fixture
def bouardOutlineTest():
    fileLinesMock = [
        '$BOARD',
        'ARC 0.2900811 3.820681 0.250711 3.860051 0.250711 3.820681',
        'LINE 0.2900811 2.129768 0.2506389 2.090325',
        'LINE 0.2506389 2.090325 0.2506389 1.712375',
        'ARC -4.046038 3.859678 -4.08 3.820681 -4.04063 3.820681',
        'CIRCLE -2.8661417 2.527559 0.08070866',
        'ARTWORK artwork1450 SILKSCREEN_TOP',
        'LINE 1967.441 2267.244 -2026.496 -2267.244',
        '$ENDBOARD'
    ]
    return fileLinesMock

@pytest.fixture
def padsTest():
    fileLinesMock = [
        '$PADS',
        'PAD "Round 32" ROUND -1',
        'CIRCLE 0.000000 0.000000 0.406400',
        'PAD "Oblong 3.2x5.2" FINGER -1',
        'LINE -1.600000 -1.000000 -1.600000 1.000000',
        'ARC 1.600000 1.000000 -1.600000 1.000000 0.000000 1.000000',
        'LINE 1.600000 1.000000 1.600000 -1.000000',
        'PAD "Rectangle;1.15x1.65" RECTANGULAR -1',
        'RECTANGLE -0.575000 -0.825000 1.150000 1.650000',
        '$ENDPADS',
        '$PADSTACKS',
        'PADSTACK "026VIA" 0.482600',
        'PAD "Round 32" SOLDERMASK_BOTTOM 0 0',
        'PAD "Round 26" TOP 0 0',
        'PAD "Round 26" INNER 0 0',
        'PADSTACK "Smd 0.95x1.45 mm_TOP" 0.000000',
        'PAD "Rectangle;1.15x1.65" SOLDERMASK_TOP 0 0',
        '$PADSTACKS',
    ]
    return fileLinesMock

@pytest.fixture
def componentTest():
    fileLinesMock = [
        '$COMPONENTS',
        'COMPONENT VR1',
        'DEVICE 15023751_Generated',
        'PLACE -2.97 1.11',
        'LAYER BOTTOM',
        'ROTATION 0',
        'SHAPE RV-17X11X7.5P-M MIRRORY FLIP',
        'COMPONENT C90',
        'PLACE 1701.181 515.354',
        'LAYER TOP',
        'ROTATION 270.00',
        'SHAPE C0402_T 0 0',
        'DEVICE 15011408',
        'ATTRIBUTE COMPONENT_383 "DEVICETYPE" "Capacitor"',
        'ATTRIBUTE COMPONENT_384 "PARTNUMBER" "15011408"',
        'ATTRIBUTE COMPONENT_385 "-TOL" "0"',
        '$ENDCOMPONENTS'
    ]
    return fileLinesMock

@pytest.fixture
def shapesTest():
    fileLinesMock = [
        '$SHAPES',
        'SHAPE SMC_T',
        'LINE 0.13386 0.11614 0.19705 0.075',
        'LINE 0.19705 0.075 0.19705 -0.075',
        'LINE 0.19705 -0.075 0.13386 -0.11614',
        'LINE 0.13386 -0.11614 -0.13386 -0.11614',
        'LINE -0.13386 -0.11614 -0.19705 -0.075',
        'LINE -0.19705 -0.075 -0.19705 0.075',
        'LINE -0.19705 0.075 -0.13386 0.11614',
        'LINE -0.13386 0.11614 0.13386 0.11614',
        'INSERT smt',
        'HEIGHT 0.103150',
        'PIN A padstack102 0.1279528 0 TOP 270 0',
        'PIN K padstack102 -0.1279528 0 TOP 270 0',
        '$ENDSHAPES',
    ]
    return fileLinesMock

@pytest.fixture
def fullComponentTest():
    fileLinesMock = [
        '$SHAPES',
        'SHAPE IND_0603_T_3',
        'RECTANGLE -0.03149606 -0.01574803 0.06299213 0.03149606',
        'INSERT smt',
        'HEIGHT 0.035000',
        'PIN 1 padstack12 0.03098425 0 TOP 0 MIRRORY',
        'PIN 2 padstack12 -0.03098425 0 TOP 270 MIRRORY',
        '$ENDSHAPES',
        '$PADSTACKS',
        'PADSTACK padstack12 0',
        'PAD rect48x52 SOLDERMASK_TOP 0 0',
        '$ENDPADSTACKS',
        '$COMPONENTS',
        'COMPONENT L8',
        'DEVICE 15017501_Generated',
        'PLACE -0.992126 0.7244094',
        'LAYER BOTTOM',
        'ROTATION 90',
        'SHAPE IND_0603_T_3 MIRRORY FLIP',
        '$ENDCOMPONENTS',
        '$PADS',
        'PAD rect48x52 RECTANGULAR 0',
        'RECTANGLE -0.024 -0.026 0.048 0.052',
        '$ENDPADS',
    ]
    return fileLinesMock

@pytest.fixture
def netsTest():
    fileLinesMock = [
        '$SIGNALS',
        'SIGNAL +5V',
        'NODE L10 2',
        'NODE L9 2',
        'NODE R283 2',
        'NODE R283 1',
        'SIGNAL BUS1_AF',
        'NODE L10 1',
        'SIGNAL N16516693',
        'NODE L9 1',
        '$ENDSIGNALS',
        '$COMPONENTS',
        'COMPONENT L10',
        'DEVICE 15016530_Generated',
        'PLACE 0.6614173 3.925197',
        'LAYER TOP',
        'ROTATION 0',
        'SHAPE IND_LVS404018_T 0 0',
        'COMPONENT L9',
        'DEVICE 15021261_Generated',
        'PLACE 3.318898 3.283465',
        'LAYER TOP',
        'ROTATION 0',
        'SHAPE IND_COILCRAFT_XAL4040_T 0 0',
        'COMPONENT R283',
        'DEVICE 15014524_Generated',
        'PLACE 0.6299213 1.799213',
        'LAYER TOP',
        'ROTATION 270',
        'SHAPE R0603_T 0 0',
        '$ENDCOMPONENTS',
        '$SHAPES',
        'SHAPE IND_LVS404018_T',
        'LINE -0.08267717 0.08129921 0.08267717 0.08232283',
        'LINE 0.08267717 0.08232283 0.08267717 -0.08267717',
        'LINE 0.08267717 -0.08267717 -0.08267717 -0.08267717',
        'LINE -0.08267717 -0.08267717 -0.08267717 0.08129921',
        'INSERT smt',
        'HEIGHT 0.078740',
        'PIN 1 padstack33 -0.05511811 -9.84252e-08 TOP 0 0',
        'PIN 2 padstack33 0.05511811 -9.84252e-08 TOP 0 0',
        'SHAPE IND_COILCRAFT_XAL4040_T',
        'RECTANGLE -0.07874016 -0.07874016 0.1574803 0.1574803',
        'INSERT smt',
        'HEIGHT 0.161417',
        'PIN 1 padstack34 -0.04724409 0 TOP 0 0',
        'PIN 2 padstack34 0.04724409 0 TOP 0 0',
        'SHAPE R0603_T',
        'RECTANGLE -0.035 -0.02 0.07 0.04',
        'INSERT smt',
        'HEIGHT 0.018110',
        'PIN 1 padstack36 0.03110236 0 TOP 90 0',
        'PIN 2 padstack35 -0.03110236 0 TOP 90 0',
        '$ENDSHAPES',
        '$PADSTACKS',
        'PADSTACK padstack33 0',
        'PAD rect55.118x153.543 SOLDERMASK_TOP 0 0',
        'PAD rect43.307x141.732 SOLDERPASTE_TOP 0 0',
        'PAD rect47.244x145.669 TOP 0 0',
        'PADSTACK padstack34 0',
        'PAD rect46.457x153.543 SOLDERMASK_TOP 0 0',
        'PAD rect36.22x143.307 SOLDERPASTE_TOP 0 0',
        'PAD rect38.583x145.669 TOP 0 0',
        'PADSTACK padstack35 0',
        'PAD rect51.969x48.031 SOLDERMASK_TOP 0 0',
        'PAD smd_r0603+1_2314166692 SOLDERPASTE_TOP 0 0',
        'PAD rect44.094x40.157 TOP 0 0',
        'PADSTACK padstack36 0',
        'PAD rect51.969x48.031 SOLDERMASK_TOP 0 0',
        'PAD smd_r0603+1_2314166692 SOLDERPASTE_TOP 180 0',
        'PAD rect44.094x40.157 TOP 0 0',
        '$ENDPADSTACKS',
        '$PADS',
        'PAD rect55.118x153.543 RECTANGULAR 0',
        'RECTANGLE -0.02755896 -0.07677146 0.05511801 0.153543',
        'PAD rect43.307x141.732 RECTANGULAR 0',
        'RECTANGLE -0.02165344 -0.07086594 0.04330699 0.141732',
        'PAD rect47.244x145.669 RECTANGULAR 0',
        'RECTANGLE -0.02362195 -0.07283445 0.047244 0.145669',
        'PAD rect46.457x153.543 RECTANGULAR 0',
        'RECTANGLE -0.02322844 -0.07677146 0.04645699 0.153543',
        'PAD rect36.22x143.307 RECTANGULAR 0',
        'RECTANGLE -0.01810994 -0.07165344 0.03621998 0.143307',
        'PAD rect38.583x145.669 RECTANGULAR 0',
        'RECTANGLE -0.01929144 -0.07283445 0.03858297 0.145669',
        'PAD rect51.969x48.031 RECTANGULAR 0',
        'RECTANGLE -0.02598445 -0.02401545 0.051969 0.048031',
        '$ENDPADS',
    ]
    return fileLinesMock

@pytest.fixture
def tracksTest():
    fileLinesMock = [
        '$ROUTES',
        'ROUTE GND',
        'TRACK 79',
        'LAYER TOP',
        'LINE 1898.622 519.528 1907.913 510.236',
        'LINE 1907.913 510.236 1949.213 510.236',
        'LAYER BOTTOM',
        'LINE 609.843 294.882 591.339 313.386',
        'LINE 591.339 313.386 591.339 349.449',
        'ROUTE N16780000',
        'LAYER BOTTOM',
        'TRACK r11.811',
        'LINE 5.245827 3.013543 5.220472 2.988189',
        '$ENDROUTES',
    ]
    return fileLinesMock

def test__getSectionsLinesBeginEnd(sectionsRangeTest):
    instance = GenCadLoader()
    instance._getSectionsLinesBeginEnd(sectionsRangeTest)
    expected = {'BOARD':[0, 1], 'PADS':[2, 4], 'SHAPES':[5, 6], 'COMPONENTS':[7, 8], 'SIGNALS':[9, 10], 'ROUTES':[11, 12], 'MECH':[13, 14], 'PADSTACKS':[]}
    assert instance.sectionsLineNumbers == expected

def test___calculateRange(sectionsRangeTest):
    instance = GenCadLoader()
    instance._getSectionsLinesBeginEnd(sectionsRangeTest)
    assert instance._calculateRange('SIGNALS') == range(9, 10)

def test__getLineFromLINE():
    line = ['1967.441', '2267.244', '2026.496', '3267.244']    
    bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
    
    instance = GenCadLoader()
    shape, bottomLeftPoint, topRightPoint = instance._getLineFromLINE(line, bottomLeftPoint, topRightPoint)
    assert shape == gobj.Line(gobj.Point(1967.441, 2267.244), gobj.Point(2026.496, 3267.244))
    assert bottomLeftPoint == gobj.Point(1967.441, 2267.244)
    assert topRightPoint == gobj.Point(2026.496, 3267.244)

def test__getArcFromARC():
    line = ['996.063', '137.795', '956.693', '137.795', '976.378', '147.795']    
    bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
    
    instance = GenCadLoader()
    shape, bottomLeftPoint, topRightPoint = instance._getArcFromARC(line, bottomLeftPoint, topRightPoint)
    assert shape == gobj.Arc(gobj.Point(996.063, 137.795), gobj.Point(956.693, 137.795), gobj.Point(976.378, 147.795))
    assert bottomLeftPoint == gobj.Point(956.693, 137.795)
    assert topRightPoint == gobj.Point(996.063, 147.795)

def test__getCircleFromCIRCLE():
    line = ['-2.8661417', '2.527559', '0.08070866']
    bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()

    instance = GenCadLoader()
    shape, bottomLeftPoint, topRightPoint = instance._getCircleFromCIRCLE(line, bottomLeftPoint, topRightPoint)
    assert shape == gobj.Circle(gobj.Point(-2.8661417, 2.527559), 0.08070866)
    assert bottomLeftPoint == gobj.Point(-2.94685036, 2.44685034)
    assert topRightPoint == gobj.Point(-2.78543304, 2.60826766)

def test__getRectFromRECTANGLE():
    line = ['-0.02755896', '-0.03149596', '0.05511801', '0.06299203']
    bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()

    instance = GenCadLoader()
    shape, bottomLeftPoint, topRightPoint = instance._getRectFromRECTANGLE(line, bottomLeftPoint, topRightPoint)
    assert shape == gobj.Rectangle(gobj.Point(-0.02755896, -0.03149596), gobj.Point(-0.02755896 + 0.05511801, -0.03149596 + 0.06299203))
    assert bottomLeftPoint == gobj.Point(-0.02755896, -0.03149596)
    assert topRightPoint == gobj.Point(-0.02755896 + 0.05511801, -0.03149596 + 0.06299203)

def test__getBoardDimensions(bouardOutlineTest):
    instance = GenCadLoader()
    instance._getSectionsLinesBeginEnd(bouardOutlineTest)
    instance._getBoardDimensions(bouardOutlineTest, instance.boardData)  
    shapes = instance.boardData.getOutlines()

    assert len(instance.boardData.getOutlines()) == 5
    assert instance.boardData.getArea() == [gobj.Point(-4.08, 1.712375), gobj.Point(0.2900811, 3.860051)]
    assert shapes[0] == gobj.Arc(gobj.Point(0.2900811, 3.820681), gobj.Point(0.250711, 3.860051), gobj.Point(0.250711, 3.820681))
    assert shapes[1] == gobj.Line(gobj.Point(0.2900811, 2.129768), gobj.Point(0.2506389, 2.090325))
    assert shapes[2] == gobj.Line(gobj.Point(0.2506389, 2.090325), gobj.Point(0.2506389, 1.712375))
    assert shapes[3] == gobj.Arc(gobj.Point(-4.046038, 3.859678), gobj.Point(-4.08, 3.820681), gobj.Point(-4.04063, 3.820681))
    assert shapes[4] == gobj.Circle(gobj.Point(-2.8661417, 2.527559), 0.08070866)

@pytest.mark.parametrize("testInput, expected", [('PAD "Round 32" ROUND -1', ['PAD', 'Round 32', 'ROUND', '-1']), 
                                                 ('ARTWORK artwork9 SOLDERPASTE_BOTTOM', ['ARTWORK', 'artwork9', 'SOLDERPASTE_BOTTOM']), 
                                                 ('PAD    "O b l o n g 2.7x1.7"  FINGER -1', ['PAD', 'O b l o n g 2.7x1.7', 'FINGER', '-1'])])
def test__splitButNotBetweenCharacter(testInput, expected):
    instance = GenCadLoader()
    assert expected == instance._splitButNotBetweenCharacter(testInput, ' ', '"')

def test__getPadsFromPADS(padsTest):
    instance = GenCadLoader()
    instance._getSectionsLinesBeginEnd(padsTest)
    padsDict = instance._getPadsFromPADS(padsTest)
    assert list(padsDict.keys()) == ['Round 32', 'Oblong 3.2x5.2', 'Rectangle;1.15x1.65']
    
    assert padsDict['Round 32'].name == 'Round 32'
    assert padsDict['Round 32'].shape == 'CIRCLE'
    assert padsDict['Round 32'].area == [gobj.Point(-0.406, -0.406), gobj.Point(0.406, 0.406)]
    assert padsDict['Round 32'].coords == gobj.Point(0, 0)
    assert padsDict['Round 32'].width == 0.812
    assert padsDict['Round 32'].height == 0.812

    assert padsDict['Oblong 3.2x5.2'].name == 'Oblong 3.2x5.2'
    assert padsDict['Oblong 3.2x5.2'].shape == 'RECT'    
    assert padsDict['Oblong 3.2x5.2'].area == [gobj.Point(-1.6, -1), gobj.Point(1.6, 1)]
    assert padsDict['Oblong 3.2x5.2'].coords == gobj.Point(0, 0)
    assert padsDict['Oblong 3.2x5.2'].width == 3.2
    assert padsDict['Oblong 3.2x5.2'].height == 2

    assert padsDict['Rectangle;1.15x1.65'].name == 'Rectangle;1.15x1.65'
    assert padsDict['Rectangle;1.15x1.65'].shape == 'RECT'
    assert padsDict['Rectangle;1.15x1.65'].area == [gobj.Point(-0.575, -0.825), gobj.Point(0.575, 0.825)]
    assert padsDict['Rectangle;1.15x1.65'].coords == gobj.Point(0, 0)
    assert padsDict['Rectangle;1.15x1.65'].width == 1.150
    assert padsDict['Rectangle;1.15x1.65'].height == 1.650

def test__getPadstacksFromPADSTACKS(padsTest):
    instance = GenCadLoader()
    instance._getSectionsLinesBeginEnd(padsTest)
    padsDict = instance._getPadsFromPADS(padsTest)
    padstackDict = instance._getPadstacksFromPADSTACKS(padsTest, padsDict)
    assert list(padstackDict.keys()) == ['026VIA', 'Smd 0.95x1.45 mm_TOP']
    assert padstackDict['026VIA'] is padsDict['Round 32']
    assert padstackDict['Smd 0.95x1.45 mm_TOP'] is padsDict['Rectangle;1.15x1.65']

def test__getComponentsFromCOMPONENTS(componentTest):
    instance = GenCadLoader()
    instance._getSectionsLinesBeginEnd(componentTest)
    shapeDict = instance._getComponentsFromCOMPONENTS(componentTest, instance.boardData)
    componentsDict = instance.boardData.getComponents()

    assert list(componentsDict.keys()) == ['VR1', 'C90']

    assert componentsDict['VR1'].name == 'VR1'
    assert componentsDict['VR1'].coords == gobj.Point(-2.970, 1.110)
    assert componentsDict['VR1'].side == 'B'
    assert componentsDict['VR1'].angle == 0

    assert componentsDict['C90'].name == 'C90'
    assert componentsDict['C90'].coords == gobj.Point(1701.181, 515.354)
    assert componentsDict['C90'].side == 'T'
    assert componentsDict['C90'].angle == 270

    assert list(shapeDict.keys()) == ['RV-17X11X7.5P-M', 'C0402_T']
    assert shapeDict['RV-17X11X7.5P-M'] == ['VR1']    
    assert shapeDict['C0402_T'] == ['C90']

def test__coordsListToBottomLeftTopRightPoint():
    instance = GenCadLoader()
    inputData = ['0.1417323', '-0.1309055', '0.1417323', '-0.08267717', '0.1417323', '-0.08267717', '0.09448819', '-0.08267717', 
                 '0.09448819', '-0.08267717', '0.09448819', '-0.1309055', '0.09448819', '-0.1309055', '0.06299213', '-0.1309055']
    point1, point2 = instance._coordsListToBottomLeftTopRightPoint(inputData)
    assert [point1, point2] == [gobj.Point(0.06299213, -0.1309055), gobj.Point(0.1417323, -0.08267717)]

@pytest.mark.parametrize("testInput, expected", [([[1, 2, 3, 4], [5, 6]], [1, 2, 3, 4, 5, 6]), ([[1, 2, 3], [4, 5, 6]], [1, 2, 3, 4, 5, 6]), 
                                                 ([[]], []), ([], []), ([[], [5, 6]], [5, 6]), ([[1, 2, 3], []], [1, 2, 3])])
def test__unnestCoordsList(testInput, expected):
    instance = GenCadLoader()
    assert instance._unnestCoordsList(testInput) == expected

@pytest.mark.parametrize("testInput, expected", [([[-1, -2, 2, 4]], [-1, -2, 1, 2]), 
                                                 ([[-1, -2, 2, 4], [-5, -5, 10, 1]], [-1, -2, 1, 2, -5, -5, 5, -4])])
def test__unnestRectanglesList(testInput, expected):
    instance = GenCadLoader()
    assert instance._unnestRectanglesList(testInput) == expected

def test__calculateShapeAreaInPlace():
    instance = GenCadLoader()
    shapeToComponentsDict = {'LINE':[['-0.1417323', '-0.1309055', '-0.1732283', '-0.1309055'], ['-0.1732283', '-0.1309055', '-0.1732283', '-0.08267717']],
                 'ARC':[['4.043769', '-0.9228939', '4.134528', '-0.7870866', '3.889094', '-0.7212966']],
                 'RECTANGLE':[['-1.021654', '-0.8543307', '2.043307', '1.220472']],
                 'CIRCLE':[[]]}
    
    instance._calculateShapeAreaInPlace(shapeToComponentsDict)

    assert shapeToComponentsDict == {'LINE':[['-0.1417323', '-0.1309055', '-0.1732283', '-0.1309055'], ['-0.1732283', '-0.1309055', '-0.1732283', '-0.08267717']],
                                    'ARC':[['4.043769', '-0.9228939', '4.134528', '-0.7870866', '3.889094', '-0.7212966']],
                                    'RECTANGLE':[['-1.021654', '-0.8543307', '2.043307', '1.220472']],
                                    'CIRCLE':[[]],
                                    'AREA':[gobj.Point(-1.021654, -0.9228939), gobj.Point(4.134528, 0.3661413)],
                                    'AREA_NAME':'RECT'}

    shapeToComponentsDict = {'CIRCLE':[['0', '0', '0.196']]}
    instance._calculateShapeAreaInPlace(shapeToComponentsDict)

    assert shapeToComponentsDict == {'CIRCLE':[['0', '0', '0.196']],
                                    'AREA':[gobj.Point(-0.196, -0.196), gobj.Point(0.196, 0.196)],
                                    'AREA_NAME':'CIRCLE'}

def test__getAreaPinsfromSHAPES(shapesTest):
    instance = GenCadLoader()
    instance._getSectionsLinesBeginEnd(shapesTest)
    shapes = {'SMC_T':{ 
                'SHAPE': [['SMC_T']],
                'LINE':[['0.13386', '0.11614', '0.19705', '0.075'], ['0.19705', '0.075', '0.19705', '-0.075'], ['0.19705', '-0.075', '0.13386', '-0.11614'], 
                    ['0.13386', '-0.11614', '-0.13386', '-0.11614'], ['-0.13386', '-0.11614', '-0.19705', '-0.075'], ['-0.19705', '-0.075', '-0.19705', '0.075'],
                    ['-0.19705', '0.075', '-0.13386', '0.11614'], ['-0.13386', '0.11614', '0.13386', '0.11614']],
                'INSERT': [['smt']],
                'HEIGHT': [['0.103150']],
                'PIN': [['A', 'padstack102', '0.1279528', '0', 'TOP', '270', '0'], ['K', 'padstack102', '-0.1279528', '0', 'TOP', '270', '0']],
                'AREA':[gobj.Point(-0.197, -0.11614), gobj.Point(0.19705, 0.11614)],
                'AREA_NAME': 'RECT'
                }
            }
    assert instance._getAreaPinsfromSHAPES(shapesTest) == shapes

def test__addShapePadDataToComponent(fullComponentTest):
    instance = GenCadLoader()
    instance._getSectionsLinesBeginEnd(fullComponentTest)
    padsDict = instance._getPadsFromPADS(fullComponentTest)
    padstackDict = instance._getPadstacksFromPADSTACKS(fullComponentTest, padsDict)
    shapeToComponentsDict = instance._getComponentsFromCOMPONENTS(fullComponentTest, instance.boardData)
    shapesDict = instance._getAreaPinsfromSHAPES(fullComponentTest)
    instance._addShapePadDataToComponent(instance.boardData, shapeToComponentsDict, shapesDict, padstackDict)

    componentInstance = instance.boardData.getElementByName('components', 'L8')
    pin1 = componentInstance.getPinByName('1') 
    pin2 = componentInstance.getPinByName('2')
    
    assert componentInstance.name == 'L8'
    assert componentInstance.side == 'B'
    assert componentInstance.angle == 90
    assert componentInstance.getMountingType() == 'smt'
    assert componentInstance.getShape() == 'RECT'
    assert componentInstance.getShapePoints() == [gobj.Point(-0.976, 0.692), gobj.Point(-0.976, 0.756),
                                                  gobj.Point(-1.008, 0.756), gobj.Point(-1.008, 0.692)]
    assert componentInstance.getCoords() == gobj.Point(-0.992, 0.724)
    assert componentInstance.getArea() == [gobj.Point(-1.008, 0.692), gobj.Point(-0.977, 0.755)] # (-1.024, 0.708) (-0.960, 0.740) before rotation

    assert pin1 is not pin2
    assert pin1.getCoords() == gobj.Point(-0.992, 0.755) # (-0.961, 0.724) before rotation
    assert pin1.getArea() == [gobj.Point(-1.018, 0.731), gobj.Point(-0.966, 0.779)] # (-0.985, 0.698); (-0.937, 0.750) before rotation
    assert pin1.getShapePoints() == [gobj.Point(-0.966, 0.731), gobj.Point(-0.966, 0.779), gobj.Point(-1.018, 0.779), gobj.Point(-1.018, 0.731)]

    assert pin2.getCoords() == gobj.Point(-0.992, 0.693) # (-1.023, 0.724) before rotation
    assert pin2.getArea() == [gobj.Point(-1.016, 0.667), gobj.Point(-0.968, 0.719)] # (-0.026, -0.024); (0.026, 0.024) -> (-1.049, 0.700); (-0.997, 0.748) before rotation
    assert pin2.getShapePoints() == [gobj.Point(-1.016, 0.667), gobj.Point(-0.968, 0.667), gobj.Point(-0.968, 0.719), gobj.Point(-1.016, 0.719)]

def test__getNetsFromSIGNALS(netsTest):
    instance = GenCadLoader()      
    instance._getSectionsLinesBeginEnd(netsTest)
    padsDict = instance._getPadsFromPADS(netsTest)
    padstackDict = instance._getPadstacksFromPADSTACKS(netsTest, padsDict)
    shapeToComponentsDict = instance._getComponentsFromCOMPONENTS(netsTest, instance.boardData)
    shapesDict = instance._getAreaPinsfromSHAPES(netsTest)
    instance._addShapePadDataToComponent(instance.boardData, shapeToComponentsDict, shapesDict, padstackDict)
    instance._getNetsFromSIGNALS(netsTest, instance.boardData)

    boardNets = instance.boardData.getNets()
    boardComponents = instance.boardData.getComponents()

    ## name of nets
    assert list(boardNets.keys()) == ['+5V', 'BUS1_AF', 'N16516693']
    
    ## components in the nets
    assert list((boardNets['+5V'].keys())) == ['L10', 'L9', 'R283']
    assert 'L10' in boardNets['BUS1_AF']
    assert 'L9' in boardNets['N16516693']

    ## proper component mapping
    assert boardNets['+5V']['L10']['componentInstance'] is boardComponents['L10']
    assert boardNets['+5V']['L10']['pins'] == ['2']
    assert boardComponents['L10'].getPinByName('2').getNet() == '+5V'

    assert boardNets['+5V']['L9']['componentInstance'] is boardComponents['L9']
    assert boardNets['+5V']['L9']['pins'] == ['2']
    assert boardComponents['L9'].getPinByName('2').getNet() == '+5V'

    assert boardNets['+5V']['R283']['componentInstance'] is boardComponents['R283']
    assert boardNets['+5V']['R283']['pins'] == ['2', '1']
    assert boardComponents['R283'].getPinByName('2').getNet() == '+5V'
    assert boardComponents['R283'].getPinByName('1').getNet() == '+5V'

    assert boardNets['BUS1_AF']['L10']['componentInstance'] is boardComponents['L10']
    assert boardNets['BUS1_AF']['L10']['pins'] == ['1']
    assert boardComponents['L10'].getPinByName('1').getNet() == 'BUS1_AF'

    assert boardNets['N16516693']['L9']['componentInstance'] is boardComponents['L9']
    assert boardNets['N16516693']['L9']['pins'] == ['1']
    assert boardComponents['L9'].getPinByName('1').getNet() == 'N16516693'

def test__getTracksFromROUTES(tracksTest):
    instance = GenCadLoader()      
    instance._getSectionsLinesBeginEnd(tracksTest)
    instance._getTracksFromROUTES(tracksTest, instance.boardData)

    boardTracks = instance.boardData.getTracks()
    assert list(boardTracks.keys()) == ['GND', 'N16780000']
    assert boardTracks['GND']['T'] == [gobj.Line(gobj.Point(1898.622, 519.528), gobj.Point(1907.913, 510.236)),
                                       gobj.Line(gobj.Point(1907.913, 510.236), gobj.Point(1949.213, 510.236))]
    assert boardTracks['GND']['B'] == [gobj.Line(gobj.Point(609.843, 294.882), gobj.Point(591.339, 313.386)),
                                       gobj.Line(gobj.Point(591.339, 313.386), gobj.Point(591.339, 349.449))]
    
    assert boardTracks['N16780000']['T'] == []
    assert boardTracks['N16780000']['B'] == [gobj.Line(gobj.Point(5.245827, 3.013543), gobj.Point(5.220472, 2.988189))]