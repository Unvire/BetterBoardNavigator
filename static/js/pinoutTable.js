class PinoutTable{
    constructor(parentContainer){
        this.parentContainer = parentContainer;
        this.table = document.createElement('table');
        this._createHeader()
    }

    _createHeader(){
        const headerColumn1 = document.createElement('th');
        headerColumn1.textContent = 'Pin';

        const headerColumn2 = document.createElement('th');
        headerColumn2.textContent = 'Net';

        const headerRow = document.createElement('tr');
        headerRow.appendChild(headerColumn1);
        headerRow.appendChild(headerColumn2);

        
        const tableHead = document.createElement('table-head');
        tableHead.appendChild(headerRow);
        
        this.table.appendChild(tableHead);
    }

    addRows(pinMap){
        for (const [pinID, netName] of Object.entries(pinMap)) {
            const rowKey = document.createElement('td');
            rowKey.textContent = pinID;

            const rowNet = document.createElement('td');
            rowNet.textContent = netName;
            
            const row = document.createElement('tr');
            row.appendChild(rowKey);
            row.appendChild(rowNet);

            const tableBody = document.createElement('table-body');
            tableBody.appendChild(row);

            this.table.appendChild(tableBody);
        }
    }

    generateTable(){
        this.parentContainer.appendChild(this.table);
    }

}