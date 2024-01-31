let http: any = require("http");

http.createServer(function (req: any, res: any) {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end('Hello World');
}).listen(8080)
