import collections
import math
import random
import sys
from tabulate import tabulate
from itertools import accumulate

# Global Variables

NUMBER_OF_COLOURS = 8
PATTERN_SIZE = 4
POPULATION_SIZE = 150
MAX_GENERATION = 100
MAX_SIZE = 60
FITNESS_THRESHOLD = 0.2
MUTATION_PROBABILITY = 0.02
CROSSOVER_PROBABILITY = 0.2

TO_GUESS = [random.randint(0, NUMBER_OF_COLOURS-1) for _ in range(PATTERN_SIZE)]
INITIAL_GUESS = [random.randint(0, NUMBER_OF_COLOURS-1) for _ in range(PATTERN_SIZE)]
HISTORY = []

#########################################
############# MasterMind AI #############
#########################################

#########################################
################ Step 1 #################
##### Model the MasterMind problem ######
#########################################


# Question 1 #
# Propose a representation (coding) for the pawn combinations.

"""
Use an array where each index contains an integer in the range [0;k[ (see following question for \
what k is).
Each integer in said range will represent a colour.

Example: [0, 4, 3, 5] <= One possible combination
         [7, 4, 1, 2] <= Another possible combination
"""

# Question 2 #
# How many candidate solutions are there for a combination of N pawns of k colours ?
# Deduce the number of combinations for 4 pawns with 8 colours.

"""
If we have no restrictions on duplications, we have k^N possibilities.

for N = 4 and k = 8, we have a total of 4096 possibilities.
"""

# Question 3 #
# The difficult question for this project is the evaluation of the quality of a candidation solution
# based of the previous solutions. We'll decompose this into multiple questions.

# Recall that at each turn, when the algorithm proposes a candidate solution 'c', the game returns
# two integers (p_c, m_c) by comparing to the previously proposed solution, which are the number of
# correctly placed pawns 'p' and the number of pawns of the right colour but incorrectly placed 'm'.

# Question 3.1 #
# Propose a score(p => N, m => N) => N+ function that converts the number of correctly placed pawns 
# 'p' and the number of correct colours but incorrectly placed pawns 'm' into a positive integer 
# expressing a score.

def score(correctly_placed, correct_colour_but_incorrectly_placed):
    
    if correctly_placed < 0 or correct_colour_but_incorrectly_placed < 0:
        exit(1)
    elif correctly_placed == 0 and correct_colour_but_incorrectly_placed == 0:
        return 1
    else:
        # This allows to never have identical scores for different values of the (p, m) tuple
        return (NUMBER_OF_COLOURS * correctly_placed) + correct_colour_but_incorrectly_placed

# Question 3.2 #
# We now want to be capable of evaluating the quality of a candidate solution 'c' compared to an
# already played solution 'c_j'.
# To evaluate the quality of 'c', we'll suppose that it is the correct solution. In this case, the 
# virtual score obtained by 'c_j' compared to 'c' should be as close as possible to the score already 
# obtained by 'c_j' noted 'sc_j'.

# Deduce an eval(c, c_j) => N+ function which determines the difference between the virtual score of 
# 'c_j' compared to 'c' and the score already obtained by 'c_j'.
# For this, you'll need the compare(c1, c2) => (p => N, m => N) function which returns the number of
# colours of c2 correctly placed in c1 (p) and the number of colours present but incorrectly placed
# in c1 (m)

def eval(current_candidate, previous_candidate):
    # Get the (p, m) values for the previous candidate (obtained from the 'second' player) and when
    # comparing the new candidate with the previous.
    previous_candidate_p, previous_candidate_m = get_pins(previous_candidate)
    virtual_p, virtual_m = compare(previous_candidate, current_candidate)

    # Get their associated scores
    previous_candidate_score = score(previous_candidate_p, previous_candidate_m)
    virtual_score = score(virtual_p, virtual_m)

    # Use abs() to always have postive or null values
    return abs(previous_candidate_score - virtual_score)

