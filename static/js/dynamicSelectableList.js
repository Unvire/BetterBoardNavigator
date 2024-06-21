class DynamicSelectableList{
    constructor(parentContainer){
        this.parentContainer = parentContainer;
        this.selectionModesMap = {"single": this.#singleSelectionMode, "multiple":this.#multipleSelectionMode};
        this.selectionFunction = null;
        this.elements = [];
        this.callbackEventFunction = null;
        this.children = null;
    }

    set elementsList(list){
        this.elements = list;
    }

    set eventCallbackFuntion(eventFunction){
        this.callbackEventFunction = eventFunction;
    }

    set selectionMode(mode){
        this.selectionFunction = this.selectionModesMap[mode];
    }

    #bindOnClickEvent(itemDiv){
        this.selectionFunction(itemDiv);
        if (this.callbackEventFunction){
            this.callbackEventFunction(itemDiv);
        }
    }

    #singleSelectionMode(itemDiv){
        this.unselectAllItems();
        itemDiv.classList.add("selected");
    }

    #multipleSelectionMode(itemDiv){
        if (itemDiv.classList.contains("selected")){
            itemDiv.classList.remove("selected");
        } else {
            itemDiv.classList.add("selected");
        }
    }

    generateList(){
        this.clearList()

        this.elements.forEach(el => {
            const itemDiv = document.createElement("div");
            itemDiv.setAttribute("data-key", el);

            const itemChildParagraph = document.createElement("p");
            itemChildParagraph.innerText = el;
            
            itemDiv.appendChild(itemChildParagraph);
            this.parentContainer.appendChild(itemDiv);
            itemDiv.addEventListener("click", () => this.#bindOnClickEvent(itemDiv));
        });

        this.children = this.parentContainer.querySelectorAll("div");
    }

    clearList(){
        while (this.parentContainer.firstChild) {
            this.parentContainer.removeChild(this.parentContainer.firstChild);
        }
    }

    get selectedItems(){
        selectedItems = [];
        this.children.forEach(el => {
            if (el.classList.contains("selected")){
                this.selectedItems.push(el);
            }
        });
        return this.selectedItems;
    }

    unselectAllItems(){
        this.children.forEach(el => el.classList.remove("selected"));
    }

    async selectItemByName(name){
        let potentialDiv = await this.parentContainer.querySelector(`div[data-key="${name}"]`);
        if (potentialDiv){
            this.selectionFunction(potentialDiv);
        }
    }
}