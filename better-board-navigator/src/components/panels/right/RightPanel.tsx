import { useBoardStore } from '../../../store/boardStore';
import MultiSelectView from './MultiSelectView';
import InspectorView from './InspectorView';
import { Layers } from 'lucide-react';
import { useTranslation } from 'react-i18next';

export default function RightPanel() {  
  const { t } = useTranslation();

  const { selectedComponents, inspectedComponents, setInspectedComponents, isDarkMode } = useBoardStore();
  
  const selectedNames = Array.from(selectedComponents);
  const isPanelOpen = selectedNames.length > 0 || inspectedComponents.length > 0;
  
  let compToShow: string | null = null;
  if (inspectedComponents.length === 1) compToShow = inspectedComponents[0];
  else if (selectedNames.length === 1 && inspectedComponents.length === 0) compToShow = selectedNames[0];


  const glassPanelClass = `absolute top-16 bottom-4 right-4 w-72 rounded-xl border shadow-lg flex flex-col transition-transform duration-300 z-10 backdrop-blur-xl overflow-hidden ${
    isDarkMode ? 'bg-slate-900/85 border-slate-700 text-slate-300' : 'bg-white/95 border-slate-200 text-slate-700'
  }`;

  return (
    <aside className={glassPanelClass} style={{ transform: isPanelOpen ? 'translateX(0)' : 'translateX(120%)' }}>

      {selectedNames.length > 1 && inspectedComponents.length === 0 && (
        <MultiSelectView selectedNames={selectedNames} />
      )}

      {inspectedComponents.length > 1 && (
        <div className="flex flex-col h-full">
          <div className="p-3 border-b border-inherit shrink-0 flex items-center gap-2">
            <Layers size={20} className="text-cyan-500" />
            <h2 className="text-sm font-bold text-cyan-500">{`${t('rightpanel.multiple_components')}`} ({inspectedComponents.length})</h2>
          </div>
          <div className="p-3 text-xs opacity-75">
            {`${t('rightpanel.multiple_components_label')}`}
          </div>
          <div className="flex-1 overflow-y-auto p-2 space-y-1.5">
            {inspectedComponents.map(name => (
              <button 
                key={name}
                onClick={() => setInspectedComponents([name])}
                className={`w-full text-left p-2.5 rounded-md transition-colors border font-bold text-cyan-500 shadow-sm ${isDarkMode ? 'bg-cyan-900/20 border-cyan-800 hover:bg-cyan-900/40' : 'bg-cyan-50 border-cyan-200 hover:bg-cyan-100'}`}
              >
                {name}
              </button>
            ))}
          </div>
        </div>
      )}
      
      {compToShow && (
        <InspectorView compName={compToShow} isMultiSelected={selectedNames.length > 1 || inspectedComponents.length > 1} />
      )}
    </aside>
  );
}