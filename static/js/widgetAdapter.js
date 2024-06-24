class WidgetAdapter{

}

class SpanListAdapter{
    static initSpanList(parentContainer){
        let spanList =  new DynamicSpanList(parentContainer);
        spanList.clickEvent = SpanListAdapter.onClickEventSpanList;
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

class DynamicSelectableListAdapter{
    static initDynamicSelectableList(parentContainer){
        let listInstance = new DynamicSelectableList(parentContainer);
        return listInstance
    }

    static generateList(listInstance, dataList, onClickEvent, selectionMode){
        listInstance.elementsList = dataList;
        listInstance.callbackEventFunction = onClickEvent;
        listInstance.selectionMode = selectionMode;
        listInstance.generateList();
    }

    static selectItemFromListEvent(itemElement){
        let clickedComponentName = itemElement.textContent;
        _markSelectedComponentFromList(clickedComponentName);
        generatePinoutTableEvent(clickedComponentName);
    }

    static onClickItemEvent(itemElement){
        let componentName = itemElement.textContent;
        generatePinoutTableEvent(componentName);
        EngineAdapter.componentInScreenCenter(componentName);
    }
}