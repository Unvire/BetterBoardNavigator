import pytest
import math
from visecadLoader import VisecadLoader
import geometryObjects as gobj
import component as comp

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

@pytest.fixture
def geometriesSplitTest():
    fileLinesMock = [
        '<CCDoc version="7.1" application="CAMCAD.EXE">',
        '<Geometries>',
        '  <Geometry num="26" name="AP_r2184" originalName="" fileNum="-1" geomType="0" flag="73" dCode="0" shape="1" sizeA="0.085984" sizeB="0" sizeC="0" sizeD="0" rotation="0" xOffset="0" yOffset="0" numSpokes="0"></Geometry>',
        '  <Geometry num="27" name="AP_r2235" originalName="" fileNum="-1" geomType="0" flag="73" dCode="0" shape="1" sizeA="0.087992" sizeB="0.382" sizeC="0" sizeD="0" rotation="0" xOffset="0" yOffset="0" numSpokes="0"></Geometry>',
        '  <Geometry num="58" name="PADSTACK007" originalName="" fileNum="-1" geomType="4" flag="12288">',
        '    <Datas>',
        '      <Insert entityNum="58" layer="6" graphicClass="0" insertType="0" refName="" geomNum="26" x="0" y="0" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '      <Insert entityNum="59" layer="7" graphicClass="0" insertType="0" refName="" geomNum="39" x="0" y="0" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '      <Insert entityNum="60" layer="8" graphicClass="0" insertType="0" refName="" geomNum="39" x="0" y="0" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '      <Insert entityNum="61" layer="9" graphicClass="0" insertType="0" refName="" geomNum="26" x="0" y="0" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '      <Insert entityNum="62" layer="11" graphicClass="0" insertType="0" refName="" geomNum="59" x="0" y="0" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '    </Datas>',
        '  </Geometry>',
        '  <Geometry num="2" name="PCB" originalName="" fileNum="1" geomType="1" flag="4">',
        '     <Datas>',
        '       <PolyStruct entityNum="87" layer="1" graphicClass="17"></PolyStruct>',
        '       <PolyStruct entityNum="88" layer="3" graphicClass="17"></PolyStruct>',
        '       <PolyStruct entityNum="89" layer="3" graphicClass="17"></PolyStruct>',
        '       <PolyStruct entityNum="87" layer="1" graphicClass="17"></PolyStruct>',
        '       <PolyStruct entityNum="88" layer="3" graphicClass="17"></PolyStruct>',
        '       <PolyStruct entityNum="89" layer="3" graphicClass="17"></PolyStruct>',
        '       <Insert entityNum="90" layer="-1" graphicClass="0" insertType="2" refName="1" geomNum="52" x="0.030984" y="-8e-010" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '       <Insert entityNum="91" layer="-1" graphicClass="0" insertType="2" refName="2" geomNum="52" x="-0.030984" y="-8e-010" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '       <Insert entityNum="90" layer="-1" graphicClass="0" insertType="2" refName="1" geomNum="52" x="0.030984" y="-8e-010" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '       <Insert entityNum="91" layer="-1" graphicClass="0" insertType="2" refName="2" geomNum="52" x="-0.030984" y="-8e-010" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '       <Insert entityNum="90" layer="-1" graphicClass="0" insertType="2" refName="1" geomNum="52" x="0.030984" y="-8e-010" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '       <Insert entityNum="91" layer="-1" graphicClass="0" insertType="2" refName="2" geomNum="52" x="-0.030984" y="-8e-010" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '    </Datas>',
        '  </Geometry>',
        '  <Geometry num="62" name="R0603_T" originalName="R0603_T" fileNum="1" geomType="5">',
        '    <Attrib key="35" val="SMD"/>',
        '    <Attrib key="68"/>',
        '    <Datas>',
        '      <PolyStruct entityNum="87" layer="1" graphicClass="17"></PolyStruct>',
        '      <PolyStruct entityNum="88" layer="3" graphicClass="17"></PolyStruct>',
        '      <PolyStruct entityNum="89" layer="3" graphicClass="17"></PolyStruct>',
        '      <Insert entityNum="90" layer="-1" graphicClass="0" insertType="2" refName="1" geomNum="52" x="0.030984" y="-8e-010" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '      <Insert entityNum="91" layer="-1" graphicClass="0" insertType="2" refName="2" geomNum="52" x="-0.030984" y="-8e-010" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '    </Datas>',
        '  </Geometry>',
        '</Geometries>',
        '</CCDoc>'
    ]
    return fileLinesMock

