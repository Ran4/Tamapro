import json
import random
from operator import itemgetter

import item
import constants as con
import item

class Shop:
    def __init__(self):
        self.itemAndCostList = []
        self.itemAndCostDict = {}
        self._populate()

    def _populate(self):
        """Makes sure that the shop contains
        a certain number of items"""
        numItemsWanted = min(con.NUM_ITEMS_IN_SHOP, len(item.items))
        while len(self.itemAndCostDict) < numItemsWanted:
            self._addRandomItem()
    
    def getItemsNamesJSON(self):
        return json.dumps({"error": False, 
            "items": self.itemAndCostDict.keys()})
        
    def getPriceOfItem(self, itemStr):
        if itemStr not in self.itemAndCostDict:
            return 0
        else:
            return self.itemAndCostDict[itemStr]

    def update(self):
        self._removeRandomItem()
        self._populate()

    def _removeRandomItem(self):
        if self.itemAndCostDict: #don't pop if it's empty
            keyToRemove = random.choice(self.itemAndCostDict.keys())
            del self.itemAndCostDict[keyToRemove]

    def _addRandomItem(self):
        itemStr = random.choice(item.items.keys())
        cost = random.randint(4, 8)
        if item.isExpensive(itemStr):
            cost += 8
            
        self.itemAndCostDict[itemStr] = cost
