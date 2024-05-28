import pytest
from camcadLoader import CamCadLoader
import geometryObjects as gobj

@pytest.fixture
def exampleFileLines():
    fileLinesMock = [       
        ':BOARDINFO',
        '15015648 , ,-0.081 ,-4.216 ,3.857 ,0.081 ,02/16/18 , ,INCH ,0.061 ,31',
        ':ENDBOARDINFO',
        '',
        ':PARTLIST',
        '0 ,FID1 ,PNFID ,0.101 ,-0.109 ,T,0',
        '0 ,FID2 ,PNFID ,1.152 ,-1.530 ,T,0',
        '0 ,FID3 ,PNFID ,1.860 ,-0.821 ,T,0',
        '0 ,FID4 ,PNFID ,3.365 ,-3.413 ,T,0',
        ':ENDPARTLIST',
        '',
        ':NETLIST',
        '0 ,BT_OUT ,C1 ,1 ,1.799 ,-0.028 ,T,150',
        '0 ,BT_OUT ,DZ2 ,K ,0.556 ,0.260 ,T,153',
        '0 ,BT_OUT ,OC1 ,C ,0.406 ,0.371 ,T,159',
        '0 ,BT_OUT ,TP13 ,1 ,2.136 ,-0.079 ,B,161',
        '0 ,BT_OUT ,X3 ,6 ,2.140 ,-0.238 ,A,155',
        '1 ,GND ,C1 ,2 ,1.737 ,-0.028 ,T,150', 
        ':ENDNETLIST',
        '',
        ':PNDATA',
        '15004900 ,31 ,15004900 ,15 ,.0 ,0 ,0 ,D_SOT23_T',
        '15022555 ,700 ,15022555 ,2 ,.0 ,0 ,0 ,CN_STELVIO_MRT12P5_2_T',
        '15022556 ,700 ,15022556 ,2 ,.0 ,0 ,0 ,CN_STELVIO_MRT12P5_2_T',
        ':ENDPNDATA',
        '',
        ':PACKAGES',
        'CN_LUMBERG_3644_3 ,TH ,0.746 ,0.681 ,0.000',
        'CN_LUMBERG_3644_2 ,TH ,0.746 ,0.484 ,0.000',
        'CN_STELVIO_MRT12P5_2_T ,TH ,0.394 ,0.295 ,0.000',
        'CN_EDGE50_3_LUMBERG3575 ,TH ,0.480 ,0.374 ,0.000',
        'CN_EDGE25_6_LUMBERG3517 ,TH ,0.579 ,0.295 ,0.000',
        ':ENDPACKAGES',
        '',
        ':PAD',
        '0 ,Small Width ,CIRCLE ,0.000 ,0.000 ,0.000 ,0.000',
        '1 ,Zero Width ,CIRCLE ,0.000 ,0.000 ,0.000 ,0.000',
        '87 ,AP_r2000 ,CIRCLE ,0.079 ,0.079 ,0.039 ,0.039',
        ':ENDPAD',
        '',
        ':BOARDOUTLINE',
        '1, 2.238, -0.366, 2.238, -0.177',
        '2, 4.028, -0.386, 4.028, -0.287',
        '3, 4.028, -0.287, 3.938, -0.287',
        ':ENDBOARDOUTLINE'
        ]
    return fileLinesMock

@pytest.fixture
def netlistFileLines():
    fileLinesMock = [
        ':NETLIST',
        '0 ,NetC41_1 ,TP100 ,1 ,785.190 ,348.564 ,A,222',
        '22 ,NetC47_2 ,C47 ,2 ,770.839 ,342.902 ,B,276',
        '28 ,NetC47_1 ,C47 ,1 ,771.855 ,342.902 ,B,276',
        '22 ,NetC47_2 ,TP135 ,1 ,769.467 ,341.937 ,A,222',
        ':ENDNETLIST',
        ':PARTLIST',        
        ';0 ,TP100 ,PNxx , , ,M,0',        
        ';0 ,C47 ,PNxx , , ,M,0',
        ';0 ,TP135 ,PNxx , , ,M,0',
        ';0 ,TP136 ,PNxx , , ,M,0',
        ':ENDPARTLIST',
        ':PAD',
        '222 ,AP_ap_smd_r0402+1_1359_2869477608 ,RECT ,0.020 ,0.020 ,0.010 ,0.010',
        '276 ,AP_r400 ,CIRCLE ,0.016 ,0.016 ,0.008 ,0.008',
        ':ENDPAD',
    ]
    return fileLinesMock

