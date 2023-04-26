import socketserver
import socket

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):

        while True:
            global server

            # self.request is the TCP socket connected to the client
            self.data = self.request.recv(1024).strip()
            print("{} wrote:".format(self.client_address[0]))
            print(self.data, len(self.data))
            # just send back the same data, but upper-cased
            self.request.sendall(self.data.upper())
            self.request.sendall(1,100.34,322.88)
            print("sent", self.data.upper())
            if len(self.data) == 0:
                server.shutdown()


if __name__ == "__main__":
    HOST, PORT = "192.168.0.1", 9998

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
