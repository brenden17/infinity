class Validator(object):
    def __init__(self):
        print 'validator'

    def __call__(self):
        print 'validator call'

class NameValidator(Validator):
    def __init__(self):
        super(NameValidator, self).__init__()
        print 'name validator'

    def __call__(self):
        super(NameValidator, self).__call__()
        print 'name validator call'

class AgeValidator(Validator):
    def __init__(self):
        super(AgeValidator, self).__init__()
        print 'age validator'

    def __call__(self):
        super(AgeValidator, self).__call__()
        print 'age validator call'

if __name__ == '__main__':
    validators = [AgeValidator(), NameValidator()]
    for v in validators:
        v()
