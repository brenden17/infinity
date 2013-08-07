class A(object):
    def speak(cls, msg):
        print cls
        print msg

    @classmethod
    def walk(self, msg):
        print self
        print self.__name__
        print msg

    @staticmethod
    def swimming(msg):
        print msg

if __name__ == '__main__':
    a = A()
    a.speak('a')
    A.speak(a, 'a')
    #a.speak('0', 'a')
    A.walk('a')
    A.swimming('a')
