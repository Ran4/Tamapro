#list of properties
EDIBLE = 1
MAGICAL = 2
TASTY = 4
PETTABLE = 8
PLAYABLE = 16
POISONOUS = 32
HEALING = 64

#each value in the items dictionary corresponds to a property of the item
items = {
    "banana": EDIBLE | PETTABLE,
    "orange": EDIBLE,
    "child": EDIBLE | TASTY,
    "tire": PLAYABLE,
    "rotten apple": EDIBLE | POISONOUS,
    "rusty nail": PLAYABLE | POISONOUS,
    "medicine": EDIBLE | HEALING,
    "golden apple": EDIBLE | HEALING,
    "book": PLAYABLE,
}

def hasProperty(itemName, prop):
    if itemName not in items:
        return False
    return item[itemName] & prop

def isEdible(itemName):
    if itemName not in items: return False
    return items[itemName] & EDIBLE

def isTasty(itemName):
    if itemName not in items: return False
    return items[itemName] & TASTY
    
def isPettable(itemName):
    if itemName not in items: return False
    return items[itemName] & PETTABLE
    
