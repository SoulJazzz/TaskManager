import json
from typing import List

from tasks.task import Task


class Storage:
    """Управление хранилищем задач, включая загрузку, сохранение и добавление задач."""

    def __init__(self, filename='tasks.json'):
        self.filename = filename

    def load_tasks(self) -> List[Task]:
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                tasks_data = json.load(file)
                return [Task(**task) for task in tasks_data]
        except FileNotFoundError:
            return []

    def save_tasks(self, tasks) -> None:
        with open(self.filename, 'w', encoding='utf-8') as file:
            file.write(json.dumps([task.to_dict() for task in tasks], indent=4, ensure_ascii=False))

    def add_task(self, task) -> None:
        tasks = self.load_tasks()
        tasks.append(task)
        self.save_tasks(tasks)
