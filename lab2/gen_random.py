from random import randint

def gen_random(num_count, begin, end):
    for _ in range(num_count):
        yield randint(begin, end)
print(list(gen_random(5, 1, 10)))