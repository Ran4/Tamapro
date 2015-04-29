
EDIBLE = 1
MAGICAL = 2

items = {
    "banana": EDIBLE,
    "orange": EDIBLE,
    "tire": 0,
}

""" Stupid helper function, don't use it? """
def isEdible(itemName):
    if itemName not in items:
        return 
    
    return items[itemName] & EDIBLE
