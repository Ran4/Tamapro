commandList = ["eat", "pet", "playwithitem", "playwithtama", "give",
    "inventory", "getimage", "status", "statushtml", "getshopitems",
    "getmoney", "buyitem"]
requiresArguments = ["eat", "give",
    "playwithitem", "playwithtama", "buyitem"]

START_KNOWLEDGE_LEVEL = 50
MAX_KNOWLEDGE_LEVEL = 100

##############################
#Like limits
LIKE_LIMIT = 50
HATE_LIMIT = 25
LOVE_LIMIT = 75

CHANGE_ON_LIKE = 5
CHANGE_ON_DISLIKE = -5

##############################
#Mood stuff
MAX_MOOD = 100
#How much the mood value will change when playing with another tama or item
MOOD_INCREASE_IF_LOVE = 5
MOOD_INCREASE_IF_HATE = -5
MOOD_INCREASE_IF_LIKE = 3
MOOD_INCREASE_IF_DISLIKE = -3
MOOD_CHANGE_ON_HIGH_HUNGER = -5
MOOD_CHANGE_ON_MEDIUM_HUNGER = -3

##############################
#Store stuff
NUM_ITEMS_IN_SHOP = 4
SHOP_MIN_COST = 1
SHOP_MAX_COST = 4
SHOP_COST_MULTIPLIER = 10
SHOP_HIGHER_COST_OF_EXPENSIVE_ITEM = 40 #multiplier is not applied