@pytest.fixture
def packagesFileLines():
    fileLinesMock = [
        ':PARTLIST',
        '0 ,R40 ,15009285 ,1.020 ,0.878 ,T,180',
        '0 ,C10 , ,2.217 ,2.283 ,T,90',
        '0 ,LD1 ,15008648 , , ,T,270',
        ':ENDPARTLIST',
        ':NETLIST',
        '7 ,VCC_169 ,R40 ,2 ,1.042 ,0.878 ,T,288',
        '9 ,NET0003 ,R40 ,1 ,0.998 ,0.878 ,T,288',
        '33 ,NET0011 ,C10 ,1 ,2.217 ,2.305 ,T,288',
        '45 ,GND ,C10 ,2 ,2.217 ,2.261 ,T,288',
        '18 ,VCC_DISPLAY ,LD1 ,A ,0.882 ,1.930 ,A,255',
        '24 ,N16763429 ,LD1 ,K ,0.982 ,2.030 ,A,255',         
        ':ENDNETLIST',
        ':PNDATA',
        '15009285 ,1 ,15009285 ,15 ,10.0 ,0 ,0 ,R0402_T_0',
        '15008648 ,80 ,15008648 ,2 ,.0 ,0 ,0 ,LED_3MM',
        ':ENDPNDATA',
        ':PACKAGES',
        'R0402_T_0 ,SMD ,0.080 ,0.036 ,0.000',
        'LED_3MM ,TH ,0.178 ,0.078 ,0.000',
        ':PACKAGES',
        ':PAD',
        '255 ,AP_r1778 ,CIRCLE ,0.070 ,0.070 ,0.035 ,0.035',
        '288 ,AP_s711 ,RECT ,0.028 ,0.028 ,0.014 ,0.014',
        ':ENDPAD',
    ]
    return fileLinesMock

@pytest.fixture
def rotateFileLines():
    fileLinesMock = [
        ':PARTLIST',
        '0 ,C10 ,15015596 ,1.578 ,-1.249 ,B,90',
        ':ENDPARTLIST',
        ':NETLIST',
        '0 ,TEST_MODE ,C10 ,2 ,1.578 ,-1.287 ,B,1032',
        '381 ,VDD_ARM_CAP ,C10 ,1 ,1.578 ,-1.249 ,B,1032',
        ':ENDNETLIST',
        ':PAD',
        '1032 ,AP_rect20x18 ,RECT ,0.020 ,0.018 ,0.010 ,0.009',
        ':ENDPAD',
        ':PNDATA',
        '15015596 ,0 ,15015596 ,15 ,.0 ,0 ,0 , 0402_M',
        ':ENDPNDATA',
        ':PACKAGES',
        '0402_M ,SMD ,0.060 ,0.024 ,0.000',
        ':ENDPACKAGES',
    ]
    return fileLinesMock


def test__getSectionsLinesBeginEnd(exampleFileLines):
    instance = CamCadLoader()
    instance._getSectionsLinesBeginEnd(exampleFileLines)
    expected = {'BOARDINFO':[0, 2], 'PARTLIST':[4, 9], 'PNDATA':[20, 24], 'NETLIST':[11, 18], 'PAD':[34, 38], 'PACKAGES':[26, 32], 'BOARDOUTLINE':[40, 44]}
    print(instance.sectionsLineNumbers)
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
    instance._getBoardDimensions(exampleFileLines, instance.boardData)
    line1 = gobj.Line(gobj.Point(2.238, -0.366), gobj.Point(2.238, -0.177))
    line2 = gobj.Line(gobj.Point(4.028, -0.386), gobj.Point(4.028, -0.287))
    line3 = gobj.Line(gobj.Point(4.028, -0.287), gobj.Point(3.938, -0.287))
    boardLine1, boardLine2, boardLine3 = instance.boardData.getOutlines()
    assert line1 == boardLine1
    assert line2 == boardLine2    
    assert line3 == boardLine3
    bottomLeftPoint = gobj.Point(2.238, -0.386)
    topRightPoint = gobj.Point(4.028, -0.177)
    assert [bottomLeftPoint, topRightPoint] == instance.boardData.getArea()

