import uuid

from bottle import Bottle, route, run, template, request, static_file

import constants as con
from tamasimulation import TamaSimulation
import item

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.app = Bottle()
        self.setupRouting()
        
        self.simulations = {}
        uid = "debuguid"
        sim = TamaSimulation(uid, "DebugNameOfTama")
        self.simulations[uid] = sim
        
        sim.inventory.append("child")
        sim.inventory.append("banana")

    def start(self):
        self.app.run(host=self.host, port=self.port)
        
    def getSimFromUID(self, uid):
        """Returns a certain simulation, or None if no simulation was found
        """
        if uid in self.simulations:
            return self.simulations[uid]
        else:
            return None
        
    def setupRouting(self):
        r = self.app.route
        #r('/', method="GET", callback=self.index)
        r('/', callback=self.index)
        r('/addtama/<name>', callback=self.createNewTama)
        r('/updatesimulation/<dt>', callback=self.updateSimulation)
        r('/<uid>', callback=self.showCommands)
        r('/<uid>/', callback=self.showCommands)
        r('/<uid>/<command>', callback=self.doAction)
        r('/<uid>/<command>/', callback=self.doAction)
        r('/<uid>/<command>/<arg>', callback=self.doAction)
        
    def index(self):
        s = ""
        
        sb = []
        for sim in self.simulations.values():
            sb.append("<p>{0.uid} - {0.name}</p>".format(sim))
        s += "<b>Simulations running:</b>"
        s += "\n".join(sb)
        
        s += "<b>List of items:</b>\n</br>"
        s += "\n</br>".join(item.items.keys())
        
        return s
        
    def createNewTama(self, name):
        uid = str(uuid.uuid4())
        uid = uid[:8]
        self.simulations[uid] = TamaSimulation(uid, name)
        
        return "New user {} with id </br>{}</br> was created!".format(
            name, uid)
        
    def doAction(self, uid, command, arg=None):
        sim = self.getSimFromUID(uid)
        if not sim:
            return "Couldn't find tama with uid {}".format(uid)
            
            
        s = "Called doAction with uid <br>{}".format(uid)
        s += "</br>and command=" + command
        if arg:
            s += "</br>and argument=%s" % arg
        else:
            s += "</br>but no argument"
        s += "<br>----------</br>"
        
        #Make sure that the command exists and that it has args if needed
        if command not in con.commandList:
            return s + "Unknown command!"
        elif command in con.requiresArguments and arg is None:
            return s + "The %s command is missing an argument" % command
            
            
        #Handle the commands!
        if command == "give":
            if arg not in item.items:
                return s + "%s is not a valid item!" % arg
            
            return s + sim.addItem(arg)
            
        elif command == "inventory":
            return "\n".join(sim.inventory)
            
        elif command == "getimage":
            fileName = sim.getImageFileName()
            print "Serving image with path %s" % fileName
            return static_file(fileName, root='')
            
        elif command == "rename":
            oldName = sim.name
            sim.name = arg
            return "%s switched name to %s" % (oldName, sim.name)
            
        elif command == "status":
            return sim.getStatusReport()
        
        elif command == "eat":
            if arg not in item.items:
                return s + "%s is not a valid item!" % arg
                
            response = sim.eat(arg)
            return response
            
        elif command == "pet":
            response = sim.pet(arg)
            print "DEBUG: After petting, pet mood is now: %s" % sim.mood
            return response
        
        #Command wasn't handled if we are here
        return s + "Command wasn't handled."
        
    def showCommands(self, uid):
        s = "Commands:</br>"
        s += "</br>".join(con.commandList)
        return s
        
    def updateSimulation(self, dt):
        try:
            dt = int(dt)
        except ValueError as e:
            return e.message
        except:
            return "error"
        
        for sim in self.simulations.values():
            sim.updateSimulation(dt)
            
        return "Successfully ran updateSimulation"
        
    #Simulation stuff

def main():
    server = Server(host='localhost', port=8089)
    server.start()
    
    """startSimulations()
    run(host='localhost', port=8080)"""
   
if __name__ == "__main__":
    main()
