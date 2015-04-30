import subprocess
import urllib2
import time

"""Starts the server and calls it every dt seconds"""

subprocess.Popen(["python", "server.py"])
print("Server started")
time.sleep(0.5)
port = "8080"
dt = 30
while True:
    url = 'http://localhost:%s/updatesimulation/%s' % (port, dt)
    urllib2.urlopen(url)
    print("Called updatesimulation with dt=%s" % dt)
    time.sleep(dt)
