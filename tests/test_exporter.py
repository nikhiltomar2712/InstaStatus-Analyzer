import os, json
from src.exporter import export_json
def test_export_json(tmp_path):
    os.chdir(tmp_path)
    data = {"test": 123}
    export_json(data, "test.json")
    with open("exports/test.json") as f:
        assert json.load(f) == data
