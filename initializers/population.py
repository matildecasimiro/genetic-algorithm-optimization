import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from initializers.individual import *

def generate_population(pop_size, points_matrix):
    '''Creates a population of individuals (routes).

    Args:
        areas (list):  Initials of all the areas in the game.
        pop_size (int): Desired population size.

    Returns:
        list: An array of individuals that compose the population.
    '''

    return [generate_individual(points_matrix) for _ in range(pop_size)]


def evaluate_population(population, points_matrix):
    '''Creates a list of the geo gains of each individual in the population.

    Args:
        population (list): Array of individuals.
        geo_gains_matrix (list): Matrix representing the points gained by moving from each area to all the other areas.

    Returns:
        list: Total geo gains values corresponding to each individual in the population.
    '''

    return [route_geo_gains(individual,points_matrix) for individual in population]

    