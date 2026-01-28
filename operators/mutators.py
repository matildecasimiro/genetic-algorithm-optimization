import random

# SWAP MUTATION 
def swap_mutation(individual, mutation_rate):
    '''Performs swap mutation on an individual with defined mutation rate. First and last elements are never modified.

    Args:
        individual (list): An individual representing a route.
        mutation_rate (float): Probability at which individual suffers mutation.

    Returns:
        list: Mutated individual.
    '''
    mutated = individual.copy()

    # Swap two random positions if random probability generated is lower than mutation rate
    if random.random() < mutation_rate:
        swap_points = random.sample(range(1, len(individual) - 1), 2)
        mutated[swap_points[0]], mutated[swap_points[1]] = mutated[swap_points[1]], mutated[swap_points[0]]

    return mutated 


# SCRAMBLE MUTATION 
def scramble_mutation(individual, mutation_rate):
    '''Performs scramble mutation on an individual with defined mutation rate. First and last elements are never modified.

    Args:
        individual (list): An individual representing a route.
        mutation_rate (float): Probability at which individual suffers mutation.

    Returns:
        list: Mutated individual.
    '''
    mutated = individual.copy()

    # scramble randomly chosen positions if random probability generated is lower than mutation rate
    if random.random() < mutation_rate:
        scramble_positions = random.sample(range(1, len(mutated) - 1), random.randint(1, len(mutated) - 2))

        scramble_areas = [mutated[i] for i in scramble_positions]
        random.shuffle(scramble_areas)

        for j in scramble_positions:
            mutated[j] = scramble_areas[0]
            scramble_areas.remove(scramble_areas[0])

    return mutated 


# DISPLACEMENT MUTATION
def displacement_mutation(individual, mutation_rate):
    '''Performs displacement mutation on an individual with defined mutation rate. First and last elements are never modified.

    Args:
        individual (list): An individual representing a route.
        mutation_rate (float): Probability at which individual suffers mutation.

    Returns:
        list: Mutated individual.
    '''
    mutated = individual.copy()

    # perform displacement of a random individual segment if random probability generated is lower than mutation rate
    if random.random() < mutation_rate:
        # segment size should be at least 1 but not larger than half the individual
        segment_size = random.randint(1, len(individual) // 2) 

        # displacement segment and position should not include the first or last position on the individual
        start_position = random.randint(1, len(individual)- 1 - segment_size)
        end_position = start_position + segment_size
        displacement_position = random.randint(1, len(individual) -1- segment_size)

        mutated = individual[:start_position] + individual[end_position:]
        mutated = mutated[:displacement_position] + individual[start_position:end_position] + mutated[displacement_position:]
    
    return mutated


# THRORS MUTATION
def thrors_mutation(individual, mutation_rate):
    '''Performs thrors mutation on an individual with defined mutation rate. First and last elements are never modified.

    Args:
        individual (list): An individual representing a route.
        mutation_rate (float): Probability at which individual suffers mutation.

    Returns:
        list: Mutated individual.
    '''
    mutated = individual.copy()
    
    # rotate 3 random positions in individual if random probability generated is lower than mutation rate
    if random.random() < mutation_rate:
        first_i = random.randint(1, len(individual)-4)
        second_i = random.randint(first_i + 1, len(individual)-3)
        third_i = random.randint(second_i + 1, len(individual)-2)

        # first becomes second, second becomes third, and third becomes first
        mutated[first_i], mutated[second_i], mutated[third_i] = mutated[third_i], mutated[first_i], mutated[second_i]
    
    return mutated


# INVERSION MUTATION
def inversion_mutation(individual, mutation_rate):
    '''Performs inversion mutation on an individual with defined mutation rate. First and last elements are never modified.

    Args:
        individual (list): An individual representing a route.
        mutation_rate (float): Probability at which individual suffers mutation.

    Returns:
        list: Mutated individual.
    '''
    mutated = individual.copy()

    # invert random subset of individual if random probability generated is lower than mutation rate
    if random.random() < mutation_rate:
        start_position = random.randint(1, len(mutated) - 4)
        end_position = random.randint(start_position + 2, len(mutated) - 2)

        inverted_segment = individual[start_position:end_position][::-1]

        mutated = individual[:start_position] + inverted_segment + individual[end_position:]

    return mutated