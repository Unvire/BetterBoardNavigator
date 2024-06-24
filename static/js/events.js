class EventHandler{
    static keyDown(event, isTextModalInputFocused, textModalInput, textModalSubmitButton){
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

    static async windowResizeEvent(){
        const RESCALE_AFTER_MS = 15;
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(EngineAdapter.resizeBoard, RESCALE_AFTER_MS);
    }

    static async loadFileEvent(event, loadedFileName){
        const file = event.target.files[0];
        if (file) {
            await removePreviousFileFromFS(pyodide, loadedFileName);
            await openAndLoadCadFile(pyodide, file);
            EventHandler.enableButtons();
            return file.name;
        }
    }

    static enableButtons(){
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

    static preserveComponentMarkesEvent(isSelectionModeSingle){
        const selectionModesMap = {true: "single", false: "multiple"};
    
        isSelectionModeSingle = !isSelectionModeSingle;
        const mode = selectionModesMap[isSelectionModeSingle];
        allComponentsList.selectionMode = mode;
        return isSelectionModeSingle;
    }


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

function mouseUpEvent(){
    isMousePressed = false;
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

function rotateEvent(){
    isRotateActive = !isRotateActive;
}

function toggleFindComponentByClickEvent(){
    isFindComponentByClickActive = !isFindComponentByClickActive;
}

function toggleNetMarkersEvent(){
    pyodide.runPython(`
        selectedNetComponent = engine.getSelectedNetComponent()
    `);
    const selectedNetComponent = pyodide.globals.get("selectedNetComponent");
    netsTreeview.selectComponentByName(selectedNetComponent);
    EngineAdapter.toggleNetMarkers();
}

function unselectNetEvent(){
    EngineAdapter.unselectNet();
    WidgetAdapter.resetSelectedNet();
}

function findComponentUsingNameEvent(){
    InputModalBoxAdapter.generateModalBox(modalSubmit, "Component name:", InputModalBoxAdapter.getComponentNameFromInput);
}

function showCommonPrefixComponentsEvent(){
    InputModalBoxAdapter.generateModalBox(modalSubmit, "Prefix:", InputModalBoxAdapter.getCommonPrefixFromInput);
}

function hideCommonPrefixComponentsEvent(){
    EngineAdapter.hideCommonPrefixComponents();
    commonPrefixSpan.innerText = "";
}