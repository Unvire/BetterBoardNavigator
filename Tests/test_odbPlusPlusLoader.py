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
    