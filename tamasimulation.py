import json

import item

class TamaSimulation(object):
    def __init__(self, uid, name, password=None):
        self.uid = uid
        self.type = "basetama"
        self.password = password
        self.name = name
        
        self.MAX_HUNGER = 100
        self.hunger = self.MAX_HUNGER
        
        self.mood = "unhappy"
        self.sick = False
        self.money = 100
        
        self.inventory = []
        self.eatingPreference = []
        
    def getDBValueLabels(self):
        """Returns a tuple of names to be used with getDBValues"""
        return ("uid", "type", "password", "name",
                "hunger", "mood", "sick","money")
        
    def getDBValues(self):
        """Returns a tuple of values to be inserted into a database"""
        return (self.uid, self.type, self.password, self.name, 
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
        self.uid, self.type, self.password, self.name, self.hunger,\
                self.mood, self.sick, self.money = dbValuesTuple
                
    def readInventoryDBValues(self, dbValuesTuple):
        """Reads a tuple of values read from a database"""
        #self.uid, self.type, self.password, self.name, self.hunger,\
        #        self.mood, self.sick, self.money = dbValuesTuple
        pass

    def possessiveName(self):
        if self.name.endswith("s","z"):
            return self.name + "'"
        else:
            return self.name + "'s"
        
    def getImageFileName(self):
        """Returns the file path to the image of the tama depending on
        it's mood and other factors
        """
        directory = "images/tama/%s/" % self.type
        
        if self.mood == "happy":
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
        return "%s now has a %s" % (self.name, itemStr)
        
    def eat(self, itemStr):
        if itemStr not in self.inventory:
            return "%s doesn't have a %s" % (self.name, itemStr)
        
        if not item.isEdible(itemStr):
            return "%s can't eat a %s" % (self.name, itemStr)
            
        s = "%s ate a %s!" % (self.name, itemStr)
            
        if item.hasProperty(itemStr, item.POISONOUS):
            if not self.sick: #only tell if we're not already sick
                s += " It sickened %s!" % self.name
            
            self.sick = True
        
        if self.sick and item.isHealing(itemStr):
            self.sick = False
            s += " It healed %s sickness." % (self.possessiveName())
            
        self.inventory.remove(itemStr)
        
        #self.mood = "happy"
        #self.hunger = 0
        #s += " %s is now %s" % (self.name, self.mood)
        
        return s
        
    def pet(self, itemStr=None):
        if item.isPettable(itemStr):
            self.mood = "happy"
        else:
            self.mood = "unhappy"
        
        if not itemStr:
            return "%s was petted! New mood: %s" % (self.name, self.mood)
    
        s = "%s was petted with a %s!" % (self.name, itemStr)
            
        if item.hasProperty(itemStr, item.POISONOUS):
            if not self.sick: #only tell if we're not already sick
                s += " It sickened %s!" % self.name
            self.sick = True
        
        s += " New mood: %s" % self.mood
        
        return s
            
    def updateMood(self):
        if self.hunger > 50:
            self.mood = "hungry"
        else:
            if self.hp < 50:
                self.mood = "unhappy"
            else:
                self.mood = "good"
        
    def updateSimulation(self, dt):
        dtMinutes = dt / 60.0
        self.hunger = min(self.hunger + dtMinutes, self.MAX_HUNGER)
        
        self.updateMood()
