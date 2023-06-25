from algorithms import Algorithms
from task_supervisor import TaskSupervisor


def main():
    print(Algorithms.lazy_student(TaskSupervisor()))
    print(Algorithms.ambitious_student(TaskSupervisor()))
    print(Algorithms.altruistic_student(TaskSupervisor()))


if __name__ == '__main__':
    main()
