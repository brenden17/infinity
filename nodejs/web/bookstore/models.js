var mongoose = require('mongoose');

var Schema = mongoose.Schema;

var Category = new Schema({
	name: String
});

var BookSchema = new Schema({
	title: {type: String, required: True},
	description: {type: String, required: False},
	publisher: {type: String, required: False},
	categories: [Category],
	published_year: {type: Number, required: False, min: 1900, max: 2100},
	modified: {type: Date, default: Date.now} 
});

exports = mongoose.model('Book', BookSchema);
