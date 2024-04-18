import pytest
from Loaders.odbPlusPlusLoader import ODBPlusPlusLoader
import geometryObjects as gobj

@pytest.fixture
def exampleTarPaths():
    fileLinesMock = [
        'odb/steps/pcb/attrlist', 
        'odb/steps/pcb/eda', 
        'odb/steps/pcb/eda/data', 
        'odb/steps/pcb/layers', 
        'odb/steps/pcb/layers/comp_+_bot/components.z', 
        'odb/steps/pcb/layers/comp_+_bot/features', 
        'odb/steps/pcb/layers/comp_+_top', 
        'odb/steps/pcb/layers/comp_+_top/components.Z', 
        'odb/steps/pcb/layers/comp_+_top/features', 
        'odb/symbols/rect27.685x31.622xr6.9528_135', 
        'odb/symbols/rect27.685x31.622xr6.9528_135/features', 
        'odb/symbols/rect27.685x31.622xr6.9528_315', 
        'odb/symbols/rect27.685x31.622xr6.9528_315/features',
        'odb/steps/pcb/profile'
        ]
    return fileLinesMock

@pytest.fixture
def exampleComponentsLines():
    compBotMock = [
        '#',
        '#Component attribute names',
        '#',
        '@0 .comp_mount_type',
        '@1 .comp_height',
        '',
        '# CMP 0',
        'CMP 16 -0.5413386 1.6830709 270 N TP49 TP ;0=1,1=0.0669',
        'TOP 0 -0.5393701 1.6830709 270 N 38 0 TP49-1',
        '#'
    ]
    compTopMock = [
        '#',
        '#Component attribute names',
        '#',
        '@0 .comp_mount_type',
        '@1 .comp_height',
        '',
        '# CMP 0',
        'CMP 8 -0.7547244 2.2295276 90 N J1 empty_part_name ;0=1,1=0.0669',
        'TOP 0 -0.8728347 2.3338582 90 N 53 22 J1-1',
        'TOP 1 -0.8728347 2.1251968 90 N 5 3 J1-2',
        'TOP 2 -0.7940946 2.3338582 90 N 52 64 J1-3',
        'TOP 3 -0.7940947 2.1251968 90 N 6 4 J1-4',
        'TOP 4 -0.7153544 2.3338582 90 N 7 5 J1-5',
        'TOP 5 -0.7153545 2.1251968 90 N 4 2 J1-6',
        'TOP 6 -0.6366143 2.3338582 90 N 54 7 J1-7',
        'TOP 7 -0.6366144 2.1251968 90 N 3 3 J1-8',
        '#',
        '# CMP 1',
        'CMP 14 0.4 1.2 270 N TP56 TP ;0=1,1=0.0669',
        'TOP 0 0.4 1.2 270 N 43 0 TP56-1',
        '#'
    ]
    return [compBotMock, compTopMock]

@pytest.fixture
def exampleProfileLines():
    profileMock = [
        'UNITS=MM',
        'ID=6',
        '#',
        '#Num Features',
        '#',
        'F 1',
        '',
        '#',
        '#Layer features',
        '#',
        'S P 0;;ID=62564',
        'OB 1.2 -36.35 H',
        'OS 1.2 -28.85',
        'OC 0 -28.85 0.6 -28.85 N',
        'OS 0 -36.35',
        'OC 1.2 -36.35 0.6 -36.35 N',
        'OE',
        'OB 16.2 -36.35 H',
        'OS 16.2 -28.85',
        'OC 15 -28.85 15.6 -28.85 Y',
        'OS 15 -36.35',
        'OC 16.2 -36.35 15.6 -36.35 N',
        'OE',
        'RC -2.5 -2.5 5 5',
        'SE'
    ]
    return profileMock

