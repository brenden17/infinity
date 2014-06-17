var setup = function(){
    var conn = new Mongo();
    var db = conn.getDB("yearlybalancedb");
    return db;
};

var yearMap = function(){
    emit({year:this.dayat.getFullYear(), month:this.dayat.getMonth()}, {count:1, expense:this.expense, income:this.income});
};

var yearReduce = function(key, values){
	var total = 0;
    var totalExpense = 0;
    var totalIncome = 0;

    values.forEach(function(value){
    	//result.sumMonth += value.expense;
		total += value.count;
        totalExpense += value.expense;
        totalIncome += value.income;
    });
    return {count:total, expense:totalExpense, income:totalIncome};
};

var db = setup();
var year = db.daily_balance.mapReduce(yearMap, yearReduce, {out:'year'});

var compareYearMap = function(){
    var k = '2011-2012-' + this._id["month"].toString();
    emit(k, {expense:this.value["expense"], income:this.value["income"]});
};

var compareYearReduce = function(key, values){
	var diffExpense = 0;
	var diffIncome = 0;
	 
    diffExpense = values[0].expense - values[1].expense;
    diffIncome = values[0].income - values[1].income;
    return {expense:diffExpense, income:diffIncome};
};

var compare = db.year.mapReduce(compareYearMap, compareYearReduce, {out:'compare'});
