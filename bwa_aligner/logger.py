import sys


class Logger:

    @staticmethod
    def log_info(message: str):
        print(message)

    @staticmethod
    def log_error(message: str):
        print(message, file=sys.stderr)
