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
        clickedComponentContainer.innerText = clickedComponents;
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

    pyodide.runPythonAsync(`
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
    pyodide.runPython(`
        engine.resetToDefaultViewInterface(SURFACE, '${side}')
        pygame.display.flip()
    `);
    
    allComponentsList.unselectAllItems();
    _generateMarkedComponentsList();
}

async function areaFromComponentsEvent(){
    side = currentSide();
    pyodide.runPython(`
        engine.changeAreaInterface(SURFACE, '${side}')
        pygame.display.flip()
    `);

    allComponentsList.unselectAllItems();
    _generateMarkedComponentsList();
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
    generatePinoutTableEvent(clickedListElement);
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
    componentSide = _getSideOfComponent(selectedComponentFromList);
    side = _changeSideIfComponentIsNotOnScreen(componentSide);

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
    markedComponentsList.eventCallbackFuntion = markedComponentsListItemClickedEvent;
    markedComponentsList.generateList()
}

function markedComponentsListItemClickedEvent(itemElement){
    let componentName = itemElement.textContent;
    generatePinoutTableEvent(componentName);
    componentInScreenCenterEvent(componentName);
}

function generatePinoutTableEvent(componentName){
    pyodide.runPython(`
        pinoutDict = engine.getComponentPinout('${componentName}')
    `);
    let pinoutMap = pyodide.globals.get('pinoutDict').toJs();
    pinoutTable.rowEvent = selectNetFromTableEvent;
    pinoutTable.beforeRowEvent = unselectNetEvent;
    pinoutTable.addRows(pinoutMap);
    pinoutTable.generateTable();
}

function selectNetFromTableEvent(netName){
    netsTreeview.scrollToBranchByName(netName);
    if(pinoutTable.getSelectedRow()){
        selectNetEvent(netName);
    }
}

function selectNetFromTreeviewEvent(netName){
    pinoutTable.selectRowByName(netName);    

    if(netsTreeview.getSelectedNet()){
        selectNetEvent(netName);
    } else {
        pinoutTable.unselectCurrentRow();
    }
}

function componentInScreenCenterEvent(componentName){
    componentSide = _getSideOfComponent(componentName);
    side = _changeSideIfComponentIsNotOnScreen(componentSide);

    pyodide.runPython(`
        engine.componentInScreenCenterInterface(SURFACE, '${componentName}', '${side}')
        pygame.display.flip()
    `);
}

function selectNetEvent(netName){
    side = currentSide();
    pyodide.runPython(`
        engine.selectNetByNameInterface(SURFACE, '${netName}', '${side}')
        pygame.display.flip()
    `);
}

function toggleNetMarkersEvent(){
    side = currentSide();
    pyodide.runPython(`
        engine.showHideMarkersForSelectedNetByNameInterface(SURFACE, '${side}')
        pygame.display.flip()
    `);
}

function selectNetComponentByNameEvent(componentName){
    componentSide = _getSideOfComponent(componentName);
    side = _changeSideIfComponentIsNotOnScreen(componentSide);

    pyodide.runPython(`
        engine.selectNetComponentByNameInterface(SURFACE, '${componentName}', '${side}')
        pygame.display.flip()
    `);
}

function unselectNetEvent(){
    side = currentSide();
    pyodide.runPython(`
        engine.unselectNetInterface(SURFACE, '${side}')
        pygame.display.flip()
    `);
}

function _getSideOfComponent(componentName){
    pyodide.runPython(`
        componentSide = engine.getSideOfComponent('${componentName}')
    `);
    return pyodide.globals.get('componentSide');
}

function _changeSideIfComponentIsNotOnScreen(componentSide){
    if (componentSide != currentSide()){
        changeSide();
    }
    return currentSide();
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
    toggleNetMarkersButton.disabled = false;
    unselectNetButton.disabled = false;
}