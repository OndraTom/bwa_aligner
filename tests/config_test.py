import os
import shutil
import json
from unittest import TestCase
from bwa_aligner.config import Config, ValidationException, ParsingException, FileNotFoundException


class ConfigTest(TestCase):

    test_dir = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_dir = os.path.dirname(os.path.abspath(__file__)) + "/config_test_dir"
        os.makedirs(cls.test_dir, exist_ok=True)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.test_dir)

    def test_valid_config(self):
        config_path = self.test_dir + "/valid_config.json"
        self._save_config({
            "parameters": {
                "reference": "/files/reference.fasta",
                "reads": [
                    "/files/read1",
                    "/files/read2"
                ]
            }
        }, config_path)
        Config(config_path)

    def test_invalid_config(self):
        config_path = self.test_dir + "/invalid_config.json"
        self._save_config({
            "parameters": {
                "reference": "/files/reference.fasta",
                "reads": [
                ]
            }
        }, config_path)
        self.assertRaises(ValidationException, Config, config_path)

    def test_invalid_json_config(self):
        config_path = self.test_dir + "/invalid_json_config.json"
        with open(config_path, "w") as f:
            f.write("invalid")
        self.assertRaises(ParsingException, Config, config_path)

    def test_non_existing_config(self):
        self.assertRaises(FileNotFoundException, Config, "invalid")

    @staticmethod
    def _save_config(config: dict, file_path: str):
        with open(file_path, "w") as f:
            f.write(json.dumps(config))
