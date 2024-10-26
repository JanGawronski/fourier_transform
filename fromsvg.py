from svg.path import parse_path
from xml.dom import minidom
from animate import animate
from fft import dft


def get_point_at(path, distance, scale, offset):
    pos = path.point(distance)
    pos += offset
    pos *= scale
    return pos.real, pos.imag


def points_from_path(path, density, scale, offset):
    step = int(path.length() * density)
    last_step = step - 1

    if last_step == 0:
        yield get_point_at(path, 0, scale, offset)
        return

    for distance in range(step):
        yield get_point_at(
            path, distance / last_step, scale, offset)


def points_from_doc(doc, density=5, scale=1, offset=0):
    offset = offset[0] + offset[1] * 1j
    points = []
    for element in doc.getElementsByTagName("path"):
        for path in parse_path(element.getAttribute("d")):
            points.extend(points_from_path(
                path, density, scale, offset))

    return points


def main():
    with open("fourier.svg") as file:
        data = file.read() 

    doc = minidom.parseString(data)
    points = points_from_doc(doc, density=.2, scale=-.002, offset=(-1000, -550))
    doc.unlink()

    data = [x + 1j*y for x, y in points]

    sampleRate = len(data)

    dftnumbers = dft(data)

    animate(dftnumbers, sampleRate)


if __name__ == "__main__":
    main()