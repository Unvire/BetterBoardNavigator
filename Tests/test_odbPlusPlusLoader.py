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
        'CMP 16 0.4 1.2 270 N TP56 TP ;0=1,1=0.0669',
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
        'PIN 1 T -0.0177166 0 0 U U',
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
        'PIN 2 T 0.0177166 0 0 U U',
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
        '#'
    ]
    return packagesMock

@pytest.fixture
def exampleNetLines():
    netMock = [
        '# PKG 0',
        '# NET 0',
        'NET GND ',
        'SNT TRC',
        'FID C 0 0',
        'FID C 0 1',
        'SNT TRC',
        'FID C 0 2',
        'SNT TOP B 21 12',
        'FID C 6 722',
        'FID C 7 19',
        'FID C 8 17',
        'SNT TOP B 40 0',
        'FID C 6 865',
        'FID C 7 159',
        'SNT TOP B 55 0',
        'FID C 6 870',
        'FID C 7 164',
        'FID C 8 139',
        '#NET 1',
        'NET NetQ11_1',
        'SNT TOP T 21 0',
        'FID C 6 721',
        'FID C 7 18',
        'FID C 8 16',
        'SNT TOP T 21 3',
        'FID C 6 861',
        'FID C 7 155'
    ]
    return netMock

@pytest.fixture
def exampleComponentMatchLines():
    componentMockLines = [
        '# CMP 16',
        'CMP 0 -0.046063 0.9043307 90 N C1 RFANT5220110A2T ;0=1,1=0.0492',
        'TOP 0 -0.046063 0.9978346 0 N 51 0 C1-1',
        'TOP 1 -0.046063 0.8108268 0 N 0 0 C1-2',
        '#'
    ]

    packagesMockLines = [
        '# PKG 0',
        'PKG RFANT5220110A2T 0.1870078 -0.1131889 -0.0433071 0.1131889 0.0433071',
        'CT',
        'OB 0.1062992 -0.0433071 I',
        'OS -0.1062992 -0.0433071',
        'OS -0.1062992 0.0433071',
        'OS 0.1062992 0.0433071',
        'OS 0.1062992 -0.0433071',
        'OE',
        'CE',
        'PIN 1 S -0.0935039 0 0 U U',
        'CT',
        'OB -0.1131039 -0.0433 I',
        'OS -0.1131039 0.0433',
        'OS -0.0739039 0.0433',
        'OS -0.0739039 -0.0433',
        'OS -0.1131039 -0.0433',
        'OE',
        'CE',
        'PIN 2 S 0.0935039 0 0 U U',
        'CT',
        'OB 0.0739039 -0.0433 I',
        'OS 0.0739039 0.0433',
        'OS 0.1131039 0.0433',
        'OS 0.1131039 -0.0433',
        'OS 0.0739039 -0.0433',
        'OE',
        'CE',
        '#'
    ]
    return componentMockLines, packagesMockLines

@pytest.fixture
def exampleNetPinsMatchLines():
    bottomComponentMockLines = [
        '# CMP 16',
        'CMP 0 -0.046063 0.9043307 90 N C1 RFANT5220110A2T ;0=1,1=0.0492',
        'TOP 0 -0.046063 0.9978346 0 N 51 0 C1-1',
        'TOP 1 -0.046063 0.8108268 0 N 0 0 C1-2',
        '#'
    ]

    topComponentMockLines = [
        '# CMP 1',
        'CMP 14 0.4 1.2 270 N TP56 TP ;0=1,1=0.0669',
        'TOP 0 0.4 1.2 270 N 43 0 TP56-1',
        '#',
        '# CMP 2',
        'CMP 0 -0.0393701 1.6761811 45 N C13 100nF/50V ;0=1,1=0.0000',
        'TOP 0 -0.0268426 1.6887086 135 N 52 63 C13-1',
        'TOP 1 -0.0518976 1.6636536 135 N 53 21 C13-2',
        '#'
    ]

    netsMockLines = [
        '#NET 1',
        'NET GND',
        'SNT TOP B 16 1',
        'FID C 6 816v',
        'FID C 7 111',
        'SNT TOP T 1 0',
        'FID C 6 712',
        'SNT TOP T 2 0',
        'SNT TRC',
        'FID C 6 300',
        '#NET 6',
        'NET SWCLK',
        'SNT TOP B 16 0',
        'FID C 2 5',
        'FID C 3 299',
        '#NET 11',
        'NET NetQ15_1',
        'SNT TOP T 2 1',
        'FID C 6 769'
    ]
    return bottomComponentMockLines, topComponentMockLines, netsMockLines

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
    packageIDToComponentNameDict, componentIDToNameDict = instance._getComponentsFromCompBotTopFiles(botFileLines, topFileLines, instance.boardData)
    
    boardComponents = instance.boardData.getComponents()
    expectedPackageIDToComponentNameDict = {'16':['TP49', 'TP56'], '8': ['J1']}

    assert packageIDToComponentNameDict == expectedPackageIDToComponentNameDict
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

    pin = boardComponents['TP49'].getPinByName('1')
    assert pin.getCoords() == gobj.Point(-0.5393701, 1.6830709)

    pinNumbers = ['1', '2', '3', '4', '5', '6', '7', '8']
    pinCoords = [(-0.8728347, 2.3338582), (-0.8728347, 2.1251968), (-0.7940946, 2.3338582), (-0.7940947, 2.1251968), 
                 (-0.7153544, 2.3338582), (-0.7153545, 2.1251968), (-0.6366143, 2.3338582), (-0.6366144, 2.1251968)]
    for pinNumber, pinCoords in zip(pinNumbers, pinCoords):
        pin = boardComponents['J1'].getPinByName(pinNumber)
        x, y = pinCoords
        assert pin.getCoords() == gobj.Point(x, y)

    pin = boardComponents['TP56'].getPinByName('1')
    assert pin.getCoords() == gobj.Point(0.4, 1.2)

    expectedComponentIDToNameDict = {'B-0':'TP49', 'T-0':'J1', 'T-1':'TP56'}
    assert componentIDToNameDict == expectedComponentIDToNameDict

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

