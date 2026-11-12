export interface Point {
  x: number;
  y: number;
}

export interface Line {
  type: 'Line';
  start: Point;
  end: Point;
}

export interface Arc {
  type: 'Arc';
  center: Point;
  radius: number;
  startAngle: number;
  endAngle: number;
}

export interface Circle {
  type: 'Circle';
  center: Point;
  radius: number;
}

export interface Rectangle {
  type: 'Rectangle';
  points: Point[];
}

export type ShapeData = Line | Arc | Circle | Rectangle;

export interface Pin {
  name: string;
  net: string | null;
  shapeType: 'RECT' | 'CIRCLE';
  shapeData: ShapeData;
  coords: Point | null;
}

export interface Component {
  name: string;
  side: 'T' | 'B';
  angle: number;
  mountingType: 'SMT' | 'TH';
  shapeType: string;
  shapeData: ShapeData;
  coords: Point | null;
  pins: Record<string, Pin>;
}

export interface NetData {
  pins: string[];
}

export interface BoardData {
  boardDimensions: [number, number];
  area: Point[];
  outlines: ShapeData[];
  components: Record<string, Component>;
  nets: Record<string, Record<string, NetData>>;
  mostCommonPrefix: string;
}