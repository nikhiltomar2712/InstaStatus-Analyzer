import csv
import json
from pathlib import Path

from src.exporter import export_csv, export_json


def test_export_json_writes_to_output_dir(tmp_path):
    data = {"test": 123}

    path = export_json(data, "test.json", output_dir=tmp_path)

    assert Path(path) == tmp_path / "test.json"
    assert json.loads(Path(path).read_text(encoding="utf-8")) == data


def test_export_csv_uses_all_keys(tmp_path):
    rows = [
        {"username": "one", "bot_label": "real"},
        {"username": "two", "sentiment_score": 0.4},
    ]

    path = export_csv(rows, "followers.csv", output_dir=tmp_path)

    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        exported_rows = list(reader)

    assert reader.fieldnames == ["username", "bot_label", "sentiment_score"]
    assert exported_rows[0]["username"] == "one"
    assert exported_rows[1]["sentiment_score"] == "0.4"
