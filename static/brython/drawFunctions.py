from browser import window

def drawLine(context:'canvas.getContext()', startPointTuple:tuple[int, int], endPointTuple:tuple[int, int], color:str, lineWidth:int):
    x0, y0 = startPointTuple
    x1, y1 = endPointTuple
    context.beginPath()
    context.moveTo(x0, y0)
    context.lineTo(x1, y1)
    _setCommonParameters(context, color, lineWidth, False)

def drawRectangle(context:'canvas.getContext()', bottomLeftPoint:tuple[int, int], topRightPoint:tuple[int, int], color:str, lineWidth:int, isFill:bool=False, fillColor:str='red'):
    x0, y0 = bottomLeftPoint
    x1, y1 = topRightPoint
    context.beginPath()
    width, height = x1 - x0, y1 - y0
    context.rect(x0, y0, width, height)
    context.strokeStyle = color
    context.lineWidth = lineWidth
    _setCommonParameters(context, color, lineWidth, isFill)

def drawCircle(context:'canvas.getContext()', centerPoint:tuple[int, int], radius:float|int, color:str, lineWidth:int, isFill:bool=False, fillColor:str='red'):
    drawArc(context, centerPoint, radius, 0, 2 * window.Math.PI, color, lineWidth, isFill, fillColor)

def drawArc(context:'canvas.getContext()', centerPoint:tuple[int, int], radius:float|int, startAngleRad:float|int, endAngleRad:float|int, color:str, lineWidth:int, isFill:bool=False, fillColor:str='red'):
    x0, y0 = centerPoint
    context.beginPath()
    context.arc(x0, y0, radius, startAngleRad, endAngleRad)
    _setCommonParameters(context, color, lineWidth, isFill)

def _setCommonParameters(context:'canvas.getContext()', color:str, lineWidth:int, isFill:bool=False, fillColor:str='red'):
    context.strokeStyle = color
    context.lineWidth = lineWidth
    context.stroke()
    if isFill:
        context.fillStyle = fillColor
        context.fill()