# Simple toy with Monogdb mapReduce

Suppose that I have my own business which is so small but deals with big money. I have been writing down financial book by myself since Jaunary of 2011. Today I want to know the months expension between 2011 and 2012.

Requiremnts

~~~
mongodb
mongoengine
~~~

Firstly, I make dummy(fake) data with mongoengine. The schema(Class) is so simple. The data is generated randomly.

~~~
class DailyBalance(me.Document):
    dayat = me.DateTimeField(default=datetime.now)
    income = me.FloatField()
    expense = me.FloatField()
~~~

You would have over 30 document after running python code. Then you need to create map and reduce code on mongo. Before that, you can check some commands on mongo.

~~~
$mongo
>show dbs
>show collections
>use yearlybalancedb
>db.dayly_balance.find()
~~~

Open analysis.js. You need two couple of map and reduce. One of them is for conbining everyday expense to month expense. The other one is for comparing between 2011 and 2012.

~~~
var year = db.daily_balance.mapReduce(yearMap, yearReduce, {out:'year'});
var compare = db.year.mapReduce(compareYearMap, compareYearReduce, {out:'compare'});
~~~

run script.
~~~
$mongo analysis.js 
~~~
Finally, you will see compare collections and 12 document.


