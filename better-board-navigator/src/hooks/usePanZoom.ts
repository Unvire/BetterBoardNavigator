import { useState, useCallback, useEffect, useRef } from "react";
import type { RefObject } from "react";


export function usePanZoom(
  canvasRef: RefObject<HTMLCanvasElement | null>,
  onCanvasClick?: (worldX: number, worldY: number, isMultiSelect: boolean) => void
) {
  const [scale, setScale] = useState(1);
  const [offset, setOffset] = useState({ x: 0, y: 0 });

  const [isDragging, setIsDragging] = useState(false);
  const [lastMousePos, setLastMousePos] = useState({ x: 0, y: 0 });

  const [mouseDownPos, setMouseDownPos] = useState({ x: 0, y: 0 });

  // storing offset and scale values for synchronus operations
  const scaleRef = useRef(scale);
  useEffect(() => { 
    scaleRef.current = scale; 
  }, [scale]);

  const offsetRef = useRef(offset);
  useEffect(() => { 
    offsetRef.current = offset; 
  }, [offset]);



  const onMouseDown = useCallback((e: React.MouseEvent) => {
    setIsDragging(true);
    setLastMousePos({ x: e.clientX, y: e.clientY });
    setMouseDownPos({ x: e.clientX, y: e.clientY });
  }, []);


  const onMouseMove = useCallback((e: React.MouseEvent) => {
    if (!isDragging) return;

    const dx = e.clientX - lastMousePos.x;
    const dy = e.clientY - lastMousePos.y;

    setOffset((prev) => ({ x: prev.x + dx, y: prev.y + dy }));
    setLastMousePos({ x: e.clientX, y: e.clientY });
  }, [isDragging, lastMousePos]);


  const onMouseUp = useCallback((e: React.MouseEvent) => {
    setIsDragging(false);

    const dx = Math.abs(e.clientX - mouseDownPos.x);
    const dy = Math.abs(e.clientY - mouseDownPos.y);

    // calculate world (board) XY when mouse was moved less than 3px relative to previous position
    if (dx < 3 && dy < 3 && canvasRef.current) {
      const rect = canvasRef.current.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      const worldX = (mouseX - offsetRef.current.x) / scaleRef.current;
      const worldY = (mouseY - offsetRef.current.y) / scaleRef.current;
			
      const isMultiSelect = e.ctrlKey || e.metaKey;
      onCanvasClick?.(worldX, worldY,isMultiSelect);
    }
  }, [mouseDownPos, canvasRef, onCanvasClick]);


  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const handleWheel = (e: WheelEvent) => {
      e.preventDefault();

      const zoomSensitivity = 0.1;
      const zoomFactor = e.deltaY < 0 ? 1 + zoomSensitivity : 1 - zoomSensitivity;
      
      const prevScale = scaleRef.current;
      const prevOffset = offsetRef.current;

      const newScale = prevScale * zoomFactor;
      if (newScale < 0.0001 || newScale > 1000000) return;

      const rect = canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;
			
      // zooming on cursor position
      const newOffsetX = mouseX - (mouseX - prevOffset.x) * zoomFactor;
      const newOffsetY = mouseY - (mouseY - prevOffset.y) * zoomFactor;

      setScale(newScale);
      setOffset({ x: newOffsetX, y: newOffsetY });
    };

    canvas.addEventListener('wheel', handleWheel, { passive: false });
    return () => canvas.removeEventListener('wheel', handleWheel);
  }, [canvasRef]);


  const resetView = useCallback((boardData: any) => {
    const canvas = canvasRef.current;
    if (!canvas || !boardData) return;

    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;

    const expandBoundingBox = (x: number, y: number) => {
      if (x < minX) minX = x;
      if (x > maxX) maxX = x;
      if (y < minY) minY = y;
      if (y > maxY) maxY = y;
    };

    if (boardData.area && boardData.area.length > 0) {
      boardData.area.forEach((point: any) => expandBoundingBox(point.x, point.y));
    } else {
      Object.values(boardData.components).forEach((comp: any) => {
        if (comp.coords) expandBoundingBox(comp.coords.x, comp.coords.y);
      });
    }

    if (minX === Infinity) { minX = 0; maxX = 100; minY = 0; maxY = 100; }

    const boardWidth = maxX - minX;
    const boardHeight = maxY - minY;

    const canvasWidth = canvas.clientWidth;
    const canvasHeight = canvas.clientHeight;

    const scaleX = (canvasWidth * 0.9) / boardWidth;
    const scaleY = (canvasHeight * 0.9) / boardHeight;
    const newScale = Math.min(scaleX, scaleY);

    const newOffsetX = (canvasWidth - (boardWidth * newScale)) / 2 - (minX * newScale);
    const newOffsetY = (canvasHeight - (boardHeight * newScale)) / 2 - (minY * newScale);

    setScale(newScale);
    setOffset({ x: newOffsetX, y: newOffsetY });
  }, [canvasRef]);

  const focusOnBoundingBox = useCallback((minX: number, maxX: number, minY: number, maxY: number) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    // 0.0001 is a small number that prevents 0 division
    const compWidth = Math.max(maxX - minX, 0.0001);
    const compHeight = Math.max(maxY - minY, 0.0001);
    const canvasWidth = canvas.clientWidth;
    const canvasHeight = canvas.clientHeight;
    
    const scaleX = (canvasWidth * 0.3) / compWidth;
    const scaleY = (canvasHeight * 0.3) / compHeight;
    const newScale = Math.min(scaleX, scaleY);
    
    const newOffsetX = (canvasWidth - (compWidth * newScale)) / 2 - (minX * newScale);
    const newOffsetY = (canvasHeight - (compHeight * newScale)) / 2 - (minY * newScale);

    setScale(newScale);
    setOffset({ x: newOffsetX, y: newOffsetY });
  }, [canvasRef]);

  return {
    scale, offset, resetView, focusOnBoundingBox,
    handlers: {
      onMouseDown,
      onMouseMove,
      onMouseUp,
      onMouseLeave: onMouseUp
    }
  };
}