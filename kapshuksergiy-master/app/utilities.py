import json


def json_to_dict(file_name):
    with open(file_name) as f:
        data = json.load(f)

    return data

def json_w(file_name, data):
    with open(file_name, 'w') as f:
        print(data)
        json.dump(data, f)