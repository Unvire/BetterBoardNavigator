import { useState, useRef, useEffect, useCallback } from 'react';
import { useBoardStore } from '../../store/boardStore';
import { usePanZoom } from '../../hooks/usePanZoom';
import { useBoardGeometry } from '../../hooks/useBoardGeometry';
import { renderBoard } from './canvasRenderer';


const getComponentBounds = (comp: any) => {
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;

    if (comp.pins) {
      Object.values(comp.pins).forEach((pin: any) => {
        if (pin.coords) {
          minX = Math.min(minX, pin.coords.x);
          maxX = Math.max(maxX, pin.coords.x);
          minY = Math.min(minY, pin.coords.y);
          maxY = Math.max(maxY, pin.coords.y);
        }
      });
    }

    if (comp.coords && minX === Infinity) {
      minX = comp.coords.x;
      maxX = comp.coords.x;
      minY = comp.coords.y;
      maxY = comp.coords.y;
    }

    // Safety margin
    if (minX === maxX) { minX -= 0.1; maxX += 0.1; }
    if (minY === maxY) { minY -= 0.1; maxY += 0.1; }

    return minX !== Infinity ? { minX, maxX, minY, maxY } : null;
  };

  const transformBounds = (
    bounds: {minX: number, maxX: number, minY: number, maxY: number}, 
    rotation: number, isMirrored: boolean, cx: number, cy: number) => {

    const rad = (rotation * Math.PI) / 180;
    const cos = Math.cos(rad);
    const sin = Math.sin(rad);

    const transformPoint = (x: number, y: number) => {
      let nx = x, ny = y;
      if (rotation !== 0) {
        const dx = nx - cx;
        const dy = ny - cy;
        nx = dx * cos - dy * sin + cx;
        ny = dx * sin + dy * cos + cy;
      }
      if (isMirrored) nx = cx * 2 - nx;
      return { x: nx, y: ny };
    };

    const p1 = transformPoint(bounds.minX, bounds.minY);
    const p2 = transformPoint(bounds.maxX, bounds.minY);
    const p3 = transformPoint(bounds.maxX, bounds.maxY);
    const p4 = transformPoint(bounds.minX, bounds.maxY);

    return {
      tMinX: Math.min(p1.x, p2.x, p3.x, p4.x),
      tMaxX: Math.max(p1.x, p2.x, p3.x, p4.x),
      tMinY: Math.min(p1.y, p2.y, p3.y, p4.y),
      tMaxY: Math.max(p1.y, p2.y, p3.y, p4.y)
    };
  };



function BoardCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [canvasSize, setCanvasSize] = useState({ width: 0, height: 0 });
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        
        canvas.width = width;
        canvas.height = height;
        
        setCanvasSize({ width, height });
      }
    });

    resizeObserver.observe(canvas);
    return () => resizeObserver.disconnect();
  }, []);


  const [isSelectionMode, _] = useState(false);
  const [isHovering, setIsHovering] = useState(false);
  const hoverStateRef = useRef(false); 

  const store = useBoardStore();
  const isMirrored = store.mirrorState[store.currentSide];
  const { boardCenterX, boardCenterY, componentHitboxes } = useBoardGeometry(store.boardData, store.currentSide);


  const getHitboxCoords = useCallback((rawWx: number, rawWy: number) => {
    let wx = rawWx;
    let wy = rawWy;

    if (isMirrored) {
      wx = boardCenterX * 2 - wx;
    }

    if (store.rotation !== 0) {
      const rad = (-store.rotation * Math.PI) / 180;
      const dx = wx - boardCenterX;
      const dy = wy - boardCenterY;

      wx = dx * Math.cos(rad) - dy * Math.sin(rad) + boardCenterX;
      wy = dx * Math.sin(rad) + dy * Math.cos(rad) + boardCenterY;
    }

    return { wx, wy };
  }, [isMirrored, store.rotation, boardCenterX, boardCenterY]);


  // Click logic
  const handleCanvasClick = useCallback((rawWorldX: number, rawWorldY: number, isMultiSelect: boolean) => {
    if (!store.boardData) return;

    const { wx, wy } = getHitboxCoords(rawWorldX, rawWorldY);
    
    const clickedNames = componentHitboxes
      .filter(box => wx >= box.minX && wx <= box.maxX && wy >= box.minY && wy <= box.maxY)
      .map(box => box.name);

    if (clickedNames.length === 0) {
      if (!isMultiSelect) store.setInspectedComponents([]);
      return; 
    }

    const firstComp = store.boardData.components[clickedNames[0]];
    if (firstComp && firstComp.side !== store.currentSide && firstComp.mountingType !== 'TH') {
      store.setCurrentSide(firstComp.side);
    }

    if (isMultiSelect) {
      if (store.inspectedComponents.length > 0) store.setInspectedComponents([]);
      if (store.highlightedPrefix) store.setHighlightedPrefix(null);
      store.selectComponents(clickedNames, true);
    } else {
      store.setInspectedComponents(clickedNames);
    }
  }, [store, boardCenterX, componentHitboxes, getHitboxCoords]);


  // Camera
  const { scale, offset, handlers, resetView, focusOnBoundingBox } = usePanZoom(canvasRef, handleCanvasClick);


  // Auto focus
  useEffect(() => {
    if (!store.componentToFocus || !store.boardData) return;

    const comp = store.boardData.components[store.componentToFocus];
    if (comp) {
      const bounds = getComponentBounds(comp);
      
      if (bounds) {
        const { tMinX, tMaxX, tMinY, tMaxY } = transformBounds(
          bounds, 
          store.rotation, 
          isMirrored, 
          boardCenterX, 
          boardCenterY
        );
        focusOnBoundingBox(tMinX, tMaxX, tMinY, tMaxY);
      }
    }

    store.clearFocus();
    
  }, [store.componentToFocus, store.boardData, focusOnBoundingBox, isMirrored, boardCenterX, boardCenterY, store.rotation]);
  

  // Reset View
  useEffect(() => {
    if (store.boardData) resetView(store.boardData);
  }, [store.boardData, resetView]);
  

  // Rendering
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !store.boardData) return;
    
    if (canvas.parentElement) {
      canvas.width = canvas.parentElement.clientWidth;
      canvas.height = canvas.parentElement.clientHeight;
    }

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    renderBoard({
      ctx,
      boardData: store.boardData,
      scale,
      offset,
      boardCenterX,
      boardCenterY,
      rotation: store.rotation,
      isMirrored: isMirrored,
      isDarkMode: store.isDarkMode,
      showOutlines: store.showOutlines,
      currentSide: store.currentSide,
      selectedComponents: store.selectedComponents,
      inspectedComponents: store.inspectedComponents,
      selectedNet: store.selectedNet,
      highlightedPrefix: store.highlightedPrefix,
      showLabels: store.showLabels,
      componentHitboxes: componentHitboxes,
      partNumbers: store.partNumbers,
      highlightedPartNumber: store.highlightedPartNumber,
      hideUnassignedPNs: store.hideUnassignedPNs,
      hiddenComponents: store.hiddenComponents
    });
  }, [store, scale, offset, boardCenterX, boardCenterY, isMirrored, canvasSize]);


  // Mouse Clicking
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();

      // revert Camera offset and scale
      const rawWx = ((e.clientX - rect.left) - offset.x) / scale;
      const rawWy = ((e.clientY - rect.top) - offset.y) / scale;

      // revert mirroring and rotation
      const { wx, wy } = getHitboxCoords(rawWx, rawWy);

      const foundHover = componentHitboxes.some(box => 
        wx >= box.minX && wx <= box.maxX && 
        wy >= box.minY && wy <= box.maxY
      );

      if (foundHover !== hoverStateRef.current) {
        hoverStateRef.current = foundHover;
        setIsHovering(foundHover);
      }
    };

    canvas.addEventListener('mousemove', handleMouseMove);
    return () => canvas.removeEventListener('mousemove', handleMouseMove);
  }, [componentHitboxes, scale, offset, getHitboxCoords]);


  return (
    <div className="w-full h-full relative block overflow-hidden">
      <canvas 
        ref={canvasRef}
        {...handlers}
        className={`absolute inset-0 block w-full h-full touch-none active:cursor-grabbing ${
          isSelectionMode ? 'cursor-crosshair' : (isHovering ? 'cursor-pointer' : 'cursor-grab')
        }`}
      />
    </div>
  );
}

export default BoardCanvas;