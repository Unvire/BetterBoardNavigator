import { useEffect } from 'react';
import { useBoardStore } from '../../store/boardStore';
import { X, Mouse, Keyboard } from 'lucide-react';
import { useTranslation } from 'react-i18next';


export default function HelpModal() {
  const { t } = useTranslation();
  const { isHelpOpen, toggleHelp, isDarkMode } = useBoardStore();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isHelpOpen) {
        toggleHelp();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isHelpOpen, toggleHelp]);

  if (!isHelpOpen) return null;

  const kbdClass = `inline-block px-1.5 py-0.5 mx-0.5 text-[11px] font-mono font-bold border rounded shadow-sm ${
    isDarkMode ? 'bg-slate-800 border-slate-600 text-slate-200' : 'bg-slate-100 border-slate-300 text-slate-700'
  }`;

  return (
    <div 
      className="absolute inset-0 z-50 flex items-center justify-center bg-slate-900/40 dark:bg-slate-950/70 backdrop-blur-sm transition-all"
      onClick={toggleHelp}
    >
      <div 
        onClick={(e) => e.stopPropagation()}
        className={`relative w-full max-w-2xl max-h-[80vh] flex flex-col rounded-2xl shadow-2xl border overflow-hidden animate-in fade-in zoom-in-95 duration-200 ${
          isDarkMode ? 'bg-slate-900 border-slate-700 text-slate-200' : 'bg-white border-slate-200 text-slate-800'
        }`}
      >
        {/* HEADER */}
        <div className="flex items-center justify-between p-5 border-b border-inherit shrink-0">
          <h2 className="text-xl font-bold flex items-center gap-2">
            <span className="text-blue-500">BBN</span> {t('help.title')}
          </h2>
          <button 
            onClick={toggleHelp} 
            className="p-1.5 rounded-md opacity-60 hover:opacity-100 hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* CONTENT */}
        <div className="p-6 overflow-y-auto space-y-6 text-sm">
          
          <section>
            <h3 className="font-bold text-lg mb-3 flex items-center gap-2 text-cyan-600 dark:text-cyan-400">
              <Mouse size={18} /> {t('help.mouse_controls')}
            </h3>
            <ul className="space-y-2.5 opacity-90">
              <li><kbd className={kbdClass}>{t('help.keys.left_click')}</kbd> - {t('help.desc.inspect')}</li>
              <li><kbd className={kbdClass}>Ctrl</kbd> + <kbd className={kbdClass}>{t('help.keys.left_click')}</kbd> - {t('help.desc.multiselect')}</li>
              <li><kbd className={kbdClass}>{t('help.keys.drag')}</kbd> - {t('help.desc.pan')}</li>
              <li><kbd className={kbdClass}>{t('help.keys.scroll')}</kbd> - {t('help.desc.zoom')}</li>
            </ul>
          </section>

          <section>
            <h3 className="font-bold text-lg mb-3 flex items-center gap-2 text-cyan-600 dark:text-cyan-400">
              <Keyboard size={18} /> {t('help.keyboard_shortcuts')}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 opacity-90">
              <ul className="space-y-2.5">
                <li><kbd className={kbdClass}>Ctrl</kbd> + <kbd className={kbdClass}>O</kbd> - {t('help.desc.load_cad')}</li>
                <li><kbd className={kbdClass}>Ctrl</kbd> + <kbd className={kbdClass}>P</kbd> - {t('help.desc.load_bom')}</li>
                <li><kbd className={kbdClass}>Space</kbd> - {t('help.desc.switch_side')}</li>
                <li><kbd className={kbdClass}>F</kbd> - {t('help.desc.flip')}</li>
              </ul>
              <ul className="space-y-2.5">
                <li><kbd className={kbdClass}>R</kbd> - {t('help.desc.rotate_cw')}</li>
                <li><kbd className={kbdClass}>Shift</kbd> + <kbd className={kbdClass}>R</kbd> - {t('help.desc.rotate_ccw')}</li>
                <li><kbd className={kbdClass}>L</kbd> - {t('help.desc.labels')}</li>
                <li><kbd className={kbdClass}>Esc</kbd> - {t('help.desc.clear_selection')}</li>
              </ul>
            </div>
          </section>

        </div>
      </div>
    </div>
  );
}