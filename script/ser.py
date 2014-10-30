import SocketServer #imports the socket server library

class EchoHandler( SocketServer.StreamRequestHandler ): #declares the class
    def handle(self): #installs handler
        input= self.request.recv(1024) #defines request buffer
        print "****************Input: %r" % ( input, ) #prints data received
        self.request.send("!!!!!!!!!!!!!!!!!!!!!!Received: %r" % ( input, ) ) #sends message to client saying..

#.."message received"

server= SocketServer.TCPServer( ("",7000), EchoHandler )#adds listener at port 7000
print "-----------------------------------Starting Server... Yo Yo Ya YA Go go Go"
server.serve_forever() #enables the server to run forever as long as a client is connected

