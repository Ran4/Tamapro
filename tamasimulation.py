import item

class TamaSimulation(object):
    def __init__(self, uid, name, password=None):
        self.uid = uid
        self.name = name
        
        self.password = password
        
        self.type = "basetama"
        
        self.mood = "unhappy"
        
        self.MAX_HUNGER = 100
        self.hunger = self.MAX_HUNGER
        
        self.MAX_HP = 100
        self.hp = self.MAX_HP
        
        self.poisoned = False
        
        self.inventory = []
        self.eatingPreference = []
        
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
            
    def getStatusReport(self):
        return """<img src='{1}'></img>
        mood: {0.mood}
        hunger: {0.hunger}/{0.MAX_HUNGER}
        hp: {0.hp}/{0.MAX_HP}
        
        type: {0.type}
        """.replace("\n","</br>\n").format(self, "/"+self.getImageFileName())
        
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
            if not self.poisoned: #only tell if we're not already poisoned
                s += " It poisoned %s!" % self.name
            
            self.poisoned = True
        
        if self.poisoned and item.isHealing(itemStr):
            self.poisoned = False
            s += " It healed %s poison." % (self.possessiveName())
            
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
            if not self.poisoned: #only tell if we're not already poisoned
                s += " It poisoned %s!" % self.name
            self.poisoned = True
        
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
