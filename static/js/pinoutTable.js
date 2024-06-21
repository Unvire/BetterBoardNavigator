class PinoutTable{
    constructor(parentContainer){
        this.parentContainer = parentContainer;
        this.selectRowEvent = null;
        this.beforeSelectionEvent = null;
        this.selectedRow = null;

        this.tableContainer = document.createElement("div");
        this.tableHeader = document.createElement("div");
        this.tableBody = document.createElement("div"); 
        
        this.#createHeader();
    }

    getSelectedRow(){
        return this.selectedRow;
    }

    set rowEvent(eventFunction){
        this.selectRowEvent = eventFunction;
    }

    set beforeRowEvent(eventFunction){
        this.beforeSelectionEvent = eventFunction;
    }

    #createHeader(){
        const row = document.createElement("div");
        this.#createRow(this.tableHeader, row, "header", "Pin", "Net");
        this.tableContainer.appendChild(this.tableHeader);

        this.parentContainer.appendChild(this.tableContainer) // debug
    }
    
    #createRow(parentContainer, row, rowAttriubute, textColumn1, textColumn2){
        row.classList.add("table-row");

        const column1 = document.createElement("div");
        const paragraph1 = document.createElement("p");
        paragraph1.innerText = textColumn1;
        column1.appendChild(paragraph1);

        const column2 = document.createElement("div");
        const paragraph2 = document.createElement("p");
        paragraph2.innerText = textColumn2;
        column2.appendChild(paragraph2);

        row.appendChild(column1);
        row.appendChild(column2);
        row.setAttribute("data-key", rowAttriubute);

        parentContainer.appendChild(row);
    }

    addRows(pinMap){
        this.clearBody();
        for (const [pinID, netName] of Object.entries(pinMap)) {
            const rowa = document.createElement("div");
            row.classList.add("table-row");


            const rowKey = document.createElement("td");
            rowKey.textContent = pinID;

            const rowNet = document.createElement("td");
            rowNet.textContent = netName;
            
            const row = document.createElement("tr");
            row.setAttribute("data-key", netName);
            row.appendChild(rowKey);
            row.appendChild(rowNet);
            row.addEventListener("click", () => { 
                this.beforeSelectionEvent();

                const isSkipSelectionHandling = row === this.selectedRow;
                this.unselectCurrentRow();

                if (!isSkipSelectionHandling){
                    this.selectedRow = this.#singleSelectionModeEvent(row);
                }

                this.selectRowEvent(netName);
            });

            this.tableBody.appendChild(row);

            this.table.appendChild(this.tableBody);
        }
    }

    #singleSelectionModeEvent(row){
        row.classList.add("table-highlighted");
        return row;
    }

    unselectCurrentRow(){
        if (this.selectedRow){
            this.selectedRow.classList.remove("table-highlighted");
            this.selectedRow = null;
        }
    }

    async selectRowByName(netName){
        let potentialRow = await this.tableBody.querySelector(`tr[data-key="${netName}"]`);
        if (potentialRow){
            const isSkipSelectionHandling = potentialRow === this.selectedRow;
            this.unselectCurrentRow();

            if (!isSkipSelectionHandling){
                this.selectedRow = this.#singleSelectionModeEvent(potentialRow);
            }
        } else {            
            this.unselectCurrentRow();
        }
    }

    generateTable(){
        this.parentContainer.appendChild(this.table);
    }

    clearBody(){
        while (this.tableContainer.firstChild){
            this.tableContainer.removeChild(this.tableContainer.firstChild);
        }
    }
}