@pytest.fixture
def examplePackageLines():
    packagesMock = [
        'SNT TRC',
        'FID C 6 8',
        '# PKG 0',
        'PKG 0402 0.0354332 -0.0275591 -0.011811 0.0275591 0.011811',
        'CT',
        'OB 0.0206738 -0.0106266 I',
        'OS -0.0206646 -0.0106266',
        'OS -0.0206646 0.0106334',
        'OS 0.0206738 0.0106334',
        'OS 0.0206738 -0.0106266',
        'OE',
        'CE',
        'PIN 1 S -0.0177166 0 0 U U',
        'CT',
        'OB -0.0078741 -0.0088582 I',
        'OC -0.0108269 -0.011811 -0.0108269 -0.0088582 Y',
        'OS -0.0246063 -0.011811 I',
        'OC -0.0275591 -0.0088582 -0.0246063 -0.0088582 Y',
        'OS -0.0275591 0.0088582 I',
        'OC -0.0246063 0.011811 -0.0246063 0.0088582 Y',
        'OS -0.0108269 0.011811 I',
        'OC -0.0078741 0.0088582 -0.0108269 0.0088582 Y',
        'OS -0.0078741 -0.0088582 I',
        'OE',
        'CE',
        'PIN 2 S 0.0177166 0 0 U U',
        'CT',
        'OB 0.0275591 -0.0088582 I',
        'OC 0.0246063 -0.011811 0.0246063 -0.0088582 Y',
        'OS 0.0108269 -0.011811 I',
        'OC 0.0078741 -0.0088582 0.0108269 -0.0088582 Y',
        'OS 0.0078741 0.0088582 I',
        'OC 0.0108269 0.011811 0.0108269 0.0088582 Y',
        'OS 0.0246063 0.011811 I',
        'OC 0.0275591 0.0088582 0.0246063 0.0088582 Y',
        'OS 0.0275591 -0.0088582 I',
        'OE',
        'CE',
        '#',
        '# PKG 54',
        'PKG MARKER 0 -1.5 -1.5 1.5 1.5;;ID=1515',
        'RC -1.5 -1.5 3 3',
        "PRP PACKAGE_NAME 'MARKER'", 
        'PIN un_1 S 0 0 0 U U ID=1518',
        'CR 0 0 1',
        '#',
    ]
    return packagesMock

def test__getTarPathsToEdaComponents(exampleTarPaths):
    instance = ODBPlusPlusLoader()
    expected = [
        'odb/steps/pcb/eda/data', 
        'odb/steps/pcb/layers/comp_+_bot/components.z', 
        'odb/steps/pcb/layers/comp_+_top/components.Z',
        'odb/steps/pcb/profile'
        ]
    assert instance._getTarPathsToEdaComponents(exampleTarPaths) == expected

def test__getComponentsFromCompBotTopFiles(exampleComponentsLines):
    botFileLines, topFileLines = exampleComponentsLines
    instance = ODBPlusPlusLoader()
    matchDict = instance._getComponentsFromCompBotTopFiles(botFileLines, topFileLines, instance.boardData)
    
    
    boardComponents = instance.boardData.getComponents()
    expectedMatchDict = {'TP49': {'packageID':'16', '0':'38'},
                        'J1': {'packageID':'8', '0':'53', '1':'5', '2':'52', '3':'6', '4':'7', '5':'4', '6':'54', '7':'3'},
                        'TP56': {'packageID': '14', '0':'43'}}

    assert matchDict == expectedMatchDict
    assert list(boardComponents.keys()) == ['TP49', 'J1', 'TP56']
    
    assert boardComponents['TP49'].getCoords() == gobj.Point(-0.5413386, 1.6830709)
    assert boardComponents['TP49'].getSide() == 'B'
    assert boardComponents['TP49'].getAngle() == 270
    assert boardComponents['J1'].getCoords() == gobj.Point(-0.7547244, 2.2295276)
    assert boardComponents['J1'].getSide() == 'T'
    assert boardComponents['J1'].getAngle() == 90
    assert boardComponents['TP56'].getCoords() == gobj.Point(0.4, 1.2)
    assert boardComponents['TP56'].getSide() == 'T'
    assert boardComponents['TP56'].getAngle() == 270

    pin = boardComponents['TP49'].getPinByName('0')
    assert pin.getCoords() == gobj.Point(-0.5393701, 1.6830709)

    pinNumbers = ['0', '1', '2', '3', '4', '5', '6', '7']
    pinCoords = [(-0.8728347, 2.3338582), (-0.8728347, 2.1251968), (-0.7940946, 2.3338582), (-0.7940947, 2.1251968), 
                 (-0.7153544, 2.3338582), (-0.7153545, 2.1251968), (-0.6366143, 2.3338582), (-0.6366144, 2.1251968)]
    for pinNumber, pinCoords in zip(pinNumbers, pinCoords):
        pin = boardComponents['J1'].getPinByName(pinNumber)
        x, y = pinCoords
        assert pin.getCoords() == gobj.Point(x, y)

    pin = boardComponents['TP56'].getPinByName('0')
    assert pin.getCoords() == gobj.Point(0.4, 1.2)

