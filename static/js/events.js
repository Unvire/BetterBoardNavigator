async function windowResizeEvent(event){
    let RESCALE_AFTER_MS = 3;
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(resizeCanvas, RESCALE_AFTER_MS);
};

function mouseDownEvent(event){
    const x = event.offsetX; 
    const y = event.offsetY;
    isMousePressed = true;
    isMouseClickedFirstTime = true;
};

function mouseUpEvent(){
    isMousePressed = false;
};

async function mouseMoveEvent(event){
    if (isMousePressed){
        if (!isMouseClickedFirstTime){
            const x = event.movementX; 
            const y = event.movementY;

            pyodide.runPythonAsync(`
                if engine:
                    deltaVector = [int('${x}'), int('${y}')]
                    engine.moveBoardInterface(SURFACE, deltaVector)
                    pygame.display.flip()
            `);
        } else {
            isMouseClickedFirstTime = false;
        }
    }
};

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