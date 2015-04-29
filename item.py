#list of properties
EDIBLE = 1
MAGICAL = 2
TASTY = 4
PETTABLE = 8
PLAYFUL = 16

#each value in the items dictionary corresponds to a property of the item
items = {
    "banana": EDIBLE | PETTABLE,
    "orange": EDIBLE,
    "child": EDIBLE | TASTY,
    "tire": PLAYFUL,
    
}

def isEdible(itemName):
    if itemName not in items: return False
    return items[itemName] & EDIBLE

def isTasty(itemName):
    if itemName not in items: return False
    return items[itemName] & TASTY
    
def isPettable(itemName):
    if itemName not in items: return False
    return items[itemName] & PETTABLE
    