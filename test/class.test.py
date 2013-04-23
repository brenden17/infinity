class Parent(object):
    CLASS_STRING = 'Parnet Class'
    def __init__(self):
        self.name = 'self name'

    def self_call(self, a):
        print '== self method ================================'
        try:
            print 'print ' + self.name
        except Exception, e:
            print '*** Not access to self in self method'
            print str(e)

        try:
            print 'print ' + cls.CLASS_STRING
        except Exception, e:
            print '*** Not access to class in self method : cls'
            print str(e)

        try:
            print 'print ' + Parent.CLASS_STRING
        except Exception, e:
            print '*** Not access to class in self method : C'
            print str(e)

    @classmethod
    def class_call(cls, a):
        print '== class method ================================'
        try:
            print 'print ' + self.name
        except Exception, e:
            print '*** Not access to self in class method'
            print str(e)

        try:
            print 'print ' + cls.CLASS_STRING
        except Exception, e:
            print '*** Not access to class in class method'
            print str(e)

        try:
            print 'print ' + Parent.CLASS_STRING
        except Exception, e:
            print '*** Not access to class in class method : C'
            print str(e)

    @staticmethod
    def static_call(a):
        print '== static method ================================'
        try:
            print 'print ' + self.name
        except Exception, e:
            print '*** Not access to self in static method'
            print str(e)

        try:
            print 'print ' + cls.CLASS_STRING
        except Exception, e:
            print '*** Not access to class in static method'
            print str(e)

        try:
            print 'print ' + Parent.CLASS_STRING
        except Exception, e:
            print '*** Not access to class in static method : C'
            print str(e)

class Child(Parent):
    CLASS_STRING = 'Child Class'

class CallClass(object):
    def self_call(self, a):
        print 'print self call'

    def self_caller(self, a):
        print '== self method ================================'
        try:
            self.self_call(a)
        except Exception, e:
            print '*** Not access to self method in class method'
        try:
            self.class_call(a)
        except Exception, e:
            print '*** Not access to self method in class method'
        try:
            cls.class_call(a)
        except Exception, e:
            print '*** Not access to class method in class method'
        try:
            cls.self_call(a)
        except Exception, e:
            print '*** Not access to class method in class method'
        try:
            cls.static_call(a)
        except Exception, e:
            print '*** Not access to static method in class method'
        try:
            CallClass.static_call(a)
        except Exception, e:
            print '*** Not access to static method in class method'

    @classmethod
    def class_call(cls, a):
        print 'print class call'

    @classmethod
    def class_caller(cls, a):
        print '== class method ================================'
        try:
            self.self_call(a)
        except Exception, e:
            print '*** Not access to self method in class method'
        try:
            self.class_call(a)
        except Exception, e:
            print '*** Not access to self method in class method'
        try:
            cls.class_call(a)
        except Exception, e:
            print '*** Not access to class method in class method'
        try:
            cls.self_call(a)
        except Exception, e:
            print '*** Not access to class method in class method'
        try:
            cls.static_call(a)
        except Exception, e:
            print '*** Not access to static method in class method'
        try:
            CallClass.static_call(a)
        except Exception, e:
            print '*** Not access to static method in class method'

    @staticmethod
    def static_call(a):
        print 'static class'

    @staticmethod
    def static_caller(a):
        pass

if __name__ == '__main__':
    '''
    print '## Parent #######################'
    p = Parent()
    p.self_call('')
    p.class_call('')
    p.static_call('')
    Parent.class_call('')
    Parent.static_call('')

    print '## Child #######################'
    c = Child()
    c.self_call('')
    c.class_call('')
    c.static_call('')
    '''

    print '## caller #######################'
    c = CallClass()
    c.self_caller('')
    c.class_caller('')
    CallClass.class_caller('')