@pytest.fixture
def polyStructTest():
    fileLinesMock = [
        '<Datas>',
        '<PolyStruct entityNum="78905" layer="17" graphicClass="0">',
        '  <Poly widthIndex="0">',
        '    <Pnt x="4.248031" y="10.177165"/>',
        '    <Pnt x="4.248031" y="10.177165" bulge="1"/>',
        '    <Pnt x="4.248031" y="10.098425"/>',
        '  </Poly>',
        '</PolyStruct>',
        '<PolyStruct entityNum="78907" layer="17" graphicClass="0">',
        '  <Poly widthIndex="0">',
        '    <Pnt x="4.031496" y="10.098425"/>',
        '    <Pnt x="4.031496" y="9.322835"/>',
        '    <Pnt x="4.299213" y="9.322835"/>',
        '    <Pnt x="4.299213" y="10.098425"/>',
        '    <Pnt x="4.031496" y="10.098425"/>',
        '  </Poly>',
        '</PolyStruct>',
        '</Datas>'
    ]
    return fileLinesMock

@pytest.fixture
def componentsInsertTest():
    fileLinesMock = [
        '<CCDoc>',
        '  <Datas>',
        '    <Insert entityNum="86" layer="-1" graphicClass="0" colorOverride="1" overrideColor="7895160" insertType="3" refName="CN1" geomNum="61" x="1.039331" y="0.448779" angle="0" mirror="0" placeBottom="1" scale="1"></Insert>',
        '    <Insert entityNum="93" layer="-1" graphicClass="0" insertType="3" refName="R4" geomNum="62" x="0.599606" y="0.311024" angle="4.712389" mirror="0" placeBottom="0" scale="1"></Insert>',
        '    <Insert entityNum="95" layer="-1" graphicClass="0" insertType="3" refName="R1" geomNum="62" x="0.641732" y="0.425197" angle="1.570796" mirror="0" placeBottom="0" scale="1"></Insert>',
        '    <Insert entityNum="27" layer="0" graphicClass="0" insertType="1" refName="" geomNum="46" x="0.467323" y="0.285433" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '    <Insert entityNum="27" layer="0" graphicClass="0" insertType="1" refName="Via0001" geomNum="46" x="0.467323" y="0.285433" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '  </Datas>',
        '</CCDoc>',
    ]
    return fileLinesMock

