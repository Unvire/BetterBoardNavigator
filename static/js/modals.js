class ModalBox{
    constructor(parentContainer, closeSpan, header){
        this.parentContainer = parentContainer;
        this.closeSpan = closeSpan;
        this.header = header;

        this.closeSpan.addEventListener("click", () => { 
            this.close();
        });

        
        window.addEventListener("click", (event) => { 
            if (event.target == this.parentContainer) {
                this.close();
            }
        });
    }

    show(){
        this.parentContainer.style.display = "block";
    }

    close(){
        this.header.innerText = "";
        this.parentContainer.style.display = "none";
    }

    setHeader(text){
        this.header.innerText = text;
    }
}

class ModalSubmit extends ModalBox{
    constructor(parentContainer, closeSpan, header, textInput, submitButton){
        super(parentContainer, closeSpan, header)
        this.textInput = textInput;
        this.submitButton = submitButton;
    }

    set buttonEvent(eventFunction){
        this.submitEvent = eventFunction;
        this.submitButton.addEventListener("click", () => {
            this.submitEvent(this.textInput.value);
            this.close();
        });
    }

    close(){
        this.textInput.value = "";
        super.close();
    }
}

class ModalParagraph extends ModalBox{
    constructor(parentContainer, closeSpan, header, textParagraph){
        super(parentContainer, closeSpan, header)
        this.textParagraph = textParagraph;
    }

    clearParagraph(){
        this.setParagraphText("");
    }

    setParagraphText(text){
        this.textParagraph.innerText = text;
    }
}