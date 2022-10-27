# code taken from https://docs.python.org/3/library/socketserver.html, 2022-20-26.
# run this if flask is not allowed for this assignment.
# code is mostly reused from assignment webserver
import socketserver
import os

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        # https://stackoverflow.com/a/606199, Aaron Maenpaa
        split = (self.data.decode("utf-8").split(" "))
        method = split[0]

        if(method == "GET"):
            http_response_str = "HTTP/1.1 200 OK\r\n"

            # https://stackoverflow.com/a/7166139, Russ, 2022-09-28
            file_dir = os.path.dirname(__file__)
            file_dir = file_dir.replace("\\","/")
            filepath = split[1]
            filepath = filepath.replace("\\","/")

            print(file_dir+filepath)

            try:    
                with open(file_dir+filepath, encoding="utf-8") as f:
                    if(1):
                        cssfile=""
                        if("1" in filepath or "2" in filepath or "3" in filepath):
                            cssfile = file_dir+"/gutenberg/gutenberg.css"
                        elif("good" in filepath):
                            cssfile = file_dir+"/homepage/good.css"
                        elif("ugly" in filepath):
                            cssfile = file_dir+"/homepage/ugly.css"

                        # open css file...
                        with open(cssfile) as css, open(file_dir+filepath, encoding="utf-8") as html:
                            http_response_str += """Content-Type: text/html\r\n"""
                            self.request.sendall(http_response_str.encode())
                            self.request.sendall(("".join(html.readlines())).encode())
                            http_response = """\n<style type="text/css">\n""" +css.read() + "\n"
                            self.request.sendall(http_response.encode())
            except Exception as e:
                # throw error if file is not found...
                print(e)
                self.request.sendall("HTTP/1.1 404 Not Found".encode())

            


            

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()