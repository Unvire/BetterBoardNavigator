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

            const pins = netComponentSubMap[componentName];
            componentPinoutSpan.textContent = componentName + ": " + pins;
            componentPinoutSpan.addEventListener('click', (event) => {
                event.stopPropagation();
                let isSkipSelectionHandling = false;

                if (componentPinoutSpan === this.selectedComponent){
                    isSkipSelectionHandling = true;
                }
                
                if (this.selectedComponent){
                    this.unselectCurrentItem();
                }
                
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
            let isSkipSelectionHandling = false;
            
            this.beforeSelectionEvent();
            if (this.selectedComponent){
                this.unselectCurrentItem();
            }

            if (this.selectedNet === netSpan){
                isSkipSelectionHandling = true;
            }

            if (this.selectedNet){
                this.unselectCurrentBranch();
            }

            if (!isSkipSelectionHandling){
                this.#toggleVisibility(netSpan);
                this.selectedNet = this.#handleSingleSelection(netSpan);
            }
            this.selectNetEvent(netName);
        });
    }

    #toggleVisibility(netSpan){
        const liParent = netSpan.parentElement;
        const childUl = liParent.querySelector('ul');
        if (childUl && childUl.classList.contains('treeview-hidden')) {
            childUl.classList.remove('treeview-hidden');
            netSpan.textContent = '-' + netSpan.innerText.substring(1);
        }
    }

    #handleSingleSelection(clickedItem){
        clickedItem.classList.add('treeview-selected');
        return clickedItem;
    }

    unselectCurrentBranch(){
        const liParent = this.selectedNet.parentElement;
        const childUl = liParent.querySelector('ul');
        childUl.classList.add('treeview-hidden');

        this.selectedNet.classList.remove('treeview-selected');
        this.selectedNet.textContent = '+' + this.selectedNet.textContent.substring(1);
        this.selectedNet = null;
    }

    unselectCurrentItem(){
        this.selectedComponent.classList.remove('treeview-selected');
        this.selectedComponent = null;
    }
    
    async scrollToBranchByName(netName){
        let keyElement; 
        keyElement = await this.ulFirstLevel.querySelector(`li[data-key="${netName}"]`);
        if (!keyElement){
            return
        }
        keyElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        let netSpan = await keyElement.querySelector('span');

        if (this.selectedComponent){
            this.unselectCurrentItem();
        }

        if (this.selectedNet === netSpan){
            this.unselectCurrentBranch();
            return;   
        }

        if (this.selectedNet){
            this.unselectCurrentBranch();
        }
        
        this.#toggleVisibility(netSpan);
        this.selectedNet = this.#handleSingleSelection(netSpan);
    }

    clearTree(){
        this.ulFirstLevel.innerHTML = '';
    }

    generate(){
        this.parentContainer.appendChild(this.ulFirstLevel);
    }

}