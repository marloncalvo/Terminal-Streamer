
var express = require('express');
var app = express();
var path = require('path');
var http = require('http').Server(app);
var io = require('socket.io')(http);
var port = process.env.PORT || 3000;

var zmq = require('zeromq');
var responder = zmq.socket('pull');

app.use(express.static(__dirname));

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', function(socket){
  responder.on('message', function(request) {
    console.log(request.toString());
    socket.emit('post', request.toString());
  });
  socket.on('request', function(msg){
    console.log(msg);
    socket.emit('post', msg);
  });
});

responder.bind('tcp://*:5555', function(err) {
  if (err) {
    console.log(err);
  } else {
    console.log("Listening on 5555...");
  }
});

http.listen(port, function(){
  console.log('listening on *:' + port);
});

process.on('SIGINT', function() {
  responder.close();
});

