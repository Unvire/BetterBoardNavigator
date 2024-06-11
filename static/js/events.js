async function windowResizeEvent(){
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
    
    if (isRotateActive){
        side = currentSide();
        pyodide.runPythonAsync(`
            engine.rotateBoardInterface(SURFACE, isClockwise=True, side='${side}', angleDeg=90)
            pygame.display.flip()
        `);
    } else if (isFindComponentByClickActive){        
        const x = event.offsetX; 
        const y = event.offsetY;
        side = currentSide();

        pyodide.runPython(`
            clickedXY = [int('${x}'), int('${y}')]
            clickedComponents = engine.findComponentByClick(clickedXY, '${side}')
            
            if '${isSelectionModeSingle}' == 'false':
                for componentName in clickedComponents:
                    engine.findComponentByNameInterface(SURFACE, componentName, '${side}') #mark all clicked components
                    pygame.display.flip()
        `);
        let clickedComponents = pyodide.globals.get('clickedComponents').toJs();
        document.getElementById("clicked-components").innerText = clickedComponents;
        _generateMarkedComponentsList();
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
    side = currentSide();

    pyodide.runPython(`
    if engine:
        pointXY = [int('${x}'), int('${y}')]
        isScaleUp = '${event.deltaY < 0}' == 'true'
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
    isRotateActive = !isRotateActive;
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
    let clickedListElement = itemElement.textContent;
    _markSelectedComponentFromList(clickedListElement);
}

function preserveComponentMarkesEvent(){
    isSelectionModeSingle = !isSelectionModeSingle;
    mode = selectionModesMap[isSelectionModeSingle];
    allComponentsList.selectionMode = mode;
}

async function clearMarkersEvent(){
    isSelectionModeSingle = true;
    side = currentSide();
    pyodide.runPython(`
        engine.clearFindComponentByNameInterface(SURFACE, '${side}')
        pygame.display.flip()
    `);
    allComponentsList.unselectAllItems();
    _generateMarkedComponentsList();
}

async function _markSelectedComponentFromList(selectedComponentFromList){
    pyodide.runPython(`
        componentSide = engine.getSideOfComponent('${selectedComponentFromList}')
    `);
    let componentSide = pyodide.globals.get('componentSide');

    if (componentSide != currentSide()){
        changeSide();
    }
    side = currentSide();

    pyodide.runPython(`
        if '${isSelectionModeSingle}' == 'true':
            engine.clearFindComponentByNameInterface(SURFACE, '${side}')

        engine.findComponentByNameInterface(SURFACE, '${selectedComponentFromList}', '${side}')
        pygame.display.flip()
    `);
    _generateMarkedComponentsList();
}

function _generateMarkedComponentsList(){
    pyodide.runPython(`
        componentsList = engine.getSelectedComponents()
    `);
    let componentsList = pyodide.globals.get('componentsList').toJs();
    
    markedComponentsList.elements = componentsList
    markedComponentsList.selectionMode = 'single';
    markedComponentsList.eventCallbackFuntion = componentInScreenCenterEvent;
    markedComponentsList.generateList()
}

function componentInScreenCenterEvent(itemElement){
    let componentName = itemElement.textContent;
    pyodide.runPython(`
        componentSide = engine.getSideOfComponent('${componentName}')
    `);
    let componentSide = pyodide.globals.get('componentSide');

    if (componentSide != currentSide()){
        changeSide();
    }
    side = currentSide();

    pyodide.runPython(`
        engine.componentInScreenCenterInterface(SURFACE, '${componentName}', '${side}')
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