@ pytest.fixture
def matchShapesToIDsTest():
    fileLinesMock = [
        '<CCDoc version="7.1" application="CAMCAD.EXE">',
        '<Geometries>',
        '<!-- PCB MOCK -->',
        '<Geometry num="0" name="PCB" originalName="" fileNum="1" geomType="1" flag="4">',
        '  <Datas>',
        '    <PolyStruct entityNum="87" layer="1" graphicClass="17"></PolyStruct>',
        '    <PolyStruct entityNum="88" layer="3" graphicClass="17"></PolyStruct>',
        '    <PolyStruct entityNum="89" layer="3" graphicClass="17"></PolyStruct>',
        '    <PolyStruct entityNum="87" layer="1" graphicClass="17"></PolyStruct>',
        '    <PolyStruct entityNum="88" layer="3" graphicClass="17"></PolyStruct>',
        '    <PolyStruct entityNum="89" layer="3" graphicClass="17"></PolyStruct>',
        '    <Insert entityNum="90" layer="-1" graphicClass="0" insertType="2" refName="1" geomNum="52" x="0.030984" y="-8e-010" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '    <Insert entityNum="91" layer="-1" graphicClass="0" insertType="2" refName="2" geomNum="52" x="-0.030984" y="-8e-010" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '    <Insert entityNum="90" layer="-1" graphicClass="0" insertType="2" refName="1" geomNum="52" x="0.030984" y="-8e-010" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '    <Insert entityNum="91" layer="-1" graphicClass="0" insertType="2" refName="2" geomNum="52" x="-0.030984" y="-8e-010" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '    <Insert entityNum="90" layer="-1" graphicClass="0" insertType="2" refName="1" geomNum="52" x="0.030984" y="-8e-010" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '    <Insert entityNum="91" layer="-1" graphicClass="0" insertType="2" refName="2" geomNum="52" x="-0.030984" y="-8e-010" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '  </Datas>',
        '</Geometry>',
        '',
        '<!-- BASE SHAPE -->',
        '<Geometry num="1" name="AP_r2184" originalName="" fileNum="-1" geomType="0" flag="73" dCode="0" shape="1" sizeA="0.085" sizeB="0" sizeC="0" sizeD="0" rotation="0" xOffset="0" yOffset="0" numSpokes="0"></Geometry>',
        '<Geometry num="2" name="AP_r2235" originalName="" fileNum="-1" geomType="0" flag="73" dCode="0" shape="1" sizeA="0.087" sizeB="0.034" sizeC="0" sizeD="0" rotation="0" xOffset="0" yOffset="0" numSpokes="0"></Geometry>',
        '',
        '<!-- POLYSTRUCT AND INSERTS -->',
        '<Geometry num="3" name="RP_0_PKG" originalName="" fileNum="1" geomType="33">',
        '  <Datas>',
        '    <PolyStruct entityNum="10" layer="24" graphicClass="29">',
        '      <Poly widthIndex="0" closed="1">',
        '      <Pnt x="0.462598" y="0.149606"/>',
        '      <Pnt x="-0.462598" y="0.149606"/>',
        '      <Pnt x="-0.462598" y="-0.185039"/>',
        '      <Pnt x="0.462598" y="-0.185039"/>',
        '      <Pnt x="0.462598" y="0.149606"/>',
        '    </Poly>',
        '  </PolyStruct>',
        '  <Insert entityNum="2" layer="-1" graphicClass="0" insertType="38" refName="1" geomNum="4" x="0" y="0" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '  <Insert entityNum="4" layer="-1" graphicClass="0" insertType="38" refName="2" geomNum="5" x="0" y="0" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '  </Datas>',
        '</Geometry>',
        '<Geometry num="4" name="RP_0_PKG_PIN_1" originalName="" fileNum="1" geomType="34"></Geometry>',
        '<Geometry num="5" name="RP_0_PKG_PIN_2" originalName="" fileNum="1" geomType="34"></Geometry>',
        '',
        '<!-- NO POLYSTRUCT - USE FIRST INSERT - SECOND ITERATION LOOKUP -->',
        '<Geometry num="6" name="PADSTACK000" originalName="" fileNum="-1" geomType="4" flag="12288">',
        '  <Datas>',
        '    <Insert entityNum="6371" layer="8" graphicClass="0" insertType="0" refName="" geomNum="7" x="0" y="0" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '    <Insert entityNum="6372" layer="9" graphicClass="0" insertType="0" refName="" geomNum="800" x="0" y="0" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '    <Insert entityNum="6373" layer="10" graphicClass="0" insertType="0" refName="" geomNum="900" x="0" y="0" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '    <Insert entityNum="6374" layer="11" graphicClass="0" insertType="0" refName="" geomNum="1000" x="0" y="0" angle="0" mirror="0" placeBottom="0" scale="1"></Insert>',
        '  </Datas>',
        '</Geometry>',
        '',
        '<!-- ONLY POLYSTRUCT -->',
        '<Geometry num="7" name="R0603_T" originalName="R0603_T" fileNum="1" geomType="5">',
        '  <Datas>',
        '    <PolyStruct entityNum="87" layer="1" graphicClass="17">',
        '      <Poly widthIndex="0" closed="1">',
        '        <Pnt x="-0.030984" y="-0.015984"/>',
        '        <Pnt x="0.030984" y="-0.015984"/>',
        '        <Pnt x="0.030984" y="0.015984"/>',
        '        <Pnt x="-0.030984" y="0.015984"/>',
        '        <Pnt x="-0.030984" y="-0.015984"/>',
        '      </Poly>',
        '    </PolyStruct>',
        '  </Datas>',
        '</Geometry>',
        '',
        '<!-- SKIP - NO POLYSTRUCT AND NO INSERTS -->',
        '<Geometry num="2165" name="DRILL 461" originalName="" fileNum="-1" geomType="20" flag="80" tCode="0" toolSize="0.055118" display="0" geomNum="1" type="0" plated="1" punched="0"></Geometry>',
        '</Geometries>',
        '</CCDoc>'
    ]
    return fileLinesMock


