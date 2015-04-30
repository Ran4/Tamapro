import subprocess
import urllib2
import time
import sys

"""Starts the server and calls it every dt seconds"""

subprocess.Popen(["python", "server.py"])
time.sleep(0.7)
port = "8089"

if len(sys.argv) > 1:
    dt = int(sys.argv[1])
else:
    dt = 30
    
while True:
    url = 'http://localhost:%s/updatesimulation/%s' % (port, dt)
    urllib2.urlopen(url)
    print("Called updatesimulation with dt=%s" % dt)
    time.sleep(dt)
