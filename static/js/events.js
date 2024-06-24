async function windowResizeEvent(){
    let RESCALE_AFTER_MS = 15;
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(EngineAdapter.resizeBoard, RESCALE_AFTER_MS);
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
        EngineAdapter.rotateBoard();
    } else if (isFindComponentByClickActive){        
        const x = event.offsetX; 
        const y = event.offsetY;
        
        let clickedComponents = EngineAdapter.findClickedComponents(x, y, isSelectionModeSingle);
        SpanListAdapter.generateSpanList(clickedComponentSpanList, clickedComponents);
        DynamicSelectableListAdapter.generateMarkedComponentsList(markedComponentsList);
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

            EngineAdapter.moveBoard(x, y);
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

function preserveComponentMarkesEvent(){
    isSelectionModeSingle = !isSelectionModeSingle;
    mode = selectionModesMap[isSelectionModeSingle];
    allComponentsList.selectionMode = mode;
}

function selectNetFromTreeviewEvent(netName){
    pinoutTable.selectRowByName(netName);    

    if(netsTreeview.getSelectedNet()){
        EngineAdapter.selectNet(netName);
    }
}

function toggleNetMarkersEvent(){
    pyodide.runPython(`
        selectedNetComponent = engine.getSelectedNetComponent()
    `);
    const selectedNetComponent = pyodide.globals.get("selectedNetComponent");
    netsTreeview.selectComponentByName(selectedNetComponent);
    EngineAdapter.toggleNetMarkers();
}

function selectNetComponentByNameEvent(componentName){
    componentSide = _getSideOfComponent(componentName);
    side = _changeSideIfComponentIsNotOnScreen(componentSide);
    EngineAdapter.selectNetComponentByName(componentName, componentSide);
}

function unselectNetEvent(){
    EngineAdapter.unselectNet();
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
    EngineAdapter.findComponentByName(modalBoxComponentName, isSelectionModeSingle);
}

function showCommonPrefixComponentsEvent(){
    modalSubmit.setHeader("Prefix:");
    modalSubmit.buttonEvent = getCommonPrefixFromModalBoxEvent;
    modalSubmit.show();
}

function getComponentNameFromModalBoxEvent(componentName){
    const modalBoxComponentName = componentName.toUpperCase();
    EngineAdapter.findComponentByName(modalBoxComponentName, isSelectionModeSingle);
}

function getCommonPrefixFromModalBoxEvent(commonPrefix){
    const modalBoxCommonPrefix = commonPrefix.toUpperCase();

    EngineAdapter.showCommonPrefixComponents(modalBoxCommonPrefix);
    
    const isPrefixExist = pyodide.globals.get("isPrefixExist");
    if (isPrefixExist){
        commonPrefixSpan.innerText = modalBoxCommonPrefix;
    }
}

function hideCommonPrefixComponentsEvent(){
    EngineAdapter.hideCommonPrefixComponents();
    commonPrefixSpan.innerText = "";
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
    DynamicSelectableListAdapter.generateMarkedComponentsList(markedComponentsList);
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