async function windowResizeEvent(){
    let RESCALE_AFTER_MS = 15;
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(EngineAdapterEvents.resizeBoard, RESCALE_AFTER_MS);
}

function keyDownEvent(event){
    if (isTextModalInputFocused){
        if (event.key === "Backspace"){
            textModalInput.value = textModalInput.value.slice(0, -1);
        } else if (event.key.length === 1){
            textModalInput.value += event.key;
        } else if (event.key === "Enter"){
            textModalSubmitButton.click();
        }
        event.preventDefault();
    }
}

function mouseDownEvent(event){
    isMousePressed = true;
    isMouseClickedFirstTime = true;
    
    if (isRotateActive){
        EngineAdapterEvents.rotateBoard();
    } else if (isFindComponentByClickActive){        
        const x = event.offsetX; 
        const y = event.offsetY;
        
        let clickedComponents = EngineAdapterEvents.findClickedComponents(x, y, isSelectionModeSingle);
        generateClickedComponentsSpanList(clickedComponents);
        _generateMarkedComponentsList();
    }
}

function generateClickedComponentsSpanList(clickedComponentsList){
    clickedComponentSpanList.addSpans(clickedComponentsList);
    clickedComponentSpanList.generate();
}

function clickedComponentsClickEvent(componentName){
    generatePinoutTableEvent(componentName);
}

function mouseUpEvent(){
    isMousePressed = false;
}

