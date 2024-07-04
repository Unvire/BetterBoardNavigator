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

class ModalHelp extends ModalBox{
    constructor(parentContainer, closeSpan, header, button){
        super(parentContainer, closeSpan, header)
        this.button = button;
        this.parameterConstant = null;
        this.header.innerText = "Better Board Navigator Help";
    }

    set eventParameter(parameter){
        this.parameterConstant = parameter;
    }

    setButtonEvent(eventFunction){
        this.buttonEvent = eventFunction;
        this.button.addEventListener("click", () => {
            this.buttonEvent(this.parameterConstant);
            this.close();
        });
    }

    close(){
        this.parentContainer.style.display = "none";
    }
}