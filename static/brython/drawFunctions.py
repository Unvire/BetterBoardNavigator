from browser import window

def drawLine(context:'canvas.getContext()', startXY:tuple[int, int], endXY:tuple[int, int], color:str, lineWidth:int):
    x0, y0 = startXY
    x1, y1 = endXY
    context.beginPath()
    context.moveTo(x0, y0)
    context.lineTo(x1, y1)
    _setCommonParameters(context, color, lineWidth)

def drawRectangle(context:'canvas.getContext()', bottomLeftXY:tuple[int, int], topRightXY:tuple[int, int], color:str, lineWidth:int, isFill:bool=False, fillColor:str='red'):
    x0, y0 = bottomLeftXY
    x1, y1 = topRightXY
    context.beginPath()
    width, height = x1 - x0, y1 - y0
    context.rect(x0, y0, width, height)
    context.strokeStyle = color
    context.lineWidth = lineWidth
    _setCommonParameters(context, color, lineWidth, isFill, fillColor)

def drawCircle(context:'canvas.getContext()', centerXY:tuple[int, int], radius:float|int, color:str, lineWidth:int, isFill:bool=False, fillColor:str='red'):
    drawArc(context, centerXY, radius, 0, 2 * window.Math.PI, color, lineWidth, isFill, fillColor)

def drawArc(context:'canvas.getContext()', centerXY:tuple[int, int], radius:float|int, startAngleRad:float|int, endAngleRad:float|int, color:str, lineWidth:int, isFill:bool=False, fillColor:str='red'):
    x0, y0 = centerXY
    context.beginPath()
    context.arc(x0, y0, radius, startAngleRad, endAngleRad)
    _setCommonParameters(context, color, lineWidth, isFill, fillColor)

def _setCommonParameters(context:'canvas.getContext()', color:str, lineWidth:int, isFill:bool=False, fillColor:str='red'):
    context.strokeStyle = color
    context.lineWidth = lineWidth
    if isFill:
        context.fillStyle = fillColor
        context.fill()
    context.stroke()