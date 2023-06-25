import random
from dataclasses import dataclass
from config import *


@dataclass
class Task:
    processor: int
    load_level: float
    appearance_time: int
    duration_time: int

    @classmethod
    def generate_tasks(cls):
        tasks = []
        random.seed(SEED)
        for i in range(AMOUNT_OF_TASKS):
            tasks.append(cls(
                processor=random.randint(0, AMOUNT_OF_PROCESSORS - 1),
                load_level=random.uniform(*LOAD_LEVEL),
                appearance_time=random.randint(0, MAX_APPEARANCE_TIME),
                duration_time=random.randint(*DURATION_TIME)
            ))
        return tasks
