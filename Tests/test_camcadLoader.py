import pytest
from Loaders.camcadLoader import CamCadLoader
import geometryObjects

@pytest.fixture
def exampleFileLines():
    fileLinesMock = [       
        ':BOARDINFO\n',
        '15015648 , ,-0.081 ,-4.216 ,3.857 ,0.081 ,02/16/18 , ,INCH ,0.061 ,31\n',
        ':ENDBOARDINFO\n',
        '\n',
        ':PARTLIST\n',
        '0 ,FID1 ,PNFID ,0.101 ,-0.109 ,T,0\n',
        '0 ,FID2 ,PNFID ,1.152 ,-1.530 ,T,0\n',
        '0 ,FID3 ,PNFID ,1.860 ,-0.821 ,T,0\n',
        '0 ,FID4 ,PNFID ,3.365 ,-3.413 ,T,0\n',
        ':ENDPARTLIST\n',
        '\n',
        ':NETLIST\n',
        '0 ,BT_OUT ,C1 ,1 ,1.799 ,-0.028 ,T,150\n',
        '0 ,BT_OUT ,DZ2 ,K ,0.556 ,0.260 ,T,153\n',
        '0 ,BT_OUT ,OC1 ,C ,0.406 ,0.371 ,T,159\n',
        '0 ,BT_OUT ,TP13 ,1 ,2.136 ,-0.079 ,B,161\n',
        '0 ,BT_OUT ,X3 ,6 ,2.140 ,-0.238 ,A,155\n',
        '1 ,GND ,C1 ,2 ,1.737 ,-0.028 ,T,150\n', 
        ':ENDNETLIST\n',
        '\n',
        ':PNDATA\n',
        '15004900 ,31 ,15004900 ,15 ,.0 ,0 ,0 ,D_SOT23_T\n',
        '15022555 ,700 ,15022555 ,2 ,.0 ,0 ,0 ,CN_STELVIO_MRT12P5_2_T\n',
        '15022556 ,700 ,15022556 ,2 ,.0 ,0 ,0 ,CN_STELVIO_MRT12P5_2_T\n',
        ':ENDPNDATA\n',
        '\n',
        ':PACKAGES\n',
        'CN_LUMBERG_3644_3 ,TH ,0.746 ,0.681 ,0.000\n',
        'CN_LUMBERG_3644_2 ,TH ,0.746 ,0.484 ,0.000\n',
        'CN_STELVIO_MRT12P5_2_T ,TH ,0.394 ,0.295 ,0.000\n',
        'CN_EDGE50_3_LUMBERG3575 ,TH ,0.480 ,0.374 ,0.000\n',
        'CN_EDGE25_6_LUMBERG3517 ,TH ,0.579 ,0.295 ,0.000\n',
        ':ENDPACKAGES\n',
        '\n',
        ':PAD\n',
        '0 ,Small Width ,CIRCLE ,0.000 ,0.000 ,0.000 ,0.000\n',
        '1 ,Zero Width ,CIRCLE ,0.000 ,0.000 ,0.000 ,0.000\n',
        '87 ,AP_r2000 ,CIRCLE ,0.079 ,0.079 ,0.039 ,0.039\n',
        ':ENDPAD\n',
        '\n',
        ':BOARDOUTLINE\n',
        '1, 2.238, -0.366, 2.238, -0.177\n',
        '2, 4.028, -0.386, 4.028, -0.287\n',
        '3, 4.028, -0.287, 3.938, -0.287\n',
        ':ENDBOARDOUTLINE\n'
        ]
    return fileLinesMock

@pytest.fixture
def netlistFileLines():
    fileLinesMock = [
        ':NETLIST\n',
        '0 ,NetC41_1 ,TP100 ,1 ,785.190 ,348.564 ,A,222\n',
        '22 ,NetC47_2 ,C47 ,2 ,770.839 ,342.902 ,B,276\n',
        '28 ,NetC47_1 ,C47 ,1 ,771.855 ,342.902 ,B,276\n',
        '22 ,NetC47_2 ,TP135 ,1 ,769.467 ,341.937 ,A,222\n',
        ':ENDNETLIST\n',
        ':PARTLIST\n',        
        ';0 ,TP100 ,PNxx , , ,M,0\n',        
        ';0 ,C47 ,PNxx , , ,M,0\n',
        ';0 ,TP135 ,PNxx , , ,M,0\n',
        ':ENDPARTLIST\n',
        ':PAD\n',
        '222 ,AP_ap_smd_r0402+1_1359_2869477608 ,RECT ,0.020 ,0.020 ,0.010 ,0.010\n',
        '276 ,AP_r400 ,CIRCLE ,0.016 ,0.016 ,0.008 ,0.008\n',
        ':ENDPAD\n',
    ]
    return fileLinesMock

