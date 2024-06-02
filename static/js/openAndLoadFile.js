async function openAndLoadCadFile(pyodide, file) {
    var fileName = `/${file.name}`
    const reader = new FileReader(); 

    reader.onload = async (event) => {
        const fileContent = event.target.result;
        pyodide.FS.writeFile(fileName, new Uint8Array(fileContent));
        
        // process .cad, .gcd and .tgz files
        await pyodide.runPythonAsync(`
            from loaderSelectorFactory import LoaderSelectorFactory

            loader = LoaderSelectorFactory("/${fileName}")
            fileLines = loader.loadFile("/${fileName}")
            print(fileLines)
            board = loader.processFileLines(fileLines)
            print(board)
        `);
    };
    reader.readAsArrayBuffer(file);
}

async function removePreviousFileFromFS(pyodide, fileName){
    const pydodideFiles = pyodide.FS.readdir('/');
    if (pydodideFiles.includes(fileName)){
        pyodide.FS.unlink(`/${fileName}`);
    }
}