def test__getComponenentsFromPARTLIST(exampleFileLines):
    instance = CamCadLoader()
    instance._getSectionsLinesBeginEnd(exampleFileLines)
    partNumberToComponents = instance._getComponenentsFromPARTLIST(exampleFileLines, instance.boardData)
    component1 = instance.boardData.getElementByName('components', 'FID1')
    
    assert partNumberToComponents == {'PNFID': ['FID1', 'FID2', 'FID3', 'FID4']}
    assert component1.name == 'FID1'
    assert component1.coords.getXY() == (None, None)
    assert component1.side == 'T'
    assert component1.angle == 0

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
    instance._getComponenentsFromPARTLIST(netlistFileLines, instance.boardData)   
    padsDict = instance._getPadsFromPAD(netlistFileLines)
    matchedComponents = instance._getNetsFromNETLIST(netlistFileLines, padsDict, instance.boardData)
    
    boardNets = instance.boardData.getNets()    
    boardComponents = instance.boardData.getComponents()

    ## name of nets and components
    assert list(boardNets.keys()) == ['NetC41_1' , 'NetC47_2', 'NetC47_1']
    assert list(boardComponents.keys()) == ['TP100', 'C47', 'TP135', 'TP136']

    ## components in the nets
    assert 'TP100' in boardNets['NetC41_1'] 
    assert 'C47' in boardNets['NetC47_1'] and 'C47' in boardNets['NetC47_2']
    assert 'TP135' in boardNets['NetC47_2']

    ## proper component mapping
    assert boardNets['NetC41_1']['TP100']['componentInstance'] is boardComponents['TP100']
    assert boardNets['NetC41_1']['TP100']['pins'] == ['1']
    assert boardComponents['TP100'].pins['1'].net == 'NetC41_1'
    assert boardComponents['TP100'].pins['1'].coords == gobj.Point(785.190 ,348.564)
    assert boardComponents['TP100'].pins['1'].area == [gobj.Point(785.180 ,348.554), gobj.Point(785.200 ,348.574)]
    assert boardComponents['TP100'].pins['1'].shape == 'RECT'
    assert boardComponents['TP100'].pins['1'].getShapePoints() == [gobj.Point(785.180 ,348.554), gobj.Point(785.200 ,348.554),
                                                                   gobj.Point(785.200 ,348.574), gobj.Point(785.180 ,348.574)]

    assert boardNets['NetC47_1']['C47']['componentInstance'] is boardComponents['C47']
    assert boardNets['NetC47_1']['C47']['componentInstance'] is boardNets['NetC47_2']['C47']['componentInstance']
    assert boardNets['NetC47_1']['C47']['pins'] == ['1']    
    assert boardNets['NetC47_2']['C47']['pins'] == ['2']

    assert boardComponents['C47'].pins['1'].net == 'NetC47_1'
    assert boardComponents['C47'].pins['1'].coords == gobj.Point(771.855 ,342.902)
    assert boardComponents['C47'].pins['1'].area == [gobj.Point(771.847 ,342.894), gobj.Point(771.863 ,342.910)]
    assert boardComponents['C47'].pins['1'].shape == 'CIRCLE'
    assert boardComponents['C47'].pins['1'].getShapePoints() == [gobj.Point(771.855 ,342.902)]

    assert boardComponents['C47'].pins['2'].net == 'NetC47_2'
    assert boardComponents['C47'].pins['2'].coords == gobj.Point(770.839 ,342.902)
    assert boardComponents['C47'].pins['2'].area == [gobj.Point(770.831 ,342.894), gobj.Point(770.847 ,342.910)]    
    assert boardComponents['C47'].pins['2'].shape == 'CIRCLE'
    assert boardComponents['C47'].pins['2'].getShapePoints() == [gobj.Point(770.839 ,342.902)]

    assert boardNets['NetC47_2']['TP135']['componentInstance'] is boardComponents['TP135']
    assert boardNets['NetC47_2']['TP135']['pins'] == ['1']
    assert boardComponents['TP135'].pins['1'].net == 'NetC47_2'
    assert boardComponents['TP135'].pins['1'].coords == gobj.Point(769.467, 341.937)
    assert boardComponents['TP135'].pins['1'].area == [gobj.Point(769.457, 341.927), gobj.Point(769.477, 341.947)]
    assert boardComponents['TP135'].pins['1'].shape == 'RECT'
    assert boardComponents['TP135'].pins['1'].getShapePoints() == [gobj.Point(769.457, 341.927), gobj.Point(769.477, 341.927),
                                                                   gobj.Point(769.477, 341.947), gobj.Point(769.457, 341.947)]

    assert matchedComponents == {'C47', 'TP100', 'TP135'}

