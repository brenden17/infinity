var application_root = __dirname,
	express = require('express'),
	book = require('./routes/book');

var app = express();

app.configure(function() {
	app.use(express.logger('dev'));
	app.use(express.bodyParser());
});

app.get('/book', book.findAll);
app.get('/book/:id', book.findById);
app.post('/book', book.create);
app.put('/book/:id', book.update);
app.delete('/book/:id', book.delete);
app.listen(8080);
