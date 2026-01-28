from algorithm import *
import gc
import time

def evaluate_combination(params, algorithm, iterations, points_matrices):
    ''' Evaluates the performance of a set of parameters in an algorithm.

    Args:
        params (dict): Combination of parameters to evaluate.
        algorithm (callable): Function to test the parameters in.
        iterations (int): Number iterations to be executed to evaluate the parameters combination.
        points_matrices (list): Data matrices for each iteration.

    Returns:
        float: Average performance of the parameters combination.
    '''
    #print(f'TESTING: {params}')
    time.sleep(1)

    # try-except block to catch any potential errors that might occur during the evaluation
    try:
        performances = []

        for i in range(iterations):
            params['points_matrix'] = points_matrices[i]
            result = algorithm(**params)
            performances.append(result[1])

        print(f'Average fitness: {np.mean(performances)}')

        with open('PROJETO_OA\log\grid_search.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([np.mean(performances), params])
        
        # calculate average performance of the parameters combination
        return np.mean(performances)
    
    except Exception as e:
        print(f"Error message: {str(e)}.")
        print(f'Parameters with error: {params}')
        return 0


def clean_combinations(combinations):
    ''' Filters out redundant combinations of parameters.

    Args:
        combinations (list): All possible combinations of parameters of the genetic algorithm function.

    Returns:
        list: Combinations to test in the grid search.
    '''
    clean_combs = []

    # discard combinations of same parameters with different ts_size if the selector is not tournament selection (avoid redundancy)
    for param_comb in combinations:
        if param_comb['selector'] != tournament_selection and param_comb['ts_size'] == 5: 
            clean_combs.append(param_comb)       
        
        if param_comb['selector'] == tournament_selection:
            clean_combs.append(param_comb)  
    
    return clean_combs




from sklearn.model_selection import ParameterGrid
import multiprocessing
from functools import partial

def grid_search(algorithm, iterations, parameters):
    ''' Evaluates the performance of an algorithm with all combinations of the specified parameter across a certain amount of 
        iterations.

    Args:
        algorithm (callable): Function to test the parameters in.
        iterations (int): Number iterations to be executed to evaluate each parameters combination.
        parameters (list): All parameters to test.

    Returns:
        dict: Set of parameters that performs the best.
    '''
    # use multiple CPU cores to parallelize processing (makes the grid search run faster)
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    # Generate all parameter combinations and remove the redundant ones (optimize computation)
    combinations = ParameterGrid(parameters)    
    combinations = clean_combinations(combinations)

    print(f'There are {len(combinations)} combinations to test.')

    # generate the data matrices to test across all parameter combinations
    points_matrices = [generate_points_matrix() for _ in range(iterations)]

    
    partial_evaluator = partial(evaluate_combination, algorithm = algorithm,
                                iterations =  iterations,
                                  points_matrices = points_matrices)
    
    # parallelize evaluation of all parameter combinations
    results = pool.map(partial_evaluator,
                    combinations)
        
    print('Combinations concluded! ')        

    # Sort results based on average fitness (hightest one at the top)
    ranked_results = sorted(zip(combinations, results), key=lambda x: x[1], reverse=True)

    # delete unnecessary variables from memory
    del results, combinations, points_matrices
        
    best_params, best_fit = ranked_results[0][0], ranked_results[0][1]
    print(f'Best Parameters: {best_params}')
    print(f'Average fitness: {best_fit}')

    del ranked_results

    # garbage collection to release unused memory
    gc.collect()

    # close multiprocessing pool
    pool.close()

    return best_params



c_ops = [order_crossover,
        position_crossover,
        cycle_crossover,
        partially_mapped_crossover,
        modified_partially_mapped_crossover]

m_ops = [swap_mutation,
        scramble_mutation,
        displacement_mutation,    
        thrors_mutation,     
        inversion_mutation]

s_ops = [roulette_wheel_selection,
         tournament_selection, 
         self_adaptative_tournament_selection, 
         linear_ranking_selection,
         exponential_ranking_selection]

ga_parameters = {'initializer' : [generate_population],
                'pop_size' : [20, 50, 100],
                'points_matrix' : [gains_matrix],
                'fitness_evaluator' : [evaluate_population],
                'generations' : [5, 10, 20],
                'crossover_operator' : c_ops,
                'mutator' : m_ops,      
                'selector' : s_ops,
                'ts_size': [5, 10, 15],               
                'elite_size' : [0, 1, 2],         
                'p_xo': [0.8, 0.9, 0.95],  
                'p_m': [0.05, 0.1, 0.2],     
                'verbosity' : [False],          
                'plot': [False],
                'seed': [0, 1],
                'log': [False]}



if __name__ == '__main__':
    grid_search(genetic_algorithm, 15, ga_parameters)  


# Best Parameters:
# pop_size = 100
# generations = 20
# crossover_operator = position_crossover
# mutator = displacement_mutation
# selector = tournament_selection
# ts_size = 5
# elite_size = 0 
# p_xo = 0.95
# p_m = 0.2
# seed = 1

'''
python PROJETO_OA\algorithm\grid_serach.py
'''
