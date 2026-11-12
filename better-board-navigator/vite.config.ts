import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ command, mode }) => {
  return {
    plugins: [react()],
    // ZMIANA: Dodanie base path tylko dla wersji produkcyjnej (build)
    base: mode === 'production' ? '/BetterBoardNavigator/' : '/',
  };
});