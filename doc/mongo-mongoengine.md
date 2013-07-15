# [mongodb](http://mongodb.org)

## basic command
* connection

~~~
$mongo
~~~

* select db and get cursor

~~~
show dbs
use mydb
show collections
db.collectiosn.find()

var c = db.collection.find()
while(c.hasNext()) printjson(c.next())
printjson(c[1])
~~~

* remove database

~~~
show dbs
use mydb
db.dropDatabase()
~~~

* find document ($or, $and) 

~~~
db.collection.find({x:1})
db.collection.find({x:1, $or:[{y:'a'}, {y:'b'}]})
db.collection.findOne()
db.collection.find().limit(3)
db.collection.find().limit(3).skip(2) // skip second ite
db.collection.find().sort({x:1, y:-1}) //ascending:-1, descending:1
~~~

* insert, update, delete

~~~
db.collection.insert({x:1})
db.collection.update({x:1}, {$set:{y:'b'}})
db.collection.remove({x:1, y:'b'})
db.collection.remove() // delete all documents
db.collection.drop() // drop collection
~~~

* conditional operations($lt, $gt, $lte, $gte, $in, $nin, $not)

~~~
db.collection.find({'age':{'$gt:47}})
db.collection.find({ $or : [ { "gender" : "m", "occupation" : "developer" } ], "age" : { "$gt" : 40 } }, { "first" : 1, "last" : 1, "occupation" : 1, "dob" : 1 } )
db.collection.find({"first":/(ma|to)*/i, "last":/(se|de)/i}) //regular expression
~~~

* MapReduce

~~~
var map = function() {
    emit({gender:this.gender}, {count:1});
}

// output {'f':[1, 1, 1]}

var reduce = function(key, values) {
    var result = {count:0};

    values.forEach(function(value){
        result.count += value.count
    })
} 

var res = db.collection.mapReduce(map, reduce, {out:'gender'}) // return output as gender

db.gender.find()

var res = db.collection.mapReduce(map, reduce, {out:'gender', query:{"gender":"f" }});
~~~


* toy example of mapreduce from [Kyle Banker](http://kylebanker.com/blog/2009/12/mongodb-map-reduce-basics/)

Articles has comments consist of text, author, and vote which reader gives. We want to find total vote per an author. We can some tranditional sql operations but this shows how mapreduce works and how apply more complex problems.

~~~
{text: 'great article', author:'kbanker', votes:2}

var map = function() {
    emit(this.author, {votes:this.votes});
};

var reduce = function(key, values) {
    var sum = 0;
    values.forEach(function(doc){
        sum += doc.votes;
    });
    return {votes:sum};
};

var op = db.comments.mapReduce(map, reduce, {out:'resutl'})
~~~

* running javascript file on mongodb

edit dummy.js
~~~

printjson(db.getCollectionNames());

var c = db.user.find();
while(c.hasNext()){
        printjson(c.next());
}

~~~

run on mongodb. ref-[methods](http://docs.mongodb.org/manual/reference/method/)

~~~
$mongo dummy.js
~~~

# [mongoengine](http://mongoengine.org/) for Python
I hate handling raw sql operations(including nosql). ORM or Object in databse provide many handy things. Django ORM can make me comfortable as choosing many different database systems such as sqlite3, mysql, even mongodb. When I have to choose one of that kind of database systems, I will use Django ORM. I have right to pick up my favorite one, I will pick up mongoengine which provides various functionalities and handling objects as data. Even it supports Django database.

* install

~~~
$ pip install mongoengine
~~~

* my [modelling](https://github.com/brenden17/infinity/tree/master/test/mongoengine)

* [tutorial](http://docs.mongoengine.org/en/latest/tutorial.html)
