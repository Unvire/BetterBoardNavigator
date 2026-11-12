import pytest
import json
import geometryObjects as gobj
import component as comp
from board import Board

class MockPin:
    def __init__(self, name, net):
        self.name = name
        self.net = net
        self.shape = 'RECT'
        self.shapeData = gobj.Rectangle(gobj.Point(0,0), gobj.Point(1,1))
        self.coords = gobj.Point(0.5, 0.5)

@pytest.fixture
def mockBoard():
    b = Board()
    
    b.setArea(gobj.Point(0, 0), gobj.Point(100, 100))
    b.setOutlines([
        gobj.Line(gobj.Point(0,0), gobj.Point(10,10)),
        gobj.Circle(gobj.Point(5,5), 2.5)
    ])
    
    c1 = comp.Component('R1')
    c1.side = 'T'
    c1.mountingType = 'SMT'
    c1.shape = 'RECT'
    c1.coords = gobj.Point(50, 50)
    c1.pins = {
        '1': MockPin('1', 'GND'),
        '2': MockPin('2', 'VCC')
    }
    b.addComponent('R1', c1)
    
    b.setNets({
        'GND': {'R1': {'pins': ['1']}},
        'VCC': {'R1': {'pins': ['2']}}
    })
    b.mostCommonPrefix = 'R'
    
    return b



def test_toDict_hasAllRequiredKeys(mockBoard):
    data = mockBoard.toDict()
    
    expected_keys = ['boardDimensions', 'area', 'outlines', 'components', 'nets', 'mostCommonPrefix']
    for key in expected_keys:
        assert key in data, f'Key: "{key}" is missing!'

def test_toDict_geometrySerialization(mockBoard):
    data = mockBoard.toDict()
    
    assert data['boardDimensions'] == (100, 100)
    assert len(data['outlines']) == 2
    
    assert data['outlines'][0]['type'] == 'Line'
    assert data['outlines'][0]['start']['x'] == 0
    
    assert data['outlines'][1]['type'] == 'Circle'
    assert data['outlines'][1]['radius'] == 2.5

def test_toDict_componentAndPins(mockBoard):
    data = mockBoard.toDict()
    r1 = data['components']['R1']
    
    assert r1['mountingType'] == 'SMT'
    assert r1['side'] == 'T'
    assert r1['coords']['x'] == 50
    
    assert '1' in r1['pins']
    assert r1['pins']['1']['net'] == 'GND'
    assert r1['pins']['1']['shapeType'] == 'RECT'

def test_toDict_netsSimplification(mockBoard):
    data = mockBoard.toDict()
    
    assert 'GND' in data['nets']
    assert 'R1' in data['nets']['GND']
    assert data['nets']['GND']['R1']['pins'] == ['1']

def test_toJson_serialization(mockBoard):
    jsonStr = mockBoard.toJson()
    assert isinstance(jsonStr, str)
    
    try:
        parsed = json.loads(jsonStr)
        assert parsed['mostCommonPrefix'] == 'R'
    except json.JSONDecodeError:
        pytest.fail('Result string is not a JSON!')