from algorithm.algorithm import *

# replace the variable data with your data matrix
data = generate_points_matrix()

# run the algorithm with these parameters
genetic_algorithm(initializer=generate_population, 
                  pop_size=100,
                  points_matrix=data,
                  fitness_evaluator=evaluate_population, 
                  generations=20,
                  crossover_operator=position_crossover,
                  mutator=displacement_mutation,
                  selector=tournament_selection,
                  ts_size=5, 
                  elite_size=0, 
                  p_xo=0.95,
                  p_m=0.2,
                  verbosity=True,
                  plot=True,
                  seed=1,
                  log=False)

