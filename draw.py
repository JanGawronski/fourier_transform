from matplotlib import pyplot as plt
from matplotlib.backend_bases import MouseButton

def draw():
    figDraw, axDraw = plt.subplots()
    line, = axDraw.plot([], [], animated=True)
    x, y = [], []

    axDraw.set(xlim=(-1, 1), ylim=(-1, 1))
    axDraw.spines['top'].set_color('none')
    axDraw.spines['bottom'].set_position('zero')
    axDraw.spines['left'].set_position('zero')
    axDraw.spines['right'].set_color('none')


    def on_press(event):
        if event.inaxes and event.button is MouseButton.LEFT:
            x.append(event.xdata)
            y.append(event.ydata)
            line.set_data(x, y)
            axDraw.draw_artist(line)


    figDraw.canvas.draw() 
    def update(): 
        line.set_data(x, y)
        figDraw.canvas.blit(axDraw.bbox) 

    timer = figDraw.canvas.new_timer(interval = 1) 
    timer.add_callback(update) 
    timer.start() 
    

    binding_id = plt.connect('motion_notify_event', on_press)

    plt.show()
    
    return x, y



def main():
    x1, y1 = draw()

    with open("drawing.txt", "w+") as file:
        file.write(str([(float(x), float(y)) for x, y in zip(x1, y1)]))

if __name__ == "__main__":
    main()