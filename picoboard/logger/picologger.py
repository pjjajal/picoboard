# Copyright (c) 2023 Purvish Jajal
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import sys
from datetime import datetime
from typing import List

from loguru import logger


def name_handler(name: str):
    return name.replace(" ", "-").upper()


class PicoLogger:
    def __init__(self, log_dir: str = None, log_comment: str = "") -> None:
        if not log_dir:
            log_dir = "runs"

        log_format = "<green>{time:YYYY-MM-DDTHH:mm:ss}</green> :: <bold><cyan>{extra[name]}</cyan></bold>: <magenta>{message}</magenta>"

        date = datetime.now().strftime(r"%Y-%m-%dT%H:%M:%S")
        filename = f"{date}"
        if log_comment:
            filename += f"-{log_comment}"
        self.log_path = f"{log_dir}/{filename}.log"

        # Remove old logger and create now one.
        logger.remove()
        logger.add(sys.stderr, format=log_format)
        logger.add(self.log_path, format=log_format)

    def log_scalar(self, name: str, formated_scalar: str):
        logger.info(formated_scalar, name=name_handler(name))


class PicoParser:
    def __init__(self, log_path: str) -> None:
        self.log_path = log_path
        self.pattern = r"(?P<time>.*) :: (?P<name>.*): (?P<message>.*)"

        self.mtime = self._log_mtime()
        self.log_cache = self.get_log()

    def _log_mtime(self):
        return os.stat(self.log_path).st_mtime

    def get_log(self):
        if not hasattr(self, "log_cache"):
            log = list(logger.parse(self.log_path, self.pattern))
            self.log_cache = log

        new_mtime = self._log_mtime()
        if new_mtime > self.mtime:
            self.mtime = new_mtime
            log = list(logger.parse(self.log_path, self.pattern))
            self.log_cache = log

        return self.log_cache

    def filtered_log(self, names: List[str]):
        log = self.get_log()

        filtered_data = {}
        for name in names:
            name = name_handler(name)
            filtered_data[name] = list(filter(lambda x: x["name"] == name, log))

        return filtered_data


# if __name__ == "__main__":
#     plog = PicoLogger()
#     pparse = PicoParser(plog.log_path)
#     plog.log_scalar("val_acc", "0.22")
#     print(pparse.get_log())
#     print(pparse.filtered_log(["val_acc"]))
#     plog.log_scalar("val_acc", "0.24")
#     plog.log_scalar("train_acc", "0.24")
#     print(pparse.filtered_log(["val_acc"]))
#     print(pparse.filtered_log(["val_acc", "train_acc"]))
