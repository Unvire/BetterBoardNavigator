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

    static clearList(listInstance){
        listInstance.clearList();
    }

    static selectItemFromListEvent(itemElement){
        let itemName = itemElement.textContent;
        generatePinoutTableEvent(itemName);
        EngineAdapter.findComponentByName(itemName, side, isSelectionModeSingle);
        DynamicSelectableListAdapter.generateMarkedComponentsList(markedComponentsList)
    }

    static onClickItemEvent(itemElement){
        let itemName = itemElement.textContent;
        generatePinoutTableEvent(itemName);
        EngineAdapter.componentInScreenCenter(itemName);
    }

    static generateMarkedComponentsList(markedComponentsListInstance){
        pyodide.runPython(`
            componentsList = engine.getSelectedComponents()
        `);
        const componentsList = pyodide.globals.get("componentsList").toJs();
        DynamicSelectableListAdapter.generateList(markedComponentsListInstance, componentsList, DynamicSelectableListAdapter.onClickItemEvent, "no");
    }
}

class PinoutTableAdapter{
    static initPinoutTable(parentContainer){
        
    }
}