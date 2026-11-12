import { useMemo } from 'react';
import { useBoardStore } from '../../../store/boardStore';
import { X } from 'lucide-react';
import { useTranslation } from 'react-i18next';

export default function GroupList({ searchQuery }: { searchQuery: string }) {
  const { t } = useTranslation();
  const { boardData, isDarkMode, highlightedPrefix, setHighlightedPrefix } = useBoardStore();

  const groups = useMemo(() => {
    if (!boardData) return [];
    
    const counts: Record<string, number> = {};
    
    Object.keys(boardData.components).forEach(name => {
      const match = name.match(/^[a-zA-Z]+/);
      const prefix = match ? match[0].toUpperCase() : '#';
      counts[prefix] = (counts[prefix] || 0) + 1;
    });

    
    const q = searchQuery.toLowerCase();
    return Object.entries(counts)
      .filter(([prefix]) => prefix.toLowerCase().includes(q))
      .sort((a, b) => a[0].localeCompare(b[0]));
  }, [boardData, searchQuery]);


  if (groups.length === 0) {
    return <div className="px-3 py-2 text-center opacity-50 text-xs">Brak wyników</div>;
  }

  
  return (
    <ul className="text-sm space-y-0.5">
      {groups.map(([prefix, count]) => {
        const isSelected = highlightedPrefix === prefix;

        return (
          <li 
            key={prefix} 
            onClick={() => setHighlightedPrefix(isSelected ? null : prefix)}
            className={`px-3 py-1.5 rounded-md cursor-pointer transition-all flex items-center justify-between ${
              isSelected
                ? (isDarkMode 
                    ? 'bg-cyan-900/40 text-cyan-300 font-bold border border-cyan-500/50 shadow-[0_0_10px_rgba(6,182,212,0.2)]' 
                    : 'bg-cyan-50 text-cyan-700 font-bold border border-cyan-400 shadow-sm')
                : (isDarkMode 
                    ? 'border border-transparent hover:bg-slate-800 text-slate-300' 
                    : 'border border-transparent hover:bg-slate-200/70 text-slate-700')
            }`}
          >
            <div className="flex items-center gap-2">
              <span>{t('leftpanel.group')} <span className={isSelected ? "" : "font-semibold"}>{prefix}</span></span>
              <span className={`text-xs px-1.5 py-0.5 rounded-full ${isDarkMode ? 'bg-slate-800' : 'bg-slate-200'} opacity-80`}>
                {count}
              </span>
            </div>
            
            {isSelected && (
              <button 
                onClick={(e) => { e.stopPropagation(); setHighlightedPrefix(null); }}
                className="opacity-60 hover:opacity-100 p-0.5 rounded-full hover:bg-cyan-500/20 ml-2 shrink-0"
                title={t('leftpanel.deselect_group')}
              >
                <X size={14}/>
              </button>
            )}
          </li>
        );
      })}
    </ul>
  );
}