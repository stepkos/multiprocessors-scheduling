from config import *
from task_supervisor import TaskSupervisor


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
