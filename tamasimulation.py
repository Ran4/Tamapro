import json

import item
import constants as con

class TamaSimulation(object):
    def __init__(self, uid, password=None):
        self.uid = uid
        self.type = "basetama"
        self.password = password

        self.MAX_HUNGER = 100
        self.hunger = self.MAX_HUNGER

        self.mood = 50

        self.sick = False
        self.money = 100

        self.inventory = []
        self.knows = {}

    def getDBValueLabels(self):
        """Returns a tuple of names to be used with getDBValues"""
        return ("uid", "type", "password",
                "hunger", "mood", "sick","money")

    def getDBValues(self):
        """Returns a tuple of values to be inserted into a database"""
        return (self.uid, self.type, self.password,
                self.hunger, self.mood, self.sick, self.money)

    def getInventoryDBValues(self):
        """Returns a list of tuples of items (uid,key,amount))
        to be inserted into a database"""
        keys = set(self.inventory) #get unique values
        itemDBValues = []
        for key in keys:
            itemDBValues.append((self.uid, key, self.inventory.count(key)))

        return itemDBValues

    def readDBValues(self, dbValuesTuple):
        """Reads a tuple of values read from a database"""
        self.uid, self.type, self.password, self.hunger,\
                self.mood, self.sick, self.money = dbValuesTuple

    def readInventoryDBValues(self, dbValuesTuple):
        """Reads a tuple of values read from a database"""
        #self.uid, self.type, self.password, self.hunger,\
        #        self.mood, self.sick, self.money = dbValuesTuple
        pass

    def possessiveName(self):
        if self.uid.endswith("s","z"):
            return self.uid + "'"
        else:
            return self.uid + "'s"

    def getImageFileName(self):
        """Returns the file path to the image of the tama depending on
        it's mood and other factors
        """
        directory = "images/tama/%s/" % self.type

        if self.mood > con.LIKE_LIMIT:
            return directory + "happy.png"
        else:
            return directory + "regular.png"

    def getStatusJSON(self, formatForHTML=False):
        valueDict = dict(zip(self.getDBValueLabels(), self.getDBValues()))
        s = json.dumps(valueDict, indent=4)
        if formatForHTML:
            s = s.replace("\n", "</br>\n").replace('"','').replace(":",": ")
            s = s.replace("{","Status:").replace("}", "")
        return s
        #"<img src='%s'></img>" % ("/"+self.getImageFileName())

    def addItem(self, itemStr):
        self.inventory.append(itemStr)
        return "%s now has a %s" % (self.uid, itemStr)
        
    def addItemJSON(self, itemStr):
        self.inventory.append(itemStr)
        s = "%s now has a %s" % (self.uid, itemStr)
        return json.dumps({"error": False, "message": s})

    def eat(self, itemStr):
        if itemStr not in self.inventory:
            return "%s doesn't have a %s" % (self.uid, itemStr)

        if not item.isEdible(itemStr):
            return "%s can't eat a %s" % (self.uid, itemStr)

        s = "%s ate a %s!" % (self.uid, itemStr)

        if item.hasProperty(itemStr, item.POISONOUS):
            if not self.sick: #only tell if we're not already sick
                s += " It sickened %s!" % self.uid

            self.sick = True

        if self.sick and item.isHealing(itemStr):
            self.sick = False
            s += " It healed %s sickness." % (self.possessiveName())

        self.inventory.remove(itemStr)
        return s
        
    def eatJSON(self, itemStr):
        """Eats an item.
        Returns a dictionary to be JSON'ed later on
        """
        if itemStr is None:
            return json.dumps(
                {"error": True, "message": "Tried to eat nothing!"})
        
        if itemStr not in self.inventory:
            s = "%s doesn't have a %s" % (self.uid, itemStr)
            
            return json.dumps(
                {"error": False, "message": s})

        if not item.isEdible(itemStr):
            s = "%s can't eat a %s" % (self.uid, itemStr)
            return json.dumps({"error": False, "message": s})

        s = "%s ate a %s!" % (self.uid, itemStr)

        if item.hasProperty(itemStr, item.POISONOUS):
            if not self.sick: #only tell if we're not already sick
                s += " It sickened %s!" % self.uid

            self.sick = True

        if self.sick and item.isHealing(itemStr):
            self.sick = False
            s += " It healed %s sickness." % (self.possessiveName())

        self.inventory.remove(itemStr)
        return json.dumps({"error": False, "message": s})

    def pet(self, itemStr=None):
        if item.isPettable(itemStr):
            self.mood += con.MOOD_INCREASE_IF_LIKE
        else:
            self.mood += con.MOOD_INCREASE_IF_DISLIKE

        if not itemStr:
            return "%s was petted! New mood: %s" % (self.uid, self.mood)

        s = "%s was petted with a %s!" % (self.uid, itemStr)

        if item.hasProperty(itemStr, item.POISONOUS):
            if not self.sick: #only tell if we're not already sick
                s += " It sickened %s!" % self.uid
            self.sick = True

        jsonObj = {"error": False, "message": s}

        return jsonObj

    def petJSON(self, itemStr=None):
        if item.isPettable(itemStr):
            self.mood += con.MOOD_INCREASE_IF_LIKE
        else:
            self.mood += con.MOOD_INCREASE_IF_DISLIKE

        if not itemStr:
            s = "%s was petted!" % (self.uid)
            return json.dumps({"error": False, "message": s})

        s = "%s was petted with a %s!" % (self.uid, itemStr)

        if item.hasProperty(itemStr, item.POISONOUS):
            if not self.sick: #only tell if we're not already sick
                s += " It sickened %s!" % self.uid
            self.sick = True

        return json.dumps({"error": False, "message": s})
        
    def playWithItemJSON(self, itemStr):
        if not itemStr:
            s = "No item was given!"
            return json.dumps({"error": True, "message": s})
            
        if item.isPlayable(itemStr):
            s = "%s played with %s, becoming happier in the process!" % \
                (self.uid, itemStr)
            
            self.changeMood(con.MOOD_INCREASE_IF_LIKE)
            
        else:
            s = "%s doesn't want to play with %s..." % (self.uid, itemStr)
        
        return json.dumps({"error": False, "message": s})
        

    def changeMood(self, amount):
        self.mood += amount
        if self.mood < 0:
            self.mood = 0
        elif self.mood > con.MAX_MOOD:
            self.mood = con.MAX_MOOD

    def playWithTama(self, otherTama):
        s = ""
        id2 = otherTama.uid
        if id2 not in self.knows:
            self.knows[id2] = con.START_KNOWLEDGE_LEVEL
            s += "%s just learned about %s!</br>" % (self.uid, otherTama.uid)

        if self.knows[id2] < con.LIKE_LIMIT: #dislikes, will dislike more
            self.knows[id2] += con.CHANGE_ON_DISLIKE
            s += "%s now likes %s less...</br>" % (self.uid, otherTama.uid)
        else:
            self.knows[id2] += con.CHANGE_ON_LIKE
            s += "%s now likes %s more!</br>" % (self.uid, otherTama.uid)

        if self.knows[id2] > con.LOVE_LIMIT:
            s += "%s loves %s!</br>" % (self.uid, otherTama.uid)
            self.changeMood(con.MOOD_INCREASE_IF_LOVE)
        elif self.knows[id2] >= con.LIKE_LIMIT:
            self.changeMood(con.MOOD_INCREASE_IF_LIKE)
        elif self.knows[id2] <= con.HATE_LIMIT:
            s += "%s hates %s!</br>" % (self.uid, otherTama.uid)
            self.changeMood(con.MOOD_INCREASE_IF_HATE)
        else:
            self.changeMood(con.MOOD_INCREASE_IF_DISLIKE)

        if self.knows[id2] < 0:
            self.knows[id2] = 0
        elif self.knows[id2] > con.MAX_KNOWLEDGE_LEVEL:
            self.knows[id2] = con.MAX_KNOWLEDGE_LEVEL

        return s
        
    def playWithTamaJSON(self, otherTama):
        """Plays with another tama. This will change it's mood.
        """
        s = ""
        id2 = otherTama.uid
        if id2 not in self.knows:
            self.knows[id2] = con.START_KNOWLEDGE_LEVEL
            s += "%s just learned about %s!</br>" % (self.uid, otherTama.uid)

        if self.knows[id2] < con.LIKE_LIMIT: #dislikes, will dislike more
            self.knows[id2] += con.CHANGE_ON_DISLIKE
            s += "%s now likes %s less...</br>" % (self.uid, otherTama.uid)
        else:
            self.knows[id2] += con.CHANGE_ON_LIKE
            s += "%s now likes %s more!</br>" % (self.uid, otherTama.uid)

        if self.knows[id2] > con.LOVE_LIMIT:
            s += "%s loves %s!</br>" % (self.uid, otherTama.uid)
            self.changeMood(con.MOOD_INCREASE_IF_LOVE)
        elif self.knows[id2] >= con.LIKE_LIMIT:
            self.changeMood(con.MOOD_INCREASE_IF_LIKE)
        elif self.knows[id2] <= con.HATE_LIMIT:
            s += "%s hates %s!</br>" % (self.uid, otherTama.uid)
            self.changeMood(con.MOOD_INCREASE_IF_HATE)
        else:
            self.changeMood(con.MOOD_INCREASE_IF_DISLIKE)

        if self.knows[id2] < 0:
            self.knows[id2] = 0
        elif self.knows[id2] > con.MAX_KNOWLEDGE_LEVEL:
            self.knows[id2] = con.MAX_KNOWLEDGE_LEVEL

        return json.dumps({"error": False, "message": s})

    def updateMood(self):
        if self.hunger > 50:
            pass
        else:
            pass

    def updateSimulation(self, dt):
        dtMinutes = dt / 60.0
        self.hunger = min(self.hunger + dtMinutes, self.MAX_HUNGER)

        self.updateMood()