@pytest.fixture
def packagesFileLines():
    fileLinesMock = [
        ':PARTLIST\n',
        '0 ,R40 ,15009285 ,1.020 ,0.878 ,T,180\n',
        '0 ,C10 , ,2.217 ,2.283 ,T,90\n',
        '0 ,LD1 ,15008648 , , ,T,270\n',
        ':ENDPARTLIST\n',
        ':NETLIST\n',
        '7 ,VCC_169 ,R40 ,2 ,1.042 ,0.878 ,T,288\n',
        '9 ,NET0003 ,R40 ,1 ,0.998 ,0.878 ,T,288\n',
        '33 ,NET0011 ,C10 ,1 ,2.217 ,2.305 ,T,288\n',
        '45 ,GND ,C10 ,2 ,2.217 ,2.261 ,T,288\n',
        '18 ,VCC_DISPLAY ,LD1 ,A ,0.882 ,1.930 ,A,255\n',
        '24 ,N16763429 ,LD1 ,K ,0.982 ,2.030 ,A,255\n',         
        ':ENDNETLIST\n',
        ':PNDATA\n',
        '15009285 ,1 ,15009285 ,15 ,10.0 ,0 ,0 ,R0402_T_0\n',
        '15008648 ,80 ,15008648 ,2 ,.0 ,0 ,0 ,LED_3MM\n',
        ':ENDPNDATA\n',
        ':PACKAGES\n',
        'R0402_T_0 ,SMD ,0.080 ,0.036 ,0.000\n',
        'LED_3MM ,TH ,0.178 ,0.078 ,0.000\n',
        ':PACKAGES\n',
    ]
    return fileLinesMock


def test__getSectionsLinesBeginEnd(exampleFileLines):
    instance = CamCadLoader()
    instance._getSectionsLinesBeginEnd(exampleFileLines)
    expected = {'BOARDINFO':[0, 2], 'PARTLIST':[4, 9], 'PNDATA':[20, 24], 'NETLIST':[11, 18], 'PAD':[34, 38], 'PACKAGES':[26, 32], 'BOARDOUTLINE':[40, 44]}
    assert expected == instance.sectionsLineNumbers

def test__calculateRange(exampleFileLines):
    instance = CamCadLoader()
    instance._getSectionsLinesBeginEnd(exampleFileLines)
    assert range(0, 2) == instance._calculateRange('BOARDINFO')
    assert range(4, 9) == instance._calculateRange('PARTLIST')
    assert range(20, 24) == instance._calculateRange('PNDATA')
    assert range(11, 18) == instance._calculateRange('NETLIST')
    assert range(34, 38) == instance._calculateRange('PAD')
    assert range(26, 32) == instance._calculateRange('PACKAGES')
    assert range(40, 44) == instance._calculateRange('BOARDOUTLINE')

def test__getBoardDimensions(exampleFileLines):
    instance = CamCadLoader()
    instance._getSectionsLinesBeginEnd(exampleFileLines)
    instance._getBoardDimensions(exampleFileLines)
    line1 = geometryObjects.Line(geometryObjects.Point(2.238, -0.366), geometryObjects.Point(2.238, -0.177))
    line2 = geometryObjects.Line(geometryObjects.Point(4.028, -0.386), geometryObjects.Point(4.028, -0.287))
    line3 = geometryObjects.Line(geometryObjects.Point(4.028, -0.287), geometryObjects.Point(3.938, -0.287))
    assert line1 == instance.boardData['SHAPE'][0]
    assert line2 == instance.boardData['SHAPE'][1]    
    assert line3 == instance.boardData['SHAPE'][2]
    bottomLeftPoint = geometryObjects.Point(2.238, -0.386)
    topRightPoint = geometryObjects.Point(4.028, -0.177)
    assert bottomLeftPoint == instance.boardData['AREA'][0]
    assert topRightPoint == instance.boardData['AREA'][1]

