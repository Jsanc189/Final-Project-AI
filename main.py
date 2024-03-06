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




genome_data = data["Genome"]


produce_data = genome_data["Produce"]
land_data = genome_data["Land_Allocation"]
production_data = genome_data["Production"]

initial_data = data["initial"]
population = initial_data["population"]
land_size = initial_data["land_amount"]
budget_data = initial_data["budget"]



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


def basic_production(land, produce, production, size):
    # For each land allocation, multiply the allocation by the size and then multiply
    # the produce of that land allocation by its produce value
    produce_dict = {}
    land_keys = ["Grain_Crop", "Cotton_Crop", "Metal_Mining"]
    produce_keys = ["Grain", "Cotton", "Metal"]
    production_keys = ["wheat", "cloth", "tool"]
    
    for item in range(len(produce_keys)):
        # Calculate production value and update in the dictionary
        production_value = land[land_keys[item]] * produce[produce_keys[item]] * \
            production[production_keys[item]]["efficiency"] * size * 100
        produce_dict[production_keys[item]] = production_value

    return produce_dict


def basic_consumption(budget_data, producedGoods, marketPrice, population_size):
    #we have a budget, price, and a need
    consumption_list = []
    
    budget_keys = ["wheat", "cloth", "tool"]

    for product in budget_keys:
        budget = budget_data[product]["budget"]
        need =  budget_data[product]["need"]
        good = producedGoods[product]
        price = marketPrice[product]["price"]
        

        # budget/price = amount needed to change
        #max_consumption_budget = budget/price
        min_consumption = need * population_size
        min_budget = min_consumption * budget 
        goods_total_cost = good * price         

        #negative number, not enough
        #positive number, too much
        #want this to be 0,0,0
        #everyone has everything, the right amount
        consumption_list.append(goods_total_cost - min_budget)
        
        #we get the cost of the product produced and multiply it by the marketprice and compare those

    #max_consumption_budget = budget/price
    return consumption_list
# use production and demand to help find the price

def adjust_price_based_on_supply_demand(production_data, produce_dict):
    """
    Adjusts the price of products based on the difference between supply and demand.

    Parameters:
    - production_data: Dictionary containing production information including demand.
    - produce_dict: Dictionary containing the supply of each product.

    Returns:
    - Updated production data with adjusted prices.
    """
    updated_production_data = copy.deepcopy(production_data)

    # Iterate through the products and their supply in the produce_dict
    for product, supply in produce_dict.items():
        # Retrieve the demand and details from the production data
        if product in updated_production_data:
            details = updated_production_data[product]
            demand = details['demand']
            # Simple price adjustment logic
            if supply > demand:  # adjust to use % instead of flat number.
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



# def YourAverageJoe():
#     def demand():
#         pass
#     def consume():
#         pass
#     def doesBuy():
#         pass






# Phenome

# The phenome is a list of {good, quantity, price} tuples for all goods in the economy. 
# Quantity here == amount both produced and consumed.
# The phenome uses the produce_list

def create_phenome(produce_list, production_data):
    pass



def calculate_demands():
    pass



#########################################################################################
if __name__ == "__main__":
    full_genomes = [create_genome(land_data)]

    for genome in full_genomes:
        print(genome)
        print(basic_production(genome, produce_data, production_data, land_size))
        producedGoods = basic_production(genome, produce_data, production_data, land_size)

        print("produceGoods: ", producedGoods) #value
        
        newPrices = adjust_price_based_on_supply_demand(production_data, producedGoods)
        print("New Prices", newPrices)

        consumption = basic_consumption(budget_data, producedGoods, newPrices, population)
        print("consumption", consumption)
        # genpome["Production"]["price"] = ^^^^




#given a set area of land, our goal is to produce materials.
#If we over produce a material, the program should notice and adjust, until we get a perfect distribution. (Based of starting Demands that we set?)
#Adjust the amount of land we allocate for each material, adjust the price, that's  of the good so supply = demand
#supply is perfect to demand
