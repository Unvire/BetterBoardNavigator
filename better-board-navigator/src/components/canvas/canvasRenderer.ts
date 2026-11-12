import type { BoardData, ShapeData } from '../../types/board';
import type { Hitbox } from '../../hooks/useBoardGeometry';

export interface RenderOptions {
  ctx: CanvasRenderingContext2D;
  boardData: BoardData;
  scale: number;
  offset: { x: number; y: number };
  isMirrored: boolean;
  boardCenterX: number;
  boardCenterY: number;
  rotation: number;
  isDarkMode: boolean;
  showOutlines: boolean;
  currentSide: 'T' | 'B';
  selectedComponents: Set<string>;
  inspectedComponents: string[];
  selectedNet: string | null;
  highlightedPrefix: string | null;
  showLabels: boolean;
  componentHitboxes: Hitbox[];
  partNumbers: Record<string, string> | null;
  highlightedPartNumber: string | null;
  hideUnassignedPNs: boolean;
  hiddenComponents: Set<string>;
}


const addShapeToPath = (ctx: CanvasRenderingContext2D, shape: ShapeData) => {
  if (shape.type === 'Line' && shape.start && shape.end) {
    ctx.moveTo(shape.start.x, shape.start.y);
    ctx.lineTo(shape.end.x, shape.end.y);
  } else if (shape.type === 'Arc' && shape.center && shape.radius !== undefined && shape.startAngle !== undefined && shape.endAngle !== undefined) {
    ctx.arc(shape.center.x, shape.center.y, shape.radius, shape.startAngle, shape.endAngle);
  } else if (shape.type === 'Circle' && shape.center && shape.radius !== undefined) {
    ctx.moveTo(shape.center.x + shape.radius, shape.center.y);
    ctx.arc(shape.center.x, shape.center.y, shape.radius, 0, 2 * Math.PI);
  } else if (shape.type === 'Rectangle' && shape.points && shape.points.length === 4) {
    ctx.moveTo(shape.points[0].x, shape.points[0].y);
    ctx.lineTo(shape.points[1].x, shape.points[1].y);
    ctx.lineTo(shape.points[2].x, shape.points[2].y);
    ctx.lineTo(shape.points[3].x, shape.points[3].y);
    ctx.closePath();
  }
};


