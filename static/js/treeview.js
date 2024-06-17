class NetTreeView{
    constructor(parentContainer){
        this.parentContainer = parentContainer
        this.ulFirstLevel = document.createElement('ul');
        this.parentContainer.appendChild(this.ulFirstLevel);
        this.selectedNet = null;
        this.selectedComponent = null;
        this.selectNetEvent = null;
        this.selectComponentEvent = null;
    }

    set netEvent(eventFunction){
        this.selectNetEvent = eventFunction;
    }

    set componentEvent(eventFunction){
        this.selectComponentEvent = eventFunction;
    }
    
    addBranches(netMap){
        this.clearTree();
        for (const netName in netMap){
            const netBranch = document.createElement('li');
            const netSpan = document.createElement('span');

            this.#setNetSpan(netName, netSpan);
            netBranch.appendChild(netSpan);

            const subBranchContainer = document.createElement('ul');
            subBranchContainer.classList.add('hidden');
            this.#addSubBranches(subBranchContainer, netMap[netName]);  

            netBranch.appendChild(subBranchContainer);
            this.ulFirstLevel.appendChild(netBranch);
        }
    }

    #addSubBranches(subBranchContainer, netComponentSubMap){
        subBranchContainer.classList.add('treeview-hidden');

        for (const componentName in netComponentSubMap){
            const componentBranch = document.createElement('li');
            const componentPinoutSpan = document.createElement('span');

            const pins = netComponentSubMap[componentName];
            componentPinoutSpan.textContent = componentName + ": " + pins;
            componentPinoutSpan.addEventListener('click', (event) => {
                event.stopPropagation();
                this.selectedComponent = this.#handleSingleSelection(componentPinoutSpan, this.selectedComponent);
                if (this.selectComponentEvent){
                    this.selectComponentEvent(componentName);
                }
            });

            componentBranch.appendChild(componentPinoutSpan);
            subBranchContainer.appendChild(componentBranch);            
        }
    }
    
    #setNetSpan(netName, netSpan){
        netSpan.textContent = `+ ${netName}`;
        netSpan.addEventListener('click', (event) => {
            event.stopPropagation();

            this.#unselectCurrentBranch(this.selectedNet);
            this.#unselectCurrentItem(this.selectedComponent);
            this.#toggleVisibility(netSpan);

            this.selectedNet = this.#handleSingleSelection(netSpan, this.selectedNet);
            this.selectNetEvent('');
            if (this.selectedNet === netSpan){
                this.selectNetEvent(netName);
            }
        });
    }

    #toggleVisibility(netSpan){
        const liParent = netSpan.parentElement;
        const childUl = liParent.querySelector('ul');
        if (childUl) {
            if (childUl.classList.contains('treeview-hidden')){
                childUl.classList.remove('treeview-hidden');
                netSpan.textContent = '-' + netSpan.innerText.substring(1);
            } else {
                childUl.classList.add('treeview-hidden');
                netSpan.textContent = '+' + netSpan.innerText.substring(1);
            }
        }
    }

    #handleSingleSelection(clickedItem, currentSelectedItem){
        let currentSelectedItem;
        if (clickedItem.classList.contains('treeview-selected')){
            clickedItem.classList.remove('treeview-selected');
            currentSelectedItem = null;
        } else {
            clickedItem.classList.add('treeview-selected');
            currentSelectedItem = clickedItem;
        }
        return currentSelectedItem;
    }

    #unselectCurrentBranch(currentSelectedBranch){
        if (currentSelectedBranch){
            const liParent = currentSelectedBranch.parentElement;
            const childUl = liParent.querySelector('ul');
            childUl.classList.add('treeview-hidden');

            currentSelectedBranch.classList.remove('treeview-selected');
            currentSelectedBranch.textContent = '+' + currentSelectedBranch.textContent.substring(1);
            }
    }

    #unselectCurrentItem(currentSelectedItem){
        if (currentSelectedItem){
            currentSelectedItem.classList.remove('treeview-selected');
        }
    }

    clearTree(){
        this.ulFirstLevel.innerHTML = '';
    }

    generate(){
        this.parentContainer.appendChild(this.ulFirstLevel);
    }

}