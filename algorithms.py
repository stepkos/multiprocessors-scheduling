import statistics
from config import *
from task_supervisor import TaskSupervisor


# noinspection DuplicatedCode
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
        def __init__(self, algo_name, time):
            self.algo_name = algo_name
            self.time = time
            self.processors_load_sum = [0] * AMOUNT_OF_PROCESSORS
            self.migrate_requests_amount = 0
            self.migrate_amount = 0

        @property
        def processors_load_avg(self):
            return [load_sum / self.time.total for load_sum in self.processors_load_sum]

        @property
        def processors_load_std(self):
            return statistics.stdev(self.processors_load_avg)

        @property
        def system_load_avg(self):
            return sum(self.processors_load_avg) / AMOUNT_OF_PROCESSORS

        def __str__(self):
            return f"----- {self.algo_name.upper()} ----- \n" \
                   f"processors_load_avg: {[round(i, 4) for i in self.processors_load_avg]}, \n" \
                   f"processors_load_std: {round(self.processors_load_std, 4)}, \n" \
                   f"system_load_avg: {round(self.system_load_avg, 4)}, \n" \
                   f"migrate_requests_amount: {self.migrate_requests_amount}, \n" \
                   f"migrate_amount: {self.migrate_amount} \n"

    @staticmethod
    def lazy_student(supervisor: TaskSupervisor):
        time = Algorithms.Time()
        result = Algorithms.Result('lazy student', time)
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
                    processors = list(range(AMOUNT_OF_PROCESSORS))
                    processors.remove(task.processor)
                    for processor in random.sample(processors, LAZY_CALL_RANDOM_PROCESSORS_AMOUNT):
                        result.migrate_requests_amount += 1
                        if processors_load[processor] < LAZY_LOAD_THRESHOLD:
                            task.processor = processor
                            processors_load[processor] += task.load_level
                            result.migrate_amount += 1
                            break
                    else:
                        processors_load[task.processor] += task.load_level
                time.executing += 1

            for idx in range(AMOUNT_OF_PROCESSORS):
                result.processors_load_sum[idx] += processors_load[idx]

        return result

    @staticmethod
    def ambitious_student(supervisor: TaskSupervisor):
        time = Algorithms.Time()
        result = Algorithms.Result('ambitious student', time)
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
                    if processors_load[task.processor] < AMBITIOUS_LOAD_THRESHOLD:
                        processors_load[task.processor] += task.load_level
                    else:
                        processors = list(range(AMOUNT_OF_PROCESSORS))
                        processors.remove(task.processor)
                        for processor in random.sample(processors, AMOUNT_OF_PROCESSORS - 1):
                            result.migrate_requests_amount += 1
                            if processors_load[processor] < AMBITIOUS_LOAD_THRESHOLD:
                                task.processor = processor
                                processors_load[processor] += task.load_level
                                result.migrate_amount += 1
                                break
                        else:
                            processors_load[task.processor] += task.load_level
                time.executing += 1

            for idx in range(AMOUNT_OF_PROCESSORS):
                result.processors_load_sum[idx] += processors_load[idx]

        return result

    @staticmethod
    def altruistic_student(supervisor: TaskSupervisor):
        time = Algorithms.Time()
        result = Algorithms.Result('altruistic student', time)
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
                    if processors_load[task.processor] < ALTRUISTIC_LOAD_THRESHOLD:
                        processors_load[task.processor] += task.load_level
                    else:
                        processors = list(range(AMOUNT_OF_PROCESSORS))
                        processors.remove(task.processor)
                        for processor in random.sample(processors, AMOUNT_OF_PROCESSORS - 1):
                            result.migrate_requests_amount += 1
                            if processors_load[processor] < ALTRUISTIC_LOAD_THRESHOLD:
                                task.processor = processor
                                processors_load[processor] += task.load_level
                                result.migrate_amount += 1
                                break
                        else:
                            processors_load[task.processor] += task.load_level
                time.executing += 1

            for processor in random.sample(range(AMOUNT_OF_PROCESSORS), AMOUNT_OF_PROCESSORS):
                if processors_load[processor] <= ALTRUISTIC_GET_TASKS_FROM_OTHER_THRESHOLD:
                    most_loaded_processor = processors_load.index(max(processors_load))
                    result.migrate_requests_amount += 1
                    if processors_load[most_loaded_processor] > ALTRUISTIC_LOAD_THRESHOLD:
                        # give task from most_loaded_processor to processor
                        tasks_of_processors = supervisor.get_current_tasks_of_processor(most_loaded_processor)
                        if tasks_of_processors:
                            task = random.choice(tasks_of_processors)
                            processors_load[task.processor] -= task.load_level
                            processors_load[processor] += task.load_level
                            task.processor = processor
                            result.migrate_amount += 1

            for idx in range(AMOUNT_OF_PROCESSORS):
                result.processors_load_sum[idx] += processors_load[idx]

        return result
