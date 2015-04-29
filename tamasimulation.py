from item import *

class TamaSimulation(object):
    def __init__(self, uuidValue, name="Unnamed Tamapro"):
        self.uuid = uuidValue
        self.name = name
        
        self.mood = "unhappy"
        self.MAX_HUNGER = 100
        self.hunger = 100
        self.hp = 100
        
        self.itemList = []
        self.eatableItemsList = []
        
    def feed(self, itemStr):
        if item._id not in sim.itemList:
            return "Tama doesn't have the item %s" % item
        
        if item._id not in sim.eatableItemsList:
            return "Tama doesn't want to eat item %s" % item 
            
        self.mood = "happy"
        self.hunger = 0
        return "{} has the mood {}".format(self.name, self.mood)
            
    def updateMood(self):
        if self.hunger > 50:
            self.mood = "hungry"
        else:
            if self.hp < 50:
                self.mood = "bad"
            else:
                self.mood = "good"
        
    def spendTime(self, dt):
        self.hunger = min(self.hunger + dt, self.MAX_HUNGER)
        
        self.updateMood()
