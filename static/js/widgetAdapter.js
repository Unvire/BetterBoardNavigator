class WidgetAdapter{
    static resetWidgets(){
        WidgetAdapter.resetSelectedComponentsWidgets();
        TreeViewAdapter.resetTreeview()
    }

    static resetSelectedComponentsWidgets(){
        const allComponentsList = globalInstancesMap.getAllComponentsList()
        const pinoutTable = globalInstancesMap.getPinoutTable();

        allComponentsList.unselectAllItems();
        pinoutTable.unselectCurrentRow();
        pinoutTable.clearBody();
        DynamicSelectableListAdapter.generateMarkedComponentsList(markedComponentsList);
        selectedComponentSpan.innerText = "Component";
    }
    static resetSelectedNet(){
        const pinoutTable = globalInstancesMap.getPinoutTable();

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
        const pinoutTable = globalInstancesMap.getPinoutTable();

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
        const itemName = DynamicSelectableListAdapter.generatePinoutTableForComponent(itemElement);
        EngineAdapter.findComponentByName(itemName, isSelectionModeSingle);
        DynamicSelectableListAdapter.generateMarkedComponentsList(markedComponentsList)
    }

    static onClickItemEvent(itemElement){
        const itemName = DynamicSelectableListAdapter.generatePinoutTableForComponent(itemElement);
        EngineAdapter.componentInScreenCenter(itemName);
    }

    static generatePinoutTableForComponent(itemElement){
        let itemName = itemElement.textContent;
        PinoutTableAdapter.generatePinoutTable(itemName);
        return itemName
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

    static generatePinoutTable(componentName){
        pyodide.runPython(`
            pinoutDict = engine.getComponentPinout('${componentName}')
        `);
        let pinoutMap = pyodide.globals.get("pinoutDict").toJs();
        
        const pinoutTable = globalInstancesMap.getPinoutTable();
        pinoutTable.rowEvent = PinoutTableAdapter.selectNetFromTableEvent;
        pinoutTable.beforeRowEvent = EngineAdapter.unselectNet;
        pinoutTable.addRows(pinoutMap);
        pinoutTable.generateTable();
        
        
        const netsTreeview = globalInstancesMap.getNetsTreeview();
        const netTreeSelectedNetName = netsTreeview.getSelectedNetName();
        pinoutTable.selectRowByName(netTreeSelectedNetName);
        selectedComponentSpan.innerText = componentName;
    }

    static selectNetFromTableEvent(netName){
        const netsTreeview = globalInstancesMap.getNetsTreeview();
        const pinoutTable = globalInstancesMap.getPinoutTable();    

        netsTreeview.scrollToBranchByName(netName);
        if(pinoutTable.getSelectedRow()){
            EngineAdapter.selectNet(netName);
        }
    }

    static clearBody(){
        const pinoutTable = globalInstancesMap.getPinoutTable();

        pinoutTable.clearBody()
    }
}

class TreeViewAdapter{
    static initTreeView(parentContainer){
        let treeview = new NetTreeView(parentContainer);
        return treeview
    }

    static generateTreeView(netsMap){
        const netsTreeview = globalInstancesMap.getNetsTreeview();

        netsTreeview.eventBeforeSelection = EngineAdapter.unselectNet;
        netsTreeview.netEvent = TreeViewAdapter.selectNetFromTreeviewEvent;
        netsTreeview.componentEvent = EngineAdapter.selectNetComponentByName;
        netsTreeview.addBranches(netsMap);
        netsTreeview.generate();
    }
    
    static selectNetFromTreeviewEvent(netName){
        const netsTreeview = globalInstancesMap.getNetsTreeview();
        const pinoutTable = globalInstancesMap.getPinoutTable();

        pinoutTable.selectRowByName(netName);    

        if(netsTreeview.getSelectedNet()){
            EngineAdapter.selectNet(netName);
        }
    }

    static resetTreeview(){
        const netsTreeview = globalInstancesMap.getNetsTreeview();
        
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