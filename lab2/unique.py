import random

class Unique(object):
    def __init__(self, items, **kwargs):
        self.ignore_case = kwargs.get('ignore_case', False)
        self.seen = set()
        self.items = iter(items)

    def __next__(self):
        for item in self.items:
            comparison_item = item.lower() if self.ignore_case and isinstance(item, str) else item
            if comparison_item not in self.seen:
                self.seen.add(comparison_item)
                return item
        raise StopIteration
    def __iter__(self):
        return self

data = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
for unique_item in Unique(data):
    print(unique_item, end=" ")

print('\n')

def gen_random(count, start, end):
    for _ in range(count):
        yield random.randint(start, end)

data = gen_random(10, 1, 3)
for unique_item in Unique(data):
    print(unique_item, end=" ")

print('\n')

data = ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']
for unique_item in Unique(data):
    print(unique_item, end=" ")

print('\n')

for unique_item in Unique(data, ignore_case=True):
    print(unique_item, end=" ")