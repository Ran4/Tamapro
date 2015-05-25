import sys
import sqlite3
import time
import json
from operator import attrgetter
from operator import itemgetter

from bottle import Bottle, route, run, template, request, static_file

import constants as con
from tamasimulation import TamaSimulation
import item
import shop

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.app = Bottle()
        self.setupRouting()

        self.dbname = "tamapro_database.db"

        self.simulations = {}
        self.shop = shop.Shop()

        self.loadFromDatabase(verbose=False)

        #Debug stuff
        uid = "debuguid"
        pw = "debugpw"
        sim = TamaSimulation(uid, pw)
        self.simulations[uid] = sim

        sim.inventory.append("child")
        sim.inventory.append("banana")

        print "DEBUG: new sim was added, now saving to db"
        self.saveToDatabase(verbose=True)
        print "DEBUG: will now load from database"
        self.loadFromDatabase(verbose=True)

    def saveToDatabase(self, verbose=True):
        """Saves all simulations and shops to the database"""
        conn = sqlite3.connect(self.dbname)
        c = conn.cursor()
        if verbose:
            print "Connected to database '%s' and established cursor" % \
                    self.dbname

        #Add all the tamas base information
        tamaValues = [sim.getDBValues() for sim in self.simulations.values()]
        c.executemany("INSERT INTO tamas VALUES (?,?,?,?,?,?,?)", tamaValues)
        if verbose:
            print "  %s tamas inserted into database" % \
                    len(self.simulations)

        #Add all tamas inventory to the has table
        numItems = 0
        for sim in self.simulations.values():
            if verbose == 2: #extra verbose!
                print "    Tries inserting inventory for tama %s (uid=%s)..." %\
                        (sim.uid)

            itemDBValues = sim.getInventoryDBValues()
            c.executemany("INSERT INTO has VALUES (?,?,?)", itemDBValues)
            numItems += len(itemDBValues)

        if verbose:
            print "  %s item entries from %s tamas inserted into database" % \
                    (numItems, len(self.simulations))

        #TODO: save shops

        if verbose:
            print "Successfully saved everything to db!\n"

    def loadFromDatabase(self, verbose=True):
        """Loads all simulations and shops from the database"""
        conn = sqlite3.connect(self.dbname)
        c = conn.cursor()

        if verbose:
            print "Connected to database '%s' and established cursor" % \
                    self.dbname

        c.execute("SELECT * FROM tamas")
        propList  = c.fetchall()
        if verbose:
            print "SELECT answer:", propList


        #First, populate list of simulations
        """
        for **kwargs in c.execute("SELECT * FROM tamas"):
            print "kwargs from tamas:", kwargs
            #self.simulations[uid] = TamaSimulation(**kwargs)
            #sim = TamaSimulation(uid, pw)
        """
        #Load up all items to all tamas
        """
        for uid, itemName, amount in c.execute("SELECT uid, name, amount FROM has"):
            for _ in range(amount):
                self.simulations[uid].inventory.add(itemName)
        """


        #TODO: Load all the shop data

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
        r('/json', callback=self.index)
        r('/json/', callback=self.index)
        r('/addtama/<uid>/<password>', callback=self.createNewTama)
        r('/addtama/<uid>/<password>/', callback=self.createNewTama)
        r('/json/showiteminfo/<itemStr>', callback=self.showItemInfoJSON)
<<<<<<< HEAD
        r('/json/shopshowiteminfo/<itemStr>', callback=self.shopShowItemInfoJSON)
        r('/json/listallitems', callback=self.listAllItems)
=======
        r('/json/listallitemsinshop', callback=self.listAllItemsInShop)
