async function configurePythonPath(pyodide){
    await pyodide.runPythonAsync(`
        import sys
        sys.path.append('/')

        engine = None

        from js import document
        canvas = document.getElementById('canvas')
    `);
}

async function loadPygame(pyodide){
    await pyodide.loadPackage("micropip");
    const micropip = pyodide.pyimport("micropip");
    await micropip.install("pygame-ce");
    
    await pyodide.runPythonAsync(`
        import pygame
    `);
}

async function loadLocalModules(pyodide) {
    async function copyModuleToVirtualMemory(pyodide, moduleName){
        const baseURL = window.location.href;
        
        var response = await fetch(baseURL + `static/python/${moduleName}.py`);
        var moduleCode = await response.text();
        pyodide.FS.writeFile(`/${moduleName}.py`, moduleCode);
    }

    const modulesList = ['geometryObjects', 'abstractShape', 'pin', 'component', 'board', 'unlzw3', 
                          'camcadLoader', 'gencadLoader', 'odbPlusPlusLoader', 'loaderSelectorFactory',
                          'boardWrapper', 'pygameDrawBoard']
    
    modulesList.forEach(async (moduleName) => {
        await copyModuleToVirtualMemory(pyodide, moduleName)
    });
}