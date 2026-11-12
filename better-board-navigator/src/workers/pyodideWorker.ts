import geometryObjectsPy from '../python/geometryObjects.py?raw';
import abstractShapePy from '../python/abstractShape.py?raw';
import pinPy from '../python/pin.py?raw';
import componentPy from '../python/component.py?raw';
import boardPy from '../python/board.py?raw';
import unlzw3Py from '../python/unlzw3.py?raw';
import camcadLoaderPy from '../python/camcadLoader.py?raw';
import gencadLoaderPy from '../python/gencadLoader.py?raw';
import odbPlusPlusLoaderPy from '../python/odbPlusPlusLoader.py?raw';
import visecadLoaderPy from '../python/visecadLoader.py?raw';
import loaderSelectorFactoryPy from '../python/loaderSelectorFactory.py?raw';


interface PyodideFS {
  writeFile: (path: string, data: Uint8Array) => void;
  unlink: (path: string) => void;
}

interface PyodideInstance {
  loadPackage: (packages: string[]) => Promise<void>;
  runPythonAsync: (script: string) => Promise<string>;
  FS: PyodideFS;
}


let pyodide: PyodideInstance | null = null;
let lastUploadedFiles: string[] = []; 


async function initPyodide(baseUrl: string = '/'): Promise<PyodideInstance> {
  if (pyodide) return pyodide;
  
  const pyodideUrl = `${location.origin}${baseUrl}pyodide/pyodide.mjs`;
  const pyodideModule = await import(/* @vite-ignore */ pyodideUrl);
  
  pyodide = await pyodideModule.loadPyodide({
    indexURL: `${baseUrl}pyodide/`, 
  }) as PyodideInstance;
  
  const encoder = new TextEncoder();
  const coreModules = [
    { name: '/geometryObjects.py', code: geometryObjectsPy },
    { name: '/abstractShape.py', code: abstractShapePy },
    { name: '/pin.py', code: pinPy },
    { name: '/component.py', code: componentPy },
    { name: '/board.py', code: boardPy },
    { name: '/unlzw3.py', code: unlzw3Py },
    { name: '/camcadLoader.py', code: camcadLoaderPy },
    { name: '/gencadLoader.py', code: gencadLoaderPy },
    { name: '/odbPlusPlusLoader.py', code: odbPlusPlusLoaderPy },
    { name: '/visecadLoader.py', code: visecadLoaderPy },
    { name: '/loaderSelectorFactory.py', code: loaderSelectorFactoryPy }
  ];

  coreModules.forEach(mod => {
    pyodide!.FS.writeFile(mod.name, encoder.encode(mod.code));
  });

  return pyodide;
}


self.addEventListener('message', async (event: MessageEvent) => {
  const { type, files, baseUrl = '/' } = event.data;

  if (type === 'PROCESS_FILES') {
    try {      
      self.postMessage({ type: 'STATUS', status: 'loading_pyodide' });
      const py = await initPyodide(baseUrl);
      self.postMessage({ type: 'STATUS', status: 'processing' });

      if (lastUploadedFiles.length > 0) {
        for (const fileName of lastUploadedFiles) {
          try {
            py.FS.unlink(`/${fileName}`);
          } catch (err) {
            console.warn(`Pyodide warning - old file was not deleted: ${fileName}`);
          }
        }
        lastUploadedFiles = [];
      }

      
      for (const file of files) {
        const buffer = await file.arrayBuffer();
        py.FS.writeFile(`/${file.name}`, new Uint8Array(buffer));
        lastUploadedFiles.push(file.name);
      }

      const fileNames = files.map((f: File) => f.name);
      
      const pythonScript = `
import sys
import json
if "/" not in sys.path:
    sys.path.append("/")

from loaderSelectorFactory import LoaderSelectorFactory

def process(file_names):
    cadFile = next((f for f in file_names if f.lower().endswith(('.cad', '.gcd', '.tgz', '.zip'))), None)
    if not cadFile:
        raise ValueError("There is no file with expected extension (.cad, .gcd, .tgz, .zip)!")

    loader = LoaderSelectorFactory(cadFile)
    fileLines = loader.loadFile("/" + cadFile)
    boardInstance = loader.processFileLines(fileLines)

    return boardInstance.toJson()

process(${JSON.stringify(fileNames)})
      `;

      const resultJsonStr = await py.runPythonAsync(pythonScript);
      const result = JSON.parse(resultJsonStr);

      
      self.postMessage({ type: 'RESULT', payload: { boardData: result } });

    } catch (err: any) {
      self.postMessage({ type: 'ERROR', message: err.message });
    }
  }
});