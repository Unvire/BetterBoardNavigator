class EngineAdapter{
    static async resizeBoard(){
        setCanvasDimensions();
        side = currentSide();
        pyodide.runPythonAsync(`
            engine.changeScreenDimensionsInterface(SURFACE, [canvas.width, canvas.height], '${side}')
            pygame.display.flip()
        `);
    }

    static rotateBoard(){
        side = currentSide();
        pyodide.runPythonAsync(`
            engine.rotateBoardInterface(SURFACE, isClockwise=True, side='${side}', angleDeg=90)
            pygame.display.flip()
        `);
    }

    static findClickedComponents(x, y, isSelectionModeSingle){
    side = currentSide();
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
        
        side = currentSide();
        pyodide.runPythonAsync(`
        if engine:
            pointXY = [int('${x}'), int('${y}')]
            isScaleUp = '${isZoomIn}' == 'true'
            engine.scaleUpDownInterface(SURFACE, isScaleUp=isScaleUp, pointXY=pointXY, side='${side}')
            pygame.display.flip()
        `);
    }

    static changeSide(){
        changeSide();
        side = currentSide();
        pyodide.runPythonAsync(`
            engine.changeSideInterface(SURFACE, '${side}')
            pygame.display.flip()
        `);
    }

    static mirrorSide(){
        side = currentSide();
        pyodide.runPythonAsync(`
            engine.flipUnflipCurrentSideInterface(SURFACE, '${side}')
            pygame.display.flip()
        `);
    }

    static toggleOutlines(){
        side = currentSide();
        pyodide.runPythonAsync(`
            engine.showHideOutlinesInterface(SURFACE, '${side}')
            pygame.display.flip()
        `);
    }

    static resetView(){
        side = currentSide();
        pyodide.runPython(`
            engine.resetToDefaultViewInterface(SURFACE, '${side}')
            pygame.display.flip()
        `);
        WidgetAdapter.resetWidgets();
    }

    static areaFromComponents(){
        side = currentSide();
        pyodide.runPython(`
            engine.changeAreaInterface(SURFACE, '${side}')
            pygame.display.flip()
        `);
        WidgetAdapter.resetWidgets();
    }

    static async clearMarkers(){
        isSelectionModeSingle = true;
        side = currentSide();
        pyodide.runPython(`
            engine.clearFindComponentByNameInterface(SURFACE, '${side}')
            pygame.display.flip()
        `);
        WidgetAdapter.resetSelectedComponentsWidgets();
    }

    static componentInScreenCenter(componentName){
        const componentSide = _getSideOfComponent(componentName);
        side = _changeSideIfComponentIsNotOnScreen(componentSide);
    
        pyodide.runPython(`
            engine.componentInScreenCenterInterface(SURFACE, '${componentName}', '${side}')
            pygame.display.flip()
        `);
    }

    static selectNet(netName){
        side = currentSide();
        pyodide.runPython(`
            engine.selectNetByNameInterface(SURFACE, '${netName}', '${side}')
            pygame.display.flip()
        `);
    }

    static toggleNetMarkers(){
        side = currentSide();
        pyodide.runPython(`
            engine.showHideMarkersForSelectedNetByNameInterface(SURFACE, '${side}')
            pygame.display.flip()
        `);
    }

    static selectNetComponentByName(componentName, componentSide){
        pyodide.runPython(`
            engine.selectNetComponentByNameInterface(SURFACE, '${componentName}', '${componentSide}')
            pygame.display.flip()
        `);
    }

    static unselectNet(){
        side = currentSide();
        pyodide.runPython(`
            engine.unselectNetInterface(SURFACE, '${side}')
            pygame.display.flip()
        `);
    }

    static showCommonPrefixComponents(prefix){
        side = currentSide();
        pyodide.runPython(`
            isPrefixExist = engine.checkIfPrefixExists('${prefix}')

            if isPrefixExist:
                engine.showCommonTypeComponentsInterface(SURFACE, '${prefix}', '${side}')
                pygame.display.flip()
        `);
    }

    static hideCommonPrefixComponents(){
        side = currentSide();
        pyodide.runPython(`
            engine.clearCommonTypeComponentsInterface(SURFACE, '${side}')
            pygame.display.flip()
        `);
    }

    static findComponentByName(componentName, side, isSelectionModeSingle){
        const componentSide = _getSideOfComponent(componentName);
        if (!componentSide){
            return
        }
        side = _changeSideIfComponentIsNotOnScreen(componentSide);
        
        pyodide.runPython(`
            if '${isSelectionModeSingle}' == 'true':
                engine.clearFindComponentByNameInterface(SURFACE, '${side}')

            engine.findComponentByNameInterface(SURFACE, '${componentName}', '${side}')
            pygame.display.flip()
        `);
    }
}