class GlobalInstancesMap{
    constructor(){
        this.modalSubmit = null;
        this.textModalSubmitButton = null;
        this.textModalInput = null;
        this.modalParagraph = null;
        this.allComponentsList = null;
        this.markedComponentsList = null;
        this.pinoutTable = null;
        this.netsTreeview = null;
        this.clickedComponentSpanList = null;
        this.canvas = null;
        this.canvasParent = null;
        this.commonPrefixSpan = null;
        this.selectedComponentSpan = null;
    }

    setModalSubmit(instance){
        this.modalSubmit = instance;
    }

    getModalSubmit(){
        return this.modalSubmit;
    }

    setTextModalSubmitButton(instance){
        this.textModalSubmitButton = instance;
    }

    getTextModalSubmitButton(){
        return this.textModalSubmitButton;
    }

    setTextModalInput(instance){
        this.textModalInput = instance;
    }

    getTextModalInput(){
        return this.textModalInput;
    }

    setCanvas(instance){
        this.canvas = instance;
    }

    getCanvas(){
        return this.canvas;
    }

    setCanvasParent(instance){
        this.canvasParent = instance;
    }

    getCanvasParent(){
        return this.canvasParent;
    }

    setAllComponentsList(instance){
        this.allComponentsList = instance;
    }

    getAllComponentsList(){
        return this.allComponentsList;
    }

    setMarkedComponentsList(instance){
        this.markedComponentsList = instance;
    }

    getMarkedComponentsList(){
        return this.markedComponentsList;
    }

    setPinoutTable(instance){
        this.pinoutTable = instance;
    }

    getPinoutTable(){
        return this.pinoutTable;
    }

    setNetsTreeview(instance){
        this.netsTreeview = instance;
    }

    getNetsTreeview(){
        return this.netsTreeview;
    }
}