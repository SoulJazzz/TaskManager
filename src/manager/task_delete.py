from typing import List

from manager.task_storage import TaskStorage
from tasks.task import Task


class TaskDeleter:
    """ Удаления задачи по её ID """

    def delete_task(self, tasks: List[Task], storage: TaskStorage) -> bool:
        task_id = int(input("Введите ID задачи для удаления: "))
        task_to_delete = next((task for task in tasks if task.id == task_id), None)

        if task_to_delete:
            title = task_to_delete.title
            tasks.remove(task_to_delete)
            storage.save_tasks(tasks)
            print(f"Задача '{title}' была успешно удалена.")
            return True
        else:
            print("Задача с таким ID не найдена.")
            return False
