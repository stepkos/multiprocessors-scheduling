from task import Task


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
