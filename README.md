## Better Board Navigator
Web application for displaying PCBs (Printed Schematic Boards) given as a schematic file. Currently working formats are:
 - cad - CAMCAD
 - gcd - GenCAD
 - tgz - ODB++
 - ccz - visECAD
 
Used technologies:
- **python** - processing cad files
- **pygame** - drawing boards on canvas
- **pyodide** - using python in website
- **HTML, CSS, JS** - typical website technologies

## User interface
### Buttons and controls
- **Dragging with a left mouse button** - moving the board acros the canvas.
- **Load schematic file** - loads a file and processes it. Files are not stored on side, except the demo file.
- **Rotate** - when button is active, clicking on canvas will rotate the board 90 deg clockwise.
- **Change side** - changes currently viewed side.
- **Mirror side** - mirrors current side along X axis.
- **Board outlines** - shows/hides board outlines.
- **Default view** - resets viewed board to initial state.
- **Area from components** - recalculates board dimensions using all components. Useful when default view is not working.
- **Find component by name** - searches and displays component with given name if it exists.
- **Component name on click** - when active, displays clicked components name.
- **Multiple component selection** - changes between single selection and multiple selection of components.
- **Clear components markers** - clears markers and marked components.
- **Unselect net** - unselects selected net.
- **Prefix components** - highlights common prefix components with given prefix.
- **Unselect prefix components** - clears highlighted common prefix components.
- **Demo board** - displays example file of NPN audio amplifier.

### Panels description
- **Current side and highlighted prefix** - displays currently viewed side and displayed common prefix for components.
- **All components** - displays list with all board components. User can select one or multiple components which will be displayed in "Marked components" list.
Clicking on components will also show it pinout in the "Component pinout" table.
- **Component pinout** - displays component pins and nets. Clicking on row will highlight net.
 Clicked components - displays components clicked with a mouse. Clicking on component name will generate its pinout in the "Pinout table".
- **Marked components** - displays marked components. Clicking on item will set the component in the center of the canvas and generate its pinout in the "Pinout table".
- **Nets list** - displays nets of the PCB and components assigned to them. Clicking on the net name will reveal components and mark the net. Clicking on the component will mark the component, set it in the center of the canvas and generate its pinout table.

### Colors description
- **Bold white** - outlines of the PCB.
- **Green** - outlines of the components. Shapes of the components are simplified.
- **Yellow** - SMT pads.
- **Blue** - TH pads.
- **Red arrows** - selected components marker.
- **Violet** - pads on selected net.
- **Violet arrow** - component, whose pads are on selected net.