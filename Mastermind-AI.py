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
    
    previous_candidate_p, previous_candidate_m = get_pins(previous_candidate)
    virtual_p, virtual_m = compare(previous_candidate, current_candidate)

    previous_candidate_score = score(previous_candidate_p, previous_candidate_m)
    virtual_score = score(virtual_p, virtual_m)

    return abs(previous_candidate_score - virtual_score)

def compare(candidate_1, candidate_2):

    p = 0
    m = 0

    # Lists that will store the indexes associated
    correctly_placed_list = []
    correct_colour_but_incorrectly_placed_list = []

    for i in range(len(candidate_1)):
        if candidate_1[i] == candidate_2[i]:
            p += 1
            correctly_placed_list.append(i)

    for i in range(len(candidate_1)):
        if (i in correctly_placed_list) == False:
            for j in range(len(candidate_1)):
                if ((j in correctly_placed_list) == False) and ((j in correct_colour_but_incorrectly_placed_list) == False):
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

    for i in range(len(generation)):
        p, m = get_pins(generation[i])
        temporary_list.append((p, m, generation[i]))

    sorted_candidates = sorted(temporary_list, key=lambda element: (element[0], element[1]), reverse=True)

    return sorted_candidates[:len(sorted_candidates)//2]

# Question 2 #
# Propose one or more simple mutation operations on a candidate solution

"""
Choose two positions in the candidate and swap them
"""

def mutate(candidate):
    print(candidate)
    random_indexes = random.sample(range(PATTERN_SIZE), 2)

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
    child_candidate = []
    
    ### TO DO ###

    return child_candidate

if __name__ == "__main__":
    generation = []

    for i in range(POPULATION_SIZE):
        generation.append([random.randint(0, NUMBER_OF_COLOURS-1) for _ in range(PATTERN_SIZE)])

    print("Solution")
    print(TO_GUESS)
    print("Generation")
    print(select_m_best(generation))
