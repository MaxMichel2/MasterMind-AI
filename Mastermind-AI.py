import random
import math
import sys
import collections

# Global Variables

k = 8
N = 4

TO_GUESS = [random.randint(0, k-1) for _ in range(N)]

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
        return (k * correctly_placed) + correct_colour_but_incorrectly_placed

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
    
    previous_candidate_p, previous_candidate_m = compare(previous_candidate, TO_GUESS)
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

# Question 3.3 #
# Deduce the fitness function that compares a candidate combination 'c' with the history of all tuples
# (p, m) that we're trying to minimise.

def fitness(current_candidate):

    return 0

#########################################
################ Step 2 #################
##### Selection, Crossing, Mutation #####
#########################################

# A genetic algorithm manipulates a population of candidate solutions. Here we'll consider that its
# size 'N' is sufficently large to allow for a good exploration at each game turn.

# Question 1 #
# Propose an algorithm or an approach for the selection of the 'm' best canididates (m < N) that will
# create the next generation of candidates

"""
"""

# Question 2 #
# Propose one or more simple mutation operations on a candidate solution

"""
"""

# Question 3 #
# Propose one or more crossing operations transforming two candidate solutions into one new candidate
# solution. Make sure that the new candidate solutions are valid.

"""
"""
c1 = [random.randint(0, k-1) for _ in range(N)]
c2 = [random.randint(0, k-1) for _ in range(N)]

print("Solution")
print(TO_GUESS)
print("Candidate 1")
print(c1)
print("Candidate 2")
print(c2)

print(eval(c1, c2))