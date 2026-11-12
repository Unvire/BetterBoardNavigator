import { useEffect } from 'react';
import { useBoardStore } from '../store/boardStore';

export function useKeyboardShortcuts() {
  const store = useBoardStore();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;


      switch (e.key.toLowerCase()) {
        case 'b':
          e.preventDefault();
          store.toggleLeftPanel();
          break;

        case ' ':
          e.preventDefault();
          store.setCurrentSide(store.currentSide === 'T' ? 'B' : 'T');
          break;

        case 'f':
          e.preventDefault();
          store.toggleMirror();
          break;

        case 'r':
          e.preventDefault();
          if (e.shiftKey) {
            store.setRotation(store.rotation === 0 ? 270 : store.rotation - 90);
          } else {
            store.setRotation(store.rotation + 90);
          }
          break;

        case 'l':
          e.preventDefault();
          store.toggleLabels();
          break;

        case 't':
          e.preventDefault();
          store.toggleDarkMode();
          break;

        case 'o':
          e.preventDefault();
          if (e.ctrlKey || e.metaKey) document.getElementById('cad-file-input')?.click();
          else store.toggleOutlines();
          break;

        case 'p':
          e.preventDefault();
          if (e.ctrlKey || e.metaKey) {
            document.getElementById('bom-file-input')?.click();
          };
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [store]);
}