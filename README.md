# Better Board Navigator (BBN)

Better Board Navigator (BBN) is a modern, high-performance Single Page Application (SPA) designed for viewing, inspecting, and navigating Printed Circuit Board (PCB) layouts and schematics directly in the browser. 

By running CAD/PDF parsing entirely client-side using Web Assembly (Pyodide in a Web Worker) and rendering graphics natively via the Canvas 2D API, BBN delivers a desktop-like experience without the need for a backend server.

## Features

- **Blazing Fast Rendering:** Native HTML5 Canvas rendering engine tailored for thousands of pads and components without frame drops.
- **Offline First:** Fully functional in offline LAN environments. No external CDNs or backend required.
- **Web Worker Integration (Pyodide):** Heavy lifting (parsing CAD, ODB++, and PDF BOMs) runs in a separate background thread. The UI never freezes.
- **Advanced Navigation:** Pan, Zoom, Free Rotation, and Mirroring (Flip) natively supported via Matrix Transformations.
- **Intelligent Component Selection:** Single select, multi-select, prefix-based grouping, and part number (BOM) highlighting.
- **Netlist Explorer:** Explore electrical nets and instantly highlight connected pads across the board.
- **THT / SMT Support:** True representation of Through-Hole components visible from both Top and Bottom sides.
- **Traceability API Ready:** Native frontend integration designed to fetch and display production/testing history directly on the schematic.
- **Modern UI:** Built with React, TypeScript, and Tailwind CSS. Supports seamless Dark/Light mode switching.
- **i18n Ready:** Out-of-the-box support for multiple languages (English and Polish included).

## Technology Stack

- **Framework:** React 18
- **Build Tool:** Vite
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State Management:** Zustand
- **Graphics Engine:** HTML5 Canvas API (2D Context)
- **Background Processing:** Web Workers + Pyodide (Python in WASM)
- **Icons:** Lucide React
- **Translations:** i18next

## Getting Started

### Prerequisites
- Node.js (v18 or newer recommended)
- npm or yarn

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/better-board-navigator.git
   cd better-board-navigator
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure environment (Optional):
   Create a `.env` file based on `.env.example` if you need to configure external API endpoints for Traceability or GitHub Pages deployment paths.

### Development

To start the development server with Hot Module Replacement (HMR):

```bash
npm run dev
```
The application will be available at `http://localhost:5173`.

### Building for Production

To build the application for deployment:

```bash
npm run build
```
The compiled files will be output to the `dist` directory. These static files can be hosted on any web server, Nginx, Apache, or GitHub Pages.

## Usage

1. Open the application.
2. Click the **CAD Upload** button (or press `Ctrl+O`) in the top navigation bar to load a supported schematic file (`.tgz`, `.cad`, `.gcd`, `.zip`). Be careful with odb++ files. Component can be rotated 180deg.
3. (Optional) Click the **Database** icon (or press `Ctrl+P`) to load a Bill of Materials (`BOM.json`) to map Part Numbers to components. `BOM.json` is supposed to be a flat json map: {componentName}: {partNumber}:
```json
{
    "C1": "pn1",
    "C2": "pn1",
    "C3": "pn2",
    "...": "..."
}
```
4. Use the mouse to Pan (Left Click & Drag) and Zoom (Scroll).
5. Use the Left Panel to search components, explore nets, or filter by Part Numbers.
6. Use the Inspector on the right to view detailed pinouts and toggle component visibility.

## Keyboard Shortcuts

- `Ctrl` + `O` - Load CAD file
- `Ctrl` + `P` - Load BOM (Part Numbers) file
- `Space` - Switch view side (Top / Bottom)
- `F` - Flip (Mirror horizontally)
- `R` - Rotate Clockwise (90°)
- `Shift` + `R` - Rotate Counter-Clockwise (90°)
- `L` - Toggle component labels (Names)
- `Esc` - Clear selection / Close Inspector panel

## Architecture Notes

- **`src/components/canvas/canvasRenderer.ts`**: The core rendering loop. Avoid placing React hooks here. It consumes raw data and outputs to the Canvas Context.
- **`src/store/boardStore.ts`**: The single source of truth for the UI and Canvas state.
- **Web Worker**: Ensure Pyodide and CAD parser scripts are placed in the `public` directory so they are correctly served and bundled by Vite.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.