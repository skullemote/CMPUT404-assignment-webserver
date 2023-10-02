#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        #code reads upto 1024 bytes of data from the socket
        #stores it in self.data
        #self.request is a socket object
        self.data = self.request.recv(1024).strip().decode('utf-8')
        #print out the received request
        print ("Got a request of: %s\n" % self.data)
        #sending back a response to the client by using utf-8 encoding
        #self.request.sendall(bytearray("OK",'utf-8'))
        
        
        
        method = self.data.split()[0]
        path = self.data.split()[1]

        #checking if the method is GET
        if method[:3] != 'GET':
            self.send_response(405)
            return
        else:
            if ".." in path:
                self.send_response(404)
                return
            
            elif path[-1] == '/':
                fullpath = os.getcwd()+ "/www" + path + 'index.html'
                try:
                    file = open(fullpath)
                    f = file.read()
                    file.close()
                except:
                    self.send_response(404)
                    return
                content_type = 'text/html'
                content_length = len(f)
                self.send_response(200,content_type, content_length)
                return
            
            elif path[-5:] == ".html":
                fullpath = os.getcwd()+ "/www" + path
                try:
                    file = open(fullpath)
                    f = file.read()
                    file.close()
                except:
                    self.send_response(404)
                    return
                content_type = 'text/html'
                content_length = len(f)
                self.send_response(200,content_type, content_length)
                return
           
            elif path[-4:] == ".css":
                fullpath = os.getcwd()+ "/www" + path
                try:
                    file = open(fullpath)
                    f = file.read()
                    file.close()
                except:
                    self.send_response(404)
                    return
                content_type = 'text/css'
                content_length = len(f)
                self.send_response(200,content_type, content_length)
                
            
            else:
                fullpath = os.getcwd()+ "/www" + path + "/index.html"
                try:
                    file = open(fullpath)
                    f = file.read()
                    file.close()
                except:
                    self.send_response(404)
                    return
                self.send_response(301,  "Location: {}/\r\n".format(path))

    
    def send_response(self, status_code, content_type=None, content_length=None,Header=None):
        status_text = {
            200: 'OK',
            404: 'Not Found',
            405: 'Method Not Allowed'
        }.get(status_code, 'Unknown')
        #formats the response
        response = 'HTTP/1.1 {} {}\r\n'.format(status_code, status_text)
        if content_type:
            response += 'Content-Type: {}\r\n'.format(content_type)
        if content_length:
           response += 'Content-Length: {}\r\n'.format(content_length)
        if Header:
            response += Header
        
        #sends the response to the client with utf-8 encoding
        self.request.sendall(bytearray(response, 'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
