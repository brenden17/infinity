var express = require('express'),
	books = require('./routes/book');

var app = express();

app.get('/book', books.findAll);
app.get('/book/:id', books.findById);
app.listen(8080);