>>>>>>> 5f79b33e71a1265cac13cabf34ec98bdbf98e308
        r('/json/addtama/<uid>/<password>', callback=self.createNewTamaJSON)
        r('/json/addtama/<uid>/<password>/', callback=self.createNewTamaJSON)
        r('/json/<uid>/<password>', callback=self.login)
        r('/json/<uid>/<password>/', callback=self.login)
        r('/json/<uid>/<password>/<command>', callback=self.doActionJSON)
        r('/json/<uid>/<password>/<command>/', callback=self.doActionJSON)
        r('/json/<uid>/<password>/<command>/<arg>', callback=self.doActionJSON)
        r('/updatesimulation/<dt>', callback=self.updateSimulation)
        r('/updatesimulation/<dt>/', callback=self.updateSimulation)
        r('/images/<imagepath:path>', callback=self.getImageRouting)
        r('/<uid>/<password>', callback=self.showCommands)
        r('/<uid>/<password>/', callback=self.showCommands)
        r('/<uid>/<password>/<command>', callback=self.doAction)
        r('/<uid>/<password>/<command>/', callback=self.doAction)
        r('/<uid>/<password>/<command>/<arg>', callback=self.doAction)

    #############################################################
    # ROUTING
    #############################################################

    def getImageRouting(self, imagepath):
        fullPath = "images/" + imagepath
        return static_file(imagepath, root='images')

    def index(self):
        """Returns a list of simulations running and a list of items"""
        s = ""

        sb = []
        for sim in self.simulations.values():
            url = "{0.uid}/{0.password}/status".format(sim)
            sb.append("<a href='{0}'>{1.uid}</a></br>".format(
                url, sim))
        s += "<b>Simulations running:</b></br>"
        s += "\n".join(sb)

        s += "<b>List of items:</b>\n</br>"
        s += "\n</br>".join(item.items.keys())

        return s

    def createNewTama(self, uid, password):
        sim = self.getSimFromUID(uid)
        if not sim:
            self.simulations[uid] = TamaSimulation(uid, password)
            return "New tama with id </br>{}</br> was created!".format(uid)

        else:
            return "Tama with id </br>{}</br> already exists!".format(uid)

        return

    def createNewTamaJSON(self, uid, password):
        sim = self.getSimFromUID(uid)
        if not sim:
            self.simulations[uid] = TamaSimulation(uid, password)
            jsonObj = {"error": False, "message": "Tama created."}
            return json.dumps(jsonObj, indent=4, separators=(",", ": "))

        else:
            jsonObj = {"error": True, "message": "Tama with name {} already exists.".format(uid)}
            return json.dumps(jsonObj, indent=4, separators=(",", ": "))

        return

    def login(self, uid, password):
        sim = self.getSimFromUID(uid)
        if not sim:
            jsonObj = {"error": True, "message": "Tama {} does not exist.".format(uid)}
            return json.dumps(jsonObj, indent=4, separators=(",", ": "))

        if sim.password and sim.password != password:
            jsonObj = {"error": True, "message": "Wrong password."}
            return json.dumps(jsonObj, indent=4, separators=(",", ": "))

        jsonObj = {"error": False, "message": "Success."}
        return json.dumps(jsonObj, indent=4, separators=(",", ": "))


    def doAction(self, uid, password, command, arg=None):
        sim = self.getSimFromUID(uid)
        if not sim:
            return "Couldn't find tama with uid {}".format(uid)

        if sim.password and sim.password != password:
            return "Wrong password for tama with uid {}".format(uid)

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

        return self.handleCommand(s, sim, command, arg)

    def doActionJSON(self, uid, password, command, arg=None):
        sim = self.getSimFromUID(uid)
        if not sim:
            jsonObj = {"error": True, "message": "Tama {} does not exist.".format(uid)}
            return json.dumps(jsonObj, indent=4, separators=(",", ": "))

        if sim.password and sim.password != password:
            jsonObj = {"error": True, "message": "Wrong password."}
            return json.dumps(jsonObj, indent=4, separators=(",", ": "))

        #jsonObj = {"error": False, "message": "Success."}
        #return json.dumps(jsonObj, indent=4, separators=(",", ": "))

        #Make sure that the command exists and that it has args if needed
        if command not in con.commandList:
            jsonObj = {"error": True, "message": "Unknown command."}
            return json.dumps(jsonObj, indent=4, separators=(",", ": "))
        elif command in con.requiresArguments and arg is None:
            msg = "The %s command is missing an argument" % command
            jsonObj = {"error": True, "message": msg}
            return json.dumps(jsonObj, indent=4, separators=(",", ": "))

        return self.handleCommandJSON(sim, command, arg)

    def handleCommand(self, s, sim, command, arg):
        #Handle the commands!
        if command == "give":
            if arg not in item.items:
                return s + "%s is not a valid item!" % arg

            return s + sim.addItem(arg)

        elif command == "inventory":
            #returns item
            return "\n".join(sim.inventory)

        elif command == "getimage":
            fileName = sim.getImageFileName()
            print "Serving image with path %s" % fileName
            return static_file(fileName, root='')

        elif command == "status":
            return sim.getStatusJSON()

        elif command == "statushtml":
            return sim.getStatusJSON(formatForHTML=True)

        elif command == "eat":
            if arg not in item.items:
                return s + "%s is not a valid item!" % arg

            response = sim.eat(arg)
            return response

        elif command == "pet":
            response = sim.pet(arg)
            print "DEBUG: After petting, pet mood is now: %s" % sim.mood
            return response

        elif command == "playwithitem":
            if arg not in item.items:
                return s + "%s is not a valid item!" % arg

            response = sim.playWithItem(arg)
            print "DEBUG: After playing with the item %s," % arg,
            print "pet mood is now: %s" % sim.mood
            return response

        elif command == "playwithtama":
            if arg not in self.simulations:
                return s + "Tried playing with uid=%s, which doesn't exist!" % \
                        arg
            otherTama = self.simulations[arg]
            response = sim.playWithTama(otherTama)
            print "DEBUG: After %s played with %s," % (sim.uid, otherTama.uid),
            print "their moods are %s and %s respectively" % \
                   (sim.mood, otherTama.mood)
            return response

        elif command == "getshopitems":
            response = self.shop.getItemsNamesJSON()
            return response

        #Command wasn't handled if we are here
        return s + "Command %s wasn't handled." % command

    def handleCommandJSON(self, sim, command, arg):
        s = ""

        #Handle the commands!
        if command == "give":
            if arg not in item.items:
                s += "%s is not a valid item!" % arg
                return json.dumps({"error":True, "message": s})

            response = sim.addItemJSON(arg)
            return response

        elif command == "inventory":
            #returns item
            return {"error": False, "items": sim.inventory}

        elif command == "getimage":
            fileName = sim.getImageFileName()
            print "Serving image with path %s" % fileName
            return static_file(fileName, root='')

        elif command == "status":
            return sim.getStatusJSON()

        elif command == "eat":
            if arg not in item.items:
                s += "%s is not a valid item!" % arg
                return json.dumps({"error": True, "message": s})

            response = sim.eatJSON(arg)
            return response

        elif command == "pet":
            response = sim.petJSON(arg)
            print "DEBUG: After petting, pet mood is now: %s" % sim.mood
            return response

        elif command == "playwithitem":
            if arg not in item.items:
                s += "%s is not a valid item!" % arg
                return json.dumps({"error": True, "message": s})

            response = sim.playWithItemJSON(arg)
            print "DEBUG: After playing with the item %s," % arg,
            print "pet mood is now: %s" % sim.mood
            return response

        elif command == "playwithtama":
            if arg not in self.simulations:
                s += "Tried playing with uid=%s, which doesn't exist!" % arg
                return json.dumps({"error": True, "message": s})

            otherTama = self.simulations[arg]
            response = sim.playWithTamaJSON(otherTama)
            print "DEBUG: After %s played with %s," % (sim.uid, otherTama.uid),
            print "their moods are %s and %s respectively" % \
                   (sim.mood, otherTama.mood)
            return response

        elif command == "getshopitems":
            response = self.shop.getItemsJSON()
            return response

        elif command == "getmoney":
            return json.dumps({"error": False, "money": sim.money})

        elif command == "buyitem":
            return sim.buyItem(self.shop)

        #Command wasn't handled if we are here
        s += "Command %s wasn't handled." % command
        return json.dumps({"error": True, "message": s})

    def showItemInfoJSON(self, itemStr):
        if itemStr not in item.items:
            return json.dumps({"error": True,
                "message": "Item %s doesn't exist!" % itemStr})
        else:
            return json.dumps({"error": False,
                    "description": item.items[itemStr]["description"]})

    def shopShowItemInfoJSON(self, itemStr):
        if itemStr not in self.shop.itemAndCostDict:
            return json.dumps({"error": True,
                "message": "Item %s not in shop!" % itemStr})
        else:
            return json.dumps({"error": False,
                    "description": item.items[itemStr]["description"],
                    "price": self.shop.getPriceOfItem(itemStr)})

        response = {"error": False}
        response.update(item.items[itemStr])
        return json.dumps(response)

    def listAllItemsInShop(self):
        return self.shop.getItemsNamesJSON()

    def showCommands(self, uid, password):
        s = "<a href='../../'>(Go back to stat page)</a></br>"
        s += "Commands:</br>"
        for command in con.commandList:
            s += "<a href='%s'>%s</a></br>" % (command+"/", command)
        #s += "</br>".join(con.commandList)
        return s

    def updateSimulation(self, dt):
        try:
            dt = int(dt)
        except ValueError as e:
            return e.message
        except:
            return "error"

        self.shop.update()

        for sim in self.simulations.values():
            sim.updateSimulation(dt)

        self.saveToDatabase(verbose=True)
        return "Successfully ran updateSimulation"

    #Simulation stuff

def main():
    host = '0.0.0.0'
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
        if len(sys.argv) > 2:
            host = sys.argv[2]
    else:
        port = 8087
    server = Server(host=host, port=port)
    server.start()

if __name__ == "__main__":
    main()
