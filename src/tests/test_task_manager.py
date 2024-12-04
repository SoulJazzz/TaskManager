from unittest.mock import patch, MagicMock

import pytest

from manager.task_manager import TaskCreator, TaskEditor, TaskStorage, TaskDeleter, TaskSearcher
from tasks.task import Task


class TestTaskCreator:
    @patch('builtins.input',
           side_effect=['Изучить основы FastAPI',
                        'Пройти документацию по FastAPI и создать простой проект',
                        'Обучение',
                        '2024-11-30',
                        'высокий',
                        'не выполнена'])
    def test_create_task(self, mock_input):
        """Проверяет создание задачю"""
        creator = TaskCreator()
        task = creator.create_task(1)

        assert isinstance(task, Task)
        assert task.title == 'Изучить основы FastAPI'
        assert task.description == 'Пройти документацию по FastAPI и создать простой проект'
        assert task.category == 'Обучение'
        assert task.due_date == '2024-11-30'
        assert task.priority == 'высокий'
        assert task.status == 'не выполнена'

    @patch('builtins.input', side_effect=['', 'Допустимые данные для ввода'])
    def test_get_input_empty(self, mock_input):
        """Проверяет на случаи пустого ввода"""
        creator = TaskCreator()
        result = creator._get_input('Введите название задачи: ')
        assert result == 'Допустимые данные для ввода'

    @patch('builtins.input', side_effect=['Недействительная дата', '2024-11-30'])
    def test_get_due_date_invalid(self, mock_input):
        """Тест на случай недействительной даты"""
        creator = TaskCreator()
        result = creator._get_due_date()
        assert result == '2024-11-30'

    @patch('builtins.input', side_effect=['низкий', 'средний', 'высокий'])
    def test_get_priority_valid(self, mock_input):
        """Тест на получение допустимого приоритета"""
        creator = TaskCreator()
        result = creator._get_priority()
        assert result == 'низкий'

    @patch('builtins.input', side_effect=['не выполнена', 'выполнена'])
    def test_get_status_valid(self, mock_input):
        """Тест на получение допустимого статуса"""
        creator = TaskCreator()
        result = creator._get_status()
        assert result == 'не выполнена'


class TestTaskEditor:
    @pytest.fixture
    def setup(self):
        """Создаёт тестовые задачи."""
        self.editor = TaskEditor()
        self.task = Task(id=1,
                         title='Тестовая задача',
                         description='Описание',
                         category='Общее',
                         due_date='2020-04-28',
                         priority='средний',
                         status='не выполнена'
                         )
        self.tasks = [self.task]
        self.storage = MagicMock()

    @patch('builtins.input', side_effect=[
        "1",
        "Новая задача",
        "Новое описание",
        "Новая категория",
        "2020-04-28",
        "высокий",
        "выполнена"
    ])
    def test_edit_task_success(self, mock_input, setup):
        """Проверка, что поля задачи обновлены правильно"""
        self.editor.edit_task(self.tasks, self.storage)

        assert self.task.title == 'Новая задача'
        assert self.task.description == 'Новое описание'
        assert self.task.category == 'Новая категория'
        assert self.task.due_date == '2020-04-28'
        assert self.task.priority == 'высокий'
        assert self.task.status == 'выполнена'
        self.storage.save_tasks.assert_called_once_with(self.tasks)

    @patch('builtins.input', side_effect=["2"])
    def test_edit_task_not_found(self, mock_input, setup):
        """Тест, если задача не найдена."""
        with patch('builtins.print') as mock_print:
            self.editor.edit_task(self.tasks, self.storage)
            mock_print.assert_called_once_with("Задача не найдена.")


class TestTaskDeletion:
    @pytest.fixture
    def setup(self):
        """Создаем фиктивные задачи и мок хранилище задач."""
        tasks = [
            Task(id=1,
                 title='Задача 1',
                 description='Описание 1',
                 category='Категория 1',
                 due_date='2020-01-01',
                 priority='Высокий',
                 status='Новая'
                 ),

            Task(id=2,
                 title='Задача 2',
                 description='Описание 2',
                 category='Категория 2',
                 due_date='2007-10-10',
                 priority='Низкий',
                 status='Новая'
                 )
        ]
        mock_storage = MagicMock(spec=TaskStorage)
        return tasks, mock_storage

    def test_delete_existing_task(self, setup):
        """Проверяет, что задача успешно удаляется, когда вводится существующий ID."""
        tasks, mock_storage = setup
        task_deleter = TaskDeleter()

        with patch('builtins.input', return_value='1'):
            result = task_deleter.delete_task(tasks, mock_storage)

        assert result is True
        assert len(tasks) == 1
        mock_storage.save_tasks.assert_called_once_with(tasks)

    def test_delete_non_existing_task(self, setup):
        """Проверяет, что метод возвращает False и не изменяет список задач, когда вводится несуществующий ID."""
        tasks, mock_storage = setup
        task_deleter = TaskDeleter()

        with patch('builtins.input', return_value='3'):
            result = task_deleter.delete_task(tasks, mock_storage)

        assert result is False
        assert len(tasks) == 2
        mock_storage.save_tasks.assert_not_called()


def test_search_tasks():
    """Проверяет, что поиск по заголовку задачи возвращает правильные результаты."""
    tasks = [
        Task(1,
             "Задача 1",
             "Описание 1",
             "категория 1",
             "2007-05-01",
             "высокий",
             "открыт"
             ),

        Task(2,
             "Задача 2",
             "Описание 2",
             "категория 2",
             "2024-10-02",
             "средний",
             "закрыт"
             ),
    ]

    searcher = TaskSearcher()

    with patch('builtins.input', return_value='Задача 1'):
        found_tasks = searcher.search_tasks(tasks)

        assert len(found_tasks) == 1
        assert found_tasks[0].title == "Задача 1"
        assert found_tasks[0].description == "Описание 1"

    with patch('builtins.input', return_value='не существующая задача'):
        found_tasks = searcher.search_tasks(tasks)

        assert len(found_tasks) == 0