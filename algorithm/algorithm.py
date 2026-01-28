import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from initializers.population import *
from initializers.test_data import *
from operators.crossovers import *
from operators.mutators import *
from operators.selectors import *

from copy import deepcopy
import matplotlib.pyplot as plt
import csv

def genetic_algorithm(initializer, 
                      pop_size,
                      points_matrix,
                      fitness_evaluator, 
                      generations,
                      crossover_operator,
                      mutator,
                      selector,
                      ts_size, 
                      elite_size, 
                      p_xo,
                      p_m,
                      verbosity,
                      plot,
                      seed,
                      log):  
    ''' Performs a genetic algorithm based on various parameters.

    Args:
        initializer (Callable): The function to create the initial population.
        pop_size (int): The size of the population.,
        points_matrix (list): Matrix representing the points gained by moving from each area to all the other areas.
        fitness_evaluator (Callable): The function to evaluate the fitness of the population.
        generations (int): The number of generations to evolve the population.
        crossover_operator (Callable): The crossover operator for generating offspring individuals.
        mutator (Callable): The mutation function for offspring individuals.
        selector (Callable): The selection function for parent individuals.
        ts_size (int): Tournament size, in case selector = tournament_selection.
        elite_size (int): Quantity of best individuals to preserve in the next generation.
        verbosity (bool): Whether to display verbose output during the optimization process.
        p_xo (float): The probability of performing crossover.
        p_m (float): The probability of performing mutation.
        plot (bool): Whether to plot fitness landscape.
        seed (int): Initial value used by random number generator.
        log (bool): Whether to log the results to a file.

    Returns:
        Tuple(list, int): The best individual produced and its fitness value.
    '''
    # getting up the seed
    random.seed(seed)
    np.random.seed(seed)

    # generate initial population
    population = initializer(pop_size, points_matrix)
    # evaluate initial population
    fitnesses = fitness_evaluator(population, points_matrix)

    # verbose information: maximum fitness in population
    if verbosity:
        print('Initializing the population')
        print(f'Generation 0 | best fitness: {max(fitnesses)}')

    # create list to store best fitnesses of each generation
    best_fits = [max(fitnesses)]

    for i in range(generations):
        
        # perform elitism if specified in parameters
        if elite_size !=0:
            ranked_pop = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)
            offsprings = [ranked_pop[i][0] for i in range(elite_size)]
        else: 
            offsprings = []

        while len(offsprings) < len(population):

            # select parents to reproduce
            if selector == tournament_selection:
                 p1, p2 = selector(population, fitnesses, ts_size)
            else:
                p1, p2 = selector(population, fitnesses)
            
            # make sure the parents are different individuals (repeate only for 5 iterations, to avoid infinite loop)
            counter = 0
            while p1 == p2 and counter<5:
                if selector == tournament_selection:
                    p1, p2 = selector(population, fitnesses, ts_size)
                else:
                    p1, p2 = selector(population, fitnesses)
                counter += 1

            # perform crossover with probability p_xo
            if random.random() <= p_xo:
                c1, c2 = crossover_operator(p1, p2)

            else:
                c1, c2 = deepcopy(p1), deepcopy(p2)

            # perform mutation on children with probability p_m
            c1 = mutator(c1, p_m)
            c2 = mutator(c2, p_m)

            # add children to offspring list if they don't violate any constraints
            if not check_constraints(c1, points_matrix):
                offsprings.append(c1)
            if not check_constraints(c2, points_matrix):
                offsprings.append(c2)

        # new generation becomes the population for the next iteration
        # make sure that offpring population list is the same size as initial population 
        population = offsprings[:pop_size]
        fitnesses = fitness_evaluator(population, points_matrix)

        best_fits.append(max(fitnesses))

        # verbose information: best fitness in each generation
        if verbosity:
            print(f'Generation {i+1} | best fitness: {max(fitnesses)}')

    # plot fitness landscape (best fitness values over generations)
    if plot: 
        plt.plot(range(generations+1), best_fits)
        plt.xlabel('Generation')
        plt.ylabel('Best Fitness')
        plt.title('Fitness Landscape')
        plt.xticks(range(generations+1))
        plt.show()

    # return winner (individual with best fitness)
    winner, winner_fit = population[np.argmax(fitnesses)], max(fitnesses)

    # Log the parameters and results
    if log:
        with open('PROJETO_OA\log\ga_log.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([winner, winner_fit, points_matrix])

    # Remove PH from winner in case it appears
    if 'PH' in winner:
        winner.remove('PH')

    if verbosity:
        print(f'Best Route: {winner}.')
        print(f'Geo points gained from this route: {winner_fit}.')

    return (winner, winner_fit)

