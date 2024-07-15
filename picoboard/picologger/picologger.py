import os
from typing import List
from tinydb import TinyDB, where
from loguru import logger
from ..utils.namegen import name_generator


def name_handler(name: str):
    return name.replace(" ", "-").lower()


class PicoLogger:
    def __init__(self, log_dir: str = None, name: str = "") -> None:
        # Check arguments logging directory.
        if not log_dir:
            logger.info("No log directory provided. Writing to picologs.")
            log_dir = "picologs"
        if not os.path.exists(log_dir):
            logger.info(f"Creating log directory: {log_dir}")
            os.makedirs(log_dir)

        # Create picodb and table for data.
        self.log_db_path = f"{log_dir}/picodb.json"
        self.picodb = TinyDB(self.log_db_path)
        if not name:
            logger.info("No name provided. Generating a random name.")
            name = name_generator()
            logger.info(f"Generated name: {name}")

        # Check for table name collisions.
        name = self._check_collision(name)

        # Create the table.
        self.table = self.picodb.table(
            name_handler(name)
        )  # all data is stored in a table with a unique name for the run.

    def _check_collision(self, name):
        # Check if the table already exists.
        collision_id = 0
        new_name = name
        while name_handler(new_name) in self.picodb.tables():
            logger.info(f"Table with name {name} already exists. Creating a new table.")
            collision_id += 1
            new_name = name + f"-{collision_id}"  # Append collision id to the name.
        return new_name

    def log(self, data: dict, id: int = 0):
        data = {"id": id, **data}
        if self.table.contains(where("id") == id):
            self.table.update(data, where("id") == id)
        else:
            self.table.insert(data)