def test__getShapesAndPointsFromConturSection(exampleProfileLines):
    instance = ODBPlusPlusLoader()
    bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
    shapes, i, bottomLeftPoint, topRightPoint = instance._getShapesAndPointsFromConturSection(exampleProfileLines, 11, bottomLeftPoint, topRightPoint)

    assert i == 16
    assert [bottomLeftPoint, topRightPoint] == [gobj.Point(0, -36.35), gobj.Point(1.2, -28.85)]
    assert shapes[0] == gobj.Line(gobj.Point(1.2, -36.35), gobj.Point(1.2, -28.85))
    assert shapes[1] == gobj.Arc(gobj.Point(1.2, -28.85), gobj.Point(0, -28.85), gobj.Point(0.6, -28.85))
    assert shapes[2] == gobj.Line(gobj.Point(0, -28.85), gobj.Point(0, -36.35))
    assert shapes[3] == gobj.Arc(gobj.Point(0, -36.35), gobj.Point(1.2, -36.35), gobj.Point(0.6, -36.35))

    bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
    shapes, i, bottomLeftPoint, topRightPoint = instance._getShapesAndPointsFromConturSection(exampleProfileLines, 17, bottomLeftPoint, topRightPoint)
    assert i == 22
    assert [bottomLeftPoint, topRightPoint] == [gobj.Point(15, -36.35), gobj.Point(16.2, -28.85)]
    assert shapes[0] == gobj.Line(gobj.Point(16.2, -36.35), gobj.Point(16.2, -28.85))
    assert shapes[1] == gobj.Arc(gobj.Point(15, -28.85), gobj.Point(16.2, -28.85), gobj.Point(15.6, -28.85))
    assert shapes[2] == gobj.Line(gobj.Point(15, -28.85), gobj.Point(15, -36.35))
    assert shapes[3] == gobj.Arc(gobj.Point(15, -36.35), gobj.Point(16.2, -36.35), gobj.Point(15.6, -36.35))

def test__getBoardOutlineFromProfileFile(exampleProfileLines):
    instance = ODBPlusPlusLoader()
    instance._getBoardOutlineFromProfileFile(exampleProfileLines, instance.boardData)
    boardOutlines = instance.boardData.getOutlines()

    assert instance.boardData.getArea() == [gobj.Point(-2.5, -36.35), gobj.Point(16.2, 2.5)]    
    assert len(boardOutlines) == 9

    assert boardOutlines[0] == gobj.Line(gobj.Point(1.2, -36.35), gobj.Point(1.2, -28.85))
    assert boardOutlines[1] == gobj.Arc(gobj.Point(1.2, -28.85), gobj.Point(0, -28.85), gobj.Point(0.6, -28.85))
    assert boardOutlines[2] == gobj.Line(gobj.Point(0, -28.85), gobj.Point(0, -36.35))
    assert boardOutlines[3] == gobj.Arc(gobj.Point(0, -36.35), gobj.Point(1.2, -36.35), gobj.Point(0.6, -36.35))

    assert boardOutlines[4] == gobj.Line(gobj.Point(16.2, -36.35), gobj.Point(16.2, -28.85))
    assert boardOutlines[5] == gobj.Arc(gobj.Point(15, -28.85), gobj.Point(16.2, -28.85), gobj.Point(15.6, -28.85))
    assert boardOutlines[6] == gobj.Line(gobj.Point(15, -28.85), gobj.Point(15, -36.35))
    assert boardOutlines[7] == gobj.Arc(gobj.Point(15, -36.35), gobj.Point(16.2, -36.35), gobj.Point(15.6, -36.35))

    assert boardOutlines[8] == gobj.Rectangle(gobj.Point(-2.5, -2.5), gobj.Point(2.5, 2.5))

def test__getShapeData(examplePackageLines):
    instance = ODBPlusPlusLoader()
    bottomLeftPoint, topRightPoint = gobj.getDefaultBottomLeftTopRightPoints()
    
    shapeName, i, bottomLeftPoint, topRightPoint = instance._getShapeData(examplePackageLines, 4)
    assert shapeName == 'RECT'
    assert i == 10
    assert [bottomLeftPoint, topRightPoint] == [gobj.Point(-0.0206646, -0.0106266), gobj.Point(0.0206738, 0.0106334)] 

    shapeName, i, bottomLeftPoint, topRightPoint = instance._getShapeData(examplePackageLines, 13)
    assert shapeName == 'RECT'
    assert i == 23
    assert [bottomLeftPoint, topRightPoint] == [gobj.Point(-0.0275591, -0.011811), gobj.Point(-0.0078741, 0.011811)] 

    shapeName, i, bottomLeftPoint, topRightPoint = instance._getShapeData(examplePackageLines, 26)
    assert shapeName == 'RECT'
    assert i == 36
    assert [bottomLeftPoint, topRightPoint] == [gobj.Point(0.0078741, -0.011811), gobj.Point(0.0275591, 0.011811)] 

    shapeName, i, bottomLeftPoint, topRightPoint = instance._getShapeData(examplePackageLines, 41)
    assert shapeName == 'RECT'
    assert i == 41
    assert [bottomLeftPoint, topRightPoint] == [gobj.Point(-1.5, -1.5), gobj.Point(1.5, 1.5)] 

    shapeName, i, bottomLeftPoint, topRightPoint = instance._getShapeData(examplePackageLines, 44)
    assert shapeName == 'CIRCLE'
    assert i == 44
    assert [bottomLeftPoint, topRightPoint] == [gobj.Point(-1, -1), gobj.Point(1, 1)]