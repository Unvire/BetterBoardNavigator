class PinoutTable{
    constructor(parentContainer){
        this.parentContainer = parentContainer;
        this.tableContainer = document.createElement("div");
        this.selectRowEvent = null;
        this.beforeSelectionEvent = null;
        this.selectedRows = [];
    }

    getSelectedRows(){
        return this.selectedRows;
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

        parentContainer.appendChild(row);
    }

    addRows(pinMap){
        this.clearBody();
        for (const [pinID, netName] of Object.entries(pinMap)) {
            const row = document.createElement("div");
            this.#createRow(this.parentContainer, row, netName, pinID, netName);

            row.addEventListener("click", () => { 
                this.beforeSelectionEvent();
                this.selectRowByName(netName);
                this.selectRowEvent(netName);
            });
            
        }
    }

    #singleSelectionModeEvent(row){
        row.classList.add("selected");
        return row;
    }

    unselectCurrentRows(){
        this.selectedRows.forEach(row => {
            row.classList.remove("selected");
        });
        this.selectedRows = [];
    }

    selectRowByName(netName){
        let potentialRows = this.parentContainer.querySelectorAll(`div[data-key="${netName}"]`);
        if (potentialRows){
            const isSkipSelectionHandling = this.#isSelectedRowsTheSameAs(potentialRows);
            this.unselectCurrentRows();

            if (!isSkipSelectionHandling){
                potentialRows.forEach(row => {
                    this.selectedRows.push(this.#singleSelectionModeEvent(row));
                });
            }
        } else {            
            this.unselectCurrentRows();
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

    #isSelectedRowsTheSameAs(selectedRows){
        const listLength = this.selectedRows.length;
        if (selectedRows.length != listLength || !selectedRows || !this.selectedRows){
            return false;
        }

        const array1 = [...selectedRows].sort();
        const array2 = [...this.selectedRows].sort();
        for (let i = 0; i < listLength; i++){
            if (array1[i] !== array2[i]){
                return false;
            }
        }
        return true;
    }
}