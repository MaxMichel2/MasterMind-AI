import collections
import math
import random
import sys
from itertools import accumulate

# Global Variables

PATTERN_SIZE = 4
NUMBER_OF_COLOURS = 8
POPULATION_SIZE = 100
MAX_GENERATION = 20
MAX_SIZE = 60
MUTATION_PROBABILITY = 0.02
CROSSOVER_PROBABILITY = 0.7

TO_GUESS = []
INITIAL_GUESS = []
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

We can also note that the impact of N on the overall number of possibilites is much larger than the
impact of k.
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
    virtual_p, virtual_m = compare(current_candidate, previous_candidate)

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

    # Find the number of correctly placed pins in candidate_1 compared to candidate_2
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
                    # Check that the value of first index in the first candidate that isn't correct 
                    # is the same as that of the value of the second index in the second candidate 
                    # still available to be added
                    if candidate_1[i] == candidate_2[j]:
                        m += 1
                        correct_colour_but_incorrectly_placed_list.append(j)
                        break
            
    return p, m

# Question 3.3 #
# Deduce the fitness function that compares a candidate combination 'c' with the history of all 
# tuples (p, m) that we're trying to minimise.

def fitness(current_candidate):

    result = 0

    # To make sure HISTORY is never empty, we always start with an initial guess (more often 
    # incorrect than correct)
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

