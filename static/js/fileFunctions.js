async function openAndLoadCadFile(pyodide, file) {
    var fileName = `/${file.name}`;
    const reader = new FileReader(); 

    reader.onload = async (event) => {
        const fileContent = event.target.result;
        pyodide.FS.writeFile(fileName, new Uint8Array(fileContent));
        side = currentSide();

        await pyodide.runPython(`
            from boardWrapper import BoardWrapper
            from pygameDrawBoard import DrawBoardEngine

            cadFileName = '${fileName}'

            wrapper = BoardWrapper(canvas.width, canvas.height)
            wrapper.loadAndSetBoardFromFilePath(cadFileName)
            boardInstance = wrapper.normalizeBoard()

            pygame.init()
            pygame.display.set_caption('Better Board Navigator')

            SURFACE = pygame.display.set_mode((canvas.width, canvas.height))

            engine = DrawBoardEngine(canvas.width, canvas.height)
            engine.setBoardData(boardInstance)

            allComponents = engine.getComponents()
            netsDict = engine.getNets()

            engine.drawAndBlitInterface(SURFACE, '${side}')
            pygame.display.flip()
        `);
        let allComponents = pyodide.globals.get("allComponents").toJs();
        allComponentsList.elementsList = allComponents;
        allComponentsList.callbackEventFunction = selectComponentFromListEvent;
        allComponentsList.selectionMode = "single";
        allComponentsList.generateList();

        let netsMap = pyodide.globals.get("netsDict").toJs();
        netsTreeview.netEvent = selectNetFromTreeviewEvent;
        netsTreeview.componentEvent = selectNetComponentByNameEvent;
        netsTreeview.eventBeforeSelection = EngineAdapterEvents.unselectNet;
        netsTreeview.addBranches(netsMap);
        netsTreeview.generate();

        pinoutTable.clearBody();
        markedComponentsList.clearList();
        clickedComponentContainer.innerText = "";
        currentSideSpan.innerText = currentSide();
    }
    reader.readAsArrayBuffer(file);
}

async function removePreviousFileFromFS(pyodide, fileName){
    const pydodideFiles = pyodide.FS.readdir("/");
    if (pydodideFiles.includes(fileName)){
        pyodide.FS.unlink(`/${fileName}`);
    }
}