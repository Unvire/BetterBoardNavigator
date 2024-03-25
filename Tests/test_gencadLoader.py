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

def test__getSectionsLinesBeginEnd(sectionsRangeTest):
    instance = GenCadLoader()
    instance._getSectionsLinesBeginEnd(sectionsRangeTest)
    expected = {'BOARD':[0, 1], 'PADS':[2, 4], 'SHAPES':[5, 6], 'COMPONENTS':[7, 8], 'SIGNALS':[9, 10], 'ROUTES':[11, 12], 'MECH':[13, 14]}
    assert instance.sectionsLineNumbers == expected

def test___calculateRange(sectionsRangeTest):
    instance = GenCadLoader()
    instance._getSectionsLinesBeginEnd(sectionsRangeTest)
    assert instance._calculateRange('SIGNALS') == range(9, 10)