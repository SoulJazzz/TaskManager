from manager.task_creator import TaskCreator
from manager.task_delete import TaskDeleter
from manager.task_editor import TaskEditor
from manager.task_searcher import TaskSearcher
from manager.task_storage import TaskStorage
from manager.task_viewer import TaskViewer


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
