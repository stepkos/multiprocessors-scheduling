from dataclasses import dataclass
import random

AMOUNT_OF_TASKS = 100
AMOUNT_OF_PROCESSORS = 5
MAX_APPEARANCE_TIME = 100
DURATION_TIME = (3, 10)
LOAD_LEVEL = (0.1, 0.9)


@dataclass
class Task:
    processor: int
    load_level: float
    appearance_time: int
    duration_time: int


class TaskList:
    def __init__(self):
        self.tasks = self.generate_tasks()
        self.tasks.sort(key=lambda task: task.appearance_time)

    @staticmethod
    def generate_tasks():
        tasks = []
        for i in range(AMOUNT_OF_TASKS):
            tasks.append(Task(
                processor=random.randint(0, AMOUNT_OF_PROCESSORS - 1),
                load_level=random.uniform(*LOAD_LEVEL),
                appearance_time=random.randint(0, MAX_APPEARANCE_TIME),
                duration_time=random.randint(*DURATION_TIME)
            ))
        return tasks


task_list = TaskList()
for task in task_list.tasks:
    print(task)
