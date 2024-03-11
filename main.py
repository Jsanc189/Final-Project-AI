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
needs_data = initial_data["needs"]



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
        

    # print("TOTAL LAND ALOCATED", sum(randomNumbers))
    
    return newLand


#can manipulate the wants of each person in the genome(their utility)
def create_genome(land): #item is data
    genome = {}
    genome = copy.deepcopy(land)
    # randomize some items for later mutations using helper functions
    newGenome = randomize_land(genome)
    return newGenome


# Your genome has to be constrained in some way.  
# You can’t arbitrarily increase the quantity of arable land without losing something else. 
# - Free to make it about land, minerals, crops, weather 

#this should be which things I should make i.e. 2 things of cotton with 1 unit of land, or I can make 3 units of food with the same unit
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

#
def basic_consumption(budget_data, producedGoods, marketPrice, population_size, needs_data):
    #we have a budget, price, and a need
    consumption_dict = {"wheat": 0, "cloth": 0, "tool": 0}
    
    budget_keys = ["wheat", "cloth", "tool"]

   
    budget = budget_data

    while budget > 0:
        largest_utility = 0
        largest_product = ''
        for product in budget_keys:
            if largest_utility < needs_data[product]["utility"]:
                largest_utility = needs_data[product]["utility"]
                largest_product = product
        
        # updating budget and utilites
        budget -= marketPrice[largest_product]['price'] # this will prob end up as a negative
    
        consumption_dict[largest_product] += 1
        
        for product in needs_data:
            if product == largest_product:
                needs_data[product]["utility"] -= needs_data[product]["downWeighting"]
            else:
                needs_data[product]["utility"] += needs_data[product]["upWeighting"]


    for item in consumption_dict:
        consumption_dict[item] *= population_size
        producedGoods[item] -= consumption_dict[item]

        # budget = purchase(largest_product, budget, consumption_dict, marketPrice)
            

    return producedGoods



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

def breed_parents(genome1, genome2):
    parent1 = copy.deepcopy(genome1)
    parent2 = copy.deepcopy(genome2)

    child = copy.deepcopy(genome1)

    for key in parent1:
        child[key] = (parent1[key] * parent2[key]) / 2

    return child


def mutation(genome):
    #get a high or low randomly
    #based on this, a high would add percentage to a random land allocation
    #redefine the other two land allocations to be less than 1
    randomMutate = random.randint(0, 100)
    
    if randomMutate >= 0:
        land_uses = ["Grain_Crop", "Cotton_Crop", "Metal_Mining"]
            
        
        # Shuffle the list to randomize which land use gets which number
        random.shuffle(land_uses)
        print(land_uses[0])
        amount = random.uniform(-genome[land_uses[0]], genome[land_uses[0]])
        genome[land_uses[0]] += amount
        print("initial amount: ", amount)
        
        for i in range(1, len(land_uses)):
            randNum = random.uniform(0, amount)
            genome[land_uses[i]] -= randNum
            amount -= abs(randNum)
            print("new amount:", amount)

        if sum((genome.values())) > 1:
            difference = sum(genome.values()) - 1
            genome[land_uses[0]] -= difference

        print("Sum:", sum(genome.values()))
    return genome

    



def fitness(con_genome):
    #how do we want to calculate the score?
    #check the numbers for each key in disctionary.
    
    #positive production
    #efficiency
    #type of economy score
    
    totalScore = 0
    positiveProductionScore = 0
    efficiencyScore =0
    positive_production=0.3
    efficiency=0.6
    
    
    #posivie production:
    for key in con_genome:
        if con_genome[key] == 0:
            positiveProductionScore += 100
            efficiencyScore += 100
        else:
            positiveProductionScore += con_genome[key] *  0.1 #might need to be tweaked
        efficiencyScore += max(0, 100 - abs(con_genome[key]))
    totalScore = (positiveProductionScore * positive_production) + (efficiencyScore * efficiency)
    return totalScore


def run_function(genome):
    

    # print(genome)
    # print(basic_production(genome, produce_data, production_data, land_size))
    producedGoods = basic_production(genome, produce_data, production_data, land_size)
    # print("produceGoods: ", producedGoods) #value

    newPrices = adjust_price_based_on_supply_demand(production_data, producedGoods)
    # print("New Prices", newPrices)
    consumption = basic_consumption(budget_data, producedGoods, newPrices, population, needs_data)
    # print("consumption", consumption)
    
    # use this data to compare to the fitness
    return consumption
###################################################################################################
if __name__ == "__main__":
    genomes = {}
    numOfParents = 6
    generations = 5
    
    for i in range(numOfParents):
        genome = create_genome(land_data)
        #print("genome:", genome)
        #print("old sum:", sum(genome.values()))
        genome = mutation(genome)
        #print("mutated:" , genome)
        genome_consumption = run_function(genome)
        #print("consumption: ", genome_consumption)
        score = fitness(genome_consumption)
        print("score: ", score)
        genomes[i] = ([genome, score])
        #print(genomes[i])
        #run_function(genomes[i][genome])
        #run (for scores)
    print(genomes)
    #out of the parents, sort them and chose the best 2. Once we have lots of parents, sort in groups?
    # sorted_genomes = sorted(genomes.items(), key=lambda item: item[1]['score'], reverse=True)
    sorted_genomes = sorted(genomes.items(), key=lambda item: item[1][1], reverse=True)
    print("sorted genomes:",sorted_genomes)
    
    for i in range(generations):
        for j in range(0, len(sorted_genomes), 2):
            print("J:", j)
            print(sorted_genomes[j][1][0])
            child = breed_parents(sorted_genomes[j][1][0],sorted_genomes[j+1][1][0])
            child_genome = run_function(child)
            child_score = fitness(child_genome)
            # UPDATE THIS SH*T it be same for both parent and child, or child is always lower
            #check child and lower parent, and double check why the child is lower score
            
            print("Parent", genomes[j+1][1], "CHILD:", child_score)
            minScore = min(genomes[j+1][1],child_score)
            if(minScore == child_score):
                print("CHUILD MURDERER")
                continue
            else:
                print("Get Rekt Parent")
                genomes[j+1] = ([child_genome, child_score])
            

    #     breed_parents()


















#given a set area of land, our goal is to produce materials.
#If we over produce a material, the program should notice and adjust, until we get a perfect distribution. (Based of starting Demands that we set?)
#Adjust the amount of land we allocate for each material, adjust the price, that's  of the good so supply = demand
#supply is perfect to demand
