class WidgetAdapter{
    static initSpanList(parentContainer){
        let spanList =  new DynamicSpanList(parentContainer);
        spanList.clickEvent = WidgetAdapter.onClickEventSpanList;
        return spanList
    }

    static generateSpanList(spanList, clickedComponentsList){
        spanList.addSpans(clickedComponentsList);
        spanList.generate();
    }
    static onClickEventSpanList(componentName){
        generatePinoutTableEvent(componentName);
    }
}