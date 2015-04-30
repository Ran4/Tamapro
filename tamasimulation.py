import item

class TamaSimulation(object):
    def __init__(self, uid, name="Unnamed Tamapro"):
        self.uid = uid
        self.name = name
        
        self.type = "basetama"
        
        self.mood = "unhappy"
        
        self.MAX_HUNGER = 100
        self.hunger = self.MAX_HUNGER
        
        self.MAX_HP = 100
        self.hp = self.MAX_HP
        
        self.inventory = []
        self.eatingPreference = []
        
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
            
        self.inventory.remove(itemStr)
        
        self.mood = "happy"
        self.hunger = 0
        s = "%s ate a %s!" % (self.name, itemStr)
        s += " %s is now %s" % (self.name, self.mood)
        
        return s
        
    def pet(self, itemStr=None):
        if item.isPettable(itemStr):
            self.mood = "happy"
        else:
            self.mood = "unhappy"
        
        if itemStr:
            return "%s was petted with a %s! New mood: %s" % \
                (self.name, itemStr, self.mood)
        else:
            return "%s was petted! New mood: %s" % (self.name, self.mood)
            
    def updateMood(self):
        if self.hunger > 50:
            self.mood = "hungry"
        else:
            if self.hp < 50:
                self.mood = "unhappy"
            else:
                self.mood = "good"
        
    def updateSimulation(self, dt):
        self.hunger = min(self.hunger + dt, self.MAX_HUNGER)
        
        self.updateMood()
