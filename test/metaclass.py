import inspect

class Choice(object):
    class __metaclass__(type):
        def __init__(cls, name, bases, classdict):
            cls._data = []
            for name, value in inspect.getmembers(cls):
                #print name, value
                if not name.startswith('_') and not inspect.isfunction(value):
                    if isinstance(value, tuple) and len(value)>1:
                        data = value
                    else:
                        data = (value, ''.join([x.capitalize() for x in
                            name.split('_')]))

                    cls._data.append(data)
                    setattr(cls, name, data[0])

        def __iter__(self):
            for value, data in self._data:
                yield value, data

if __name__ == '__main__':
    class User(Choice):
        User = 1
        Admin = 2, 'admin' 
    print list(User)
    m = User()
