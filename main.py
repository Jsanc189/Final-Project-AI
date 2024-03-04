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

produce_data = data["Produce"]
land_data = data["Land_Allocation"]
production_data = data["Production"]

print("Produce: ", produce_data)
print("land:", land_data)
print("production:", production_data)

def randomize_land(land):
    #I want to change the value for one of the "crops" to a random value 0 < x < 1
    #then I want to set the second crop to a random value from 0 < y < x
    #then the last value is a random value from 0 < z < y
    # Meant to satisfy the constraint that all land a 
    newLand = copy.deepcopy(land)
    randomNumbers = []
    # Generate the first number
    randomNumbers.append(random.uniform(0.1, 1.0))
    # Generate the second number based on what's left
    remaining_allocation_after_first = 1 - randomNumbers[0]
    randomNumbers.append(random.uniform(0.01, remaining_allocation_after_first))
    # The third number is what's left from 1 after subtracting the first two numbers
    randomNumbers.append(1 - randomNumbers[0] - randomNumbers[1])
    land_uses = ["Grain_Crop", "Cotton_Crop", "Metal_Mining"]
    # Shuffle the list to randomize which land use gets which number
    random.shuffle(land_uses)

    for i, land_use in enumerate(land_uses):
        newLand[land_use] = randomNumbers[i]
        

    print("TOTAL LAND ALOCATED", sum(randomNumbers))
    
    return newLand



# #Genomes
# #We need to create genomes for the key factors that influence the price changes
# # for ex, season, player health, player inventory, player deaths...
# #genome entire shop or individual items
# def create_genome(item): #item is data
#     genome = {}
#     genome["Land_Allocation"] = item["Land_Allocation"]
#     # randomize values
#     return genome

# genomes = [create_genome(item) for item in land_data]

# for genome in genomes:
#     print(genome)
# a genome is the entire economy i.e. all the items and their pricings
# one economy is bred with another economy and creates a new one


#randomize item helper function
    
#randomize shop helper function


def create_genome(land): #item is data
    genome = {}
    genome = copy.deepcopy(land)
    # randomize some items for later mutations using helper functions
    newGenome = randomize_land(genome)
    print("random: ", genome)
    return newGenome


# Your genome has to be constrained in some way.  
# You can’t arbitrarily increase the quantity of arable land without losing something else. 
# - Free to make it about land, minerals, crops, weather 


def basic_production(land, produce, production, size=1):
    #for each land allocation, multiply the allocation by the size and then multiply
    #the produce of that land allocation by its produce value
    produce_list = []
    land_keys = ["Grain_Crop", "Cotton_Crop", "Metal_Mining"]
    produce_keys = ["Grain", "Cotton", "Metal"]
    production_keys = ["wheat", "cloth", "tool"]
    
    for item in range(len(produce_keys)):
        produce_list.append(land[land_keys[item]] * produce[produce_keys[item]] * \
            production[production_keys[item]["efficiency"]] * size)                       # prob need to change the name from "efficency"

    return produce_list


# use production and demand to help find the price

def adjust_price_based_on_supply_demand(production_data, produce_list):
    """
    Adjusts the price of products based on the difference between supply and demand.

    Parameters:
    - production_data: Dictionary containing production information including demand.
    - produce_list: List containing the supply of each product.

    Returns:
    - Updated production data with adjusted prices.
    """
    updated_production_data = copy.deepcopy(production_data)

    # Assuming produce_list order matches the production data keys order
    for supply, (product, details) in zip(produce_list, updated_production_data.items()):
        demand = details['demand']
        # Simple price adjustment logic
        if supply > demand:
            # Supply exceeds demand, reduce price to encourage buying
            price_adjustment_factor = 0.9  # reduce price by 10%
        else:
            # Demand exceeds supply, increase price due to scarcity
            price_adjustment_factor = 1.1  # increase price by 10%

        # Adjust the price based on the factor
        updated_price = details['price'] * price_adjustment_factor
        # Update the product's price in the production data
        updated_production_data[product]['price'] = updated_price

    return updated_production_data





# Phenome

# The phenome is a list of {good, quantity, price} tuples for all goods in the economy. 
# Quantity here == amount both produced and consumed.
# The phenome uses the produce_list

def create_phenome(produce_list, production_data):
    pass



#########################################################################################
if __name__ == "__main__":
    full_genomes = [create_genome(land_data)]
    poplulation = 100

    for genome in full_genomes:
        print(genome)
        print(basic_production(genome, produce_data, production_data, 100))
        producedGoods = basic_production(genome, produce_data, production_data, 100)

        
        newPrices = adjust_price_based_on_supply_demand(production_data, producedGoods)
        # genpome["Production"]["price"] = ^^^^





