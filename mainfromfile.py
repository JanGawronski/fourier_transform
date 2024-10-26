from animate import animate
from fft import dft

def main():
    speed = 500

    with open("drawing.txt") as file:
        data = eval(file.read())


    data = [x + 1j * y for x, y in data]

    new_data = [data[0]]

    for i in range(1, len(data)):
        distance = abs(data[i - 1] - data[i])
        if distance == 0:
            new_data.append(data[i])
            continue
        move = (data[i] - data[i - 1] ) / distance / speed
        for _ in range(int(distance * speed)):
            new_data.append(new_data[-1] + move)
        new_data.append(data[i])

    data = new_data

    sample_rate = len(data)

    animate(dft(data), sample_rate)


if __name__ == "__main__":
    main()