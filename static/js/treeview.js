class NetTreeView{
    constructor(parentContainer){
        this.parentContainer = parentContainer
        this.ulFirstLevel = document.createElement('ul');
        this.parentContainer.appendChild(this.ulFirstLevel);
    }
    
    addBranches(netMap){
        for (const netName in netMap){
            const netBranch = document.createElement('li');
            const toggleSpan = document.createElement('span');
            const netSpan = document.createElement('span');

            this._setToggleButton(toggleSpan, netBranch);
            this._setNetSpan(netSpan, netName);
            netBranch.appendChild(toggleSpan);
            netBranch.appendChild(netSpan);

            const subBranchContainer = document.createElement('ul');
            subBranchContainer.classList.add('hidden');
            this._addSubBranches(subBranchContainer, netMap[netName]);  

            netBranch.appendChild(subBranchContainer);
            this.ulFirstLevel.appendChild(netBranch);
        }
    }

    _addSubBranches(subBranchContainer, netComponentSubMap){
        subBranchContainer.classList.add('treeview-hidden');

        for (const componentName in netComponentSubMap){
            const componentBranch = document.createElement('li');
            const componentPinoutSpan = document.createElement('span');

            const pins = netComponentSubMap[componentName];
            componentPinoutSpan.textContent = componentName + ": " + pins;
            componentPinoutSpan.addEventListener('click', (event) => {
                event.stopPropagation();
                this._toggleSelect(componentPinoutSpan);
            });

            componentBranch.appendChild(componentPinoutSpan);
            subBranchContainer.appendChild(componentBranch);            
        }
    }

    _setToggleButton(toggleButton, liParent){
        toggleButton.textContent = '+';
        toggleButton.classList.add('toggle-button');
        toggleButton.addEventListener('click', (event) => {
            event.stopPropagation();
            this._toggleButtonVisibility(toggleButton, liParent);
        });
    }
    
    _setNetSpan(netSpan, netName){
        netSpan.textContent = netName;
        netSpan.addEventListener('click', (event) => {
            event.stopPropagation();
            this._toggleSelect(netSpan);
        });
    }

    _toggleButtonVisibility(toggleButton, liParent){
        const childUl = liParent.querySelector('ul');
        if (childUl) {
            if (childUl.classList.contains('treeview-hidden')){
                childUl.classList.remove('treeview-hidden');
                toggleButton.textContent = '-';
            } else {
                childUl.classList.add('treeview-hidden');
                toggleButton.textContent = '+';
            }
        }
    }

    _toggleSelect(item){
        item.classList.toggle('treeview-selected');
    }

    generate(){
        this.parentContainer.appendChild(this.ulFirstLevel);
    }

}