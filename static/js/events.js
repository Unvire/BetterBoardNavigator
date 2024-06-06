async function loadFileEvent(event){
    const file = event.target.files[0];
    if (file) {
        await removePreviousFileFromFS(pyodide, loadedFileName);
        await openAndLoadCadFile(pyodide, file);
        loadedFileName = file.name;
        changeSideButton.disabled = false;
    }
}

async function changeSideEvent(){
    isSideBottom = !isSideBottom;
    side = currentSide();
    pyodide.runPythonAsync(`
        if engine:
            engine.changeSideInterface(SURFACE, '${side}')
            pygame.display.flip()
    `);
};