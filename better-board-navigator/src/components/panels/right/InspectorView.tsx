import { useBoardStore } from '../../../store/boardStore';
import { X, ArrowLeft, Cpu } from 'lucide-react';
import { useTranslation } from 'react-i18next';

export default function InspectorView({ compName, isMultiSelected }: { compName: string, isMultiSelected: boolean }) {
  const { t } = useTranslation();
  const { boardData, isDarkMode, clearSelection, setInspectedComponents, selectedNet, selectNet, inspectedComponents, partNumbers, setHighlightedPartNumber } = useBoardStore();
  const component = boardData?.components[compName];

  if (!component) return null;

  return (
    <div className="flex flex-col h-full">
      <div className="flex flex-col p-3 border-b border-inherit shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            {isMultiSelected ? (
              <button 
                onClick={() => setInspectedComponents([])} 
                className={`p-1.5 -ml-1 rounded-md transition-colors ${inspectedComponents ? 'text-cyan-500 hover:bg-cyan-500/15' : 'text-rose-500 hover:bg-rose-500/15'}`}
                title={t('rightpanel.back_to_list')}
              >
                <ArrowLeft size={24} />
              </button>
            ) : (
              <Cpu size={24} className={inspectedComponents ? "text-cyan-500 dark:text-cyan-400" : "text-rose-500 dark:text-rose-400"}/>
            )}
            <h2 className={`text-lg font-bold ${inspectedComponents ? "text-cyan-500 dark:text-cyan-400" : "text-rose-500 dark:text-rose-400"}`}>
              {compName}
            </h2>
          </div>
          <button onClick={clearSelection} className="opacity-60 hover:opacity-100 transition-opacity"><X size={18}/></button>
        </div>
        <div className="text-xs opacity-70 mt-1 flex flex-col gap-0.5">
          <span>{t('rightpanel.type', { type: component.mountingType })} | {t('rightpanel.side', { side: component.side })}</span>
          
          {partNumbers?.[compName] && (
            <button 
              onClick={() => setHighlightedPartNumber(partNumbers[compName])}
              className="font-mono mt-1.5 px-2 py-1 rounded bg-slate-200/70 dark:bg-slate-800 text-left text-sm font-bold text-blue-600 dark:text-blue-400 hover:text-cyan-600 dark:hover:text-cyan-400 hover:bg-slate-300 dark:hover:bg-slate-700 transition-colors cursor-pointer w-fit"
              title={t('rightpanel.highlight_pn')}
            >
              {t('rightpanel.pn_prefix')} {partNumbers[compName]}
            </button>
          )}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto">
        <table className="w-full text-sm text-left">
          <thead className={`text-xs uppercase sticky top-0 ${isDarkMode ? 'bg-slate-900/95 text-slate-400' : 'bg-white/95 text-slate-500'}`}>
            <tr><th className="px-4 py-2 font-medium">{t('rightpanel.pin')}</th><th className="px-4 py-2 font-medium">{t('rightpanel.net')}</th></tr>
          </thead>
          <tbody>
            {component.pins ? Object.entries(component.pins).map(([pinName, pin]) => {
              const isNetSelected = pin.net !== undefined && pin.net === selectedNet;
              return (
                <tr 
                  key={pinName} 
                  onClick={() => pin.net && selectNet(isNetSelected ? null : pin.net)}
                  className={`border-b border-inherit transition-colors ${pin.net ? 'cursor-pointer' : ''} ${isNetSelected ? (isDarkMode ? 'bg-fuchsia-900/30' : 'bg-fuchsia-50') : (isDarkMode ? 'hover:bg-slate-800' : 'hover:bg-slate-50')}`}
                >
                  <td className={`px-4 py-2 font-mono ${isNetSelected ? 'font-bold text-fuchsia-400' : 'font-medium'}`}>{pinName}</td>
                  <td className={`px-4 py-2 font-semibold ${isNetSelected ? 'text-fuchsia-500' : 'text-indigo-600 dark:text-indigo-400'}`}>{pin.net || t('rightpanel.not_connected')}</td>
                </tr>
              );
            }) : (
              <tr><td colSpan={2} className="px-4 py-4 text-center opacity-50 text-xs">{t('rightpanel.no_pins')}</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}