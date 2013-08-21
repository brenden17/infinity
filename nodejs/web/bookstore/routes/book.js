var Book = require('../models);

exports.create = function(req, res) {
	new Book(req.body.title).save();
	res.send({'new book':req.body.title});
}

exports.findAll = function(req, res) {
	Book.find(function(err, result) {
		res.send(result);
	});
}

exports.findById = function(req, res) {
	res.send([{id:req.params.id}]);
}


