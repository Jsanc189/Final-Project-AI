# This is where the AI will make new economies
import json
import random
import copy

#load the data
def load_item_data(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data

data = load_item_data("data.json")

shop_data = data["Shop"]
player_state = data["PlayerState"]

print("Shop: ", shop_data)
print("Player:", player_state)

def randomize_item(item):
    curItem = copy.deepcopy(item)                           # the curent item to a copy of the item taken in
    start_price = curItem["CurrentCost"]                    # get the current cost of the item
    changed_price = random.randint(1, start_price * 2 - 1)  # generate a new price from 1 to 1 less double the original cost
    curItem["CurrentCost"] = changed_price                  # set the current item cost to the new changed price


    return curItem                                          # return the current item with the new cost
    



def randomize_shop(data):
    # Initialize an empty list to hold the randomized items
    randomized_shop = []
    # Iterate over each item in the original shop data
    for item in data:
        # Randomize each item and add it to the new shop list
        randomized_item = randomize_item(item)
        randomized_shop.append(randomized_item)
    # Return the new shop data with randomized prices
    return randomized_shop


#Genomes
#We need to create genomes for the key factors that influence the price changes
# for ex, season, player health, player inventory, player deaths...
#genome entire shop or individual items
def create_genome(item): #item is data
    genome = {}
    genome["ItemName"] = item["ItemName"]
    # randomize price
    # randomize values
    return genome

genomes = [create_genome(item) for item in shop_data]

for genome in genomes:
    print(genome)
# a genome is the entire economy i.e. all the items and their pricings
# one economy is bred with another economy and creates a new one


#randomize item helper function
    
#randomize shop helper function


def create_fullgenome(shop): #item is data
    genome = {}
    genome = copy.deepcopy(shop)
    # randomize some items for later mutations using helper functions
    newGenome = randomize_shop(genome)
    print("random: ", genome)
    return newGenome

full_genomes = [create_fullgenome(shop_data)]

for genome in full_genomes:
    print(genome)




# breeding a shop with a shop   # More overrall 'stability' / little bit more caotic?
# vs
# breeding item with item for each thing in the shop, then putting it into "final shop"  # more indiviual 'stability' / goal oriented to a specific item well

#Phenome
