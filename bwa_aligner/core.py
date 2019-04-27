import os
import subprocess
from typing import List
from bwa_aligner.config import Config
from bwa_aligner.logger import Logger


class BwaAligner:

    read_file_extension = ".fastq"
    output_file_extension = ".sam"

    def __init__(self, config: Config, output_dir_path: str, logger: Logger = None):
        self.config = config
        self.output_dir_path = output_dir_path
        self.logger = logger

    def run(self):
        for read_collection in self._get_reads_collections():
            self._execute_read_collection(read_collection)

    def _get_reads_collections(self) -> List[List[str]]:
        collections = []
        all_reads_dirs = self.config.get_reads_dir_paths()
        first_reads_dir = all_reads_dirs[0]
        other_reads_dirs = all_reads_dirs[1:]
        for filename in os.listdir(first_reads_dir):
            # Let's create collection only if it's the read file
            if not filename.endswith(self.read_file_extension):
                continue
            collection = [first_reads_dir + "/" + filename]
            for another_read_dir in other_reads_dirs:
                if os.path.exists(another_read_dir + "/" + filename):
                    collection.append(another_read_dir + "/" + filename)
                # We can break the loop if there is no following read
                else:
                    break
            collections.append(collection)
        return collections

    def _execute_read_collection(self, collection: List[str]):
        output_file = self.output_dir_path + "/" + os.path.basename(collection[0])
        output_file = ".".join(output_file.split(".")[:-1]) + self.output_file_extension
        command = " ".join(["/app/bwa/bwa", "mem", self.config.get_reference_path()] + collection) + " > " + output_file
        self._log_info("Executing command: " + command)
        return_code = subprocess.call(command, shell=True)
        if return_code != 0:
            raise BwaAlignerException("Execution of the last command ended with error")

    def _log_info(self, message: str):
        if self.logger is not None:
            self.logger.log_info(message)

    def _log_error(self, message: str):
        if self.logger is not None:
            self.logger.log_error(message)


class BwaAlignerException(Exception):
    pass
