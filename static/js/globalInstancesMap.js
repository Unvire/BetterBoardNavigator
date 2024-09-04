class GlobalInstancesMap{
    constructor(){
        this.modalSubmit = null;
        this.textModalSubmitButton = null;
        this.textModalInput = null;
        this.canvas = null;
        this.canvasParent = null;
        this.allComponentsList = null;
        this.markedComponentsList = null;
        this.pinoutTable = null;
        this.netsTreeview = null;
        this.clickedComponentSpanList = null;
        this.commonPrefixSpan = null;
        this.selectedComponentSpan = null;
        this.currentSideSpan = null;
        this.modalParagraph = null;
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

    setSelectedComponentSpan(instance){
        this.selectedComponentSpan = instance;
    }

    getSelectedComponentSpan(){
        return this.selectedComponentSpan;
    }

    setClickedComponentSpanList(instance){
        this.clickedComponentSpanList = instance;
    }

    getClickedComponentSpanList(){
        return this.clickedComponentSpanList;
    }

    setCommonPrefixSpan(instance){
        this.commonPrefixSpan = instance;
    }

    getCommonPrefixSpan(){
        return this.commonPrefixSpan;
    }

    setCurrentSideSpan(instance){
        this.currentSideSpan = instance;
    }

    getCurrentSideSpan(){
        return this.currentSideSpan;
    }

    setToggleOutlinesButton(instance){
        this.toggleOutlinesButton = instance;
    }

    getToggleOutlinesButton(){
        return this.toggleOutlinesButton;
    }

    setModalHelp(instance){
        this.modalHelp = instance;
    }

    getModalHelp(){
        return this.modalHelp;
    }

    setShowDemoBoardButton(instance){
        this.showDemoBoardButton = instance;
    }

    getShowDemoBoardButton(){
        return this.showDemoBoardButton;
    }

    setToggleFindComponentByClickButton(instance){
        this.toggleFindComponentByClickButton = instance;
    }

    getToggleFindComponentByClickButton(){
        return this.toggleFindComponentByClickButton;
    }
}