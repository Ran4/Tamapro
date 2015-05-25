#list of properties
EDIBLE = 1
MAGICAL = 2
TASTY = 4
PETTABLE = 8
PLAYABLE = 16
POISONOUS = 32
HEALING = 64
EXPENSIVE = 128

#each value in the items dictionary corresponds to a property of the item
items = {
    "banana": {"properties": EDIBLE | PETTABLE, "description": "A yellow banana."},
    "orange": {"properties": EDIBLE, "description": "A juicy orange."},
    "child": {"properties": EDIBLE | TASTY, "description": "A tasty child."},
    "tire": {"properties": PLAYABLE, "description": "A fun round tire."},
    "rotten apple": {"properties": EDIBLE | POISONOUS, "description": "A rotten apple. Yuck!"},
    "rusty nail": {"properties": PLAYABLE | POISONOUS, "description": "A pointy nail covered with rust."},
    "medicine": {"properties": EDIBLE | HEALING, "description": "A small white pill."},
    "golden apple": {"properties": EDIBLE | HEALING, "description": "A golden apple. It looks valuable."},
    "book": {"properties": PLAYABLE, "description": "An old dusty book."},
}

def hasProperty(itemName, prop):
    if itemName not in items:
        return False
    return items[itemName]["properties"] & prop

def isEdible(itemName):
    if itemName not in items: return False
    return items[itemName]["properties"] & EDIBLE

def isTasty(itemName):
    if itemName not in items: return False
    return items[itemName]["properties"] & TASTY

def isPettable(itemName):
    if itemName not in items: return False
    return items[itemName]["properties"] & PETTABLE

def isPlayable(itemName):
    if itemName not in items: return False
    return items[itemName]["properties"] & PLAYABLE

def isHealing(itemName):
    if itemName not in items: return False
    return items[itemName]["properties"] & HEALING

def isExpensive(itemName):
    if itemName not in items: return False
    return items[itemName]["properties"] & EXPENSIVE
