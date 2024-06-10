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
        this.callbackEventFunction(itemDiv);
    }

    _singleSelectionMode(itemDiv){
        this.children.forEach(el => el.classList.remove('selected'));
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
}


function generateList(containerID, elemetsList, eventFunction){
    elemetsList.forEach(element => {
        const itemElement = document.createElement('div');
        itemElement.textContent = element;
        containerID.appendChild(itemElement);
        itemElement.addEventListener('click', () => eventFunction(itemElement));
    });
}

function _selectOneScrollableListItem(containerID, itemElement){
    const allItems = containerID.querySelectorAll('div');
    allItems.forEach(el => el.classList.remove('selected'));

    itemElement.classList.add('selected');
}

function _selectMultipleListItems(itemElement){
    if (itemElement.classList.contains('selected')){
        itemElement.classList.remove('selected')
    } else {
        itemElement.classList.add('selected');
    }
}

function clearList(containerID){
    while (containerID.firstChild) {
        containerID.removeChild(containerID.firstChild);
    }
}