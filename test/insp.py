import inspect

class X(object):
    """X class """
    x = 1

xx = type('Y', (object,), {'__doc__':'test','x':1})

for name, data in inspect.getmembers(xx):
    if name == '__builtins__':
        continue
    print '%s :' % name, repr(data)

print('============================')
for name, data in inspect.getmembers(X):
    if name == '__builtins__':
        continue
    print '%s :' % name, repr(data)
print(X.__class__)
print(X.__class__.__class__)
