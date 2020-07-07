import http.server
import socketserver
import threading
import time

from monitor_script import py_monitor

PORT = 8000


##### Sample http server for testing
from http.server import HTTPServer, SimpleHTTPRequestHandler # Python 3

server = HTTPServer(('localhost', 8888), SimpleHTTPRequestHandler)
print("Testing socket server serving at port", 8888)
thread = threading.Thread(target = server.serve_forever)
thread.daemon = True
thread.start()


# initialize the monitor. By default, interval is 60
s = py_monitor(interval=3)


# get the current usage
current_usage = s.get_usage()
print("Getting current usage: ", current_usage)
    
# start recording for 10 seconds 
print("start recording for 10 seconds ")
s.record_usage()
time.sleep(10)

# stop recording
s.stop_record_usage()
print("recording stopped")

# retrieve result from monitor class
print(s.records)

