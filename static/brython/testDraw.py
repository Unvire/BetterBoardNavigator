from browser import window

def drawOnCanvas(canvas):
    if canvas.getContext:
        ctx = canvas.getContext('2d')
        
        # Rysowanie prostokąta bez wypełnienia
        ctx.beginPath()
        ctx.rect(50, 50, 200, 100)  # x, y, szerokość, wysokość
        ctx.strokeStyle = 'blue'
        ctx.lineWidth = 5
        ctx.stroke()
        
        # Rysowanie linii prostej
        ctx.beginPath()
        ctx.moveTo(300, 300)  # Punkt początkowy
        ctx.lineTo(450, 450)  # Punkt końcowy
        ctx.strokeStyle = 'green'
        ctx.lineWidth = 2
        ctx.stroke()
        
        # Rysowanie koła
        ctx.beginPath()
        ctx.arc(150, 400, 50, 0, 2 * window.Math.PI)  # x, y, promień, kąt początkowy, kąt końcowy
        ctx.strokeStyle = 'red'
        ctx.lineWidth = 3
        ctx.stroke()
        
        # Ustawienie stylów dla łuku
        ctx.fillStyle = 'yellow'
        ctx.beginPath()
        
        # Rysowanie łuku
        # ctx.arc(x, y, radius, startAngle, endAngle, anticlockwise)
        ctx.arc(380, 150, 100, 5.497787143782138, 0.2617993877991494)  # np. łuk 315 -> 15 stopni
        #ctx.arc(380, 150, 100, 3.4033920413889422, 4.4505895925855405)  # np. łuk 195 -> 255 stopni
        #ctx.arc(380, 150, 100, 1.3089969389957472, 2.356194490192345)  # np. łuk 75 -> 135 stopni
        # Zakończenie rysowania i wypełnienie łuku			
        ctx.strokeStyle = 'yellow'
        ctx.stroke()
        ctx.fill()