def test__getComponenentsFromPARTLIST(exampleFileLines):
    instance = CamCadLoader()
    instance._getSectionsLinesBeginEnd(exampleFileLines)
    instance._getComponenentsFromPARTLIST(exampleFileLines)
    component1 = instance.boardData['COMPONENTS']['FID1']
    
    assert component1.name == 'FID1'
    assert component1.coords == geometryObjects.Point(0.101, -0.109)
    assert component1.partNumber == 'PNFID'
    assert component1.side == 'T'
    assert component1.angle == 0

@pytest.mark.parametrize('input, expected', [('1', 1.0), (' ', None),('-1.0', -1.0), ('10.123', 10.123), ('0', 0.0), ('1y9897a', None),])
def test_floatOrNone(input, expected):
    assert CamCadLoader.floatOrNone(input) == expected

def test__getPadsFromPAD(netlistFileLines):
    instance = CamCadLoader()
    instance._getSectionsLinesBeginEnd(netlistFileLines)
    padsDict = instance._getPadsFromPAD(netlistFileLines)
    assert list(padsDict.keys()) == ['222', '276']
    
    pad1 = padsDict['222']
    assert pad1.name == 'AP_ap_smd_r0402+1_1359_2869477608'
    assert pad1.shape == 'RECT'
    assert pad1.width == 0.020
    assert pad1.height == 0.020
    
    pad1 = padsDict['276']
    assert pad1.name == 'AP_r400'
    assert pad1.shape == 'CIRCLE'
    assert pad1.width == 0.016
    assert pad1.height == 0.016

def test__getNetsFromNETLIST(netlistFileLines):
    instance = CamCadLoader()
    instance._getSectionsLinesBeginEnd(netlistFileLines)
    instance._getComponenentsFromPARTLIST(netlistFileLines)    
    instance._getNetsFromNETLIST(netlistFileLines)
    
    ## name of nets
    assert list(instance.boardData['NETS'].keys()) == ['NetC41_1' , 'NetC47_2', 'NetC47_1']

    ## components in the nets
    assert 'TP100' in instance.boardData['NETS']['NetC41_1'] 
    assert 'C47' in instance.boardData['NETS']['NetC47_1'] and 'C47' in instance.boardData['NETS']['NetC47_2']
    assert 'TP135' in instance.boardData['NETS']['NetC47_2']

    ## proper component mapping
    assert instance.boardData['NETS']['NetC41_1']['TP100']['componentInstance'] is instance.boardData['COMPONENTS']['TP100']
    assert instance.boardData['NETS']['NetC41_1']['TP100']['pins'] == ['1']
    assert instance.boardData['COMPONENTS']['TP100'].pins['1']['netName'] == 'NetC41_1'
    assert instance.boardData['COMPONENTS']['TP100'].pins['1']['point'] == geometryObjects.Point(785.190 ,348.564)

    assert instance.boardData['NETS']['NetC47_1']['C47']['componentInstance'] is instance.boardData['COMPONENTS']['C47']
    assert instance.boardData['NETS']['NetC47_1']['C47']['componentInstance'] is instance.boardData['NETS']['NetC47_2']['C47']['componentInstance']
    assert instance.boardData['COMPONENTS']['C47'].pins['1']['netName'] == 'NetC47_1'
    assert instance.boardData['COMPONENTS']['C47'].pins['1']['point'] == geometryObjects.Point(771.855 ,342.902)
    assert instance.boardData['COMPONENTS']['C47'].pins['2']['netName'] == 'NetC47_2'
    assert instance.boardData['COMPONENTS']['C47'].pins['2']['point'] == geometryObjects.Point(770.839 ,342.902)

def test__getPackages(packagesFileLines):
    instance = CamCadLoader()
    instance._getSectionsLinesBeginEnd(packagesFileLines)
    instance._getComponenentsFromPARTLIST(packagesFileLines)    
    instance._getNetsFromNETLIST(packagesFileLines)
    instance._getPackages(packagesFileLines)

    component1_p1, component1_p2 = instance.boardData['COMPONENTS']['R40'].package
    assert component1_p1 == geometryObjects.Point(0.98, 0.860) and component1_p2 == geometryObjects.Point(1.060, 0.896)

    component2_p1, component2_p2 = instance.boardData['COMPONENTS']['C10'].package
    assert component2_p1 == geometryObjects.Point(2.102, 2.148) and component2_p2 == geometryObjects.Point(2.110, 2.190)

    component3_p1, component3_p2 = instance.boardData['COMPONENTS']['LD1'].package
    assert component3_p1 == geometryObjects.Point(0.843, 1.941) and component3_p2 == geometryObjects.Point(1.021, 2.019)