printjson(db.getCollectionNames());

var c = db.user.find();
while(c.hasNext()){
	printjson(c.next());
}

