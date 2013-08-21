/**
 * Module dependencies.
 */

var express = require('express');
var app = express();

// all environments
var http = require('http');
var path = require('path');
var appdir =  __dirname
app.set('port', process.env.PORT || 8080);
app.set('views', appdir + '/views');
app.set('view engine', 'ejs');
app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.cookieParser());
app.use(express.bodyParser());
app.use(express.methodOverride());
app.use(app.router);
app.use(express.static(path.join(appdir, 'public')));

// development only
if ('development' == app.get('env')) {
  app.use(express.errorHandler());
}

// models
var mongoose = require('mongoose');
require('./models');
app.configure('development', function() {
  mongoose.connect('mongodb://localhost/todos');
});

// routes
var routes = require('./routes');
var user = require('./routes/user');
//app.use(routes.current_user());
app.get('/', routes.index);
app.post('/create', routes.create);
app.get('/destroy/:id', routes.destroy);
app.post('/edit/:id', routes.edit);
app.get('/users', user.list);

http.createServer(app).listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
});
