class WidgetAdapter{
    static resetWidgets(){
        WidgetAdapter.resetSelectedComponentsWidgets();
        TreeViewAdapter.resetTreeview()
    }

    static resetSelectedComponentsWidgets(){
        allComponentsList.unselectAllItems();
        pinoutTable.unselectCurrentRow();
        pinoutTable.clearBody();
        DynamicSelectableListAdapter.generateMarkedComponentsList(markedComponentsList);
        selectedComponentSpan.innerText = "Component";
    }
    static resetSelectedNet(){
        TreeViewAdapter.resetTreeview();
        pinoutTable.unselectCurrentRow();
    }
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
        DynamicSelectableListAdapter.generatePinoutTableForComponent(itemElement);
        EngineAdapter.findComponentByName(itemName, isSelectionModeSingle);
        DynamicSelectableListAdapter.generateMarkedComponentsList(markedComponentsList)
    }

    static onClickItemEvent(itemElement){
        DynamicSelectableListAdapter.generatePinoutTableForComponent(itemElement);
        EngineAdapter.componentInScreenCenter(itemName);
    }

    static generatePinoutTableForComponent(itemElement){
        let itemName = itemElement.textContent;
        PinoutTableAdapter.generatePinoutTable(pinoutTable, itemName);
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

class TreeViewAdapter{
    static initTreeView(parentContainer){
        let treeview = new NetTreeView(parentContainer);
        return treeview
    }

    static generateTreeView(treeviewInstance, netsMap){
        treeviewInstance.eventBeforeSelection = EngineAdapter.unselectNet;
        treeviewInstance.netEvent = TreeViewAdapter.selectNetFromTreeviewEvent;
        treeviewInstance.componentEvent = EngineAdapter.selectNetComponentByName;
        treeviewInstance.addBranches(netsMap);
        treeviewInstance.generate();
    }
    
    static selectNetFromTreeviewEvent(netName){
        pinoutTable.selectRowByName(netName);    
    
        if(netsTreeview.getSelectedNet()){
            EngineAdapter.selectNet(netName);
        }
    }

    static resetTreeview(){
        netsTreeview.unselectCurrentBranch();
        netsTreeview.unselectCurrentItem();
    }
}

class InputModalBoxAdapter{
    static generateModalBox(modalboxInstance, headerString, submitEvent){
        modalboxInstance.setHeader(headerString);
        modalboxInstance.buttonEvent = submitEvent;
        modalboxInstance.show();
    }

    static getComponentNameFromInput(componentName){
        const modalBoxComponentName = componentName.toUpperCase();
        EngineAdapter.findComponentByName(modalBoxComponentName, isSelectionModeSingle);
    }

    static getCommonPrefixFromInput(commonPrefix){
        const modalBoxCommonPrefix = commonPrefix.toUpperCase();
    
        const isPrefixExist = EngineAdapter.showCommonPrefixComponents(modalBoxCommonPrefix);
        if (isPrefixExist){
            commonPrefixSpan.innerText = modalBoxCommonPrefix;
        }
    }
}