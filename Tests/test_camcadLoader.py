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
    assert component1.package == 'PNFID'
    assert component1.side == 'T'
    assert component1.angle == 0

def test__getNetsfromNETLIST(netlistFileLines):
    instance = CamCadLoader()
    instance._getSectionsLinesBeginEnd(netlistFileLines)
    instance._getComponenentsFromPARTLIST(netlistFileLines)    
    instance._getNetsfromNETLIST(netlistFileLines)
    
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