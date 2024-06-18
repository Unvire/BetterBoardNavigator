class PinoutTable{
    constructor(parentContainer){
        this.parentContainer = parentContainer;
        this.selectRowEvent = null;
        this.beforeSelectionEvent = null;
        this.selectedRow = null;
        
        this.table = document.createElement('table');
        this.tableHead = document.createElement('table-head');
        this.tableBody = document.createElement('table-body');
        this.#createHeader();
    }

    set rowEvent(eventFunction){
        this.selectRowEvent = eventFunction;
    }

    set beforeRowEvent(eventFunction){
        this.beforeSelectionEvent = eventFunction;
    }

    #createHeader(){
        const headerColumn1 = document.createElement('th');
        headerColumn1.textContent = 'Pin';

        const headerColumn2 = document.createElement('th');
        headerColumn2.textContent = 'Net';

        const headerRow = document.createElement('tr');
        headerRow.appendChild(headerColumn1);
        headerRow.appendChild(headerColumn2);

        this.tableHead.appendChild(headerRow);
        this.table.appendChild(this.tableHead);
        this.children = null;
    }

    addRows(pinMap){
        this.clearBody();
        for (const [pinID, netName] of Object.entries(pinMap)) {
            const rowKey = document.createElement('td');
            rowKey.textContent = pinID;

            const rowNet = document.createElement('td');
            rowNet.textContent = netName;
            
            const row = document.createElement('tr');
            row.appendChild(rowKey);
            row.appendChild(rowNet);
            row.addEventListener('click', () => {
                this.selectedRow = this.#singleSelectionModeEvent(row, this.selectedRow);                
                this.beforeSelectionEvent();
                this.selectRowEvent(netName);
            });

            this.tableBody.appendChild(row);

            this.table.appendChild(this.tableBody);
        }
        this.children = this.tableBody.querySelectorAll('tr');
    }

    #singleSelectionModeEvent(row, currentSelectedRow){
        if (row.classList.contains('table-highlighted')){
            row.classList.remove('table-highlighted');
            currentSelectedRow = null;
        } else {
            if (currentSelectedRow){
                currentSelectedRow.classList.remove('table-highlighted');
            }
            row.classList.add('table-highlighted');
            currentSelectedRow = row;
        }
        return currentSelectedRow;
    }

    generateTable(){
        this.parentContainer.appendChild(this.table);
    }

    #unselectAllRows(){
        this.children.forEach(tr => tr.classList.remove('table-highlighted'));
    }

    clearBody(){
        while (this.tableBody.firstChild){
            this.tableBody.removeChild(this.tableBody.firstChild);
        }
        this.children = [];
    }
}