import sys
import json
import argparse
import geopy
import geopy.distance


def load_data(filepath):
    with open(filepath, encoding="utf-8") as json_file:
        bars = json.loads(json_file.read())
    return bars


def get_biggest_bar(bars):
    bar = max(bars, key=lambda x: x["Cells"]["SeatsCount"])
    return bar["Cells"]["Name"]


def get_smallest_bar(bars):
    bar = min(bars, key=lambda x: x["Cells"]["SeatsCount"])
    return bar["Cells"]["Name"]


def get_closest_bar(bars, longitude, latitude):
    coordinates_list = [(bar["Cells"]["Name"],
            geopy.Point(bar["Cells"]["geobars"]["coordinates"][0],
                bar["Cells"]["geobars"]["coordinates"][1])) for bar in bars]
    coordinate = geopy.Point(longitude, latitude)
    distances = [(bar[0], geopy.distance.distance(bar[1], 
            coordinate).km) for bar in coordinates_list]
    return min(distances, key=lambda x: x[1])[0]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file")
    namespace = parser.parse_args()
    try:
        bars = load_data(namespace.json_file)
    except AttributeError:
        print("Пожалуйста, запустите программу, передав как аргумент json-файл со списком баров")
        sys.exit()
    print("Самый большой бар - {}".format(get_biggest_bar(bars)))
    print("Самый маленький бар - {}".format(get_smallest_bar(bars)))
    longitude = input("Input your longitude:")
    latitude = input("Input your latitude:")
    print("Ближайший к указанным координатам бар - \
{}".format(get_closest_bar(bars, longitude, latitude)))
