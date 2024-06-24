class SideHandler{
    constructor(){
        this.isSideBottom = true;
        this.sideMap = {true: "B", false: "T"};
    }

    currentSide(){
        return this.sideMap[this.isSideBottom];
    }

    changeSide(){            
        this.isSideBottom = !(this.isSideBottom);

        const currentSideSpan = globalInstancesMap.getCurrentSideSpan();
        currentSideSpan.innerText = this.currentSide();
        
        return this.currentSide();
    }

    getSideOfComponent(componentName){
        pyodide.runPython(`
            componentSide = engine.getSideOfComponent('${componentName}')
        `);
        return pyodide.globals.get("componentSide");
    }

    setComponentSideAsCurrentSide(componentName){
        const componentSide = this.getSideOfComponent(componentName);
        if (componentSide != this.currentSide()){
            return this.changeSide();
        }
        return this.currentSide();
    }
}