import os
import json
import jsonschema
from typing import List


class Config:

    schema = {
        "type": "object",
        "properties": {
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string"
                    },
                    "reads": {
                        "type": "array",
                        "item": {
                            "type": "string"
                        },
                        "minItems": 1
                    }
                },
                "required": [
                    "reference",
                    "reads"
                ]
            }
        },
        "required": [
            "parameters"
        ]
    }

    def __init__(self, config_file_path: str):
        """
        :raises ConfigValidationException: If the configuration is not valid
        """
        self.config = self._get_parsed_config(config_file_path)
        self._validate_config()

    def get_reference_path(self) -> str:
        return self.config["parameters"]["reference"]

    def get_reads_dir_paths(self) -> List[str]:
        return self.config["parameters"]["reads"]

    @staticmethod
    def _get_parsed_config(config_file_path: str) -> dict:
        if not os.path.exists(config_file_path):
            raise FileNotFoundException("File (" + config_file_path + ") doesn't exist")
        try:
            with open(config_file_path) as config_file:
                return json.load(config_file)
        except json.JSONDecodeError:
            raise ParsingException("Configuration file contents invalid JSON")
        except Exception as e:
            raise ParsingException(str(e))

    def _validate_config(self):
        try:
            jsonschema.validate(instance=self.config, schema=self.schema)
        except jsonschema.ValidationError as exp:
            raise ValidationException("Configuration is not valid: {}".format(exp))
        except Exception as e:
            raise ValidationException(str(e))
        reference_path = self.get_reference_path()
        if not os.path.exists(reference_path):
            raise ValidationException("Reference file '" + reference_path + "' doesn't exist")
        if not os.path.isfile(reference_path):
            raise ValidationException("Reference path '" + reference_path + "' is not a file")
        for read_dir_path in self.get_reads_dir_paths():
            if not os.path.exists(read_dir_path):
                raise ValidationException("Reads directory '" + read_dir_path + "' doesn't exist")
            if not os.path.isdir(read_dir_path):
                raise ValidationException("Reads path '" + read_dir_path + "' is not a directory")


class ConfigException(Exception):
    pass


class ValidationException(ConfigException):
    pass


class FileNotFoundException(ConfigException):
    pass


class ParsingException(ConfigException):
    pass
