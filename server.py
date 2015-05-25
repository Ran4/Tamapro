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
        
        self.createNewTamaJSON("debuguid", "debugpw")
        self.simulations["debuguid"].addItemJSON("tire")
        self.simulations["debuguid"].addItemJSON("child")
        self.simulations["debuguid"].addItemJSON("banana")
        self.createNewTamaJSON("debuguid2", "debugpw2")
        self.simulations["debuguid"].addFriend("debuguid2")
        
        self.saveToDatabase(verbose=2)
        
        self.loadFromDatabase(verbose=True)
        
    def getDatabaseReadyForUpdate(self, verbose=True):
        conn = sqlite3.connect(self.dbname)
        c = conn.cursor()
        
        c.execute("DELETE FROM tamas")
        c.execute("DELETE FROM has")
        c.execute("DELETE FROM knows")
        c.execute("DELETE FROM shopitems")

        print "Database ready for updating!"
        conn.commit()

    def saveToDatabase(self, verbose=True):
        """Saves all simulations and shops to the database"""
        
        self.getDatabaseReadyForUpdate()
        
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
                print "    Tries inserting inventory = %s for tama %s..." %\
                        (str(sim.inventory), sim.uid)

            itemDBValues = sim.getInventoryDBValues()
            c.executemany("INSERT INTO has VALUES (?,?,?)", itemDBValues)
            numItems += len(itemDBValues)
           
            #add tama relationships
            for uid2, level in sim.knows.items():
                c.execute("INSERT INTO knows VALUES (?, ?, ?)", 
                        (sim.uid, uid2, level))

        if verbose:
            print "  %s item entries from %s tamas inserted into database" % \
                    (numItems, len(self.simulations))

        #TODO: save shops
        
        conn.commit()

        if verbose:
            print "Successfully saved everything to db!\n"

    def loadFromDatabase(self, verbose=True):
        """Loads all simulations and shops from the database"""
        #Connect to database
        conn = sqlite3.connect(self.dbname)
        c = conn.cursor()

        if verbose:
            print "loadFromDatabase: Connected to database '%s' and established cursor" % \
                    self.dbname

        #First, populate list of simulations
        c.execute("SELECT * FROM tamas")
        propList  = c.fetchall()
        self.simulations = {}
        if verbose: print "SELECT answer:", propList
            
        for prop in propList:
            uid = prop[0]
            pw = prop[2]
            self.simulations[uid] = TamaSimulation(uid, pw)
            self.simulations[uid].readDBValues(prop)
            
        if verbose:
            print "self.simulations: %s" % str(self.simulations)
            
        #Load up all items to all tamas
        c.execute("SELECT * FROM has")
        hasList = c.fetchall()
        if verbose: print "has SELECT answer:", hasList
        for has in hasList:
            uid, name, amount = has
            for _ in range(amount):
                self.simulations[uid].inventory.append(name)

        #Load up all relationships
        c.execute("SELECT * FROM knows")
        knowsList = c.fetchall()
        if verbose: print "knows SELECT answer:", knowsList
        for knows in knowsList:
            print "knows:", knows
            #uid, name, amount = knows

        #TODO: Load all the shop data

    def start(self):
        self.app.run(host=self.host, port=self.port)

    def getSimFromUID(self, uid):
        """Returns a certain simulation, or None if no simulation was found
        """
        print "in getSimFromUID, simulations:", str(self.simulations)
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
        r('/json/showiteminfo/<itemStr>', callback=self.showItemInfoJSON)
        r('/json/shopshowiteminfo/<itemStr>', callback=self.shopShowItemInfoJSON)
        r('/json/listallitemsinshop', callback=self.listAllItemsInShop)
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

        s += "<b>List of items in shop:</b>\n</br>"
        s += "\n</br>".join(self.shop.itemAndCostDict.keys())
        
        s += "</br><b>List of all items:</b>\n</br>"
        s += "\n</br>".join(item.items.keys())

        return s

    def createNewTamaJSON(self, uid, password):
        sim = self.getSimFromUID(uid)
        if not sim:
            self.simulations[uid] = TamaSimulation(uid, password)
            jsonObj = {"error": False, "message": "Tama created."}
            self.saveToDatabase(verbose=False)
            return json.dumps(jsonObj, indent=4, separators=(",", ": "))
        else:
            jsonObj = {"error": True, "message": "Tama with name {} already exists.".format(uid)}
            return json.dumps(jsonObj, indent=4, separators=(",", ": "))
        

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
            return sim.buyItem(self.shop, arg)
        
        elif command == "commands":
            return self.showCommands()
        
        elif command == "addfriend":
            if arg not in self.simulations:
                return json.dumps({"error":True,
                    "message": "No tama named %s exists!" % arg})
            return sim.addFriend(arg)

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

    def showCommands(self):
        """Used for debug only: returns an HTML page"""
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
