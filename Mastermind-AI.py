import random
import math
import sys

#########################################
############# MasterMind AI #############
#########################################

#########################################
################ Step 1 #################
##### Model the MasterMind problem ######
#########################################


# Question 1 #
# Propose a representation (coding) for the pawn combinations

"""
Use an array where each index contains an integer in the range [0;k[ (see following question for \
what k is)
Each integer in said range will represent a colour

Example: [0, 4, 3, 5] <= One possible combination
         [7, 4, 1, 2] <= Another possible combination
"""

# Question 2 #
# How many candidate solutions are there for a combination of N pawns of k colours ?
# Deduce the number of combinations for 4 pawns with 8 colours

"""
If we have no restrictions on duplications, we have k^N possibilities

for N = 4 and k = 8, we have a total of 4096 possibilities
"""

# Question 3 #
# The difficult question for this project is the evaluation of the quality of a candidation solution
# based of the previous solutions. We'll decompose this into multiple questions

# Recall that at each turn, when the algorithm proposes a candidate solution 'c', the game returns
# two integers (p_c, m_c) by comparing to the previously proposed solution, which are the number of
# correctly placed pawns 'p' and the number of pawns of the right colour but incorrectly placed 'm'

# Question 3.1 #
# Propose a score(p, m) function (p_c, m_c are positive or null and score returns a strictly positive
# integer) that converts the number of correctly placed pawns 'p' and the number of correct colours 
# but incorrectly placed pawns 'm' into a positive integer expressing a score

def score(correctly_placed, correct_colour_but_incorrectly_placed):
    
    if correctly_placed < 0 or correct_colour_but_incorrectly_placed < 0:
        exit(1)
    elif correctly_placed == 0 and correct_colour_but_incorrectly_placed == 0:
        return 1
    else:
        # This is a way of coding the correct placement of full pawns or only colours
        # By doing a modulo with 100, we get the number of correct colours incorrectly placed
        # and by dividing by 100 (with the floor function) we get the number of correctly placed
        # pawns.
        # This is probably unnecessary in the scope of this project but could be useful if the 
        # values of 'N' and 'k' were to increase drastically
        return (100 * correctly_placed) + correct_colour_but_incorrectly_placed

# Question 3.2 #

"""
"""

#########################################
################ Step 2 #################
##### Selection, Crossing, Mutation #####
#########################################

# Question 1 #

"""
"""

# Question 2 #

"""
"""

# Question 3 #

"""
"""