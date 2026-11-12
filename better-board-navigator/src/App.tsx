import { useEffect } from 'react';
import { useBoardStore } from './store/boardStore';
import BoardCanvas from './components/canvas/BoardCanvas'; 
import TopBar from './components/layout/TopBar';
import LeftPanel from './components/panels/left/LeftPanel';
import RightPanel from './components/panels/right/RightPanel';
import { Layers, Cpu, AlertTriangle } from 'lucide-react';
import { useKeyboardShortcuts } from './hooks/useKeyboardShortcuts';
import { useTranslation } from 'react-i18next';
import HelpModal from './components/modals/HelpModal';


function App() {
  const { t } = useTranslation();
  
  const { 
    boardData, isDarkMode,
    workerStatus, workerError
  } = useBoardStore();


  useKeyboardShortcuts();


  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        const state = useBoardStore.getState();
        
        if (state.inspectedComponents.length > 0) {
          state.setInspectedComponents([]);
        } else if (state.selectedNet || state.selectedComponents.size > 0 || state.highlightedPrefix) {
          state.clearSelection();
        }
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);


  return (
    <div className={`relative w-screen h-screen overflow-hidden transition-colors duration-500 ${isDarkMode ? 'dark bg-slate-950 text-slate-200' : 'bg-slate-100 text-slate-800'}`}>

      {/* LAYER 0: CANVAS - background */}
      <div className="absolute inset-0 z-0">
        {boardData ? (
          <BoardCanvas />
        ) : (
          <div className="flex flex-col items-center justify-center w-full h-full select-none">
            <Cpu size={80} className="mb-6 opacity-30 text-blue-500" />
            <h1 className={`text-3xl font-bold tracking-tight mb-3 transition-colors duration-500 ${isDarkMode ? 'text-slate-300' : 'text-slate-600'}`}>
              Better Board Navigator
            </h1>
            <p className={`text-lg transition-colors duration-500 ${isDarkMode ? 'text-slate-500' : 'text-slate-400'}`}>
              {`${t('main_screen.init_message')}`}
            </p>
          </div>
        )}
      </div>

      {/* LAYER 1: FLOATING UI */}
      <TopBar/>
      {boardData && <LeftPanel/>}
      {boardData && <RightPanel />}

      {/* LAYER 2: LOADING OVERLAY */}
      {(workerStatus === 'loading_pyodide' || workerStatus === 'processing') && (
        <div className="absolute inset-0 z-50 flex items-center justify-center bg-slate-900/40 dark:bg-slate-950/70 backdrop-blur-sm transition-colors duration-500">
          <div className="flex flex-col items-center p-8 bg-white dark:bg-slate-800 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-700 transition-colors duration-500">
            <Layers className="animate-spin text-blue-500 mb-5" size={48} />
            <h2 className="text-xl font-bold mb-2 text-slate-800 dark:text-slate-100 transition-colors duration-500">
              {workerStatus === 'loading_pyodide' 
                ? `${t('main_screen.init_pyodide')}`
                : `${t('main_screen.parsing_cad_files')}`}
            </h2>
            <p className="text-sm text-slate-500 dark:text-slate-400 transition-colors duration-500">
              {`${t('main_screen.waiting')}`}
            </p>
          </div>
        </div>
      )}

      {/* LAYER 3: ERRORS */}
      {workerStatus === 'error' && workerError && (
        <div className="absolute bottom-6 right-6 z-50 max-w-sm bg-rose-500 text-white p-4 rounded-xl shadow-lg flex items-start gap-3 animate-in slide-in-from-bottom-5">
          <AlertTriangle size={24} className="shrink-0" />
          <div>
            <h3 className="font-bold">{`${t('main_screen.parsing')}`}</h3>
            <p className="text-sm opacity-90 mt-1">{workerError}</p>
          </div>
        </div>
      )}

      {/* LAYER 4: MODALS */}
      <HelpModal />

    </div>
  );
}

export default App;