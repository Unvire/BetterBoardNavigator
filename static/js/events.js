class EventHandler{
    static keyDown(event, isTextModalInputFocused){
        if (isTextModalInputFocused){
            const textModalInput = globalInstancesMap.getTextModalInput();
            const textModalSubmitButton = globalInstancesMap.getTextModalSubmitButton();
            
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

    static setCanvasDimensions(){
        const canvas = globalInstancesMap.getCanvas();
        const canvasParent = globalInstancesMap.getCanvasParent();

        canvas.width = canvasParent.clientWidth;
        canvas.height = canvasParent.clientHeight;
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
        const allComponentsList = globalInstancesMap.getAllComponentsList();
        const selectionModesMap = {true: "single", false: "multiple"};
    
        isSelectionModeSingle = !isSelectionModeSingle;
        allComponentsList.selectionMode = selectionModesMap[isSelectionModeSingle];
        EventHandler.toggleButton(preserveComponentMarkesButton);
        return isSelectionModeSingle;
    }

    static toggleNetMarkers(){
        const netsTreeview = globalInstancesMap.getNetsTreeview();

        pyodide.runPython(`
            selectedNetComponent = engine.getSelectedNetComponent()
        `);
        const selectedNetComponent = pyodide.globals.get("selectedNetComponent");
        netsTreeview.selectComponentByName(selectedNetComponent);
        EventHandler.toggleButton(toggleNetMarkersButton);
        EngineAdapter.toggleNetMarkers();
    }

    static unselectNet(){
        EngineAdapter.unselectNet();
        WidgetAdapter.resetSelectedNet();
    }

    static findComponentUsingName(){
        const modalSubmit = globalInstancesMap.getModalSubmit();
        InputModalBoxAdapter.generateModalBox(modalSubmit, "Component name:", InputModalBoxAdapter.getComponentNameFromInput);
    }
    
    static showCommonPrefixComponents(){
        const modalSubmit = globalInstancesMap.getModalSubmit();
        InputModalBoxAdapter.generateModalBox(modalSubmit, "Prefix:", InputModalBoxAdapter.getCommonPrefixFromInput);
    }
    
    static hideCommonPrefixComponents(){
        const commonPrefixSpan = globalInstancesMap.getCommonPrefixSpan();
        
        EngineAdapter.hideCommonPrefixComponents();
        commonPrefixSpan.innerText = "";
    }

    static toggleOutlines(){
        EngineAdapter.toggleOutlines();
        EventHandler.toggleButton(toggleOutlinesButton);
    }

    static toggleButton(button){
        if (button.classList.contains("button-selected")){
            button.classList.remove("button-selected");
        } else {
            button.classList.add("button-selected");
        }
    }
}