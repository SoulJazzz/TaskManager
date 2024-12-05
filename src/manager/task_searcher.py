import json
from typing import List

from tasks.task import Task


class TaskSearcher:
    """ Поиск задач.  """

    def search_tasks(self, tasks: List[Task]) -> List[Task]:
        keyword = input("Введите ключевое слово для поиска: ")
        found_tasks = [task for task in tasks if keyword in task.title or keyword in task.description]
        for task in found_tasks:
            print(json.dumps(task.to_dict(), indent=4, ensure_ascii=False))
        return found_tasks
