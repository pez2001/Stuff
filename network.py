import socketserver

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


HOST, PORT = "localhost", 9999
server = socketserver.TCPServer((HOST, PORT), Handler)
server.serve_forever()