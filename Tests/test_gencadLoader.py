import pytest
from Loaders.gencadLoader import GenCadLoader
import geometryObjects

@pytest.fixture
def sectionsRangeTest():
    fileLinesMock = [
        '$BOARD\n',
        '$ENDBOARD\n',
        '$PADS\n',        
        'PIN\n',
        '$ENDPADS\n',
        '$SHAPES\n',
        '$ENDSHAPES\n',
        '$COMPONENTS\n',
        '$ENDCOMPONENTS\n',
        '$SIGNALS\n',
        '$ENDSIGNALS\n',
        '$ROUTES\n',
        '$ENDROUTES\n',
        '$MECH\n',
        '$ENDMECH\n',
    ]
    return fileLinesMock

@pytest.fixture
def bouardOutlineTest():
    fileLinesMock = [
        '$BOARD\n',
        'ARC 0.2900811 3.820681 0.250711 3.860051 0.250711 3.820681\n',
        'LINE 0.2900811 2.129768 0.2506389 2.090325\n',
        'LINE 0.2506389 2.090325 0.2506389 1.712375\n',
        'ARC -4.046038 3.859678 -4.08 3.820681 -4.04063 3.820681\n',
        'CIRCLE -2.8661417 2.527559 0.08070866\n',
        'ARTWORK artwork1450 SILKSCREEN_TOP\n',
        'LINE 1967.441 2267.244 -2026.496 -2267.244\n',
        '$ENDBOARD\n'
    ]
    return fileLinesMock

def test__getSectionsLinesBeginEnd(sectionsRangeTest):
    instance = GenCadLoader()
    instance._getSectionsLinesBeginEnd(sectionsRangeTest)
    expected = {'BOARD':[0, 1], 'PADS':[2, 4], 'SHAPES':[5, 6], 'COMPONENTS':[7, 8], 'SIGNALS':[9, 10], 'ROUTES':[11, 12], 'MECH':[13, 14]}
    assert instance.sectionsLineNumbers == expected

def test___calculateRange(sectionsRangeTest):
    instance = GenCadLoader()
    instance._getSectionsLinesBeginEnd(sectionsRangeTest)
    assert instance._calculateRange('SIGNALS') == range(9, 10)

def test__getLineFromLINE():
    line = ['1967.441', '2267.244', '2026.496', '3267.244']    
    bottomLeftPoint = geometryObjects.Point(float('Inf'), float('Inf'))
    topRightPoint = geometryObjects.Point(float('-Inf'), float('-Inf'))
    
    instance = GenCadLoader()
    shape, bottomLeftPoint, topRightPoint = instance._getLineFromLINE(line, bottomLeftPoint, topRightPoint)
    assert shape == geometryObjects.Line(geometryObjects.Point(1967.441, 2267.244), geometryObjects.Point(2026.496, 3267.244))
    assert bottomLeftPoint == geometryObjects.Point(1967.441, 2267.244)
    assert topRightPoint == geometryObjects.Point(2026.496, 3267.244)

def test__getArcFromARC():
    line = ['996.063', '137.795', '956.693', '137.795', '976.378', '147.795']    
    bottomLeftPoint = geometryObjects.Point(float('Inf'), float('Inf'))
    topRightPoint = geometryObjects.Point(float('-Inf'), float('-Inf'))
    
    instance = GenCadLoader()
    shape, bottomLeftPoint, topRightPoint = instance._getArcFromARC(line, bottomLeftPoint, topRightPoint)
    assert shape == geometryObjects.Arc(geometryObjects.Point(996.063, 137.795), geometryObjects.Point(956.693, 137.795), geometryObjects.Point(976.378, 147.795))
    assert bottomLeftPoint == geometryObjects.Point(956.693, 137.795)
    assert topRightPoint == geometryObjects.Point(996.063, 147.795)

def test__getCircleFromCIRCLE():
    line = ['-2.8661417', '2.527559', '0.08070866']
    bottomLeftPoint = geometryObjects.Point(float('Inf'), float('Inf'))
    topRightPoint = geometryObjects.Point(float('-Inf'), float('-Inf'))

    instance = GenCadLoader()
    shape, bottomLeftPoint, topRightPoint = instance._getCircleFromCIRCLE(line, bottomLeftPoint, topRightPoint)
    assert shape == geometryObjects.Circle(geometryObjects.Point(-2.8661417, 2.527559), 0.08070866)
    assert bottomLeftPoint == geometryObjects.Point(-2.94685036, 2.44685034)
    assert topRightPoint == geometryObjects.Point(-2.78543304, 2.60826766)

def test__getBoardDimensions(bouardOutlineTest):
    instance = GenCadLoader()
    instance._getSectionsLinesBeginEnd(bouardOutlineTest)
    instance._getBoardDimensions(bouardOutlineTest, instance.boardData)  
    shapes = instance.boardData.getOutlines()

    assert len(instance.boardData.getOutlines()) == 5
    assert instance.boardData.getArea() == [geometryObjects.Point(-4.08, 1.712375), geometryObjects.Point(0.2900811, 3.860051)]
    assert shapes[0] == geometryObjects.Arc(geometryObjects.Point(0.2900811, 3.820681), geometryObjects.Point(0.250711, 3.860051), geometryObjects.Point(0.250711, 3.820681))
    assert shapes[1] == geometryObjects.Line(geometryObjects.Point(0.2900811, 2.129768), geometryObjects.Point(0.2506389, 2.090325))
    assert shapes[2] == geometryObjects.Line(geometryObjects.Point(0.2506389, 2.090325), geometryObjects.Point(0.2506389, 1.712375))
    assert shapes[3] == geometryObjects.Arc(geometryObjects.Point(-4.046038, 3.859678), geometryObjects.Point(-4.08, 3.820681), geometryObjects.Point(-4.04063, 3.820681))
    assert shapes[4] == geometryObjects.Circle(geometryObjects.Point(-2.8661417, 2.527559), 0.08070866)

@pytest.mark.parametrize("testInput, expected", [('PAD "Round 32" ROUND -1', ['PAD', '"Round_32"', 'ROUND', '-1']), 
                                                 ('ARTWORK artwork9 SOLDERPASTE_BOTTOM', ['ARTWORK', 'artwork9', 'SOLDERPASTE_BOTTOM']), 
                                                 ('PAD "O b l o n g 2.7x1.7" FINGER -1', ['PAD', '"O_b_l_o_n_g_2.7x1.7"', 'FINGER', '-1'])])
def test__splitButNotBetweenCharacter(testInput, expected):
    instance = GenCadLoader()
    assert expected == instance._splitButNotBetweenCharacter(testInput, ' ', '"')