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
        PinoutTableAdapter.generatePinoutTable(pinoutTable, componentName);
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
        PinoutTableAdapter.generatePinoutTable(pinoutTable, itemName);
        EngineAdapter.findComponentByName(itemName, side, isSelectionModeSingle);
        DynamicSelectableListAdapter.generateMarkedComponentsList(markedComponentsList)
    }

    static onClickItemEvent(itemElement){
        let itemName = itemElement.textContent;
        PinoutTableAdapter.generatePinoutTable(pinoutTable, itemName);
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
        let table = new PinoutTable(parentContainer);
        return table;
    }

    static generatePinoutTable(pinoutTableInstance, componentName){
        pyodide.runPython(`
            pinoutDict = engine.getComponentPinout('${componentName}')
        `);
        let pinoutMap = pyodide.globals.get("pinoutDict").toJs();

        pinoutTableInstance.rowEvent = PinoutTableAdapter.selectNetFromTableEvent;
        pinoutTableInstance.beforeRowEvent = EngineAdapter.unselectNet;
        pinoutTableInstance.addRows(pinoutMap);
        pinoutTableInstance.generateTable();

        const netTreeSelectedNetName = netsTreeview.getSelectedNetName();
        pinoutTableInstance.selectRowByName(netTreeSelectedNetName);
        selectedComponentSpan.innerText = componentName;
    }

    static selectNetFromTableEvent(netName){
        netsTreeview.scrollToBranchByName(netName);
        if(pinoutTable.getSelectedRow()){
            EngineAdapter.selectNet(netName);
        }
    }

    static clearBody(pinoutTableInstance){
        pinoutTableInstance.clearBody()
    }
}