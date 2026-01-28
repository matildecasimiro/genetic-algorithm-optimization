import random 
import numpy as np


# ROULETTE WHEEL SELECTION 
def roulette_wheel_selection(population, fitnesses):
    '''Performs roullete wheel selection to choose parents from a population.

    Args:
        population (list): Array of individuals.
        fitnesses (list): Fitness values of the population.

    Returns:
        tuple: Selected individuals.
    '''    
    # calculate selection probabilities for each individual (based on fitness values)
    probabilities = [fit / sum(fitnesses) for fit in fitnesses]

    # select two parents 
    parents = random.choices(population, probabilities, k=2)

    return tuple(parents)



# TOURNAMENT SELECTION 
def ts_inner(population, fitnesses, t_size=5):
    '''Performs tournament selection on a population.

    Args:
        population (list): Array of individuals.
        fitnesses (list): Fitness values of the population.
        t_size (int): Tournament size.

    Returns:
        list: Selected individual.
    '''    
    # select individuals randomly from population to participate in tournament
    t_indexes = random.sample(range(len(population)), t_size)
    t_fitnesses = [fitnesses[i] for i in t_indexes]

    # choose winner (max fitness, since it is a maximization problems)
    winner_index = t_indexes[np.argmax(t_fitnesses)]
    
    return population[winner_index]

def tournament_selection(population, fitnesses, t_size=5):
    '''Performs tournament selection to choose parents from a population.
    Args:
        population (list): Array of individuals.
        fitnesses (list): Fitness values of the population.
        t_size (int): Tournament size.

    Returns:
        tuple: Selected individuals.
    '''        
    return (ts_inner(population, fitnesses, t_size), 
            ts_inner(population, fitnesses, t_size))



# SELF-ADAPTATIVE TOURNAMENT SELECTION
def calculate_diversity(fitnesses):
    ''' Calculates the diversity of the population.

    Args:
        fitnesses (list): Fitness values of the population.

    Returns:
        float: Selected individuals.
    '''   
    avg_fit = sum(fitnesses) / len(fitnesses)
    max_fit = max(fitnesses)
    min_fit = min(fitnesses)
    fit_range = max_fit - min_fit

    # Handle the case when fit_range is zero
    if fit_range == 0:
        return sum(abs(fit - avg_fit) for fit in fitnesses) / (len(fitnesses) * 1/2)
    
    return sum(abs(fit - avg_fit) for fit in fitnesses) / (len(fitnesses) * fit_range/ 2)

def self_adaptative_tournament_selection(population, fitnesses):
    '''Performs self-adaptative tournament selection to choose parents from a population.
    Args:
        population (list): Array of individuals.
        fitnesses (list): Fitness values of the population.

    Returns:
        tuple: Selected individuals.
    '''   
    # calculate tournament size based in population diversity
    adapt_t_size = int(2 + (len(population) -2) * calculate_diversity(fitnesses))

    return (ts_inner(population, fitnesses, adapt_t_size), 
            ts_inner(population, fitnesses, adapt_t_size))



# LINEAR RANKING SELECTION
def linear_ranking_selection(population, fitnesses, select_press=1.5):
    ''' Performs linear ranking selection to choose parents from a population.

    Args:
        population (list): Array of individuals.
        fitnesses (list): Fitness values of the population.
        select_press (float): Selection pressure (typically between 1 and 2).

    Returns:
        tuple: Selected individuals.
    '''
    # sort population based on fitness (descending order if maximization = true)
    ranked_pop = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)

    # calculate rank for each individual in the population
    ranks = np.arange(1, len(population) + 1)

    # calculate selection probabilities for each individual 
    probabilities = (2-select_press) / len(population) + 2 * (ranks- 1) * (select_press -1) / (len(population)*(len(population)-1))
    
    # select parents
    parents = random.choices([individual for individual, fitness_value in ranked_pop], probabilities, k=2)

    return tuple(parents)



# EXPONENTIAL RANKING SELECTION 
def exponential_ranking_selection(population, fitnesses, k=1.0):
    ''' Performs exponential ranking selection to choose parents from a population.

    Args:
        population (list): Array of individuals.
        fitnesses (list): Fitness values of the population.
        k (float): Constant that controls the shape of the probability distribution.

    Returns:
        tuple: Selected individuals.
    '''
    # sort population based on fitness (descending order if maximization = true)
    ranked_pop = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)

    # calculate rank for each individual in the population
    ranks = np.arange(1, len(population) + 1)

    # calculate selection probabilities for each individual 
    probabilities = (1 - np.exp(-ranks /k))
    
    # select parents
    parents = random.choices([individual for individual, fitness_value in ranked_pop], probabilities, k=2)
    
    return tuple(parents)


















def calculate_probabilities(fitnesses, maximization):
    if maximization:
        probabilities = [fit / sum(fitnesses) for fit in fitnesses]
    else:
        probabilities = [1 - (fit / sum(fitnesses)) for fit in fitnesses]
    return probabilities


def stochastic_universal_sampling(maximization):
    def inner_fps(population, fitnesses):
        probabilities = calculate_probabilities(fitnesses, maximization)
        total_fitness = sum(fitnesses)
        pointer_distance = total_fitness / len(population)
        start = random.uniform(0, pointer_distance)
        pointers = [start + i * pointer_distance for i in range(len(population))]
        selected = []
        current_fitness = 0
        index = 0
        for pointer in pointers:
            while current_fitness < pointer:
                current_fitness += probabilities[index]
                index = (index + 1) % len(population)
            selected.append(population[index])
        selected_probabilities = [probabilities[population.index(individual)] for individual in selected]
        return random.choices(selected, selected_probabilities)[0]
    return inner_fps

