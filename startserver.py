import subprocess
import urllib2
import time
import sys

"""Starts the server and calls it every dt seconds
args: [port[, host[, dt]]]
"""

port = "8087"
host = "0.0.0.0"
dt = 30

if len(sys.argv) > 1:
    port = sys.argv[1] 
    if len(sys.argv) > 2:
        host = sys.argv[2]
        if len(sys.argv) > 3:
            dt = int(sys.argv[3])
    
subprocess.Popen(["python", "server.py", port, host])
time.sleep(1.5)

while True:
    url = 'http://localhost:%s/updatesimulation/%s' % (port, dt)
    urllib2.urlopen(url)
    print("Called updatesimulation with dt=%s" % dt)
    time.sleep(dt)
