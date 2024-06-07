async function windowResizeEvent(event){
    let RESCALE_AFTER_MS = 15;
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(_resizeBoard, RESCALE_AFTER_MS);
}

function keyDownEvent(event){
    var keyID = event.which;
    switch(keyID){
        case 18: // alt
        break;
    }
}

function mouseDownEvent(event){
    isMousePressed = true;
    isMouseClickedFirstTime = true;
    
    if (isRotateEnable){
        side = currentSide();
        pyodide.runPythonAsync(`
            engine.rotateBoardInterface(SURFACE, isClockwise=True, side='${side}', angleDeg=90)
            pygame.display.flip()
        `);
    } else if (isFindComponentByClickActive){        
        const x = event.offsetX; 
        const y = event.offsetY;        
        let clickedComponents = new Array();

        side = currentSide();
        pyodide.runPython(`
            clickedXY = [int('${x}'), int('${y}')]
            clickedComponents = engine.findComponentByClick(clickedXY, '${side}')
            
            if '${isPresereMarkedComponentsActive}' == 'true':
                for componentName in clickedComponents:
                    engine.findComponentByNameInterface(SURFACE, componentName, '${side}')
                    pygame.display.flip()
        `);
        clickedComponents = pyodide.globals.get('clickedComponents').toJs();
        document.getElementById("clicked-components").innerText = clickedComponents;
    }
}

function mouseUpEvent(){
    isMousePressed = false;
}

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
}

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
}

async function loadFileEvent(event){
    const file = event.target.files[0];
    if (file) {
        await removePreviousFileFromFS(pyodide, loadedFileName);
        await openAndLoadCadFile(pyodide, file);
        loadedFileName = file.name;
        _enableButtons();
    }
}

async function changeSideEvent(){
    changeSide();
    side = currentSide();
    pyodide.runPythonAsync(`
        engine.changeSideInterface(SURFACE, '${side}')
        pygame.display.flip()
    `);
}

function rotateEvent(){
    isRotateEnable = !isRotateEnable
}

async function mirrorSideEvent(){
    side = currentSide();
    pyodide.runPythonAsync(`
        engine.flipUnflipCurrentSideInterface(SURFACE, '${side}')
        pygame.display.flip()
    `);
}

async function toggleOutlinesEvent(){
    side = currentSide();
    pyodide.runPythonAsync(`
        engine.showHideOutlinesInterface(SURFACE, '${side}')
        pygame.display.flip()
    `);
}

async function resetViewEvent(){
    side = currentSide();
    pyodide.runPythonAsync(`
        engine.resetToDefaultViewInterface(SURFACE, '${side}')
        pygame.display.flip()
    `);
}

async function areaFromComponentsEvent(){
    side = currentSide();
    pyodide.runPythonAsync(`
        engine.changeAreaInterface(SURFACE, '${side}')
        pygame.display.flip()
    `);
}

function toggleFindComponentByClickEvent(){
    isFindComponentByClickActive = !isFindComponentByClickActive;
}

async function _resizeBoard(){
    setCanvasDimensions();
    side = currentSide();
    pyodide.runPythonAsync(`
        engine.changeScreenDimensionsInterface(SURFACE, [canvas.width, canvas.height], '${side}')
        pygame.display.flip()
    `);
}

function selectComponentFromListEvent(itemElement){
    const allItems = componentsList.querySelectorAll('div');
    allItems.forEach(el => el.classList.remove('selected'));
    
    itemElement.classList.add('selected');
    let selectedComponent = itemElement.textContent;
    _markSelectedComponentFromList(selectedComponent);
}

function preserveComponentMarkesEvent(){
    isPresereMarkedComponentsActive = !isPresereMarkedComponentsActive;
}

async function clearMarkersEvent(){
    isPresereMarkedComponentsActive = false;
    side = currentSide();
    pyodide.runPythonAsync(`
        engine.clearFindComponentByNameInterface(SURFACE, '${side}')
        pygame.display.flip()
    `);
}


function _enableButtons(){
    changeSideButton.disabled = false;
    rotateButton.disabled = false;
    mirrorSideButton.disabled = false;
    toggleOutlinesButton.disabled = false;
    resetViewButton.disabled = false;
    areaFromComponentsButton.disabled = false;
    toggleFindComponentByClickButton.disabled = false;
    preserveComponentMarkesButton.disabled = false;
    clearMarkersButton.disabled = false;
}

async function _markSelectedComponentFromList(selectedComponentFromList){
    pyodide.runPython(`
        componentName = '${selectedComponentFromList}'
        componentSide = engine.getSideOfComponent(componentName)
    `);
    
    let componentSide = pyodide.globals.get('componentSide');
    side = currentSide();

    if (componentSide != side){
        changeSide();
        side = currentSide();
    }
    pyodide.runPython(`
        if '${isPresereMarkedComponentsActive}' == 'false':
            engine.clearFindComponentByNameInterface(SURFACE, '${side}')

        engine.findComponentByNameInterface(SURFACE, componentName, '${side}')
        pygame.display.flip()
    `);
}