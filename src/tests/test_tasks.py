import pytest

from tasks.task import Task


def test_task_initialization():
    task = Task(1, "Изучить основы FastAPI", "Пройти документацию по FastAPI и создать простой проект",
                "Обучение", "2024-11-30", "Высокий", "Не выполнена")
    assert task.id == 1
    assert task.title == "Изучить основы FastAPI"
    assert task.description == "Пройти документацию по FastAPI и создать простой проект"
    assert task.category == "Обучение"
    assert task.due_date == "2024-11-30"
    assert task.priority == "Высокий"
    assert task.status == "Не выполнена"


def test_task_to_dict():
    task = Task(1, "Изучить основы FastAPI", "Пройти документацию по FastAPI и создать простой проект",
                "Обучение", "2024-11-30", "Высокий", "Не выполнена")
    expected_dict = {
        "id": 1,
        "title": "Изучить основы FastAPI",
        "description": "Пройти документацию по FastAPI и создать простой проект",
        "category": "Обучение",
        "due_date": "2024-11-30",
        "priority": "Высокий",
        "status": "Не выполнена",
    }
    assert task.to_dict() == expected_dict