def test__getOutlinesLayers(layerLines):
    instance = VisecadLoader()
    rootXML = instance._parseXMLFromFileLines(layerLines)

    expected = ['0', '8', '19']
    assert expected == instance._getOutlinesLayers(rootXML)

def test__processNetsTag(netsLines):
    instance = VisecadLoader()
    rootXML = instance._parseXMLFromFileLines(netsLines)

    shapesIDDict = instance._processNetsTag(rootXML, instance.boardData)

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

def test__processGeometriesTag(geometriesSplitTest):
    instance = VisecadLoader()
    rootXML = instance._parseXMLFromFileLines(geometriesSplitTest)
    shapesXMLDict, padstackXMLDict, pcbXML = instance._processGeometriesTag(rootXML)

    assert list(shapesXMLDict.keys()) == ['26', '27']
    assert shapesXMLDict['26'].attrib['name'] == 'AP_r2184'
    assert shapesXMLDict['27'].attrib['name'] == 'AP_r2235'

    assert list(padstackXMLDict.keys()) == ['58', '62']
    assert padstackXMLDict['58'].attrib['name'] == 'PADSTACK007'
    assert padstackXMLDict['62'].attrib['name'] == 'R0603_T'
    
    assert pcbXML.attrib['name'] == 'PCB'
    assert pcbXML.attrib['num'] == '2'

def test__processPolyStruct(polyStructTest):
    instance = VisecadLoader()
    rootXML = instance._parseXMLFromFileLines(polyStructTest)
    polyStructsXML = rootXML.findall('PolyStruct')
    expected = [
        [gobj.Line(gobj.Point(4.248031, 10.177165), gobj.Point(4.248031, 10.098425))],
        [gobj.Line(gobj.Point(4.031496, 10.098425), gobj.Point(4.031496, 9.322835)), 
         gobj.Line(gobj.Point(4.031496, 9.322835), gobj.Point(4.299213, 9.322835)),
         gobj.Line(gobj.Point(4.299213, 9.322835), gobj.Point(4.299213, 10.098425)), 
         gobj.Line(gobj.Point(4.299213, 10.098425), gobj.Point(4.031496, 10.098425))]
    ]

    for i, polyStructXML in enumerate(polyStructsXML):
        assert expected[i] == instance._processPolyStruct(polyStructXML)

def test__getBoardOutlines(polyStructTest):
    instance = VisecadLoader()

    boardOutlinesTestLines = ['<CCDoc>'] + polyStructTest + ['</CCDoc>']
    pcbXML = instance._parseXMLFromFileLines(boardOutlinesTestLines)
    OUTLINES_LAYERS_IDS = ['0', '17']
    instance._getBoardOutlines(pcbXML, instance.boardData, OUTLINES_LAYERS_IDS)
    assert instance.boardData.getOutlines() == [gobj.Line(gobj.Point(4.248031, 10.177165), gobj.Point(4.248031, 10.098425)),
                                                gobj.Line(gobj.Point(4.031496, 10.098425), gobj.Point(4.031496, 9.322835)), 
                                                gobj.Line(gobj.Point(4.031496, 9.322835), gobj.Point(4.299213, 9.322835)),
                                                gobj.Line(gobj.Point(4.299213, 9.322835), gobj.Point(4.299213, 10.098425)), 
                                                gobj.Line(gobj.Point(4.299213, 10.098425), gobj.Point(4.031496, 10.098425))]

