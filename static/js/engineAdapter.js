class EngineAdapter{
    static async resizeBoard(){
        setCanvasDimensions();
        const side = sideHandler.currentSide();
        pyodide.runPythonAsync(`
            engine.changeScreenDimensionsInterface(SURFACE, [canvas.width, canvas.height], '${side}')
            pygame.display.flip()
        `);
    }

    static rotateBoard(){
        const side = sideHandler.currentSide();
        pyodide.runPythonAsync(`
            engine.rotateBoardInterface(SURFACE, isClockwise=True, side='${side}', angleDeg=90)
            pygame.display.flip()
        `);
    }

    static findClickedComponents(x, y, isSelectionModeSingle){
        const side = sideHandler.currentSide();
        pyodide.runPython(`
            clickedXY = [int('${x}'), int('${y}')]
            clickedComponents = engine.findComponentByClick(clickedXY, '${side}')
            
            if '${isSelectionModeSingle}' == 'false':
                for componentName in clickedComponents:
                    engine.findComponentByNameInterface(SURFACE, componentName, '${side}') #mark all clicked components
                    pygame.display.flip()
        `);
        return pyodide.globals.get("clickedComponents").toJs();
    }

    static moveBoard(x, y){
        pyodide.runPythonAsync(`
            if engine:
                deltaVector = [int('${x}'), int('${y}')]
                engine.moveBoardInterface(SURFACE, deltaVector)
                pygame.display.flip()
        `);
    }

    static zoomInOut(event){
        const x = event.offsetX; 
        const y = event.offsetY;
        const isZoomIn = event.deltaY < 0
        
        const side = sideHandler.currentSide();
        pyodide.runPythonAsync(`
        if engine:
            pointXY = [int('${x}'), int('${y}')]
            isScaleUp = '${isZoomIn}' == 'true'
            engine.scaleUpDownInterface(SURFACE, isScaleUp=isScaleUp, pointXY=pointXY, side='${side}')
            pygame.display.flip()
        `);
    }

    static changeSide(){
        const side = sideHandler.changeSide();
        pyodide.runPythonAsync(`
            engine.changeSideInterface(SURFACE, '${side}')
            pygame.display.flip()
        `);
    }

    static mirrorSide(){
        const side = sideHandler.currentSide();
        pyodide.runPythonAsync(`
            engine.flipUnflipCurrentSideInterface(SURFACE, '${side}')
            pygame.display.flip()
        `);
    }

    static toggleOutlines(){
        const side = sideHandler.currentSide();
        pyodide.runPythonAsync(`
            engine.showHideOutlinesInterface(SURFACE, '${side}')
            pygame.display.flip()
        `);
    }

    static resetView(){
        const side = sideHandler.currentSide();
        pyodide.runPython(`
            engine.resetToDefaultViewInterface(SURFACE, '${side}')
            pygame.display.flip()
        `);
        WidgetAdapter.resetWidgets();
    }

    static areaFromComponents(){
        const side = sideHandler.currentSide();
        pyodide.runPython(`
            engine.changeAreaInterface(SURFACE, '${side}')
            pygame.display.flip()
        `);
        WidgetAdapter.resetWidgets();
    }

    static async clearMarkers(){
        isSelectionModeSingle = true;

        const side = sideHandler.currentSide();
        pyodide.runPython(`
            engine.clearFindComponentByNameInterface(SURFACE, '${side}')
            pygame.display.flip()
        `);
        WidgetAdapter.resetSelectedComponentsWidgets();
    }

    static componentInScreenCenter(componentName){
        const side = sideHandler.setComponentSideAsCurrentSide(componentName);
        pyodide.runPython(`
            engine.componentInScreenCenterInterface(SURFACE, '${componentName}', '${side}')
            pygame.display.flip()
        `);
    }

    static selectNet(netName){
        const side = sideHandler.currentSide();
        pyodide.runPython(`
            engine.selectNetByNameInterface(SURFACE, '${netName}', '${side}')
            pygame.display.flip()
        `);
    }

    static toggleNetMarkers(){
        const side = sideHandler.currentSide();
        pyodide.runPython(`
            engine.showHideMarkersForSelectedNetByNameInterface(SURFACE, '${side}')
            pygame.display.flip()
        `);
    }

    static selectNetComponentByName(componentName){
        const side = sideHandler.setComponentSideAsCurrentSide(componentName);
        pyodide.runPython(`
            engine.selectNetComponentByNameInterface(SURFACE, '${componentName}', '${side}')
            pygame.display.flip()
        `);
    }

    static unselectNet(){
        const side = sideHandler.currentSide();
        pyodide.runPython(`
            engine.unselectNetInterface(SURFACE, '${side}')
            pygame.display.flip()
        `);
    }

    static showCommonPrefixComponents(prefix){
        const side = sideHandler.currentSide();
        pyodide.runPython(`
            isPrefixExist = engine.checkIfPrefixExists('${prefix}')

            if isPrefixExist:
                engine.showCommonTypeComponentsInterface(SURFACE, '${prefix}', '${side}')
                pygame.display.flip()
        `);
    }

    static hideCommonPrefixComponents(){
        const side = sideHandler.currentSide();
        pyodide.runPython(`
            engine.clearCommonTypeComponentsInterface(SURFACE, '${side}')
            pygame.display.flip()
        `);
    }

    static findComponentByName(componentName, isSelectionModeSingle){
        const componentSide = sideHandler.getSideOfComponent(componentName);
        if (!componentSide){
            return
        }
        
        const side = sideHandler.setComponentSideAsCurrentSide(componentName);
        pyodide.runPython(`
            if '${isSelectionModeSingle}' == 'true':
                engine.clearFindComponentByNameInterface(SURFACE, '${side}')

            engine.findComponentByNameInterface(SURFACE, '${componentName}', '${side}')
            pygame.display.flip()
        `);
    }
}