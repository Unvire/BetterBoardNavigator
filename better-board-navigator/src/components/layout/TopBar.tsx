import { useRef } from 'react';
import { useBoardStore } from '../../store/boardStore';
import { 
  Upload, FlipHorizontal, RotateCw, RotateCcw, HelpCircle, Database,
  Layers, PanelLeftClose, PanelLeftOpen, Sun, Moon, Type, Loader2, SquareDashed,
  EyeOff, Eye
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useBoardWorker } from '../../hooks/useBoardWorker';
import LanguageSelector from './LanguageSelector';



export default function TopBar() {
  const { t } = useTranslation();

  const { 
    currentSide, setCurrentSide, 
    mirrorState, toggleMirror, 
    rotation, setRotation,
    showLabels, toggleLabels,
    isDarkMode, toggleDarkMode,
    isLeftPanelOpen, toggleLeftPanel,
    toggleOutlines,
    boardData,
    partNumbers,
    hideUnassignedPNs,
    toggleHideUnassignedPNs,
    isHelpOpen,
    toggleHelp
  } = useBoardStore();


  const { status, processFiles } = useBoardWorker(); 
  const fileInputRef = useRef<HTMLInputElement>(null);
  const bomInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      processFiles(e.target.files);
    }
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleBomUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const json = JSON.parse(event.target?.result as string);
        const normalizedBom: Record<string, { partNumber: string; description?: string }> = {};

        Object.entries(json).forEach(([comp, data]: [string, any]) => {
          if (typeof data === 'string') {
            normalizedBom[comp] = { partNumber: data };

          } else {
            normalizedBom[comp] = { 
              partNumber: data.partNumber || '', 
              description: data.description || '' 
            };
          }
        });
        useBoardStore.getState().setPartNumbers(normalizedBom);
      } catch (err) {
        console.error("Eror with parsing BOM JSON:", err);
      }
    };

    reader.readAsText(file);
    if (bomInputRef.current) bomInputRef.current.value = '';
  };

  
  const actionBtnClass = `p-2.5 rounded-lg transition-all flex items-center justify-center gap-1.5 font-medium text-sm
    ${isDarkMode 
      ? 'hover:bg-slate-700/80 text-slate-300 hover:text-white' 
      : 'hover:bg-slate-200/80 text-slate-600 hover:text-slate-900'}`;


  const toolGroupClass = `flex items-center p-1 rounded-xl border shadow-sm transition-colors
    ${isDarkMode ? 'bg-slate-900/50 border-slate-700/50' : 'bg-slate-200/50 border-slate-300/50'}`;

  return (
    <header className={`absolute top-0 left-0 right-0 h-14 px-4 flex items-center justify-between z-20 backdrop-blur-md border-b shadow-sm transition-colors ${isDarkMode ? 'bg-slate-900/85 border-slate-800 text-slate-200' : 'bg-slate-50/90 border-slate-200 text-slate-800'}`}>
      
      {/* 1. LEFT: UI & Branding */}
      <div className="flex items-center gap-4 flex-1">
        <button onClick={toggleLeftPanel} className={actionBtnClass} title={`${t('topbar.toggle_sidebar')} [B]`}>
          {isLeftPanelOpen ? <PanelLeftClose size={22}/> : <PanelLeftOpen size={22}/>}
        </button>
        <div className="font-bold text-lg flex items-center gap-2 tracking-tight select-none cursor-default">
          <span className="text-blue-500">Better</span> Board Navigator
        </div>
      </div>

      {/* 2. MIDDLE - TOOLS*/}
      <div className="flex items-center justify-center gap-4 flex-1">
        <div className={toolGroupClass}>
          <button 
            onClick={() => setCurrentSide(currentSide === 'T' ? 'B' : 'T')} 
            className={`${actionBtnClass} w-16`} 
            title={`${t('topbar.switch_side')} [Space]`}
          >
            <Layers size={20} className={currentSide === 'B' ? "text-amber-500" : "text-blue-500"}/>
            <span className="font-bold">{currentSide}</span>
          </button>

          <div className="w-px h-6 bg-slate-300 dark:bg-slate-600 mx-2"></div>
          
          <button onClick={toggleMirror} className={actionBtnClass} title={`${t('topbar.flip')} [F]`}>
            <FlipHorizontal size={20} className={mirrorState[currentSide] ? "text-blue-500" : "opacity-70"} />
          </button>
        </div>

        <div className={toolGroupClass}>
          <button onClick={() => setRotation(rotation === 0 ? 270 : rotation - 90)} className={actionBtnClass} title={`${t('topbar.rotate_left')} [Shift+R]`}>
            <RotateCcw size={20} className="opacity-70" />
          </button>

          <button onClick={() => setRotation(rotation + 90)} className={actionBtnClass} title={`${t('topbar.rotate_right')} [R]`}>
            <RotateCw size={20} className="opacity-70" />
          </button>
        </div>

        <div className={toolGroupClass}>
          <button onClick={toggleOutlines} className={actionBtnClass} title={`${t('topbar.toggle_outlines')} [O]`}>
            <SquareDashed size={20} />
          </button>

          <div className="w-px h-6 bg-slate-300 dark:bg-slate-600 mx-2"></div>

          <button onClick={toggleLabels} className={actionBtnClass} title={`${t('topbar.toggle_labels')} [L]`}>
            <Type size={20} className={showLabels ? "text-blue-500" : "opacity-70"} />
          </button>
        </div>
      </div>

      {/* 3. RIGHT - GLOBAL SETTINGS AND FILE LOADER*/}
      <div className="flex items-center justify-end gap-1 flex-1">
        
        <input type="file" id="cad-file-input" ref={fileInputRef} className="hidden" accept=".tgz,.gcd,.cad,.zip" onChange={handleFileUpload}/>
        <input type="file" id="bom-file-input" ref={bomInputRef} className="hidden" accept=".json" onChange={handleBomUpload} />

        <button 
          onClick={() => fileInputRef.current?.click()}
          disabled={status !== 'idle'} 
          className={`${actionBtnClass} ${status !== 'idle' ? 'opacity-50 cursor-not-allowed' : ''}`} 
          title={`${t('topbar.load_file')} [Ctrl+O]`}
        >
          {status !== 'idle' ? <Loader2 size={20} className="animate-spin text-blue-500" /> : <Upload size={20} />}
        </button>

        <div className="w-px h-6 bg-slate-300 dark:bg-slate-600 mx-2"></div>

        <button 
          onClick={() => bomInputRef.current?.click()}
          disabled={!boardData}
          className={`${actionBtnClass} ${!boardData ? 'opacity-50 cursor-not-allowed' : ''}`} 
          title={`${t('topbar.load_bom')} [Ctrl+P]`}
        >
          <Database size={20} className={partNumbers ? "text-cyan-500" : ""} />
        </button>

        <button 
          onClick={toggleHideUnassignedPNs}
          disabled={!boardData || !partNumbers}
          className={`${actionBtnClass} ${(!boardData || !partNumbers) ? 'opacity-50 cursor-not-allowed' : ''}`}
          title={`${t('topbar.hide_comps_no_bom')}`}
        >
          {hideUnassignedPNs 
            ? <EyeOff size={20} className="text-cyan-500" /> 
            : <Eye size={20} />
          }
        </button>
        
        <div className="w-px h-6 bg-slate-300 dark:bg-slate-600 mx-2"></div>
        
        <LanguageSelector actionBtnClass={actionBtnClass} />
        
        <button onClick={toggleDarkMode} className={actionBtnClass} title={`${t('topbar.theme')} [T]`}>
          {isDarkMode ? <Sun size={20} className="text-amber-400" /> : <Moon size={20} />}
        </button>
        <button onClick={toggleHelp} className={actionBtnClass} title={`${t('topbar.help')}`}>
          <HelpCircle size={20} className={isHelpOpen ? "text-cyan-500" : ""} />
        </button>
      </div>

    </header>
  );
}