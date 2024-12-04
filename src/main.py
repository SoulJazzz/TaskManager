from manager.task_manager import TaskManager


def main():
    """Выполнение административных задач"""

    task_manager = TaskManager()

    actions = {
        '1': task_manager.view_tasks,
        '2': task_manager.add_task,
        '3': task_manager.edit_task,
        '4': task_manager.delete_task,
        '5': task_manager.search_tasks,
        '0': exit_program
    }

    while True:
        print("\nМенеджер задач")
        print("1. Просмотр")
        print("2. Добавление")
        print("3. Изменение")
        print("4. Удаление")
        print("5. Поиск")
        print("0. Выход")

        choice = input("Выберите действие: ")

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Неверный выбор. Попробуйте снова.")


def exit_program():
    """Выход из программы"""

    print("Выход из программы.")
    exit()


if __name__ == "__main__":
    main()
