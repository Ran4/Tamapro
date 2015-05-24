import json
import random

import item
import constants as con
import item

class Shop:
    def __init__(self):
        self.itemAndCostList = []
        self._populate()

    def _populate(self):
        for _ in range(8): #start off with a few items...
            self._addRandomItem()

    def getItemsJSON(self):
        json.dumps({"error": False, "items": self.itemAndCostList})

    def update(self):
        self._removeRandomItem()
        self._addRandomItem()

    def _removeRandomItem(self):
        if self.itemAndCostList: #don't pop if it's empty
            self.itemAndCostList.pop(random.randrange(len(self.itemAndCostList)))

    def _addRandomItem(self):
        itemStr = random.choice(item.items.keys())
        cost = random.randint(4, 8)
        if item.isExpensive(itemStr):
            cost += 8

        self.itemAndCostList.append([itemStr, cost])
