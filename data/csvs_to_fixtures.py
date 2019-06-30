#!/usr/bin/env python
import csv
import json
from pathlib import Path

OUTPUT_FILE = "fixtures.json"

# file -> SQL table name
CSV_FILES = {
    'testers.csv': 'tester_matching.tester',
    'devices.csv': 'tester_matching.device',
    'tester_device.csv': 'tester_matching.testerdevice',
    'bugs.csv': 'tester_matching.bug',
}

for k in CSV_FILES.keys():
    assert Path(k).is_file()

data = []


def fixture_el(model, pk, fields):
    return {
        'model': model,
        'pk': pk,
        'fields': fields,
    }


for csv_file in CSV_FILES.keys():
    model = CSV_FILES[csv_file]

    with open(csv_file) as fr:
        reader = csv.reader(fr)
        field_names = next(reader)

        for ind, row in enumerate(reader):
            fix_el = {}
            if len(row) is 0:
                continue
            for field_name, field in zip(field_names, row):
                fix_el[field_name] = field

            data.append(fixture_el(model, ind, fix_el))

with open(OUTPUT_FILE, "w") as fw:
    json.dump(data, fw, indent=2)
