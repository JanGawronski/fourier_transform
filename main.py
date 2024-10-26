from math import e, pi
from draw import draw
from animate import animate


def main():
    x1, y1 = draw()

    data = [x + 1j*y for x, y in zip(x1, y1)]

    sampleRate = len(data)
    dft = lambda T: [sum([T[n]*e**(-1j * 2*pi * k * n / sampleRate) for n in range(sampleRate)])/sampleRate for k in range(sampleRate)]

    dftnumbers = dft(data)

    animate(dftnumbers, sampleRate)


if __name__ == "__main__":
    main()