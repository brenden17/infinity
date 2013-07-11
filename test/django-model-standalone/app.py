import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.conf import settings
from data.models import Tweet

t = Tweet(text='jeon')
t.save()

print 'aaa'

