var mongoose = require('mongoose');
var ToDo = mongoose.model('ToDo');
var utils = require('connect').utils;

exports.index = function(req, res, next){
  if( !req.cookies.user_id ){
    res.cookie( 'user_id', utils(24));
	console.log(req.cookies.user_id);
  }
  ToDo.find({
	  user_id:req.cookies.user_id
    }).
    sort('-updated_at').
    exec(function (err, todos, count){
	if(err){
	  return next(err);
	}
    res.render( 'index', {
      title : 'Todo',
      todos : todos
    });
  });
};

exports.create = function(req, res, next){
  console.log(req.cookies);
  new ToDo({
	user_id:req.cookies.user_id,	 
	what:req.body.what,
	updated_at:Date.now()
  }).save(function(err, ToDo, Count) {
	if(err){
	  return next(err);
	}
	 res.redirect('/');
  });	  
};

exports.edit = function(req, res, next){
  ToDo.findById(req.params.id,  function (err, todo){
	if(err){
	  return next(err);
	}
	if(todo.user_id !== req.cookies.user_id){
	  return utils.forbidden(res);
	}
	todo.what = req.body.what;
	todo.updated_at = Date.now();
	todo.save(function(err, todo, count){
		res.redirect('/');
	});
  });
};

exports.destroy = function(req, res, next){
  ToDo.findById(req.params.id, function(err, todo){
	if(err){
	  return next(err);
	}
	if(todo.user_id !== req.cookies.user_id){
	  return utils.forbidden(res);
	}
    todo.remove(function(err, todo){
	  res.redirect('/');
	});
  });
};

exports.current_user = function(req, res, next){
  if(!req.cookies.user_id){
    res.cookie('user_id', utils.uid(232));
  }
  next();
};
