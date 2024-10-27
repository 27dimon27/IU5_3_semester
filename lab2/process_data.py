import json
import random
from cm_timer import cm_timer_1
from print_result import print_result


path = 'data_light.json'
with open(path, encoding="utf-8") as f:
    data = json.load(f)


@print_result
def f1(arg):
    return sorted(set(job['job-name'].strip() for job in arg), key=str.casefold)


@print_result
def f2(arg):
    return list(filter(lambda job: job.lower().startswith('программист'), arg))


@print_result
def f3(arg):
    return list(map(lambda job: f"{job} с опытом Python", arg))


@print_result
def f4(arg):
    salaries = [random.randint(100000, 200000) for _ in arg]
    return [f"{job}, зарплата {salary} руб." for job, salary in zip(arg, salaries)]


if __name__ == '__main__':
    with cm_timer_1():
        f4(f3(f2(f1(data))))