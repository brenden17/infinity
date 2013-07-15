from mongoengine import *

connect('test')

class User(Document):
    email = StringField(required=True)

if __name__ == '__main__':
    c = User(email='chulwook.jeon@gmail.com')
    c.save()
    for u in User.objects:
        print u.email