const drawLabels = (ctx: CanvasRenderingContext2D, options: RenderOptions) => {
  const { 
    scale, offset, rotation, boardCenterX, boardCenterY,
    isDarkMode, componentHitboxes, selectedComponents, 
    inspectedComponents, highlightedPrefix, showLabels, isMirrored,
    partNumbers, highlightedPartNumber
  } = options;
  
  const canvasWidth = ctx.canvas.width;
  const canvasHeight = ctx.canvas.height;
  
  // converting screen to board coordinate system
  const getOrigCoords = (sx: number, sy: number) => {
    let wx = (sx - offset.x) / scale;
    let wy = (sy - offset.y) / scale;
    if (isMirrored) wx = boardCenterX * 2 - wx;
    if (rotation !== 0) {
      const rad = (-rotation * Math.PI) / 180;
      const dx = wx - boardCenterX;
      const dy = wy - boardCenterY;
      wx = dx * Math.cos(rad) - dy * Math.sin(rad) + boardCenterX;
      wy = dx * Math.sin(rad) + dy * Math.cos(rad) + boardCenterY;
    }
    return { wx, wy };
  };

  const c1 = getOrigCoords(0, 0);
  const c2 = getOrigCoords(canvasWidth, 0);
  const c3 = getOrigCoords(0, canvasHeight);
  const c4 = getOrigCoords(canvasWidth, canvasHeight);

  const margin = 50 / scale;
  const vMinX = Math.min(c1.wx, c2.wx, c3.wx, c4.wx) - margin;
  const vMaxX = Math.max(c1.wx, c2.wx, c3.wx, c4.wx) + margin;
  const vMinY = Math.min(c1.wy, c2.wy, c3.wy, c4.wy) - margin;
  const vMaxY = Math.max(c1.wy, c2.wy, c3.wy, c4.wy) + margin;


  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  
  const shadowColor = isDarkMode ? 'rgba(10, 10, 10, 0.8)' : 'rgba(255, 255, 255, 0.8)';
  const charWidthRatio = 0.6; 

  componentHitboxes.forEach(box => {
    // discard labels outside screen
    if (box.maxX < vMinX || box.minX > vMaxX || box.maxY < vMinY || box.minY > vMaxY) return; 

    const compName = box.name;
    const isSelected = selectedComponents.has(compName);
    const isInspected = inspectedComponents.includes(compName);

    // fast prefix checking
    let compPrefix = '#';
    for (let i = 0; i < compName.length; i++) {
      if (!isNaN(Number(compName[i]))) {
        compPrefix = compName.substring(0, i).toUpperCase();
        break;
      }
    }
    const isPrefixHighlighted = highlightedPrefix === compPrefix;
    const isPNHighlighted = 
      highlightedPartNumber !== null && 
      partNumbers !== null && 
      partNumbers[compName] === highlightedPartNumber;

    const isHighlighted = isSelected || isInspected || isPrefixHighlighted || isPNHighlighted;

    const compWidth = box.maxX - box.minX;
    const compHeight = box.maxY - box.minY;
    const shortestSide = Math.min(compWidth, compHeight);
    const longestSide = Math.max(compWidth, compHeight);
    
  
    let targetWorldFontSize = shortestSide * 0.3;
    const maxFontBasedOnWidth = longestSide / (compName.length * charWidthRatio);
    
    if (targetWorldFontSize > maxFontBasedOnWidth) targetWorldFontSize = maxFontBasedOnWidth * 0.8; 
    if (targetWorldFontSize > 2) targetWorldFontSize = 2;
    if (targetWorldFontSize < 0.001) targetWorldFontSize = 0.5;
    if (isHighlighted) targetWorldFontSize *= 1.2;

    const visualPixelSize = targetWorldFontSize * scale;
    let shouldDraw = false;

    if (showLabels && visualPixelSize > 8) shouldDraw = true;
    else if (isHighlighted) {
      const approxTextWidth = compName.length * (targetWorldFontSize * charWidthRatio);
      const maxAllowedTextWidth = Math.max(compWidth, compHeight) * 1.5; 

      if (approxTextWidth <= maxAllowedTextWidth) shouldDraw = true;
    }

    if (shouldDraw) {
      const cx = (box.minX + box.maxX) / 2;
      const cy = (box.minY + box.maxY) / 2;

      ctx.save();
      
      // revert all translations so that text is in native pixels
      ctx.translate(cx, cy);
      if (rotation !== 0) ctx.rotate((-rotation * Math.PI) / 180);
      if (isMirrored) ctx.scale(-1, 1);
      ctx.scale(1 / scale, 1 / scale);

      ctx.fillStyle = isHighlighted
        ? (isDarkMode ? '#ffffff' : '#000000')
        : (isDarkMode ? '#94a3b8' : '#64748b');

      ctx.font = isHighlighted 
         ? `bold ${visualPixelSize.toFixed(1)}px sans-serif` 
         : `600 ${visualPixelSize.toFixed(1)}px sans-serif`;

      if (isHighlighted) {
        ctx.shadowColor = shadowColor;
        ctx.shadowBlur = 3; 
      } else {
        ctx.shadowBlur = 0; 
      }

      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      
      ctx.fillText(compName, 0, 0);
      ctx.restore();
    }
  });

  ctx.shadowBlur = 0;
};

