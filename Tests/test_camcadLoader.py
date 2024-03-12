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
        '19, 2.238, -0.366, 2.238, -0.177\n',
        ':ENDBOARDOUTLINE\n'
        ]
    return fileLinesMock

def test__getSectionsLinesBeginEnd(exampleFileLines):
    instance = CamCadLoader()
    instance._getSectionsLinesBeginEnd(exampleFileLines)
    expected = {'BOARDINFO':[0, 2], 'PARTLIST':[4, 9], 'PNDATA':[20, 24], 'NETLIST':[11, 18], 'PAD':[34, 38], 'PACKAGES':[26, 32], 'BOARDOUTLINE':[40, 42]}
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
    assert range(40, 42) == instance._calculateRange('BOARDOUTLINE')

def test__getBoardDimensions(exampleFileLines):
    pass