def compare(candidate_1, candidate_2):
    # Set p and m to 0
    p = 0
    m = 0

    # Lists that will store the associated indexes
    correctly_placed_list = []
    correct_colour_but_incorrectly_placed_list = []

    for i in range(PATTERN_SIZE):
        if candidate_1[i] == candidate_2[i]:
            p += 1
            correctly_placed_list.append(i)

    for i in range(PATTERN_SIZE):
        # If the current index isn't part of the ones that are correct...
        if (i in correctly_placed_list) == False:
            for j in range(PATTERN_SIZE):
                # Check that the next loop index isn't in either list (so it can be added)...
                if ((j in correctly_placed_list) == False) and ((j in correct_colour_but_incorrectly_placed_list) == False):
                    # Check that the value of first index in the first candidate that isn't correct is 
                    # the same as that of the value of the second index in the second candidate still 
                    # available to be added
                    if candidate_1[i] == candidate_2[j]:
                        m += 1
                        correct_colour_but_incorrectly_placed_list.append(j)
                        break
            
    return p, m

# Gets tha values 'p' and 'm' from a given candidate compared to the solution. Acts as a second 
# player

def get_pins(candidate):

    return compare(candidate, TO_GUESS)

# Question 3.3 #
# Deduce the fitness function that compares a candidate combination 'c' with the history of all tuples
# (p, m) that we're trying to minimise.

def fitness(current_candidate):

    result = 0

    # To make sure HISTORY is never empty, we always start with an initial guess (more often incorrect
    # than correct)
    for i in range(len(HISTORY)):
        result += eval(current_candidate, HISTORY[i])

    return result/len(HISTORY)

#########################################
################ Step 2 #################
#### Selection, Crossover, Mutation #####
#########################################

# A genetic algorithm manipulates a population of candidate solutions. Here we'll consider that its
# size 'N' is sufficently large to allow for a good exploration at each game turn.

# Question 1 #
# Propose an algorithm or an approach for the selection of the 'm' best canididates (m < N) that will
# create the next generation of candidates

"""
Evaluate the fitness of each candidate in a generation, normalize the fitness to have values between
0 and 1. Sort the population in order of fitness (in our case it would be descending but it is 
important to note that usually we aim for a high fitness, it often depends on how we imagine our
fitness function).

Determine the accumulated fitness and then select a random value between 0 and 1 which will be our
limit and we will return the m best candidates that are below said limit.

OR 

Return the candidates with a fitness of 0. If there are none, return the single candidate with
the lowest fitness
"""

########## DO THE SECOND SELECTION THING BECAUSE IT WILL WORK BETTER (Hopefully)

def select_m_best(generation):

    # Get random limit
    limit = random.uniform(0, FITNESS_THRESHOLD)

    # Will be used to store the candidates and their fitness
    candidate_info_list = []

    #For the normalization
    total_fitness = 0

    for i in range(POPULATION_SIZE):
        candidate_fitness = fitness(generation[i])
        total_fitness += candidate_fitness
        candidate_info_list.append((candidate_fitness, generation[i]))

    # Sort the list and divide their fitness to get a normalized value
    candidate_info_list = sorted(candidate_info_list, key=lambda element: element[0])
    candidate_info_list = [((candidate_info[0]/total_fitness), candidate_info[1]) for candidate_info in candidate_info_list]

    # Accumulate the normalized fitness values
    accumulated_fitness = list(accumulate([candidate_info[0] for candidate_info in candidate_info_list]))

    # Find the index of the value closest to the limit
    closest_to_limit = min(enumerate(accumulated_fitness), key=lambda element: abs(element[1] - limit))

    # Return the candidates with a cumulative fitness less than the limit
    return [candidate_info[1] for candidate_info in candidate_info_list[:closest_to_limit[0]]]

# Question 2 #
# Propose one or more simple mutation operations on a candidate solution

"""
Choose two positions in the candidate and swap them
OR
Replace the colour at one random index
"""

