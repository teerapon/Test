
import socket

class Client( object ): #defines client class
    rbufsize= -1 #sets read buffer
    wbufsize= 0 #sets write buffer
    def __init__( self, address=('localhost',7000) ): #defines initialisation function
        self.server=socket.socket( socket.AF_INET, socket.SOCK_STREAM )#initiates socket by passing address and protocol parameters
        self.server.connect( address ) # connects to set address and port
        self.rfile = self.server.makefile('rb', self.rbufsize) #makes file object for response processing
        self.wfile = self.server.makefile('wb', self.wbufsize) # same as above but for writing/response sending
    def makeRequest( self, text ): # request function which will handle the data transfer
        self.wfile.write( text )
        data= self.rfile.read()
        self.server.close() # closes this instance of the connection
        return data

print "Connecting to Echo Server"
i = 0 #from here to end of file, infinite loop for message sending to server
while (i > -1):
    c= Client()
    response = c.makeRequest(raw_input("Enter something: "))
    print repr(response)
    print "Finished"
