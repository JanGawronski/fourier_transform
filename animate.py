from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from math import e, pi

def animate(dftnumbers, sample_rate, save = "", axis_off = False):
    dftnumbers = sorted([(index, x) for index, x in enumerate(dftnumbers)], key = lambda x: abs(x[1]), reverse=True)

    circle_centers = [[0 for _ in range(sample_rate)] for _ in range(sample_rate)]

    for x in range(sample_rate):
        for i in range(1, sample_rate):
            circle_centers[x][i] = circle_centers[x][i - 1] + dftnumbers[i][1] * e**(dftnumbers[i][0] * x * 1j * 2 * pi / sample_rate)


    f = lambda x: sum(c*e**(k*x*1j) for k, c in dftnumbers)

    fpoints = lambda x: [c*e**(k*x*1j) for k, c in dftnumbers]

    circles = [plt.Circle((0,0), abs(c), fill=False, edgecolor="lightgray", animated=True, linewidth=.3) for x, c in dftnumbers[:min(sample_rate, 32)]]

    fig, ax = plt.subplots(figsize=(7, 7))

    lines = [ax.plot([],[], linewidth=.5, color="gray")[0], ax.plot([],[])[0],]

    for i in range(len(circles)):
        ax.add_artist(circles[i])

    def init():
        for line in lines:
            line.set_data([],[])
        return lines

    x1,y1 = [],[]
    x2,y2 = [],[]


    def init():
        if axis_off:
            plt.axis('off')
        ax.set(xlim=(-1, 1), ylim=(-1, 1))
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        for line in lines:
            line.set_data([],[])
        return lines

    def update(frame):
        nonlocal x1
        nonlocal y1
        x1.append(f(2*pi*frame/sample_rate).real)
        y1.append(f(2*pi*frame/sample_rate).imag)

        x2 = [0, *[x.real for x in fpoints(2*pi*frame/sample_rate)]]
        y2 = [0, *[x.imag for x in fpoints(2*pi*frame/sample_rate)]]


        for i in range(1, len(x2)):
            x2[i] += x2[i - 1]
            y2[i] += y2[i - 1]


        if len(x1) > sample_rate:
            x1 = []
            y1 = []

        for i in range(len(circles)):
            circles[i].set(center = (x2[i], y2[i]))

        xlist = [x2, x1]
        ylist = [y2, y1]

        for lnum,line in enumerate(lines):
            line.set_data(xlist[lnum], ylist[lnum])
        
        return [*lines, *circles]

    ani = FuncAnimation(
        fig, update,
        frames=range(sample_rate),
        interval=30,
        init_func=init, blit=True)


    if len(save) > 0:
        ani.save(filename=save, writer="ffmpeg", fps=60, dpi=200)
    else:
        plt.show()


def main():
    from fft import dft
    sample_rate = 2**10
    number = lambda x: 0.25*e**(-2*x*1j) + 0.5*e**(-x*1j) 

    #number = lambda x: x/pi - 1


    dftnumbers = dft([number(2*pi*x/sample_rate) for x in range(sample_rate)])


    animate(dftnumbers, sample_rate)




if __name__ == "__main__":
    main()