def test__getPackagesFromEda(examplePackageLines):
    instance = ODBPlusPlusLoader()
    packagesDict = instance._getPackagesFromEda(examplePackageLines)
    
    assert list(packagesDict.keys()) == ['0', '54']
    assert packagesDict['0']['Area'] == [gobj.Point(-0.0206646, -0.0106266), gobj.Point(0.0206738, 0.0106334)]
    assert packagesDict['0']['Shape'] == 'RECT'
    
    assert list(packagesDict['0']['Pins'].keys()) == ['1', '2']
    assert packagesDict['0']['Pins']['1']['Area'] == [gobj.Point(-0.0275591, -0.011811), gobj.Point(-0.0078741, 0.011811)]
    assert packagesDict['0']['Pins']['1']['Shape'] == 'RECT'
    assert packagesDict['0']['Pins']['2']['Area'] == [gobj.Point(0.0078741, -0.011811), gobj.Point(0.0275591, 0.011811)]
    assert packagesDict['0']['Pins']['2']['Shape'] == 'RECT'

    assert packagesDict['54']['Area'] == [gobj.Point(-1.5, -1.5), gobj.Point(1.5, 1.5)]
    assert packagesDict['54']['Shape'] == 'RECT'

    assert list(packagesDict['54']['Pins'].keys()) == ['1']
    assert packagesDict['54']['Pins']['1']['Area'] == [gobj.Point(-1, -1), gobj.Point(1, 1)]
    assert packagesDict['54']['Pins']['1']['Shape'] == 'CIRCLE'

@pytest.mark.parametrize('inputData, expected', [(2, 'GND'), (20, 'NetQ11_1')])
def test__getNetName(exampleNetLines, inputData, expected):
    instance = ODBPlusPlusLoader()
    
    netName = instance._getNetName(exampleNetLines, inputData)
    assert netName == expected

def test__getPinsOnNet(exampleNetLines):
    instance = ODBPlusPlusLoader()
    
    i, netDict = instance._getPinsOnNet(exampleNetLines, 2)
    assert i == 19
    assert list(netDict.keys()) == ['B-21', 'B-40', 'B-55']
    assert netDict['B-21'] == ['13']
    assert netDict['B-40'] == ['1']
    assert netDict['B-55'] == ['1']

    i, netDict = instance._getPinsOnNet(exampleNetLines, 20)
    assert i == 28
    assert list(netDict.keys()) == ['T-21']
    assert netDict['T-21'] == ['1', '4']

def test__getNetsFromEda(exampleNetLines):
    instance = ODBPlusPlusLoader()

    netsDict = instance._getNetsFromEda(exampleNetLines)
    assert list(netsDict.keys()) == ['GND', 'NetQ11_1']
    assert list(netsDict['GND'].keys()) == ['B-21', 'B-40', 'B-55']
    assert netsDict['GND']['B-21'] == ['13']
    assert netsDict['GND']['B-40'] == ['1']
    assert netsDict['GND']['B-55'] == ['1']
    
    assert list(netsDict['NetQ11_1'].keys()) == ['T-21']
    assert netsDict['NetQ11_1']['T-21'] == ['1', '4']

