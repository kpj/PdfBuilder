import socketserver, json, subprocess
import http.server, urllib.parse


# latex variables
compile_substring = "main" # compile .tex file if this substring is present
suppress_commit = "[pdfupdate]" # don't consider commit if this substring appears

# server variables
port = 8080

# helper functions
def handle_git_request(req):
	for commit in req["commits"]:
		if not suppress_commit in commit["message"]:
			stuff = commit["modified"] + commit["added"]
			for entry in [e for e in stuff if compile_substring in e]:
				subprocess.call(["./latex_maker.sh", entry])

def get_data(sock, con_len):
	return urllib.parse.unquote(sock.recv(con_len).decode(encoding="UTF-8"))

class RequestHandler(http.server.CGIHTTPRequestHandler):
	def do_POST(self):
		req = json.loads(get_data(self.request, int(self.headers["Content-Length"]))[8:])
		handle_git_request(req)

# start server
httpd = socketserver.TCPServer(("0.0.0.0", port), RequestHandler)
httpd.serve_forever()
