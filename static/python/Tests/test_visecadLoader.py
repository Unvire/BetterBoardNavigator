import pytest
from visecadLoader import VisecadLoader
import geometryObjects as gobj

@pytest.fixture
def layerLines():
    fileLinesMock = [
        '<CCDoc version="7.1" application="CAMCAD.EXE">',
        '  <Keywords>',
        '  </Keywords>',
        '  <Layers>',
        '    <Layer num="0" name="Board Outline" visible="1" editable="1" color="65535" layerType="28" originalVisible="1" originalEditable="1"/>',
        '    <Layer num="1" name="Assembly Top" visible="1" editable="1" color="65280" layerType="35" mirror="2" originalVisible="1" originalEditable="1"/>',
        '    <Layer num="2" name="Assembly Bottom" visible="1" editable="1" color="16776960" layerType="36" mirror="1" originalVisible="1" originalEditable="1"/>',
        '    <Layer num="3" name="Pin Assembly Top" visible="1" editable="1" color="16711680" layerType="25" mirror="4" originalVisible="1" originalEditable="1"/>',
        '    <Layer num="4" name="Pin Assembly Bottom" visible="1" editable="1" color="16711935" layerType="26" mirror="3" originalVisible="1" originalEditable="1"/>',
        '    <Layer num="5" name="Spt" visible="1" editable="1" color="16711935" layerType="11" artworkStackup="1" originalVisible="1" originalEditable="1"/>',
        '    <Layer num="6" name="Smt" visible="1" editable="1" color="255" layerType="13" mirror="9" artworkStackup="2" originalVisible="1" originalEditable="1"/>',
        '    <Layer num="7" name="Top" visible="1" editable="1" color="65535" layerType="1" mirror="8" electricStackup="1" artworkStackup="3" originalVisible="1" originalEditable="1"/>',
        '    <Layer num="8" name="Outlines" visible="1" editable="1" color="65280" layerType="2" mirror="7" electricStackup="2" artworkStackup="4" originalVisible="1" originalEditable="1"/>',
        '    <Layer num="9" name="Smb" visible="1" editable="1" color="16776960" layerType="14" mirror="6" artworkStackup="5" originalVisible="1" originalEditable="1"/>',
        '    <Layer num="10" name="Rout" visible="1" editable="1" color="16711680" layerType="27" artworkStackup="6" originalVisible="1" originalEditable="1"/>',
        '    <Layer num="11" name="Drill" visible="1" editable="1" color="16711935" layerType="24" artworkStackup="7" originalVisible="1" originalEditable="1"/>',
        '    <Layer num="12" name="Sqa_areas" visible="1" editable="1" color="255" layerType="53" artworkStackup="8" originalVisible="1" originalEditable="1"/>',
        '    <Layer num="13" name="Draw_foratura" visible="1" editable="1" color="65535" layerType="53" artworkStackup="9" originalVisible="1" originalEditable="1"/>',
        '    <Layer num="14" name="Package Body Top" visible="1" editable="1" color="255" layerType="49" mirror="15" originalVisible="1" originalEditable="1"/>',
        '    <Layer num="15" name="Package Body Bottom" visible="1" editable="1" color="65535" layerType="50" mirror="14" originalVisible="1" originalEditable="1"/>',
        '    <Layer num="16" name="Package Pin Top" visible="1" editable="1" color="65280" layerType="43" mirror="17" originalVisible="1" originalEditable="1"/>',
        '    <Layer num="17" name="Package Pin Bottom" visible="1" editable="1" color="16776960" layerType="44" mirror="16" originalVisible="1" originalEditable="1"/>',
        '    <Layer num="18" name="REFDES_TOP" visible="1" editable="1" color="16711680" layerType="25" mirror="19" originalVisible="1" originalEditable="1"/>',
        '    <Layer num="19" name="Maybe Outlines" visible="1" editable="1" color="16711935" layerType="26" mirror="18" originalVisible="1" originalEditable="1"/>',
        '  </Layers>',
        '</CCDoc>'
    ]
    return fileLinesMock

