var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var ToDoSchema = new Schema({
	user_id : String,
	what : String,
	updated_at : Date
});

mongoose.model('ToDo', ToDoSchema);
