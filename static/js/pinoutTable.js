class PinoutTable{
    constructor(parentContainer){
        this.parentContainer = parentContainer;
        this.tableContainer = document.createElement("div");
        this.selectRowEvent = null;
        this.beforeSelectionEvent = null;
        this.selectedRow = null;
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

        this.parentContainer.appendChild(row);
    }

    addRows(pinMap){
        this.clearBody();
        for (const [pinID, netName] of Object.entries(pinMap)) {
            const row = document.createElement("div");
            this.#createRow(this.parentContainerGe, row, netName, pinID, netName);

            row.addEventListener("click", () => { 
                this.beforeSelectionEvent();

                const isSkipSelectionHandling = row === this.selectedRow;
                this.unselectCurrentRow();

                if (!isSkipSelectionHandling){
                    this.selectedRow = this.#singleSelectionModeEvent(row);
                }

                this.selectRowEvent(netName);
            });
            
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
        let potentialRow = await this.parentContainer.querySelector(`div[data-key="${netName}"]`);
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
        this.parentContainer.appendChild(this.tableContainer);
    }

    clearBody(){
        while (this.parentContainer.firstChild){
            this.parentContainer.removeChild(this.parentContainer.firstChild);
        }
    }
}