def test__getPackages(packagesFileLines):
    gobj.Point.DECIMAL_POINT_PRECISION = 3
    instance = CamCadLoader()
    instance._getSectionsLinesBeginEnd(packagesFileLines)
    partNumberToComponents = instance._getComponenentsFromPARTLIST(packagesFileLines, instance.boardData)  
    padsDict = instance._getPadsFromPAD(packagesFileLines)  
    instance._getNetsFromNETLIST(packagesFileLines, padsDict, instance.boardData)
    _ = instance._getPackages(packagesFileLines, partNumberToComponents, instance.boardData)

    boardComponents = instance.boardData.getComponents()
    assert boardComponents['R40'].area == [gobj.Point(0.98, 0.860), gobj.Point(1.060, 0.896)]
    assert boardComponents['R40'].mountingType == 'SMD'
    assert boardComponents['R40'].shape == 'RECT'
    assert boardComponents['R40'].getShapePoints() == [gobj.Point(0.98, 0.860), gobj.Point(1.060, 0.860), 
                                                       gobj.Point(1.060, 0.896), gobj.Point(0.98, 0.896)]
    
    assert boardComponents['C10'].area == [gobj.Point(2.213, 2.260), gobj.Point(2.221, 2.306)]
    assert boardComponents['C10'].mountingType == 'SMT'
    assert boardComponents['C10'].shape == 'RECT'
    assert boardComponents['C10'].getShapePoints() == [gobj.Point(2.213, 2.260), gobj.Point(2.221, 2.260), 
                                                       gobj.Point(2.221, 2.306), gobj.Point(2.213, 2.306)]

    assert boardComponents['LD1'].area == [gobj.Point(0.843, 1.941), gobj.Point(1.021, 2.019)]
    assert boardComponents['LD1'].mountingType == 'TH'
    assert boardComponents['LD1'].shape == 'RECT'
    assert boardComponents['LD1'].getShapePoints() == [gobj.Point(0.843, 1.941), gobj.Point(1.021, 1.941), 
                                                       gobj.Point(1.021, 2.019), gobj.Point(0.843, 2.019)]

def test__rotateComponents(rotateFileLines):
    gobj.Point.DECIMAL_POINT_PRECISION = 3
    instance = CamCadLoader()
    instance._getSectionsLinesBeginEnd(rotateFileLines)
    partNumberToComponents = instance._getComponenentsFromPARTLIST(rotateFileLines, instance.boardData)
    padsDict = instance._getPadsFromPAD(rotateFileLines)
    instance._getNetsFromNETLIST(rotateFileLines, padsDict, instance.boardData)
    noMatchedComponents = instance._getPackages(rotateFileLines, partNumberToComponents, instance.boardData)
    instance._rotateComponents(instance.boardData, noMatchedComponents)

    componentInstance = instance.boardData.getElementByName('components', 'C10')
    assert componentInstance.getCoords() == gobj.Point(1.578, -1.268)
    assert componentInstance.getArea() == [gobj.Point(1.566, -1.298), gobj.Point(1.590, -1.238)]
    assert componentInstance.getShapePoints() == [gobj.Point(1.590, -1.298), gobj.Point(1.590, -1.238), 
                                                  gobj.Point(1.566, -1.238), gobj.Point(1.566, -1.298)]
    
    pin1 = componentInstance.getPinByName('1')
    assert pin1.getCoords() == gobj.Point(1.578, -1.249)
    assert pin1.getArea() == [gobj.Point(1.568, -1.258), gobj.Point(1.588, -1.240)]
    assert pin1.getShapePoints() == [gobj.Point(1.568, -1.258), gobj.Point(1.588, -1.258), 
                                     gobj.Point(1.588, -1.240), gobj.Point(1.568, -1.240)]
    
    pin2 = componentInstance.getPinByName('2')
    assert pin2.getCoords() == gobj.Point(1.578 ,-1.287)
    assert pin2.getArea() == [gobj.Point(1.568, -1.296), gobj.Point(1.588, -1.278)]
    assert pin2.getShapePoints() == [gobj.Point(1.568, -1.296), gobj.Point(1.588, -1.296), 
                                     gobj.Point(1.588, -1.278), gobj.Point(1.568, -1.278)]