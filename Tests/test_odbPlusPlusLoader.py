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
        'odb/symbols/rect27.685x31.622xr6.9528_315/features'
        ]
    return fileLinesMock

def test__getTarPathsToEdaComponents(exampleTarPaths):
    instance = ODBPlusPlusLoader()
    expected = [
        'odb/steps/pcb/eda/data', 
        'odb/steps/pcb/layers/comp_+_bot/components.z', 
        'odb/steps/pcb/layers/comp_+_top/components.Z'
        ]
    assert instance._getTarPathsToEdaComponents(exampleTarPaths) == expected