def test__updateComponents(componentsInsertTest):
    instance = VisecadLoader()
    for componentName in ['CN1', 'R4', 'R1']:
        componentInstance = comp.Component(componentName)
        instance.boardData.addComponent(componentName, componentInstance)

    pcbXML = instance._parseXMLFromFileLines(componentsInsertTest)
    shapesIDToComponentDict = instance._updateComponents(pcbXML, instance.boardData)

    ## test components
    componentInstance = instance.boardData.getElementByName('components', 'CN1')
    assert componentInstance.coords == gobj.Point(1.039331, 0.448779)
    assert componentInstance.angle == 0
    assert componentInstance.side == 'B'

    componentInstance = instance.boardData.getElementByName('components', 'R4')
    assert componentInstance.coords == gobj.Point(0.599606, 0.311024)
    assert componentInstance.angle == math.degrees(4.712389)
    assert componentInstance.side == 'T'

    componentInstance = instance.boardData.getElementByName('components', 'R1')
    assert componentInstance.coords == gobj.Point(0.641732, 0.425197)
    assert componentInstance.angle == math.degrees(1.570796)
    assert componentInstance.side == 'T'

    ## test shapesIDDict
    assert list(shapesIDToComponentDict.keys()) == ['61', '62']
    assert shapesIDToComponentDict['61'] == [instance.boardData.getElementByName('components', 'CN1')]
    assert shapesIDToComponentDict['62'] == [instance.boardData.getElementByName('components', 'R4'), instance.boardData.getElementByName('components', 'R1')]

def test__getRectangleFromPolyStruct(polyStructTest):
    instance = VisecadLoader()
    rootXML = instance._parseXMLFromFileLines(polyStructTest)
    polyStructsXML = rootXML.findall('PolyStruct')

    assert instance._getRectangleFromPolyStruct(polyStructsXML[0]) == gobj.Rectangle(gobj.Point(-4.248031, -10.137795), gobj.Point(4.248031, 10.137795))
    assert instance._getRectangleFromPolyStruct(polyStructsXML[1]) == gobj.Rectangle(gobj.Point(-4.165354, -9.71063), gobj.Point(4.165354, 9.71063))

def test__calculateBaseShapes(geometriesSplitTest):
    instance = VisecadLoader()
    rootXML = instance._parseXMLFromFileLines(geometriesSplitTest)
    shapesXMLDict, _, _ = instance._processGeometriesTag(rootXML)    
    shapesDict = instance._calculateBaseShapes(shapesXMLDict)        

    assert list(shapesDict.keys()) == ['26', '27']
    assert shapesDict['26'] == gobj.Circle(gobj.Point(0, 0), 0.085984 / 2)
    assert shapesDict['27'] == gobj.Rectangle(gobj.Point(-0.043996, -0.191), gobj.Point(0.043996, 0.191))

def test__getPadstackShapeID(matchShapesToIDsTest):
    instance = VisecadLoader()
    rootXML = instance._parseXMLFromFileLines(matchShapesToIDsTest)
    shapesXMLDict, padstackXMLDict, _ = instance._processGeometriesTag(rootXML)
    shapesDict = instance._calculateBaseShapes(shapesXMLDict)
    padstackShapeIDDict = instance._getPadstackShapeID(padstackXMLDict, shapesDict)

    assert sorted(list(shapesDict.keys())) == ['1', '2', '3', '4', '5', '6', '7']
    assert shapesDict['1'] == gobj.Circle(gobj.Point(0, 0), 0.085 / 2)
    assert shapesDict['2'] == gobj.Rectangle(gobj.Point(-0.0435, -0.017), gobj.Point(0.0435, 0.017))

    rectBL = gobj.Point(-0.462598, -0.1673225)
    rectTR = gobj.Point(0.462598, 0.1673225)
    rectMain = gobj.Rectangle(rectBL, rectTR)
    rectPins = gobj.Rectangle(gobj.Point.scale(rectBL, 1 / 2), gobj.Point.scale(rectTR, 1 / 2))
    assert shapesDict['3'] == rectMain
    assert shapesDict['4'] == rectPins
    assert shapesDict['5'] == rectPins
    assert shapesDict['6'] == padstackShapeIDDict['7']
    assert shapesDict['7'] == gobj.Rectangle(gobj.Point(-0.030984, -0.015984), gobj.Point(0.030984, 0.015984))