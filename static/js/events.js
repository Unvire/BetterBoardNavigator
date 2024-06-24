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

    static async windowResize(){
        const RESCALE_AFTER_MS = 15;
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(EngineAdapter.resizeBoard, RESCALE_AFTER_MS);
    }

    static async loadFile(event, loadedFileName){
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

    static preserveComponentMarkes(isSelectionModeSingle){
        const selectionModesMap = {true: "single", false: "multiple"};
    
        isSelectionModeSingle = !isSelectionModeSingle;
        const mode = selectionModesMap[isSelectionModeSingle];
        allComponentsList.selectionMode = mode;
        return isSelectionModeSingle;
    }

    static toggleNetMarkers(){
        pyodide.runPython(`
            selectedNetComponent = engine.getSelectedNetComponent()
        `);
        const selectedNetComponent = pyodide.globals.get("selectedNetComponent");
        netsTreeview.selectComponentByName(selectedNetComponent);
        EngineAdapter.toggleNetMarkers();
    }

    static unselectNet(){
        EngineAdapter.unselectNet();
        WidgetAdapter.resetSelectedNet();
    }

    static findComponentUsingName(){
        InputModalBoxAdapter.generateModalBox(modalSubmit, "Component name:", InputModalBoxAdapter.getComponentNameFromInput);
    }
    
    static showCommonPrefixComponents(){
        InputModalBoxAdapter.generateModalBox(modalSubmit, "Prefix:", InputModalBoxAdapter.getCommonPrefixFromInput);
    }
    
    static hideCommonPrefixComponents(){
        EngineAdapter.hideCommonPrefixComponents();
        commonPrefixSpan.innerText = "";
    }
}