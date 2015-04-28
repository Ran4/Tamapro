import uuid

from bottle import Bottle, route, run, template, request

from tamasimulation import TamaSimulation

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.app = Bottle()
        self.setupRouting()
        
        self.simulations = {}

    def start(self):
        self.app.run(host=self.host, port=self.port)
        
    def setupRouting(self):
        r = self.app.route
        r('/', method="GET", callback=self.index)
        r('/hello/<name>', callback=self.hello)
        r('/createnewuser/<name>', callback=self.createNewUser)
        r('/updatesimulation/<dt>', callback=self.updateSimulation)
    
    #Routing stuff

    def index(self):
        return 'Welcome'

    def hello(self, name="Guest"):
        return template('Hello {{name}}, how are you?', name=name)
        
    def createNewUser(self, name):
        uid = uuid.uuid4()
        self.simulations[uid] = TamaSimulation(uid, name)
        
        return "New user {} with id '{}' was created!".format(
            name, uid)
        
    def updateSimulation(self, dt):
        try:
            dt = int(dt)
        except ValueError as e:
            #return "</br>".join(dir(e))
            return e.message
        except:
            return "error"
        
        for sim in self.simulations.values():
            sim.spendTime(dt)
            
        return "Successfully ran updateSimulation"
        
    #Simulation stuff

"""
        
def startSimulations():
    simulations = {}
    simulations["myFirstSimulation"] = tamasimulation.TamaSimulation()

@route('/createnewuser/<userID>')
def createNewUser(userID):
        return template(
            '<b>Hello {{userID}}</b>!',
            userID=userID)
            
@route('/runsimulation/')
def runSimulation():
    for key in simulations:
        
"""
def main():
    server = Server(host='localhost', port=8080)
    server.start()
    
    """startSimulations()
    run(host='localhost', port=8080)"""
   
if __name__ == "__main__":
    main()
