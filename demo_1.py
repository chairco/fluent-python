# demo_1.py
import registration
import random


class BingoCage:

    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):
        return self.pick()


def demo_listcomp():
    """
    python2.x -> x='c', dummy='c'
    python3,x => x='my precious', dummy='abc'
    """
    x = 'my precious'
    dummy=[x for x in 'abc']
    print(x)
    print(dummy)


def deco(func):
    def inner():
        print('running inner()')
    return inner


@deco
def target():
    print('running target()')


if __name__ == '__main__':
    target()
    print(target)
    print(registration.registry)
    
    print('running BingoCage')
    bingo = BingoCage(range(3))
    print(bingo.pick())
    print(bingo())
