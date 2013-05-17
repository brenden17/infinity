def say(message='hello'):
    print message


def man(func=say, option=None):
    func(**option) if option else func()

if __name__ == '__main__':
    option = {'message':'I am a boy'}
    man(option=option)
    man()
