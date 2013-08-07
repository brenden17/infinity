import inspect

class MetaChoice(type):
    def __init__(cls, name, bases, classdict):
        cls._data = list()
        for name, value in classdict.items():
            if name == 'attr':
                for idx, item in enumerate(value):
                    cls._data.append((idx, item.capitalize()))


class MyChoice(object, metaclass=MetaChoice):
    pass

if __name__ == '__main__':
    class MyUser(MyChoice):
        attr = ('user', 'admin')
    m = MyUser()
    print(m._data)
