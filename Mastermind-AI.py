import random
import math
import sys
import collections

# Global Variables

NUMBER_OF_COLOURS = 8
PATTERN_SIZE = 4
POPULATION_SIZE = 100
MAX_GENERATION = 100000

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
Get the (p, m) values for the N candidates, order them in descending order for the values of 'p' then
the values of 'm' then choose the best half of candidates
"""

def select_m_best(generation):

    temporary_list = []

    # Iterate through all the candidates of the generation
    for i in range(len(generation)):
        p, m = get_pins(generation[i])
        temporary_list.append((p, m, generation[i]))

    # Sort the (p, m) for each candidate by p then m
    sorted_candidates = sorted(temporary_list, key=lambda element: (element[0], element[1]), reverse=True)

    # Select the 3rd element in the tuple in the sorted list (the actual candidate) and return them
    # as a list
    return [candidate_info[2] for candidate_info in sorted_candidates[:len(sorted_candidates)//2]]

# Question 2 #
# Propose one or more simple mutation operations on a candidate solution

"""
Choose two positions in the candidate and swap them
"""

def mutate(candidate):
    # Choose two random indexes
    random_indexes = random.sample(range(PATTERN_SIZE), 2)

    # Swap them
    temp = candidate[random_indexes[0]]
    candidate[random_indexes[0]] = candidate[random_indexes[1]]
    candidate[random_indexes[1]] = temp
    print(candidate)

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

    # Set the child index to the same as the parent. From this point on, both indexes can move
    # independently (they don't always need to)
    child_index = parent_index

    # Iterate whil the child has unasigned indexes (contains a '-1')
    while -1 in child_candidate:
        # If the value at parent_index is already in the child, go to the next index
        if parent_candidate_2[parent_index] in child_candidate:
            parent_index += 1
            parent_index %= PATTERN_SIZE
        # Else add it to the child and move both indexes
        else:
            child_candidate[child_index] = parent_candidate_2[parent_index]
            child_index += 1
            child_index %= PATTERN_SIZE
            parent_index += 1
            parent_index %= PATTERN_SIZE

    return child_candidate

#########################################
##### Full AI Genetic Algorithm Loop ####
#########################################

if __name__ == "__main__":

    HISTORY.append(INITIAL_GUESS)
    generation = []

    # This will be set to True if, and only if, one of the candidates has a value of p equal to
    # PATTERN_SIZE. This means all colours are at the right place
    solution_found = False

    
    for i in range(POPULATION_SIZE):
        generation.append([random.randint(0, NUMBER_OF_COLOURS-1) for _ in range(PATTERN_SIZE)])

