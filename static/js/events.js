class EventHandler{
    static compensateUserDevicePixelRatio(){
        const dpr = window.devicePixelRatio;
        const dynamicVH = dpr * 100;

        document.body.style.zoom = `${Math.floor(1 / dpr * 100)}%`;
        document.documentElement.style.setProperty('--GRID-CONTAINER-HEIGHT', dynamicVH + 'vh');
    }

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

    static loadFile(event, loadedFileName){
        const file = event.target.files[0];
        if (file) {
            removePreviousFileFromFS(pyodide, loadedFileName);
            openAndLoadCadFile(pyodide, file);
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

    static unselectNet(){
        EngineAdapter.unselectNet();
        WidgetAdapter.resetSelectedNet();
    }

    static findComponentUsingName(){
        const modalSubmit = globalInstancesMap.getModalSubmit();
        InputModalBoxAdapter.generateModalBox(modalSubmit, "Component name", InputModalBoxAdapter.getComponentNameFromInput);
    }
    
    static showCommonPrefixComponents(){
        const modalSubmit = globalInstancesMap.getModalSubmit();
        InputModalBoxAdapter.generateModalBox(modalSubmit, "Prefix", InputModalBoxAdapter.getCommonPrefixFromInput);
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

    static loadDemoFile(loadedFileName){
        fetch("./static/cad_files/demo.cad")
            .then(response => response.blob())
            .then(blob => {
                const file = new File([blob], "demo.cad", {type: "application/octet-stream"});
                const simulatedEvent = {
                    target: {
                        files: [file]
                    }
                };
                EventHandler.loadFile(simulatedEvent, loadedFileName);
                return "demo.cad"
            });
    }
}