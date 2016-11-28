import sys
import json
import argparse
import geopy
import geopy.distance


def load_data(filepath):
    with open(filepath, encoding="utf-8") as json_file:
        data = json.loads(json_file.read())
    return data


def get_biggest_bar(data):
    bar = max(data, key=lambda x: x["Cells"]["SeatsCount"])
    return bar["Cells"]["Name"]


def get_smallest_bar(data):
    bar = min(data, key=lambda x: x["Cells"]["SeatsCount"])
    return bar["Cells"]["Name"]


def get_closest_bar(data, longitude, latitude):
    coordinates_list = [(bar["Cells"]["Name"],
            geopy.Point(bar["Cells"]["geoData"]["coordinates"][0],
                bar["Cells"]["geoData"]["coordinates"][1])) for bar in data]
    coordinate = geopy.Point(longitude, latitude)
    distances = [(bar[0], geopy.distance.distance(bar[1], 
            coordinate).km) for bar in coordinates_list]
    return min(distances, key=lambda x: x[1])[0]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file")
    try:
        data = load_data(argparse.json_file)
    except AttributeError:
        print("Пожалуйста, запустите программу, передав как аргумент json-файл со списком баров")
        sys.exit()
    print("Самый большой бар - {}".format(get_biggest_bar(data)))
    print("Самый маленький бар - {}".format(get_smallest_bar(data)))
    longitude = input("Input your longitude:")
    latitude = input("Input your latitude:")
    print("Ближайший к указанным координатам бар - \
{}".format(get_closest_bar(data, longitude, latitude)))
