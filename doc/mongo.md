# [mongodb](http://mongodb.org)

## basic command
* connection

~~~
$mongo
~~~

* select db and get cursor

~~~
showdbs
use mydb
show collections
db.collectiosn.find()

var c = db.collection.find()
while(c.hasNext()) printjson(c.next())
printjson(c[1])
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

// output {'f':1}

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
