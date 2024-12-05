PRIORITY = ['Низкий', 'Средний', 'Высокий']
STATUS = ['Выполнена', ' Не выполнена']

INPUT_TASK_NAME = "Введите название задачи: "
INPUT_TASK_DESCRIPTION = "Введите описание задачи: "
INPUT_TASK_CATEGORY = "Введите категорию задачи: "
INPUT_DUE_DATE = "Введите срок выполнения (формат: ГГГГ-ММ-ДД): "
INPUT_PRIORITY = f"Введите приоритет ({', '.join(PRIORITY)}): "
INPUT_STATUS = f"Введите статус ({', '.join(STATUS)}): "

EMPTY_INPUT_ERROR = "Ввод не может быть пустым. Пожалуйста, введите снова."

INVALID_DATE_ERROR = "Необходимо ввести дату в правильном формате (ГГГГ-ММ-ДД)."
INVALID_PRIORITY_ERROR = f"Приоритет должен быть: {', '.join(PRIORITY)}."
INVALID_STATUS_ERROR = f"Статус должен быть: ({', '.join(STATUS)})"

INPUT_TASK_ID = "Введите ID задачи для редактирования: "
INPUT_NEW_TITLE = "Новое название задачи (текущее: {}): "
INPUT_NEW_DESCRIPTION = "Новое описание задачи (текущее: {}): "
INPUT_NEW_CATEGORY = "Новая категория задачи (текущая: {}): "
INPUT_NEW_DUE_DATE = "Новый срок выполнения (текущий: {}): "
INPUT_NEW_PRIORITY = f"Новый приоритет ({', '.join(PRIORITY)}) (текущий: {{}}): "
INPUT_NEW_STATUS = f"Новый статус ({', '.join(STATUS)}) (текущий: {{}}): "
INPUT_ATTEMPTS_EXCEEDED = "Превышено количество попыток ввода даты."
