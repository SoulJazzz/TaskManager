import json
from typing import List

from tasks.task import Task


class TaskViewer:
    """ Отображение задач. """

    def view_tasks(self, tasks: List[Task]) -> None:
        for task in tasks:
            task_dict = task.to_dict()
            pretty_print = json.dumps(task_dict, indent=4, ensure_ascii=False)
            print(pretty_print)