async function mouseMoveEvent(event){
    if (isMousePressed){
        if (!isMouseClickedFirstTime){
            const x = event.movementX; 
            const y = event.movementY;

            EngineAdapterEvents.moveBoard(x, y);
        } else {
            isMouseClickedFirstTime = false;
        }
    }
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

function rotateEvent(){
    isRotateActive = !isRotateActive;
}

function toggleFindComponentByClickEvent(){
    isFindComponentByClickActive = !isFindComponentByClickActive;
}

function selectComponentFromListEvent(itemElement){
    let clickedComponentName = itemElement.textContent;
    _markSelectedComponentFromList(clickedComponentName);
    generatePinoutTableEvent(clickedComponentName);
}

function preserveComponentMarkesEvent(){
    isSelectionModeSingle = !isSelectionModeSingle;
    mode = selectionModesMap[isSelectionModeSingle];
    allComponentsList.selectionMode = mode;
}

async function _markSelectedComponentFromList(selectedComponentFromList){
    _findComponentByNameHelper(selectedComponentFromList);
    _generateMarkedComponentsList();
}

function _generateMarkedComponentsList(){
    pyodide.runPython(`
        componentsList = engine.getSelectedComponents()
    `);
    let componentsList = pyodide.globals.get("componentsList").toJs();
    
    markedComponentsList.elements = componentsList
    markedComponentsList.selectionMode = "no";
    markedComponentsList.eventCallbackFuntion = markedComponentsListItemClickedEvent;
    markedComponentsList.generateList()
}

function markedComponentsListItemClickedEvent(itemElement){
    let componentName = itemElement.textContent;
    generatePinoutTableEvent(componentName);
    EngineAdapterEvents.componentInScreenCenter(componentName);
}

function generatePinoutTableEvent(componentName){
    pyodide.runPython(`
        pinoutDict = engine.getComponentPinout('${componentName}')
    `);
    let pinoutMap = pyodide.globals.get("pinoutDict").toJs();
    pinoutTable.rowEvent = selectNetFromTableEvent;
    pinoutTable.beforeRowEvent = EngineAdapterEvents.unselectNet;
    pinoutTable.addRows(pinoutMap);
    pinoutTable.generateTable();

    const netTreeSelectedNetName = netsTreeview.getSelectedNetName();
    pinoutTable.selectRowByName(netTreeSelectedNetName);
    selectedComponentSpan.innerText = componentName;
}

function selectNetFromTableEvent(netName){
    netsTreeview.scrollToBranchByName(netName);
    if(pinoutTable.getSelectedRow()){
        EngineAdapterEvents.selectNet(netName);
    }
}

function selectNetFromTreeviewEvent(netName){
    pinoutTable.selectRowByName(netName);    

    if(netsTreeview.getSelectedNet()){
        EngineAdapterEvents.selectNet(netName);
    }
}

function toggleNetMarkersEvent(){
    pyodide.runPython(`
        selectedNetComponent = engine.getSelectedNetComponent()
    `);
    const selectedNetComponent = pyodide.globals.get("selectedNetComponent");
    netsTreeview.selectComponentByName(selectedNetComponent);
    EngineAdapterEvents.toggleNetMarkers();
}

function selectNetComponentByNameEvent(componentName){
    componentSide = _getSideOfComponent(componentName);
    side = _changeSideIfComponentIsNotOnScreen(componentSide);
    EngineAdapterEvents.selectNetComponentByName(componentName, componentSide);
}

function unselectNetEvent(){
    EngineAdapterEvents.unselectNet();
    netsTreeview.unselectCurrentBranch();
    netsTreeview.unselectCurrentItem();
    pinoutTable.unselectCurrentRow();
}

function findComponentUsingNameEvent(){
    modalSubmit.setHeader("Component name:");
    modalSubmit.buttonEvent = getComponentNameFromModalBoxEvent;
    modalSubmit.show();
}

function getComponentNameFromModalBoxEvent(componentName){
    const modalBoxComponentName = componentName.toUpperCase();
    _findComponentByNameHelper(modalBoxComponentName);
}

function showCommonPrefixComponentsEvent(){
    modalSubmit.setHeader("Prefix:");
    modalSubmit.buttonEvent = getCommonPrefixFromModalBoxEvent;
    modalSubmit.show();
}

function getComponentNameFromModalBoxEvent(componentName){
    const modalBoxComponentName = componentName.toUpperCase();
    _findComponentByNameHelper(modalBoxComponentName);
}

function getCommonPrefixFromModalBoxEvent(commonPrefix){
    const modalBoxCommonPrefix = commonPrefix.toUpperCase();

    EngineAdapterEvents.showCommonPrefixComponents(modalBoxCommonPrefix);
    
    const isPrefixExist = pyodide.globals.get("isPrefixExist");
    if (isPrefixExist){
        commonPrefixSpan.innerText = modalBoxCommonPrefix;
    }
}

function hideCommonPrefixComponentsEvent(){
    EngineAdapterEvents.hideCommonPrefixComponents();
    commonPrefixSpan.innerText = "";
}

function _findComponentByNameHelper(componentName){
    componentSide = _getSideOfComponent(componentName);
    if (!componentSide){
        return
    }

    side = _changeSideIfComponentIsNotOnScreen(componentSide);
    EngineAdapterEvents.findComponentByName(componentName, side, isSelectionModeSingle);

    generatePinoutTableEvent(componentName);
    _generateMarkedComponentsList();
}

function _getSideOfComponent(componentName){
    pyodide.runPython(`
        componentSide = engine.getSideOfComponent('${componentName}')
    `);
    return pyodide.globals.get("componentSide");
}

function _changeSideIfComponentIsNotOnScreen(componentSide){
    if (componentSide != currentSide()){
        changeSide();
    }
    return currentSide();
}

function _resetWidgets(){
    _resetTreeview();
    _resetSelectedComponentsWidgets();
}

function _resetTreeview(){
    netsTreeview.unselectCurrentBranch();
    netsTreeview.unselectCurrentItem();
}

function _resetSelectedComponentsWidgets(){
    allComponentsList.unselectAllItems();
    pinoutTable.unselectCurrentRow();
    pinoutTable.clearBody();
    _generateMarkedComponentsList();
    selectedComponentSpan.innerText = "Component";
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
    findComponentUsingNameButton.disabled = false;
    prefixComponentsButton.disabled = false;
    unselectPrefixComponentsButton.disabled = false;
}