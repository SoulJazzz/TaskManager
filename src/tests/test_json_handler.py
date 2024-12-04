import json
import pytest
from unittest.mock import mock_open, patch
from handler.json_handler import Storage
from tasks.task import Task


@pytest.fixture
def storage():
    return Storage('test_tasks.json')


def test_load_tasks_file_not_found(storage):
    with patch('builtins.open', side_effect=FileNotFoundError):
        tasks = storage.load_tasks()
    assert tasks == []


def test_load_tasks_success(storage):
    mock_tasks = [
        {'id': 1, 'title': 'Изучить основы FastAPI', 'description': '', 'category': '', 'due_date': '', 'priority': '', 'status': ''},
        {'id': 2, 'title': 'Изучить Django', 'description': '', 'category': '', 'due_date': '', 'priority': '', 'status': ''}
    ]
    m = mock_open(read_data=json.dumps(mock_tasks))

    with patch('builtins.open', m):
        tasks = storage.load_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == 'Изучить основы FastAPI'
    assert tasks[1].title == 'Изучить Django'


def test_save_tasks(storage):
    task1 = Task(id=1, title='Изучить основы FastAPI', description='', category='', due_date='', priority='', status='')
    task2 = Task(id=2, title='Изучить Django', description='', category='', due_date='', priority='', status='')
    tasks = [task1, task2]

    m = mock_open()
    with patch('builtins.open', m):
        storage.save_tasks(tasks)

    m().write.assert_called_once_with(json.dumps([task.to_dict() for task in tasks], indent=4, ensure_ascii=False))


def test_add_task(storage):
    task = Task(1, 'Изучить основы FastAPI', '', '', '', '', '')

    with patch.object(storage, 'load_tasks', return_value=[]):
        with patch.object(storage, 'save_tasks') as mock_save:
            storage.add_task(task)
            mock_save.assert_called_once_with([task])
