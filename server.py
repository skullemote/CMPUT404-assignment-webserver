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
        self.data = self.request.recv(1024).strip()
        #print out the received request
        print ("Got a request of: %s\n" % self.data)
        #sending back a response to the client by using utf-8 encoding
        self.request.sendall(bytearray("OK",'utf-8'))

        #parsing HTTP request header lines
        request_lines = self.data.decode('utf-8').split('\r\n')
        #splits the first line of the request into method, path, version
        method, path, version = request_lines[0].split(' ')

        #checking if the method is GET
        if method != 'GET':
            self.send_response(405)
            return
        
        #maps the request path to the local path
        local_path = self.map_path(path)

        #give a 404 error if the path does not exist
        if not os.path.exists(local_path):
            self.send_response(404)
            return
        
        #if the request path is a directory, append index.html to the path
        if os.path.isdir(local_path):
            local_path = os.path.join(local_path, 'index.html')
            #checkig if the index.html exists
            if not os.path.exists(local_path):
                self.send_response(404)
                return
            
        #mime type describes the type of data in the file
        mime_type = self.get_mime_type(local_path)
        
        #opens the file and reads the content into the 'content' variable
        with open(local_path, 'r') as f:
            content = f.read()

        #this sends a 200 OK response to the client mentionign the content type and length
        self.send_response(200)
        self.send_header('Content-Type', mime_type)
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.request.sendall(content)

    def map_path(self, path):
        #constructs the local path from the request path
        #www nedds to be in the same directory as the server.py
        #getcwd() returns the current working directory
        www_path = os.path.join(os.getcwd(), 'www')
        #path.lstrip('/') removes the leading '/' from the path
        #os.path.join() joins the path with the www_path
        #os.path.normpath() normalizes the path and makes sure that the path is valid
        local_path = os.path.normpath(os.path.join(www_path, path.lstrip('/')))
        return local_path
    
    def get_mime_type(self, path):
        #splits the path into the file name and extension
        #we need the extension to get the mime type
        file_extension = os.path.splitext(path)[1]
        #this dictionary maps the file extension to the mime type
        mime_type = {
            '.html': 'text/html',
            '.css': 'text/css'
        }
        #returns a default MIME type of 'application/octet-stream'
        #which is a generic binary file type used when the MIME type is unknown or not specified.
        return mime_type.get(file_extension, 'application/octet-stream')
    
    def send_response(self, status_code):
        status_text = {
            200: 'OK',
            404: 'Not Found',
            405: 'Method Not Allowed'
        }.get(status_code, 'Unknown')
        #formats the response
        response = 'HTTP/1.1 {} {}\r\n'.format(status_code, status_text)
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
