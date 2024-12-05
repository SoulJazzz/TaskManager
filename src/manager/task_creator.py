from datetime import datetime

from manager.messages import (
    INPUT_TASK_NAME,
    INPUT_TASK_DESCRIPTION,
    INPUT_TASK_CATEGORY,
    INPUT_STATUS,
    INPUT_DUE_DATE,
    INPUT_PRIORITY,

    INVALID_DATE_ERROR,
    EMPTY_INPUT_ERROR,
    INVALID_PRIORITY_ERROR,
    INVALID_STATUS_ERROR
)

from tasks.task import Task


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