@pytest.fixture
def netsLines():
    fileLinesMock = [
        '<CCDoc version="7.1" application="CAMCAD.EXE">',
        '<Files>',
        '<File num="1" name="PCB" refName="" geomNum="2" origGeomNum="2" geomType="1" x="0" y="0" scale="1" rotation="0" mirror="0" show="1" sourceCAD="48" curDFTSolution="" curMachineSolution="">',
        '<Nets>',
        '<Net name="N07757" entity="154" flag="0">',
        '  <CompPin comp="R5" pin="1" entity="155" pinCoords="1" x="0.374016" y="0.356339" rotation="4.712389" mirror="0" padstackGeomNum="53" visible="1">',
        '    <Attrib key="5" val="0"/>',
        '    <Attrib key="35" val="THRU"/>',
        '    <Attrib key="68"/>',
        '    <Attrib key="224" val="case"/>',
        '    <Attrib key="226" val="0"/>',
        '  </CompPin>',
        '  <CompPin comp="R2" pin="1" entity="156" pinCoords="1" x="0.374016" y="0.234213" rotation="1.570796" mirror="0" padstackGeomNum="53" visible="1">',
        '    <Attrib key="5" val="0"/>',
        '    <Attrib key="35" val="SMD"/>',
        '    <Attrib key="68"/>',
        '    <Attrib key="224" val="SMD_R1206"/>',
        '    <Attrib key="226" val="0"/>',
        '  </CompPin>',
        '  <CompPin comp="L1" pin="K" entity="157" pinCoords="1" x="0.5" y="0.237283" rotation="1.570796" mirror="0" padstackGeomNum="54" visible="1">',
        '    <Attrib key="5" val="1"/>',
        '    <Attrib key="35" val="SMD"/>',
        '    <Attrib key="68"/>',
        '    <Attrib key="224" val="SMD_PLCC2"/>',
        '    <Attrib key="226" val="0"/>',
        '  </CompPin>',
        '</Net>',
        '<Net name="N08344" entity="158" flag="0">',
        '  <CompPin comp="SW1" pin="2" entity="159" pinCoords="1" x="0.834646" y="0.448819" rotation="0" mirror="0" padstackGeomNum="49" visible="1">',
        '    <Attrib key="5" val="1"/>',
        '    <Attrib key="35" val="SMD"/>',
        '    <Attrib key="68"/>',
        '    <Attrib key="224" val="PAD_SW_AC_SINGOLO_SK25"/>',
        '    <Attrib key="226" val="0"/>',
        '  </CompPin>',
        '  <CompPin comp="R1" pin="1" entity="160" pinCoords="1" x="0.641732" y="0.456181" rotation="1.570796" mirror="0" padstackGeomNum="52" visible="1">',
        '    <Attrib key="5" val="0"/>',
        '    <Attrib key="35" val="SMD"/>',
        '    <Attrib key="68"/>',
        '    <Attrib key="224" val="SMD_R0603"/>',
        '    <Attrib key="226" val="0"/>',
        '  </CompPin>',
        '    <CompPin comp="R1" pin="2" entity="160" pinCoords="1" x="0.641732" y="0.456181" rotation="1.570796" mirror="0" padstackGeomNum="52" visible="1">',
        '    <Attrib key="5" val="0"/>',
        '    <Attrib key="35" val="SMD"/>',
        '    <Attrib key="68"/>',
        '    <Attrib key="224" val="SMD_R0603"/>',
        '    <Attrib key="226" val="0"/>',
        '  </CompPin>',
        '</Net>',
        '</Nets>',
        '</File>',
        '</Files>',
        '</CCDoc>'
    ]
    return fileLinesMock

def test__getOutlinesLayers(layerLines):
    instance = VisecadLoader()
    root = instance._parseXMLFromFileLines(layerLines)

    expected = ['0', '8', '19']
    assert expected == instance._getOutlinesLayers(root)

def test__processNetsTag(netsLines):
    instance = VisecadLoader()
    root = instance._parseXMLFromFileLines(netsLines)

    shapesIDDict = instance._processNetsTag(root, instance.boardData)

    nets = instance.boardData.getNets()
    components = instance.boardData.getComponents()

    ## nets test
    assert list(nets.keys()) == ['N07757', 'N08344']
    assert list(nets['N07757'].keys()) == ['R5', 'R2', 'L1']
    assert list(nets['N08344'].keys()) == ['SW1', 'R1']
    
    assert nets['N07757']['R5']['componentInstance'] is components['R5']
    assert nets['N07757']['R2']['componentInstance'] is components['R2']
    assert nets['N07757']['L1']['componentInstance'] is components['L1']
    assert nets['N08344']['SW1']['componentInstance'] is components['SW1']
    assert nets['N08344']['R1']['componentInstance'] is components['R1']

    assert nets['N07757']['R5']['pins'] == ['1']
    assert nets['N07757']['R2']['pins'] == ['1']
    assert nets['N07757']['L1']['pins'] == ['K']
    assert nets['N08344']['SW1']['pins'] == ['2']
    assert nets['N08344']['R1']['pins'] == ['1', '2']

    ## components test
    assert list(components.keys()) == ['R5', 'R2', 'L1', 'SW1', 'R1']
    assert components['R5'].getMountingType() == 'TH'
    assert components['R2'].getMountingType() == 'SMT'
    assert components['L1'].getMountingType() == 'SMT'
    assert components['SW1'].getMountingType() == 'SMT'
    assert components['R1'].getMountingType() == 'SMT'

    ## pins test
    componentNamesListTest = 'R5', 'R2', 'L1', 'SW1', 'R1', 'R1'
    pinNamesListTest = '1', '1', 'K', '2', '1', '2'
    coordsPointListTest = (gobj.Point(0.374016, 0.356339), gobj.Point(0.374016, 0.234213), gobj.Point(0.5, 0.237283),
                           gobj.Point(0.834646, 0.448819), gobj.Point(0.641732, 0.456181), gobj.Point(0.641732, 0.456181))    
    for componentName, pinName, coordsPoint in zip(componentNamesListTest, pinNamesListTest, coordsPointListTest): 
        pinInstance = components[componentName].getPinByName(pinName)
        assert pinInstance.getCoords() == coordsPoint
    
    ## shapesIDDict test
    assert list(shapesIDDict.keys()) == ['53', '54', '49', '52']
    assert shapesIDDict['53'] == [[components['R5'].getPinByName('1'), '4.712389'], [components['R2'].getPinByName('1'), '1.570796']]
    assert shapesIDDict['54'] == [[components['L1'].getPinByName('K'), '1.570796']]
    assert shapesIDDict['49'] == [[components['SW1'].getPinByName('2'), '0']]
    assert shapesIDDict['52'] == [[components['R1'].getPinByName('1'), '1.570796'], [components['R1'].getPinByName('2'), '1.570796']]