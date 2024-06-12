class PinoutTable{
    constructor(parentContainer){
        this.parentContainer = parentContainer;

        this.table = document.createElement('table');
        this.tableBody = document.createElement('table-body');
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

    generateTable(){
        this.parentContainer.appendChild(this.table);
    }

}