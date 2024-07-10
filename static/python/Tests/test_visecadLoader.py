import pytest
from visecadLoader import VisecadLoader
import geometryObjects as gobj

@pytest.fixture
def layerLines():
    fileLinesMock = [
        '<CCDoc version="7.1" application="CAMCAD.EXE">',
        ' <Keywords>',
        ' </Keywords>',
        ' <Layers>',
        '  <Layer num="0" name="Board Outline" visible="1" editable="1" color="65535" layerType="28" originalVisible="1" originalEditable="1"/>',
        '  <Layer num="1" name="Assembly Top" visible="1" editable="1" color="65280" layerType="35" mirror="2" originalVisible="1" originalEditable="1"/>',
        '  <Layer num="2" name="Assembly Bottom" visible="1" editable="1" color="16776960" layerType="36" mirror="1" originalVisible="1" originalEditable="1"/>',
        '  <Layer num="3" name="Pin Assembly Top" visible="1" editable="1" color="16711680" layerType="25" mirror="4" originalVisible="1" originalEditable="1"/>',
        '  <Layer num="4" name="Pin Assembly Bottom" visible="1" editable="1" color="16711935" layerType="26" mirror="3" originalVisible="1" originalEditable="1"/>',
        '  <Layer num="5" name="Spt" visible="1" editable="1" color="16711935" layerType="11" artworkStackup="1" originalVisible="1" originalEditable="1"/>',
        '  <Layer num="6" name="Smt" visible="1" editable="1" color="255" layerType="13" mirror="9" artworkStackup="2" originalVisible="1" originalEditable="1"/>',
        '  <Layer num="7" name="Top" visible="1" editable="1" color="65535" layerType="1" mirror="8" electricStackup="1" artworkStackup="3" originalVisible="1" originalEditable="1"/>',
        '  <Layer num="8" name="Outlines" visible="1" editable="1" color="65280" layerType="2" mirror="7" electricStackup="2" artworkStackup="4" originalVisible="1" originalEditable="1"/>',
        '  <Layer num="9" name="Smb" visible="1" editable="1" color="16776960" layerType="14" mirror="6" artworkStackup="5" originalVisible="1" originalEditable="1"/>',
        '  <Layer num="10" name="Rout" visible="1" editable="1" color="16711680" layerType="27" artworkStackup="6" originalVisible="1" originalEditable="1"/>',
        '  <Layer num="11" name="Drill" visible="1" editable="1" color="16711935" layerType="24" artworkStackup="7" originalVisible="1" originalEditable="1"/>',
        '  <Layer num="12" name="Sqa_areas" visible="1" editable="1" color="255" layerType="53" artworkStackup="8" originalVisible="1" originalEditable="1"/>',
        '  <Layer num="13" name="Draw_foratura" visible="1" editable="1" color="65535" layerType="53" artworkStackup="9" originalVisible="1" originalEditable="1"/>',
        '  <Layer num="14" name="Package Body Top" visible="1" editable="1" color="255" layerType="49" mirror="15" originalVisible="1" originalEditable="1"/>',
        '  <Layer num="15" name="Package Body Bottom" visible="1" editable="1" color="65535" layerType="50" mirror="14" originalVisible="1" originalEditable="1"/>',
        '  <Layer num="16" name="Package Pin Top" visible="1" editable="1" color="65280" layerType="43" mirror="17" originalVisible="1" originalEditable="1"/>',
        '  <Layer num="17" name="Package Pin Bottom" visible="1" editable="1" color="16776960" layerType="44" mirror="16" originalVisible="1" originalEditable="1"/>',
        '  <Layer num="18" name="REFDES_TOP" visible="1" editable="1" color="16711680" layerType="25" mirror="19" originalVisible="1" originalEditable="1"/>',
        '  <Layer num="19" name="Maybe Outlines" visible="1" editable="1" color="16711935" layerType="26" mirror="18" originalVisible="1" originalEditable="1"/>',
        ' </Layers>',
        '</CCDoc>'
    ]
    return fileLinesMock

def test__getOutlinesLayers(layerLines):
    instance = VisecadLoader()
    root = instance._parseXMLFromFileLines(layerLines)

    expected = ['0', '8', '19']
    assert expected == instance._getOutlinesLayers(root)
