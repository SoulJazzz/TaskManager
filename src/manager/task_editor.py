import os
from datetime import datetime
from typing import List
from dotenv import load_dotenv

load_dotenv()

from manager.messages import (
    INPUT_ATTEMPTS_EXCEEDED,
    INPUT_NEW_STATUS,
    INPUT_NEW_PRIORITY,
    INPUT_NEW_DUE_DATE,
    INPUT_NEW_CATEGORY,
    INPUT_NEW_DESCRIPTION,
    INPUT_NEW_TITLE,
    INPUT_TASK_ID,

    INVALID_STATUS_ERROR,
    INVALID_PRIORITY_ERROR,
    INVALID_DATE_ERROR,

    EMPTY_INPUT_ERROR
)
from manager.task_storage import TaskStorage
from tasks.task import Task


class TaskEditor:
    """Редактирование задач."""

    def edit_task(self, tasks: List[Task], storage: TaskStorage) -> None:
        task_id_input = input(INPUT_TASK_ID).strip()
        if not task_id_input:
            print("Идентификатор задачи не может быть пустым.")
            return
        task_id = int(task_id_input)
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
            print(EMPTY_INPUT_ERROR)

    def _get_due_date(self, prompt: str) -> str:
        """Метод для получения срока выполнения с проверкой формата даты."""
        attempts = 0
        while attempts < int(os.getenv('MAX_ATTEMPTS')):
            due_date = input(prompt).strip()
            if self._is_valid_date(due_date):
                return due_date
            attempts += 1
            print(INVALID_DATE_ERROR)

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
            print(INVALID_PRIORITY_ERROR)

    def _get_status(self, prompt: str) -> str:
        """Получение статуса с проверкой на допустимые значения."""
        valid_statuses = {'выполнена', 'не выполнена'}
        while True:
            status = input(prompt).strip()
            if status in valid_statuses:
                return status
            print(INVALID_STATUS_ERROR)
