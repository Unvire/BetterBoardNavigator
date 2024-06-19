class NetTreeView{
    constructor(parentContainer){
        this.parentContainer = parentContainer
        this.ulFirstLevel = document.createElement('ul');
        this.parentContainer.appendChild(this.ulFirstLevel);
        this.selectedNet = null;
        this.selectedComponent = null;
        this.selectNetEvent = null;
        this.selectComponentEvent = null;
        this.beforeSelectionEvent = null;
    }

    getSelectedNet(){
        return this.selectedNet;
    }

    getSelectedNetName(){
        if (this.selectedNet){
            return this.selectedNet.textContent.substring(2); // first 2 characters are '+ ' or '- '
        }
        return '';
    }

    set netEvent(eventFunction){
        this.selectNetEvent = eventFunction;
    }
    

    set componentEvent(eventFunction){
        this.selectComponentEvent = eventFunction;
    }

    set eventBeforeSelection(eventFunction){
        this.beforeSelectionEvent = eventFunction;
    }
    
    addBranches(netMap){
        this.clearTree();
        for (const netName in netMap){
            const netBranch = document.createElement('li');
            const netSpan = document.createElement('span');

            this.#setNetSpan(netName, netSpan);
            netBranch.appendChild(netSpan);
            netBranch.setAttribute('data-key', netName);

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
            
            componentBranch.setAttribute('data-key', componentName);

            const pins = netComponentSubMap[componentName];
            componentPinoutSpan.textContent = componentName + ": " + pins;
            componentPinoutSpan.addEventListener('click', (event) => {
                event.stopPropagation();

                const isSkipSelectionHandling = componentPinoutSpan === this.selectedComponent;
                this.unselectCurrentItem();
                
                if (!isSkipSelectionHandling){
                    this.selectedComponent = this.#handleSingleSelection(componentPinoutSpan);
                }
                
                this.selectComponentEvent(componentName);
            });

            componentBranch.appendChild(componentPinoutSpan);
            subBranchContainer.appendChild(componentBranch);            
        }
    }
    
    #setNetSpan(netName, netSpan){
        netSpan.textContent = `+ ${netName}`;
        netSpan.addEventListener('click', (event) => {
            event.stopPropagation();

            this.beforeSelectionEvent();
            this.unselectCurrentItem();

            const isSkipSelectionHandling = this.selectedNet === netSpan;
            this.unselectCurrentBranch();

            if (!isSkipSelectionHandling){
                this.#toggleVisibility(netSpan);
                this.selectedNet = this.#handleSingleSelection(netSpan);
            }
            this.selectNetEvent(netName);
        });
    }

    #handleSingleSelection(clickedItem){
        clickedItem.classList.add('treeview-selected');
        return clickedItem;
    }
    
    async scrollToBranchByName(netName){
        let keyElement = await this.ulFirstLevel.querySelector(`li[data-key="${netName}"]`);
        if (!keyElement){
            return
        }
        keyElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        let netSpan = await keyElement.querySelector('span');

        this.unselectCurrentItem();
        if (this.selectedNet === netSpan){
            this.unselectCurrentBranch();
            return;  
        }

        this.unselectCurrentBranch();
        this.#toggleVisibility(netSpan);
        this.selectedNet = this.#handleSingleSelection(netSpan);
    }

    async selectComponentByName(componentName){
        if (!this.selectedNet){
            return;
        }
        
        const selectedNetUl = this.#getUlFromSpan(this.selectedNet);

        let componentLi = await selectedNetUl.querySelector(`li[data-key="${componentName}"]`);
        console.log(this.selectedNet, componentLi)

    }

    unselectCurrentBranch(){
        if (this.selectedNet){
            const selectedNetUl = this.#getUlFromSpan(this.selectedNet);
            selectedNetUl.classList.add('treeview-hidden');

            this.selectedNet.classList.remove('treeview-selected');
            this.selectedNet.textContent = '+' + this.selectedNet.textContent.substring(1);
            this.selectedNet = null;
        }
    }

    unselectCurrentItem(){
        if (this.selectedComponent){
            this.selectedComponent.classList.remove('treeview-selected');
            this.selectedComponent = null;
        }
    }

    #toggleVisibility(netSpan){
        const netUl = this.#getUlFromSpan(netSpan);
        if (netUl && netUl.classList.contains('treeview-hidden')) {
            netUl.classList.remove('treeview-hidden');
            netSpan.textContent = '-' + netSpan.innerText.substring(1);
        }
    }

    #getUlFromSpan(span){
        const liParent = span.parentElement;
        return liParent.querySelector('ul');
    }

    clearTree(){
        this.ulFirstLevel.innerHTML = '';
    }

    generate(){
        this.parentContainer.appendChild(this.ulFirstLevel);
    }

}