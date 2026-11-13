import { create } from 'zustand';
import type { BoardData } from '../types/board';

export type WorkerStatus = 'idle' | 'loading_pyodide' | 'processing' | 'error';

export interface BOMItem {
  partNumber: string;
  description?: string;
}


interface BoardState {
  workerStatus: WorkerStatus;
  setWorkerStatus: (status: WorkerStatus) => void;
  workerError: string | null;
  setWorkerError: (error: string | null) => void;

  boardData: BoardData | null;
  setBoardData: (data: BoardData) => void;

  isLeftPanelOpen: boolean;
  toggleLeftPanel: () => void;

  isDarkMode: boolean;
  toggleDarkMode: () => void;
  showOutlines: boolean;
  toggleOutlines: () => void;
  
  // --- CHANGE SIDE AND MIRROR SIDE ---
  currentSide: 'T' | 'B';
  setCurrentSide: (side: 'T' | 'B') => void;
  mirrorState: { T: boolean, B: boolean };
  toggleMirror: () => void;
  
  // --- ROTATION ---
  rotation: number;
  setRotation: (rotation: number) => void;

  // --- SELECTION ---
  selectedComponents: Set<string>;
  selectComponents: (names: string[], isMultiSelect?: boolean) => void;
  clearSelection: () => void;

  selectedNet: string | null;
  selectNet: (net: string | null) => void;

  // --- CAMERA / ZOOM ---
  componentToFocus: string | null;
  triggerFocus: (compName: string) => void;
  clearFocus: () => void;

  // --- 2ND SELECTION ---
  inspectedComponents: string[];
  setInspectedComponents: (names: string[]) => void;

  // --- COMPONENT TYPES ---
  highlightedPrefix: string | null;
  setHighlightedPrefix: (prefix: string | null) => void;

  // --- COMPONENT NAMES --- 
  showLabels: boolean;
  toggleLabels: () => void;

  // --- PART NUMBERS ---
  partNumbers: Record<string, BOMItem> | null;
  setPartNumbers: (data: Record<string, BOMItem> | null) => void;
  highlightedPartNumber: string | null;
  setHighlightedPartNumber: (pn: string | null) => void;
  hideUnassignedPNs: boolean;
  hiddenComponents: Set<string>;
  toggleHideUnassignedPNs: () => void;
  toggleComponentVisibility: (compName: string) => void;

  // --- MODALS ---
  isHelpOpen: boolean;
  toggleHelp: () => void;
}

export const useBoardStore = create<BoardState>((set) => ({
  workerStatus: 'idle', 
  workerError: null,

  boardData: null,
  isLeftPanelOpen: true,

  isDarkMode: true,
  showOutlines: true,
  
  currentSide: 'T',
  mirrorState: { T: false, B: true },
  rotation: 0,
  
  selectedComponents: new Set<string>(),
  selectedNet: null,
  componentToFocus: null,

  inspectedComponents: [],
  highlightedPrefix: null,

  showLabels: false,

  partNumbers:null,
  highlightedPartNumber: null,
  hideUnassignedPNs: false,
  hiddenComponents: new Set<string>(),

  isHelpOpen: false,


  setWorkerStatus: (status) => set({ workerStatus: status }), 
  setWorkerError: (error) => set({ workerError: error }),

  setBoardData: (data) => set({ 
    boardData: data,
    selectedComponents: new Set(),
    inspectedComponents: [],
    hiddenComponents: new Set(),
    selectedNet: null,
    highlightedPrefix: null,
    componentToFocus: null,
    currentSide: 'T'
  }),

  toggleLeftPanel: () => set((state) => ({ isLeftPanelOpen: !state.isLeftPanelOpen })),
  
  toggleDarkMode: () => set((state) => ({ isDarkMode: !state.isDarkMode })),
  
  toggleOutlines: () => set((state) => ({ showOutlines: !state.showOutlines })),
  
  setCurrentSide: (side) => set({ currentSide: side }),
  
  toggleMirror: () => set((state) => ({
    mirrorState: {
      ...state.mirrorState,
      [state.currentSide]: !state.mirrorState[state.currentSide]
    }
  })),

  setRotation: (rot) => set({ rotation: rot % 360 }),

  selectComponents: (names, isMultiSelect = false) => set((state) => {
    if (isMultiSelect) {
      const newSelection = new Set(state.selectedComponents);
      const allAlreadySelected = names.every(name => newSelection.has(name));
      
      names.forEach(name => {
        if (allAlreadySelected) newSelection.delete(name);
        else newSelection.add(name);
      });
      return { selectedComponents: newSelection };
    }
    return { selectedComponents: new Set(names) };
  }),

  clearSelection: () => set({ 
    selectedComponents: new Set(), 
    selectedNet: null,
    inspectedComponents: [],
    highlightedPrefix: null,
    highlightedPartNumber: null
  }),

  selectNet: (net) => set({ 
    selectedNet: net
  }),

  triggerFocus: (compName) => set({ componentToFocus: compName }),
  
  clearFocus: () => set({ componentToFocus: null }),

  setInspectedComponents: (names) => set({ 
    inspectedComponents: names, 
    highlightedPrefix: null,
    highlightedPartNumber: null,
  }),

  setHighlightedPrefix: (prefix) => set({ 
    highlightedPrefix: prefix,
    inspectedComponents: [],
    highlightedPartNumber: null
  }),

  toggleLabels: () => set((state) => ({ showLabels: !state.showLabels })),

  setPartNumbers: (data) => set(() => ({ 
    partNumbers: data,
    hideUnassignedPNs: data !== null ? true : false
  })),

  setHighlightedPartNumber: (pn) => set({ 
    highlightedPartNumber: pn,
    highlightedPrefix: null,
    inspectedComponents: []
  }),

  toggleHideUnassignedPNs: () => set((state) => ({ hideUnassignedPNs: !state.hideUnassignedPNs })),
  
  toggleComponentVisibility: (compName: string) => set((state) => {
    const newHidden = new Set(state.hiddenComponents);
    if (newHidden.has(compName)) {
      newHidden.delete(compName);
    } else {
      newHidden.add(compName);
    }
    
    const newSelected = new Set(state.selectedComponents);
    newSelected.delete(compName);
    const newInspected = state.inspectedComponents.filter(c => c !== compName);

    return { 
      hiddenComponents: newHidden,
      selectedComponents: newSelected,
      inspectedComponents: newInspected
    };
  }),

  toggleHelp: () => set((state) => ({ isHelpOpen: !state.isHelpOpen })),
}));