class DynamicSelectableList{
    constructor(parentContainer){
        this.parentContainer = parentContainer;
        this.selectionModesMap = {'single': this._singleSelectionMode, 'multiple':this._multipleSelectionMode};
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

    _bindOnClickEvent(itemDiv){
        this.selectionFunction(itemDiv);
        if (this.callbackEventFunction){
            this.callbackEventFunction(itemDiv);
        }
    }

    _singleSelectionMode(itemDiv){
        this.unselectAllItems();
        itemDiv.classList.add('selected');
    }

    _multipleSelectionMode(itemDiv){
        if (itemDiv.classList.contains('selected')){
            itemDiv.classList.remove('selected');
        } else {
            itemDiv.classList.add('selected');
        }
    }

    generateList(){
        this.clearList()

        this.elements.forEach(el => {
            const itemDiv = document.createElement('div');
            itemDiv.textContent = el;
            
            this.parentContainer.appendChild(itemDiv);
            itemDiv.addEventListener('click', () => this._bindOnClickEvent(itemDiv));
        });

        this.children = this.parentContainer.querySelectorAll('div');
    }

    clearList(){
        while (this.parentContainer.firstChild) {
            this.parentContainer.removeChild(this.parentContainer.firstChild);
        }
    }

    get selectedItems(){
        selectedItems = [];
        this.children.forEach(el => {
            if (el.classList.contains('selected')){
                this.selectedItems.push(el);
            }
        });
        return this.selectedItems;
    }

    unselectAllItems(){
        this.children.forEach(el => el.classList.remove('selected'));
    }
}