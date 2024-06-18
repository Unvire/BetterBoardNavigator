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
            row.setAttribute('data-key', netName);
            row.appendChild(rowKey);
            row.appendChild(rowNet);
            row.addEventListener('click', () => {         
                let isSkipSelectionHandling = false;

                this.beforeSelectionEvent();
                if (row === this.selectedRow){
                    isSkipSelectionHandling = true;
                }

                if (this.selectedRow){
                    this.unselectCurrentRow();
                }

                if (!isSkipSelectionHandling){
                    this.selectedRow = this.#singleSelectionModeEvent(row);
                }

                this.selectRowEvent(netName);
            });

            this.tableBody.appendChild(row);

            this.table.appendChild(this.tableBody);
        }
        this.children = this.tableBody.querySelectorAll('tr');
    }

    #singleSelectionModeEvent(row){
        row.classList.add('table-highlighted');
        return row;
    }

    unselectCurrentRow(){
        this.selectedRow.classList.remove('table-highlighted');
        this.selectedRow = null;
    }

    async selectRowByName(netName){
        let potentialRow; 
        potentialRow = await this.tableBody.querySelector(`tr[data-key="${netName}"]`);
        if (!potentialRow){
            this.unselectCurrentRow();
            return;
        }

        let isSkipSelectionHandling = false;
        
        if (potentialRow === this.selectedRow){
            isSkipSelectionHandling = true;
        }

        if (this.selectedRow){
            this.unselectCurrentRow();
        }

        if (!isSkipSelectionHandling){
            this.selectedRow = this.#singleSelectionModeEvent(potentialRow);
        }
    }

    generateTable(){
        this.parentContainer.appendChild(this.table);
    }

    clearBody(){
        while (this.tableBody.firstChild){
            this.tableBody.removeChild(this.tableBody.firstChild);
        }
        this.children = [];
    }
}