def test__assignPackagesToComponents(exampleComponentMatchLines):
    bottomComponentLines, packageLines = exampleComponentMatchLines
    instance = ODBPlusPlusLoader()
    packageIDToComponentNameDict, _ = instance._getComponentsFromCompBotTopFiles(bottomComponentLines, [], instance.boardData)
    packagesDict = instance._getPackagesFromEda(packageLines)
    instance._assignPackagesToComponents(packageIDToComponentNameDict, packagesDict, instance.boardData)

    components = instance.boardData.getComponents()
    assert list(components.keys()) == ['C1']

    componentInstance = instance.boardData.getElementByName('components', 'C1')
    assert componentInstance.name == 'C1'
    assert componentInstance.side == 'B'
    assert componentInstance.angle == 90
    assert componentInstance.getMountingType() == 'SMT'
    assert componentInstance.getShape() == 'RECT'
    assert componentInstance.getCoords() == gobj.Point(-0.046063, 0.9043307)
    assert componentInstance.getArea() == [gobj.Point(-0.089370, 0.798032), gobj.Point(-0.002756, 1.010630)] # (-0.152362 0.861024), (0.060236 0.947638) before rotation
    assert componentInstance.getShapePoints() == [gobj.Point(-0.002756, 0.798032), gobj.Point(-0.002756, 1.010630),
                                                  gobj.Point(-0.089370, 1.010630), gobj.Point(-0.089370, 0.798032)]

    pin1 = componentInstance.getPinByName('1')
    pin2 = componentInstance.getPinByName('2')
    assert pin1 is not pin2

    assert pin1.getCoords() == gobj.Point(-0.139567, 0.904331) # (-0.046063, 0.9978346) before rotation
    assert pin1.getArea() == [gobj.Point(-0.182867, 0.791227), gobj.Point(-0.096267, 0.830427)] # (-0.159167, 0.954535), (-0.119967, 1.041135) before rotation
    assert pin1.getShapePoints() == [gobj.Point(-0.096267, 0.791227), gobj.Point(-0.096267, 0.830427),
                                     gobj.Point(-0.182867, 0.830427), gobj.Point(-0.182867, 0.791227)]
    
    assert pin2.getCoords() == gobj.Point(0.047441, 0.904331) # (-0.046063, 0.810827) before rotation
    assert pin2.getArea() == [gobj.Point(0.004141, 0.978235), gobj.Point(0.090741, 1.017435)] # (0.027841, 0.767527), (0.067041, 0.854127) before rotation
    assert pin2.getShapePoints() == [gobj.Point(0.090741, 0.978235), gobj.Point(0.090741, 1.017435),
                                     gobj.Point(0.004141, 1.017435), gobj.Point(0.004141, 0.978235)]
    
def test__assignNetsAndPins(exampleNetPinsMatchLines):
    bottomComponentLines, topComponentLines, netsLines = exampleNetPinsMatchLines
    instance = ODBPlusPlusLoader()
    _, componentIDToNameDict = instance._getComponentsFromCompBotTopFiles(bottomComponentLines, topComponentLines, instance.boardData)
    netsDict = instance._getNetsFromEda(netsLines)
    instance._assignNetsAndPins(componentIDToNameDict, netsDict, instance.boardData)

    boardNets = instance.boardData.getNets()
    assert list(boardNets.keys()) == ['GND', 'SWCLK', 'NetQ15_1']
    assert list(boardNets['GND'].keys()) == ['C1', 'TP56', 'C13']
    assert instance.boardData.getElementByName('components', 'C1') is boardNets['GND']['C1']['componentInstance']
    assert instance.boardData.getElementByName('components', 'TP56') is boardNets['GND']['TP56']['componentInstance']
    assert instance.boardData.getElementByName('components', 'C13') is boardNets['GND']['C13']['componentInstance']
    assert boardNets['GND']['C1']['pins'] == ['2']
    assert boardNets['GND']['TP56']['pins'] == ['1']
    assert boardNets['GND']['C13']['pins'] == ['1']

    assert list(boardNets['SWCLK'].keys()) == ['C1']
    assert instance.boardData.getElementByName('components', 'C1') is boardNets['SWCLK']['C1']['componentInstance']
    assert boardNets['SWCLK']['C1']['pins'] == ['1']

    assert list(boardNets['NetQ15_1'].keys()) == ['C13']
    assert instance.boardData.getElementByName('components', 'C13') is boardNets['NetQ15_1']['C13']['componentInstance']
    assert boardNets['NetQ15_1']['C13']['pins'] == ['2']

    component = instance.boardData.getElementByName('components', 'C1')
    for pinNumber, netName in zip(['1', '2'], ['SWCLK', 'GND']):
        pin = component.getPinByName(pinNumber)
        assert pin.getNet() == netName
    
    component = instance.boardData.getElementByName('components', 'TP56')
    pin = component.getPinByName('1')
    pin.getNet() == 'GND'

    component = instance.boardData.getElementByName('components', 'C13')
    for pinNumber, netName in zip(['1', '2'], ['GND', 'NetQ15_1']):
        pin = component.getPinByName(pinNumber)
        assert pin.getNet() == netName