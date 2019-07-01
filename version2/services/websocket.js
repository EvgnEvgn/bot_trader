const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 8765 });
const connections = [];

wss.on('connection', function connection(ws) {
    ws.on('message', function incoming(message) {
        console.log('received: %s', message);
    });

    connections.push(ws);
});

module.exports = {
    sendAll: data=>{
        for(let ws of connections){
            ws.send(JSON.stringify(data));
        }
    }
};