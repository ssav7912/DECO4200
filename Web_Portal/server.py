from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 8080

class MyServer(SimpleHTTPRequestHandler):
    # def do_GET(self):
    #     self.send_response(200)
    #     self.send_header("Content-type", "application/json")
    #     self.end_headers()

    def do_PUT(self):
        filename = os.path.basename(self.path)

        file_length = int(self.headers['Content-Length'])
        with open(filename, 'wb') as output_file:
            output_file.write(self.rfile.read(file_length))
            self.send_response(201, 'Created!')
            self.end_headers()
            reply_body = "Saved"
            self.wfile.write(reply_body.encode('utf8'))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server Started")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Stopped")