# MasterMind AI

This repository contains a simple implementation of a MasterMind solver using a genetic algorithm.

The code is divided into two sections: MasterMind modelisation, Genetic algorithm components

## Section 1: MasterMind modelisation

This section contains all the basic elements necessary to be able to play around with the general MasterMind game.

I won't go over the rules of the game, you can find them [here](https://en.wikipedia.org/wiki/Mastermind_%28board_game%29)

## Section 2: Genetic algorithm components

This section contains basic genetic algorithm elments including the following:
* Selection
* Mutation
* Crossover

Each component is clearly identifiable and the way each of them work is explained in quite some detail. If you have any experience with AI and/or genetic algorithms, you shouldn't feel lost. If this is new to you, you should still be able to get a general understanding about what's going on.

## Running the code

To run the code, simply clone this repository on your machine, open a terminal/cmd, navigate to the cloned folder and run the following: `python MasterMind-AI.py`

### Extra control

There are 7 different parameters that can be modified directly at the command line for you to tailor the behaviour of the program:
* *PATTERN_SIZE* controls the length of the code that the AI has to guess
* *NUMBER_OF_COLOURS* controls the number of different "colours" each code can contain
* *POPULATION_SIZE* controls the number of candidates in each generation
* *MAX_GENERATION* controls the maximum number of generations produced before taking a guess
* *MAX_SIZE* controls the maximum amount of eligible candidates per iteration. If the algorithm finds more than `MAX_SIZE` eligible candidates, it will stop to take a guess
* *MUTATION_PROBABILITY* controls the probability of mutation in the algorithm
* *CROSSOVER_PROBABILITY* controls the probability of crossover in the algorithm