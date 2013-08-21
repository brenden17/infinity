from datetime import datetime
import mongoengine as me

DBNAME = 'tweetdb'
me.connect(DBNAME)


class User(me.Document):
   idstr = me.StringField(required=True, unique=True, primary_key=True)
   name = me.StringField(max_length=50)
   screen_name = me.StringField(max_length=50)


class Status(me.Document):
   idstr = me.StringField(required=True, unique=True, primary_key=True)
   text = me.StringField(max_length=150)
   processed_text = me.StringField(max_length=150)
   create_at = me.DateTimeField(default=datetime.now)
   user = me.ListField(me.ReferenceField(User))
   words = me.ListField(me.ReferenceField('Word'))
   links = me.ListField(me.ReferenceField('Link'))


class Word(me.Document):
   stem = me.StringField(required=True, unique=True)
   status = me.ListField(me.ReferenceField(Status))


class Link(me.Document):
   url= me.StringField(required=True, unique=True)
   status = me.ListField(me.ReferenceField(Status))

if __name__ == '__main__':
    u = User()
    print(dir(u))
    print(u.name)
