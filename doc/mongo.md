# [mongodb](http://mongodb.org)

## basic command
1.connection

~~~
mongo
~~~

1. select db and get cursor

~~~
showdbs
use mydb
show collections
db.collectiosn.find()

var c = db.collection.find()
while(c.hasNext()) printjson(c.next())
printjson(c[1])
~~~

1. find document

~~~
db.collection.find({x:1})
db.collection.findOne()
db.collection.find().limit(3)
~~~

1. insert, delete, change document
~~~
db.collection.insert({x:1})

~~~
