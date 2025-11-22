import os
import json

def load_json_data(filename):
    base_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    file_path = os.path.join(base_dir, filename)
    with open(file_path) as fileName:
        return json.load(fileName)