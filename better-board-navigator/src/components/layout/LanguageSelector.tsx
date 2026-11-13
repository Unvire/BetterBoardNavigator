import { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Globe } from 'lucide-react';
import { useBoardStore } from '../../store/boardStore';

const SUPPORTED_LANGUAGES = [
  { code: 'en', label: 'English' },
  { code: 'pl', label: 'Polski' }
];

interface LanguageSelectorProps {
  actionBtnClass: string;
}

export default function LanguageSelector({ actionBtnClass }: LanguageSelectorProps) {
  const { t, i18n } = useTranslation();
  const { isDarkMode } = useBoardStore();
  
  const [isOpen, setIsOpen] = useState(false);
  
  const menuRef = useRef<HTMLDivElement>(null);


  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="relative" ref={menuRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={actionBtnClass}
        title={t('topbar.language')}
      >
        <Globe size={18} className="opacity-70" />
        <span className="font-bold text-xs">{i18n.language.substring(0, 2).toUpperCase()}</span>
      </button>

      {isOpen && (
        <div className={`absolute right-0 mt-2 py-1 w-32 max-h-60 overflow-y-auto rounded-lg shadow-lg border z-50 transition-colors ${
          isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'
        }`}>
          {SUPPORTED_LANGUAGES.map((lang) => {
            const isActive = i18n.language.startsWith(lang.code);
            return (
              <button
                key={lang.code}
                onClick={() => {
                  i18n.changeLanguage(lang.code);
                  setIsOpen(false);
                }}
                className={`w-full text-left px-4 py-2 text-sm transition-colors ${
                  isActive
                    ? (isDarkMode ? 'bg-cyan-900/40 text-cyan-400 font-bold' : 'bg-cyan-50 text-cyan-700 font-bold')
                    : (isDarkMode ? 'text-slate-300 hover:bg-slate-700' : 'text-slate-600 hover:bg-slate-100')
                }`}
              >
                {lang.label}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}