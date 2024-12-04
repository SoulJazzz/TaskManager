import json
from datetime import datetime
from typing import List

from manager.messages import (
    INPUT_TASK_NAME,
    INPUT_TASK_DESCRIPTION,
    INPUT_TASK_CATEGORY,
    EMPTY_INPUT_ERROR,
    INPUT_DUE_DATE,
    INVALID_DATE_ERROR,
    INPUT_PRIORITY,
    INVALID_PRIORITY_ERROR,
    INPUT_STATUS,
    INVALID_STATUS_ERROR,
    INPUT_INVALID_STATUS,
    INPUT_INVALID_PRIORITY,
    INPUT_ATTEMPTS_EXCEEDED,
    INPUT_INVALID_DATE,
    INPUT_EMPTY,
    INPUT_NEW_STATUS,
    INPUT_NEW_PRIORITY,
    INPUT_NEW_DUE_DATE,
    INPUT_NEW_CATEGORY,
    INPUT_NEW_DESCRIPTION,
    INPUT_NEW_TITLE,
    INPUT_TASK_ID
)

from tasks.task import Task
from handler.json_handler import Storage


class TaskStorage:
    """ Загрузку и сохранение задач. """

    def __init__(self):
        self.storage = Storage()

    def load_tasks(self) -> List:
        return self.storage.load_tasks()

    def save_tasks(self, tasks: list) -> None:
        self.storage.save_tasks(tasks)


class TaskViewer:
    """ Отображение задач. """

    def view_tasks(self, tasks: List[Task]) -> None:
        for task in tasks:
            task_dict = task.to_dict()
            pretty_print = json.dumps(task_dict, indent=4, ensure_ascii=False)
            print(pretty_print)


class TaskCreator:
    """Создание новых задач."""

    def create_task(self, next_id: int) -> Task:
        title = self._get_input(INPUT_TASK_NAME)
        description = self._get_input(INPUT_TASK_DESCRIPTION)
        category = self._get_input(INPUT_TASK_CATEGORY)
        due_date = self._get_due_date()
        priority = self._get_priority()
        status = self._get_status()

        return Task(next_id, title, description, category, due_date, priority, status)

    def _get_input(self, prompt: str) -> str:
        """Метод для получения ввода от пользователя."""
        while True:
            user_input = input(prompt).strip()
            if user_input:
                return user_input
            print(EMPTY_INPUT_ERROR)

    def _get_due_date(self) -> str:
        """Запрашивает у пользователя срок выполнения задачи и проверяет его корректность."""
        while True:
            due_date = input(INPUT_DUE_DATE).strip()
            if self._is_valid_date(due_date):
                return due_date
            print(INVALID_DATE_ERROR)

    def _is_valid_date(self, date_str: str) -> bool:
        """ Проверяет корректность формата даты. """
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _get_priority(self) -> str:
        """Запрашивает у пользователя приоритет задачи и проверяет его корректность."""
        valid_priorities = {'низкий', 'средний', 'высокий'}
        while True:
            priority = input(INPUT_PRIORITY).strip().lower()
            if priority in valid_priorities:
                return priority
            print(INVALID_PRIORITY_ERROR)

    def _get_status(self) -> str:
        """Запрашивает у пользователя статус задачи и проверяет его корректность."""
        valid_statuses = {'выполнена', 'не выполнена'}
        while True:
            status = input(INPUT_STATUS).strip().lower()
            if status in valid_statuses:
                return status
            print(INVALID_STATUS_ERROR)


class TaskEditor:
    """Редактирование задач."""

    def edit_task(self, tasks: List[Task], storage: TaskStorage) -> None:
        task_id = int(input(INPUT_TASK_ID))
        task_to_edit = next((task for task in tasks if task.id == task_id), None)

        if task_to_edit:
            new_title = self._get_input(INPUT_NEW_TITLE.format(task_to_edit.title))
            task_to_edit.title = new_title

            new_description = self._get_input(INPUT_NEW_DESCRIPTION.format(task_to_edit.description))
            task_to_edit.description = new_description

            new_category = self._get_input(INPUT_NEW_CATEGORY.format(task_to_edit.category))
            task_to_edit.category = new_category

            new_due_date = self._get_due_date(INPUT_NEW_DUE_DATE.format(task_to_edit.due_date))
            task_to_edit.due_date = new_due_date

            new_priority = self._get_priority(INPUT_NEW_PRIORITY.format(task_to_edit.priority))
            task_to_edit.priority = new_priority

            new_status = self._get_status(INPUT_NEW_STATUS.format(task_to_edit.status))
            task_to_edit.status = new_status

            storage.save_tasks(tasks)
        else:
            print("Задача не найдена.")

    def _get_input(self, prompt: str) -> str:
        """Проверка на пустое значение."""
        while True:
            user_input = input(prompt).strip()
            if user_input:
                return user_input
            print(INPUT_EMPTY)

    def _get_due_date(self, prompt: str) -> str:
        """Метод для получения срока выполнения с проверкой формата даты."""
        attempts = 0
        while attempts < 2:
            due_date = input(prompt).strip()
            if self._is_valid_date(due_date):
                return due_date
            attempts += 1
            print(INPUT_INVALID_DATE)

        raise ValueError(INPUT_ATTEMPTS_EXCEEDED)

    def _is_valid_date(self, date_str: str) -> bool:
        """Проверяет корректность формата даты."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _get_priority(self, prompt: str) -> str:
        """Получение приоритета с проверкой на допустимые значения."""
        valid_priorities = {'низкий', 'средний', 'высокий'}
        while True:
            priority = input(prompt).strip().lower()
            if priority in valid_priorities:
                return priority
            print(INPUT_INVALID_PRIORITY)

    def _get_status(self, prompt: str) -> str:
        """Получение статуса с проверкой на допустимые значения."""
        valid_statuses = {'выполнена', 'не выполнена'}
        while True:
            status = input(prompt).strip()
            if status in valid_statuses:
                return status
            print(INPUT_INVALID_STATUS)


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


class TaskSearcher:
    """ Поиск задач.  """

    def search_tasks(self, tasks: List[Task]) -> List[Task]:
        keyword = input("Введите ключевое слово для поиска: ")
        found_tasks = [task for task in tasks if keyword in task.title or keyword in task.description]
        for task in found_tasks:
            print(json.dumps(task.to_dict(), indent=4, ensure_ascii=False))
        return found_tasks


class TaskManager:
    """ Управление задачами. """

    def __init__(self):
        self.storage = TaskStorage()
        self.tasks = self.storage.load_tasks()
        self.next_id = len(self.tasks) + 1
        self.viewer = TaskViewer()
        self.editor = TaskEditor()
        self.deleter = TaskDeleter()
        self.searcher = TaskSearcher()
        self.creator = TaskCreator()

    def view_tasks(self) -> None:
        self.viewer.view_tasks(self.tasks)

    def add_task(self) -> None:
        task = self.creator.create_task(self.next_id)
        self.tasks.append(task)
        self.storage.save_tasks(self.tasks)
        self.next_id += 1

    def edit_task(self):
        self.editor.edit_task(self.tasks, self.storage)

    def delete_task(self) -> None:
        self.deleter.delete_task(self.tasks, self.storage)

    def search_tasks(self) -> None:
        self.searcher.search_tasks(self.tasks)
