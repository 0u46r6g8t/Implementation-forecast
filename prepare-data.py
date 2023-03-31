#!/usr/bin/python
import os
import json
import csv
from random import randint
from datetime import datetime

PATHS_EXAMPLES = "Datasets"
PATH_WRITER = 'assets'
PATH_CSV = 'new_csv'
FILES = {}
global count
count = 0


def format_data(new_data):
    type_used = ['Measure', 'Medição', 'Actual']
    data = {}
    global count
    count = randint(0, 100)
    date = datetime(randint(2000, 2003), randint(1, 12), randint(1, 28))
    data['timestamp'] = date.strftime('%Y-%m-%d')
    data['item_id'] = count
    for i in type_used:
        try:
            data['target_value'] = abs(new_data[i])
        except:
            pass

    return data


def save_json(data, filename):
    with open(PATHS_EXAMPLES + "/" + PATH_WRITER + "/" + filename, 'w') as outfile:
        outfile.write(data)


def save_csv(data, filename, keys):
    with open(PATHS_EXAMPLES + "/" + PATH_CSV + "/" + filename.split('.')[0]+".csv", 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


def read_file(filename, typeof):
    file = open(PATHS_EXAMPLES + "/" + typeof + '/' + filename)
    json_file = json.loads(file.read())

    name_file = str(filename).replace(' ', '_').split('.')[0]

    new_json = {name_file: []}

    # Generate json default
    for item in json_file:
        new_json[name_file].append(format_data(item))

    new_json_bkp = new_json[name_file]
    # Format data
    new_json = json.dumps(new_json, ensure_ascii=False, indent=4)

    # Save data to json
    save_json(new_json, filename)

    # Convert data to csv
    save_csv(new_json_bkp, filename, [*new_json_bkp[0].keys()])

    file.close()


def get_files():
    for path in os.walk(PATHS_EXAMPLES):

        if ('/' in path[0]):
            _, typeof = path[0].split('/')

            FILES[typeof] = path[2]


get_files()
for file in FILES['json']:
    read_file(file, "json")
