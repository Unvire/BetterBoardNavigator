async function windowResizeEvent(event){
    let RESCALE_AFTER_MS = 3;
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(_resizeBoard, RESCALE_AFTER_MS);
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

async function mouseScrollEvent(event){
    const x = event.offsetX; 
    const y = event.offsetY;
    pyodide.runPythonAsync(`
        pointXY = [int('${x}'), int('${y}')]
    `);

    if (event.deltaY < 0) {
        pyodide.runPythonAsync(`
            isScaleUp = True
            isDoScroll = True
        `);
    } else if (event.deltaY > 0) {
        pyodide.runPythonAsync(`
            isScaleUp = False
            isDoScroll = True
        `);
    }
    
    side = currentSide()
    pyodide.runPythonAsync(`
    if engine and isDoScroll:
        pointXY = [int('${x}'), int('${y}')]        
        isDoScroll = False
        engine.scaleUpDownInterface(SURFACE, isScaleUp=isScaleUp, pointXY=pointXY, side='${side}')
        pygame.display.flip()
`);
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
        engine.changeSideInterface(SURFACE, '${side}')
        pygame.display.flip()
    `);
};

async function _resizeBoard(){
    setCanvasDimensions();
    side = currentSide();
    pyodide.runPythonAsync(`
        engine.changeScreenDimensionsInterface(SURFACE, [canvas.width, canvas.height], '${side}')
        pygame.display.flip()
    `);
};