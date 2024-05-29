async function loadLocalModules(pyodide) {
    async function copyModuleToVirtualMemory(pyodide, moduleName){
        var response = await fetch(`/static/python/${moduleName}.py`);
        var moduleCode = await response.text();
        pyodide.FS.writeFile(`/${moduleName}.py`, moduleCode);
    }


    const modulesList = ['geometryObjects', 'abstractShape', 'pin', 'component', 'board', 'unlzw3', 
                          'camcadLoader', 'gencadLoader', 'odbPlusPlusLoader', 'loaderSelectorFactory',
                          'boardWrapper', 'pygameDrawBoard']

    for (let i = 0; i < modulesList.length; i++) {
        var moduleName = modulesList[i]
        await copyModuleToVirtualMemory(pyodide, moduleName)
    }
}

async function loadPygame(pyodide){
    await pyodide.loadPackage("micropip");
    const micropip = pyodide.pyimport("micropip");
    await micropip.install("pygame-ce");
}