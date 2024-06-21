class DynamicSpanList{
    constructor(parentContainer){
        this.parentContainer = parentContainer;
        this.spanListContainer = document.createElement("div");
        this.spanListContainer.classList.add("span-list")

        this.callbackEventFunction = null;
    }

    set clickEvent(eventFunction){
        this.callbackEventFunction = eventFunction;
    }

    clearList(){
        while (this.spanListContainer.firstChild) {
            this.spanListContainer.removeChild(this.spanListContainer.firstChild);
        }
    }

    addSpans(elementList){
        this.clearList();
        const lastItem = elementList[elementList.length - 1];
        console.log(elementList, lastItem)
        elementList.forEach(elementString => {
            const elementSpan = document.createElement("span");
            elementSpan.innerText = elementString;
            elementSpan.addEventListener("click", () => {
                this.callbackEventFunction(elementString);
            });
            
            this.spanListContainer.appendChild(elementSpan);
            if (elementString !== lastItem){
                const spearatorSpan = document.createElement("span");
                spearatorSpan.innerText = ", ";
                this.spanListContainer.appendChild(spearatorSpan);
            }
        });
    }

    generate(){
        this.parentContainer.appendChild(this.spanListContainer);
    }
}