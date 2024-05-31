async function configurePythonPath(pyodide){
    await pyodide.runPythonAsync(`
                import sys
                sys.path.append("/")
    `);
}

async function loadPygame(pyodide){
    await pyodide.loadPackage("micropip");
    const micropip = pyodide.pyimport("micropip");
    await micropip.install("pygame-ce");
}

async function loadLocalModules(pyodide) {
    async function copyModuleToVirtualMemory(pyodide, moduleName){
        var response = await fetch(`/static/python/${moduleName}.py`);
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