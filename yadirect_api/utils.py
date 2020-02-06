import json
from tempfile import NamedTemporaryFile


def get_cred_temp_file(json_field):

    with NamedTemporaryFile('w') as jsonfile:
        json.dump(json_field, jsonfile)
        jsonfile.flush()  # make sure all data is flushed to disk
        # pass the filename to something that expects a string
        with open(jsonfile.name, 'r') as jf:
            data = json.load(jf)
            print(data)
        return jsonfile.name
