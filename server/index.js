var bodyParser = require('body-parser')
var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.use(express.static(__dirname));
app.use(bodyParser.text({ type: 'text/*' }))

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', function(socket){
  console.log('connected!')
  app.post('/new', function(req, res){
    res.end()
	  console.log('received ', req.body)
    socket.emit('post', req.body)
  });
});

http.listen(3000, function(){
  console.log('listening on *:' + 3000);
});
