var setup = function(){
    var conn = new Mongo();
    var db = conn.getDB("yearlybalancedb");
    return db;
};

var yearMap = function(){
    var year = this.dayat.getFullYear().toString();
    var month = this.dayat.getMonth() + 1;
    var k = year.toString() + '-' +  month.toString();
    //var k = new Array(year, month);// error 
    var v = this.expense;
    emit(k, {expense:v});
};

var yearReduce = function(key, values){
    var result = {sumMonth:0};
    values.forEach(function(value){
        result.sumMonth += value.expense;
    });
    result.meanMonth = result.sumMonth / 12;
    return result;
};

var db = setup();
var year = db.daily_balance.mapReduce(yearMap, yearReduce, {out:'year'});

var compareYearMap = function(){
    var k = '2011-2012-' + this._id.split('-')[1];
    var v = this.value['sumMonth'];
    emit(k, {month:v});
};

var compareYearReduce = function(key, values){
    var result = {diff:0, percent:0};
    result.diff = values[0].month - values[1].month;
    result.percent = (values[0].month - values[1].month)/values[0].month*100;
    return result;
};

var compare = db.year.mapReduce(compareYearMap, compareYearReduce, {out:'compare'});
