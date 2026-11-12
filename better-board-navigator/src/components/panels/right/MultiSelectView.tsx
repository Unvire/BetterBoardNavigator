import { useBoardStore } from '../../../store/boardStore';
import { X, ChevronRight } from 'lucide-react';
import { useTranslation } from 'react-i18next';

export default function MultiSelectView({ selectedNames }: { selectedNames: string[] }) {
  const { t } = useTranslation();
  const { clearSelection, setInspectedComponents, triggerFocus, selectComponents, boardData, isDarkMode, partNumbers } = useBoardStore();

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between p-3 border-b border-inherit shrink-0">
        <h2 className="text-sm font-bold text-amber-500">{t('rightpanel.selected_count', { count: selectedNames.length })}</h2>
        <button onClick={clearSelection} className="opacity-60 hover:opacity-100"><X size={18}/></button>
      </div>
      <div className="p-3 text-xs opacity-75">
        {t('rightpanel.click_to_view_pins')}
      </div>
      <div className="flex-1 overflow-y-auto p-2 space-y-1.5">
        {selectedNames.map(name => (
          <div key={name} className={`group flex items-stretch w-full rounded-md border transition-all ${isDarkMode ? 'bg-slate-800/50 border-slate-700' : 'bg-white border-slate-200 shadow-sm'}`}>
            <button 
              onClick={() => { setInspectedComponents([name]); triggerFocus(name); }}
              className="flex-1 flex justify-between items-center text-left p-2.5 pl-3 transition-colors rounded-l-md hover:bg-blue-500/10"
              title={t('rightpanel.show_pins_tooltip')}
            >
              <div className="flex flex-col">
                <span className="font-bold text-blue-500 block leading-tight">{name}</span>
                <div className="flex items-center gap-2 mt-0.5">
                  <span className="text-xs opacity-60">{t('rightpanel.side', { side: boardData?.components[name]?.side })}</span>
                  
                  {partNumbers?.[name] && (
                    <span className="text-[10px] font-mono px-1.5 bg-slate-200 dark:bg-slate-700 rounded opacity-75">
                      {partNumbers[name]}
                    </span>
                  )}
                  
                </div>
              </div>
              <ChevronRight size={16} className="text-blue-500/50 opacity-0 group-hover:opacity-100 transition-opacity -mr-1" />
            </button>
            <div className={`w-px my-2 ${isDarkMode ? 'bg-slate-700' : 'bg-slate-100'}`}></div>
            <button
              onClick={() => selectComponents([name], true)} 
              className={`px-3 flex items-center justify-center rounded-r-md transition-colors ${isDarkMode ? 'text-slate-500 hover:text-rose-400 hover:bg-rose-500/10' : 'text-slate-300 hover:text-rose-500 hover:bg-rose-50'}`}
              title={t('rightpanel.deselect_component')}
            >
              <X size={14} className="stroke-[2.5]" />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}