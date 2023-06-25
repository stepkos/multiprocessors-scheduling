from collections import namedtuple
from dataclasses import dataclass
import random

AMOUNT_OF_TASKS = 100
AMOUNT_OF_PROCESSORS = 5
MAX_APPEARANCE_TIME = 100
DURATION_TIME = (3, 10)
LOAD_LEVEL = (0.1, 0.9)
# SEED = 123
SEED = random.randint(0, 1000000)

LAZY_CALL_RANDOM_PROCESSORS_AMOUNT = 3
LAZY_PROCESSOR_THRESHOLD = 0.7


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


class TaskSupervisor:
    def __init__(self):
        self.tasks = Task.generate_tasks()
        self.tasks.sort(key=lambda task: task.appearance_time)

    def is_done(self):
        return len(self.tasks) == 0

    def pop_done_tasks(self, time):
        removed_tasks = list(filter(lambda task: task.appearance_time + task.duration_time <= time, self.tasks))
        self.tasks = list(filter(lambda task: task.appearance_time + task.duration_time > time, self.tasks))
        return removed_tasks

    def get_tasks_to_assign(self, time):
        return list(filter(lambda task: task.appearance_time == time, self.tasks))


class Algorithms:

    class Time:
        def __init__(self):
            self.executing = 0
            self.waiting = 0

        @property
        def total(self):
            return self.executing + self.waiting

        def __str__(self):
            return f"executing: {self.executing}, waiting: {self.waiting}, total: {self.total}"

    class Result:
        def __init__(self, time):
            self.processors_load_sum = [0] * AMOUNT_OF_PROCESSORS
            self.time = time

        @property
        def processors_load_avg(self):
            return [load_sum / self.time.total for load_sum in self.processors_load_sum]

        @property
        def system_load_sum(self):
            return sum(self.processors_load_sum)

        @property
        def system_load_avg(self):
            return sum(self.processors_load_avg) / AMOUNT_OF_PROCESSORS

        def __str__(self):
            return f"processors_load_avg: {self.processors_load_avg}, system_load_avg: {self.system_load_avg}"

    @staticmethod
    def lazy_student(supervisor: TaskSupervisor):
        time = Algorithms.Time()
        result = Algorithms.Result(time)
        processors_load = [0] * AMOUNT_OF_PROCESSORS

        while not supervisor.is_done():
            removed_tasks = supervisor.pop_done_tasks(time.total)
            for task in removed_tasks:
                processors_load[task.processor] -= task.load_level

            tasks_to_assign = supervisor.get_tasks_to_assign(time.total)
            if len(tasks_to_assign) == 0:
                time.waiting += 1
            else:
                # Algorithm main logic
                for task in tasks_to_assign:
                    for _ in range(LAZY_CALL_RANDOM_PROCESSORS_AMOUNT):
                        processor = random.randint(0, AMOUNT_OF_PROCESSORS - 1)
                        if processors_load[processor] < LAZY_PROCESSOR_THRESHOLD:
                            task.processor = processor
                            processors_load[processor] += task.load_level
                            break
                    else:
                        processors_load[task.processor] += task.load_level
                time.executing += 1

            for idx in range(AMOUNT_OF_PROCESSORS):
                result.processors_load_sum[idx] += processors_load[idx]

        return result


def main():
    result = Algorithms.lazy_student(TaskSupervisor())
    print(result)


if __name__ == '__main__':
    main()
