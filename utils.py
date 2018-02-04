import json
import os

with open(os.getenv('CITY_FILE', 'blob.json'), 'r') as fp:
    cities = json.load(fp)