Here I used the second approach since it feels more appropriate
"""

def select_m_best(generation):

    # Will be used to store the candidates and their fitness
    m_best = []

    for i in range(POPULATION_SIZE):
        candidate_fitness = fitness(generation[i])
        m_best.append((candidate_fitness, generation[i]))

    # Sort the list and extract their fitness into a new list
    m_best = sorted(m_best, key=lambda element: element[0])
    fitness_values = [candidate_info[0] for candidate_info in m_best]

    # If there are no candidates with a fitness of 0, choose the one with the lowest fitness
    if 0 not in fitness_values:
        return [m_best[0][1]]
    
    # Find the index of the first non null value in the fitness list if there is one
    try:
        first_non_null_value = next(x[0] for x in enumerate(fitness_values) if x[1] > 0)
    except StopIteration:
        first_non_null_value = len(m_best)

    return [candidate_info[1] for candidate_info in m_best[:first_non_null_value]]

# Question 2 #
# Propose one or more simple mutation operations on a candidate solution

"""
Choose two positions in the candidate and swap them (This is a permutation)
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
    # Define a random position and colour to be placed in that position
    random_index = random.randint(0, PATTERN_SIZE-1)
    random_colour = random.randrange(0, NUMBER_OF_COLOURS)

    # While the colour that was chosen is the same as the one already there, find a new colour
    while random_colour == candidate[random_index]:
        random_colour = random.randrange(0, NUMBER_OF_COLOURS)

    # Swap the new colour
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
    parent_index = random.randrange(0, PATTERN_SIZE)

    # Add N/2 elements of the first parent to the child (at the same position)
    for i in range(PATTERN_SIZE//2):
        child_candidate[(parent_index+i)%PATTERN_SIZE] = parent_candidate_1[(parent_index+i)%PATTERN_SIZE]

    # Set the parent to the next index (use of modulo to stay in index bounds)
    parent_index += (PATTERN_SIZE//2)
    parent_index %= PATTERN_SIZE

    # Iterate while the child has unasigned indexes (contains a '-1')
    while -1 in child_candidate:
        child_candidate[parent_index] = parent_candidate_2[parent_index]
        parent_index += 1
        parent_index %= PATTERN_SIZE

    return child_candidate

#########################################
##### Full AI Genetic Algorithm Loop ####
#########################################

# Gets the values 'p' and 'm' from a given candidate compared to the solution. Acts as a second 
# player

def get_pins(candidate):

    return compare(candidate, TO_GUESS)

# Create a population of random candidates

def intialise_population():

    return [[random.randrange(0, NUMBER_OF_COLOURS) for _ in range(PATTERN_SIZE)] for _ in range(POPULATION_SIZE)]

# Apply the mutation and crossover to the generation given as input and return the new modified
# generation

def generate_new_population(generation):
    
    new_generation = []

    # Select (1-CROSSOVER_PROBABILITY) % of the candidates to copy directly to the next generation
    number_of_candidates_to_copy = math.ceil(len(generation)*(1-CROSSOVER_PROBABILITY))

    # Allows to always have a pair number of candidates to undergo crossover
    if (len(generation) - number_of_candidates_to_copy)%2 != 0:
        number_of_candidates_to_copy -= 1
    copy_candidates_indexes = random.sample(list(range(0, len(generation))), number_of_candidates_to_copy)
    
    for index in copy_candidates_indexes:
        new_generation.append(generation[index])

    # Remaining candidates will produce offspring
    crossover_candidates_indexes = []

    # Extract the remaining candidates  
    for i in range(len(generation)):       
        if i not in copy_candidates_indexes:
            crossover_candidates_indexes.append(i)

    # Shuffle the indexes of the candidates to undergo the crossover process and split the list in 
    # half
    random.shuffle(crossover_candidates_indexes)
    parent_1_indexes = crossover_candidates_indexes[:len(crossover_candidates_indexes)//2]
    parent_2_indexes = crossover_candidates_indexes[len(crossover_candidates_indexes)//2:]

    # Since crossover() only produces one child, repeat the function call but swap the parents to get
    # two different offspring
    for i in range(len(parent_1_indexes)):
        child_candidate_1 = crossover(generation[parent_1_indexes[i]], generation[parent_2_indexes[i]])
        child_candidate_2 = crossover(generation[parent_2_indexes[i]], generation[parent_1_indexes[i]])
        new_generation.append(child_candidate_1)
        new_generation.append(child_candidate_2)

    # Once a new population has been created, the population must undergo the mutation process to 
    # avoid the algorithm getting stuck in a local optima
    for i in range(len(new_generation)):
        mutation_chance = random.random()
        if mutation_chance <= MUTATION_PROBABILITY:
            new_generation[i] = mutate(new_generation[i])
    
    # Since the generation given to this function will "never" be of size POPULATION_SIZE, fill
    # the rest of population with random candidates
    while len(new_generation) < POPULATION_SIZE:
        random_candidate = [random.randrange(0, NUMBER_OF_COLOURS) for _ in range(PATTERN_SIZE)]
        if random_candidate not in new_generation:
            new_generation.append(random_candidate)

    return new_generation

# Main loop

if __name__ == "__main__":

    # Extract parameters from the user if any were given
    if len(sys.argv) > 8:
        print("Only 7 variables can be set:\n\t\
PATTERN_SIZE (default = 4)\n\t\
NUMBER_OF_COLOURS (default = 8)\n\t\
POPULATION_SIZE (default = 100)\n\t\
MAX_GENERATION (default = 20)\n\t\
MAX_SIZE (default = 60)\n\t\
MUTATION_PROBABILITY (default = 0.02)\n\t\
CROSSOVER_PROBABILITY (default = 0.7)")
        exit(1)
    else:
        global_variables = [-1 for _ in range(7)]
        for i in range(1, len(sys.argv)):
            global_variables[i-1] = sys.argv[i] # Start at 1 since sys.argv[0] is the script

        PATTERN_SIZE = int(global_variables[0]) if int(global_variables[0]) != -1 else 4
        NUMBER_OF_COLOURS = int(global_variables[1]) if int(global_variables[1]) != -1 else 8
        POPULATION_SIZE = int(global_variables[2]) if int(global_variables[2]) != -1 else 100
        MAX_GENERATION = int(global_variables[3]) if int(global_variables[3]) != -1 else 20
        MAX_SIZE = int(global_variables[4]) if int(global_variables[4]) != -1 else 60
        MUTATION_PROBABILITY = float(global_variables[5]) if float(global_variables[5]) != -1 else 0.02
        CROSSOVER_PROBABILITY = float(global_variables[6]) if float(global_variables[6]) != -1 else 0.7

        # Set up an initial code and guess
        TO_GUESS = [random.randrange(0, NUMBER_OF_COLOURS) for _ in range(PATTERN_SIZE)]
        INITIAL_GUESS = [random.randrange(0, NUMBER_OF_COLOURS) for _ in range(PATTERN_SIZE)]
    
    # Counter for the number of iterations, inital 'p' and 'm' for the algorithm stop condition and
    # a list to store the possible candidates from the given iteration
    iteration_counter = 0
    guess_p, guess_m = get_pins(INITIAL_GUESS)
    iteration_candidates = []
    #HISTORY.append(INITIAL_GUESS) # Testing purpose
    #generation = intialise_population()
    #generation = generate_new_population(generation)

    # Run while all pins aren't correctly placed
    while guess_p != PATTERN_SIZE:
        HISTORY.append(INITIAL_GUESS) # This makes sure HISTORY is never empty (hence no division by 0)
        iteration_counter += 1
        generation_counter = 1
        generation = intialise_population()
        print("Current iteration:", iteration_counter)

        # While we haven't gone through the sepcified number of generations and found enough candidates
        while generation_counter <= MAX_GENERATION and len(iteration_candidates) <= MAX_SIZE:
            if generation_counter != 1:
                generation = generate_new_population(generation) # Modify current generation
            print("Current generation:", generation_counter)
            generation = select_m_best(generation) # Choose the best candidates

            # Add them to the list of possible candidates if they aren't already in it
            for candidate in generation:
                if candidate not in iteration_candidates:
                    iteration_candidates.append(candidate)

            generation_counter += 1
        
        # Choose a random candidate from those available, guess it and add it to the history
        guess_index = random.randint(0, len(iteration_candidates)-1)
        guess = iteration_candidates[guess_index]
        HISTORY.append(guess)
        guess_p, guess_m = get_pins(guess) # Extract the 'p' and 'm' from the guess
        print("Guess at iteration", iteration_counter," is", guess)
        iteration_candidates = []
    
    print("Guessed correctly after", iteration_counter, "iterations")
    print("Solution:", TO_GUESS)
