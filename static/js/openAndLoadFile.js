async function openAndLoadCadFile(pyodide, file) {
    const reader = new FileReader(); 

    reader.onload = async (event) => {
        const fileContent = event.target.result;
        const fileName = `/${file.name}`
        
        pyodide.FS.writeFile(fileName, new Uint8Array(fileContent));
    };
    reader.readAsArrayBuffer(file);
}