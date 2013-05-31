class P(object):
    CLASS_STRING = 'Parnet Class'
    def __init__(self):
        self.name = 'self name'
        print self.CLASS_STRING

    @classmethod
    def say(cls):
        print cls.CLASS_STRING


if __name__ == '__main__':
    #P.say()
    p = P()
    #p.say('aaa')