def mutate(candidate):
    """
    # Choose two random indexes
    random_indexes = random.sample(range(PATTERN_SIZE), 2)

    # Swap them
    temp = candidate[random_indexes[0]]
    candidate[random_indexes[0]] = candidate[random_indexes[1]]
    candidate[random_indexes[1]] = temp
    print(candidate)
    """
    random_index = random.randint(0, PATTERN_SIZE-1)
    random_colour = random.randint(0, NUMBER_OF_COLOURS-1)

    while random_colour != candidate[random_index]:
        random_colour = random.randint(0, NUMBER_OF_COLOURS-1)

    candidate[random_index] = random_colour

    return candidate

# Question 3 #
# Propose one or more crossing operations transforming two candidate solutions into one new candidate
# solution. Make sure that the new candidate solutions are valid.

"""
Select a random starting index and add the next N/2 values from the first parent into the resulting 
candidate. Go to the next index value and check that the value at that index in the second parent
isn't already in the resulting candidate, if it is keep advancing the index (in a looping manner).
Once a value not already in the resulting candidate is found, add it at the next index and keep
going until the resulting candidate is full
"""

def crossover(parent_candidate_1, parent_candidate_2):
    # Initialise a child candidate full of -1
    child_candidate = [-1 for _ in range(PATTERN_SIZE)]

    # Start at a random index for the parents
    parent_index = random.randint(0, PATTERN_SIZE-1)

    # Add N/2 elements of the first parent to the child (at the same position)
    for i in range(PATTERN_SIZE//2):
        child_candidate[(parent_index+i)%PATTERN_SIZE] = parent_candidate_1[(parent_index+i)%PATTERN_SIZE]

    # Set the parent to the next index (use of modulo to stay in index bounds)
    parent_index += (PATTERN_SIZE//2)
    parent_index %= PATTERN_SIZE

    # Iterate whil the child has unasigned indexes (contains a '-1')
    while -1 in child_candidate:
        child_candidate[parent_index] = parent_candidate_2[parent_index]
        parent_index += 1
        parent_index %= PATTERN_SIZE

    return child_candidate

#########################################
##### Full AI Genetic Algorithm Loop ####
#########################################

def intialise_population():

    return [[random.randint(0, NUMBER_OF_COLOURS-1) for _ in range(PATTERN_SIZE)] for _ in range(POPULATION_SIZE)]

def generate_new_population(generation):
    
    new_generation = []

    for i in range(len(generation)):
        new_generation.append(generation[i])

    for i in range(len(generation)):
        if len(new_generation) < POPULATION_SIZE:
            mutation = random.random()
            if mutation <= MUTATION_PROBABILITY:
                new_generation.append(mutate(generation[i]))
            
            cross = random.random()
            if cross <= CROSSOVER_PROBABILITY:
                parent_1 = generation[i]
                parent_2 = generation[(i+1)%len(generation)]
                new_generation.append(crossover(parent_1, parent_2))

    while len(new_generation) < POPULATION_SIZE:
        random_candidate = [random.randint(0, NUMBER_OF_COLOURS-1) for _ in range(PATTERN_SIZE)]
        if random_candidate not in new_generation:
            new_generation.append(random_candidate)
    
    return new_generation

if __name__ == "__main__":
    
    iteration_counter = 0
    guess_p, guess_m = get_pins(INITIAL_GUESS)

    iteration_candidates = []
    
    while guess_p != PATTERN_SIZE:
        HISTORY.append(INITIAL_GUESS)
        iteration_counter += 1
        generation_counter = 1
        generation = intialise_population()
        print("Current iteration:", iteration_counter)

        while generation_counter <= MAX_GENERATION and len(iteration_candidates) <= MAX_SIZE:
            generation = generate_new_population(generation)
            print("Current generation:", generation_counter)
            generation = select_m_best(generation)

            for candidate in generation:
                if candidate not in iteration_candidates:
                    iteration_candidates.append(candidate)
            
            generation_counter += 1
        
        guess_index = random.randint(0, len(iteration_candidates)-1)
        guess = iteration_candidates[guess_index]
        print(fitness(guess))
        HISTORY.append(guess)
        guess_p, guess_m = get_pins(guess)
        print("Guess at iteration", iteration_counter," is", guess)
        iteration_candidates = []
    
    print("Guessed correctly after", iteration_counter, "iterations")
    print("Solution:", TO_GUESS)