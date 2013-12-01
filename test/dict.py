import inspect

def s(**params):
    for k, v in params.iteritems():
        split = k.split('__', 0)
        print 0
        print split
        split = k.split('__', 1)
        print 1 
        print split
        split = k.split('__', 2)
        print 2 
        print split

if __name__ == '__main__':
    #s(**{'a':1, 'b':2})
    a = s(ianova__kdaf__j=10, svc__C__j=.1)
    print inspect.getargspec(s)
