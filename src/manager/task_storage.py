from typing import List

from handler.json_handler import Storage


class TaskStorage:
    """ Загрузку и сохранение задач. """

    def __init__(self):
        self.storage = Storage()

    def load_tasks(self) -> List:
        return self.storage.load_tasks()

    def save_tasks(self, tasks: list) -> None:
        self.storage.save_tasks(tasks)