export const renderBoard = (options: RenderOptions) => {
  const { 
    ctx, boardData, scale, offset, isMirrored, boardCenterX, boardCenterY, rotation,
    isDarkMode, showOutlines, currentSide, 
    selectedComponents, inspectedComponents, selectedNet, highlightedPrefix, 
    partNumbers, highlightedPartNumber
  } = options;

  const canvas = ctx.canvas;
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.fillStyle = isDarkMode ? '#0a0a0a' : '#f1f5f9';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.save();
  ctx.translate(offset.x, offset.y);
  ctx.scale(scale, scale);

  if (isMirrored) {
    ctx.translate(boardCenterX, 0);
    ctx.scale(-1, 1);
    ctx.translate(-boardCenterX, 0);
  }

  if (rotation !== 0) {
    ctx.translate(boardCenterX, boardCenterY);
    ctx.rotate((rotation * Math.PI) / 180);
    ctx.translate(-boardCenterX, -boardCenterY);
  }

  const baseLineWidth = 1 / scale;

  // 1. Drawing outlines
  if (showOutlines && boardData.outlines) {
    ctx.beginPath();
    ctx.lineWidth = baseLineWidth * 2;
    ctx.strokeStyle = isDarkMode ? '#e2e8f0' : '#475569';
    boardData.outlines.forEach(shape => addShapeToPath(ctx, shape));
    ctx.stroke();
  }

  // Objects grouping
  const thtPads: ShapeData[] = [];
  const smtPads: ShapeData[] = [];
  const bodyShapes: ShapeData[] = [];
  const selectedShapes: ShapeData[] = [];
  const netShapes: ShapeData[] = [];
  const inspectedShapes: ShapeData[] = [];

  Object.entries(boardData.components).forEach(([compName, comp]) => {
    if (options.hiddenComponents.has(compName)) return;
    if (options.hideUnassignedPNs && (!options.partNumbers || !options.partNumbers[compName])) return;

    const isOnCurrentSide = comp.side === currentSide;
    const isTH = comp.mountingType === 'TH';
    const isSelected = selectedComponents.has(compName);
    const isInspected = inspectedComponents.includes(compName);
    const hasSinglePin = comp.pins ? Object.keys(comp.pins).length === 1 : false;

    const match = compName.match(/^[a-zA-Z]+/);
    const compPrefix = match ? match[0].toUpperCase() : '#';
    const isPrefixHighlighted = highlightedPrefix === compPrefix;

    const isPNHighlighted = 
      highlightedPartNumber !== null && 
      partNumbers !== null && 
      partNumbers[compName] === highlightedPartNumber;
      
    const isCyanHighlighted = isInspected || isPrefixHighlighted || isPNHighlighted;
    
    if (isOnCurrentSide && comp.shapeData && !hasSinglePin) {
      if (isCyanHighlighted) inspectedShapes.push(comp.shapeData); 
      else if (isSelected) selectedShapes.push(comp.shapeData);
      else bodyShapes.push(comp.shapeData);
    }

    if ((isOnCurrentSide || isTH) && comp.pins) {
      Object.values(comp.pins).forEach(pin => {
        if (pin.shapeData) {
          if (selectedNet && pin.net === selectedNet) netShapes.push(pin.shapeData);
          else if (isCyanHighlighted) inspectedShapes.push(pin.shapeData);
          else if (isSelected) selectedShapes.push(pin.shapeData);
          else if (isTH) thtPads.push(pin.shapeData);
          else smtPads.push(pin.shapeData);
        }
      });
    }
  });

  // Helper for drawing collections
  const drawGroup = (shapes: ShapeData[], lineW: number, strokeColor: string, fillColor?: string) => {
    if (shapes.length === 0) return;
    ctx.beginPath();
    ctx.lineWidth = lineW;
    ctx.strokeStyle = strokeColor;
    if (fillColor) ctx.fillStyle = fillColor;
    shapes.forEach(shape => addShapeToPath(ctx, shape));
    if (fillColor) ctx.fill();
    ctx.stroke();
  };

  drawGroup(bodyShapes, baseLineWidth, isDarkMode ? '#4ade80' : '#16a34a');
  drawGroup(smtPads, baseLineWidth, isDarkMode ? '#fbbf24' : '#d97706', isDarkMode ? 'rgba(251, 191, 36, 0.2)' : 'rgba(217, 119, 6, 0.2)');
  drawGroup(thtPads, baseLineWidth, isDarkMode ? '#60a5fa' : '#2563eb', isDarkMode ? 'rgba(96, 165, 250, 0.2)' : 'rgba(37, 99, 235, 0.2)');
  drawGroup(selectedShapes, baseLineWidth * 1.5, isDarkMode ? '#f43f5e' : '#e11d48', isDarkMode ? 'rgba(244, 63, 94, 0.4)' : 'rgba(225, 29, 72, 0.4)');
  drawGroup(inspectedShapes, baseLineWidth * 2, isDarkMode ? '#22d3ee' : '#0891b2', isDarkMode ? 'rgba(34, 211, 238, 0.4)' : 'rgba(8, 145, 178, 0.4)');
  drawGroup(netShapes, baseLineWidth * 2, isDarkMode ? '#d946ef' : '#c026d3', isDarkMode ? 'rgba(217, 70, 239, 0.5)' : 'rgba(192, 38, 211, 0.5)');
  drawLabels(ctx, options);

  ctx.restore(); 
};