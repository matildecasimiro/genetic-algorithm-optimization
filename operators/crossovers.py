import random

# ORDER CROSSOVER
def order_xo_one(p1,p2, point_1, point_2):
    '''Performs order crossover between two individiuals of the population, taking into account that the first and last
       elements of every individual should always be D.

    Args:
        p1 (list): An individual representing a route.
        p2 (list): An individual representing a route.
        point_1 (int): First crossover point.
        point_2 (int): Second crossover point.

    Returns:
        list: offspring of crossover.
    '''
    # perform crossover without D
    p1_xo, p2_xo = p1[1:-1], p2[1:-1]

    # child of length equal to parents ihnerits order of p1 between crossover points
    child = ['x' for _ in range(len(p1_xo))]
    child[point_1:point_2] = p1_xo[point_1:point_2]

    # remaining areas of p1 are placed into the child in the order in which they appear in p2
    remainig_areas = [area_p for area_p in p2_xo if area_p in (p1_xo[:point_1] + p1_xo[point_2:])]

    # in case crossover includes individuals with PH
    if len(remainig_areas) < len(p1_xo[:point_1] + p1_xo[point_2:]):
        if 'PH' in p1_xo: 
            remainig_areas.append('PH')
        else:
            remainig_areas.append('KS')
    
    for i in range(len(child)):
        if child[i] == 'x': 
            child[i] = remainig_areas[0]
            remainig_areas.remove(remainig_areas[0])

    return ['D'] + child  + ['D']

def order_crossover(p1,p2):
    '''Performs order crossover between two individiuals of the population.

    Args:
        p1 (list): An individual representing a route.
        p2 (list): An individual representing a route.

    Returns:
        tuple: offsprings of crossover.
    '''
    # create two random crossover points
    xo_point_1 = random.randint(0, len(p1) - 4)
    xo_point_2 = random.randint(xo_point_1+1, len(p1) - 3)

    return (order_xo_one(p1, p2, xo_point_1, xo_point_2), 
            order_xo_one(p2, p1, xo_point_1, xo_point_2))



# POSITION-BASED CROSSOVER
def position_xo_one(p1, p2, positions):
    '''Performs position-based crossover between two individiuals of the population, taking into account that the first and last
       elements of every individual should always be D.

    Args:
        p1 (list): An individual representing a route.
        p2 (list): An individual representing a route.
        positions (list): Crossover points.

    Returns:
        list: offspring of crossover.
    '''
    # perform crossover without D
    p1_xo, p2_xo = p1[1:-1], p2[1:-1]

    # child of length equal to parents ihnerits areas of p1 in the position of crossover points
    child = ['x' for _ in range(len(p1_xo))]
    for i in positions:
        child[i] = p1_xo[i]

    # remaining areas of p1 are placed into the child in the order in which they appear in p2
    remainig_areas = [area_p for area_p in p2_xo if (area_p in p1_xo) and (area_p not in child)]

    # in case crossover includes individuals with PH
    if len(remainig_areas) < len(p1_xo)-len(positions):
        if 'PH' in p1_xo: 
            remainig_areas.append('PH')
        else:
            remainig_areas.append('KS')
    
    for i in range(len(child)):
        if child[i] == 'x': 
            child[i] = remainig_areas[0]
            remainig_areas.remove(remainig_areas[0])

    return ['D'] + child  + ['D']

def position_crossover(p1, p2):
    '''Performs position-based crossover between two individiuals of the population.

    Args:
        p1 (list): An individual representing a route.
        p2 (list): An individual representing a route.

    Returns:
        tuple: offsprings of crossover.
    '''
    # Create random crossover poinst
    len_positions = random.randint(1, len(p1) - 3)
    positions_xo = random.sample(range(0, len(p1) - 3), len_positions)

    return (position_xo_one(p1, p2, positions_xo),
             position_xo_one(p2,p1, positions_xo))



# CYCLE CROSSOVER
def cycle_xo_one(p1, p2, start_index):
    '''Performs cycle crossover between two individiuals of the population

    Args:
        p1 (list): An individual representing a route.
        p2 (list): An individual representing a route.
        start_index (int): Start position for crossover.

    Returns:
        list: offspring of crossover.

    '''

    # Set to keep track of filled positions in the offspring
    filled_positions = set()

    # perform crossover without D
    p1_xo, p2_xo = p1[1:-1], p2[1:-1]

    # to avoid producing offsprings with both KS and PH, if parents have PH, it is replaced with KS 
    if 'PH' in p1_xo:
        p1_xo[p1_xo.index('PH')] = 'KS'
    if 'PH' in p2_xo:
        p2_xo[p2_xo.index('PH')] = 'KS'

    # child of length equal to parents 
    child = ['x' for _ in range(len(p1_xo))]

    while True:
        # Assign the value from parent1 to the offspring at the start position
        child[start_index] = p1_xo[start_index]

        # Mark the start position as filled
        filled_positions.add(start_index)

        # Find the index of the value in parent2 that corresponds to the value at the current start position in parent1
        index = p1_xo.index(p2_xo[start_index])

        # Set the new start position for the next iteration
        start_index = index

        # If the new start position is already filled, it indicates completion of a cycle
        if start_index in filled_positions:
            break

    # Fill the remaining None values in the offspring with the corresponding values from parent2
    for i in range(len(child)):
        if child[i] == 'x':
            child[i] = p2_xo[i]

    return ['D'] + child  + ['D']

def cycle_crossover(p1, p2):
    '''Performs position-based crossover between two individiuals of the population.

    Args:
        p1 (list): An individual representing a route.
        p2 (list): An individual representing a route.

    Returns:
        tuple: offsprings of crossover.
    '''
    # determine start index
    start = 0  # random.randint(0, size - 1)

    return (cycle_xo_one(p1, p2, start), cycle_xo_one(p2, p1, start))



# PARTIALLY-MAPPED CROSSOVER
def partially_mapped_xo_one(p1,p2, point_1, point_2):
    '''Performs partially-mapped crossover between two individiuals of the population, taking into account that the first and last
       elements of every individual should always be D.

    Args:
        p1 (list): An individual representing a route.
        p2 (list): An individual representing a route.
        point_1 (int): First crossover point.
        point_2 (int): Second crossover point.

    Returns:
        list: offspring of crossover.
    '''
    # perform crossover without D
    p1_xo, p2_xo = p1[1:-1], p2[1:-1]

    # to avoid producing offsprings with both KS and PH, if parents have PH, it is replaced with KS 
    if 'PH' in p1_xo:
        p1_xo[p1_xo.index('PH')] = 'KS'
    if 'PH' in p2_xo:
        p2_xo[p2_xo.index('PH')] = 'KS'

    # child of length equal to parents ihnerits order of p1 between crossover points
    child = ['x' for _ in range(len(p1_xo))]
    child[point_1:point_2] = p1_xo[point_1:point_2]

    # Map the elements from parent2 to the child
    for i in range(point_1, point_2):
        if p2_xo[i] not in child:
            # Find the index of the corresponding element in parent1
            index = p2_xo.index(p1_xo[i])
            # Find an empty position in the child to place the element
            while child[index] != 'x':
                index = p2_xo.index(p1_xo[index])
            # Place the element in the child
            child[index] = p2_xo[i]

    # Copy the remaining elements from parent2 to the child
    for i in range(len(child)):
        if child[i] == 'x':
            child[i] = p2_xo[i]
    
    return ['D'] + child  + ['D']

def partially_mapped_crossover(p1,p2):
    '''Performs partially-mapped crossover between two individiuals of the population.

    Args:
        p1 (list): An individual representing a route.
        p2 (list): An individual representing a route.

    Returns:
        tuple: offsprings of crossover.
    '''
    # create two random crossover points
    xo_point_1 = random.randint(0, len(p1) - 4)
    xo_point_2 = random.randint(xo_point_1+1, len(p1) - 3)

    return (partially_mapped_xo_one(p1, p2, xo_point_1, xo_point_2),
             partially_mapped_xo_one(p2, p1, xo_point_1, xo_point_2))
    


# MODIFIED PARTIALLY-MAPPED CROSSOVER 
def modified_pm_xo_one(p1,p2, point_1, point_2):
    '''Performs modified partially-mapped crossover between two individiuals of the population, taking into account that
       the first and last elements of every individual should always be D.

    Args:
        p1 (list): An individual representing a route.
        p2 (list): An individual representing a route.
        point_1 (int): First crossover point.
        point_2 (int): Second crossover point.

    Returns:
        list: offspring of crossover.
    '''
    # perform crossover without D
    p1_xo, p2_xo = p1[1:-1], p2[1:-1]
    
    # to avoid producing offsprings with both KS and PH, if parents have PH, it is replaced with KS 
    if 'PH' in p1_xo:
        p1_xo[p1_xo.index('PH')] = 'KS'
    if 'PH' in p2_xo:
        p2_xo[p2_xo.index('PH')] = 'KS'

    # child of length equal to parents ihnerits order of p1 between crossover points
    child = ['x' for _ in range(len(p1_xo))]
    child[point_1:point_2] = p1_xo[point_1:point_2]

    # Corresponding positions in p2 passes elements to child, if they have not already been inherited from parent 1
    for i in range(len(child)):
        if child[i] == 'x' and p2_xo[i] not in child:
            child[i] = p2_xo[i]
    
    # remaining areas are randomly placed in the child
    remaining_areas = [area_p for area_p in p1_xo if area_p not in child]
    random.shuffle(remaining_areas)

    for i in range(len(child)):
        if child[i] == 'x': 
            child[i] = remaining_areas[0]
            remaining_areas.remove(remaining_areas[0])

    return ['D'] + child  + ['D']

def modified_partially_mapped_crossover(p1,p2):
    '''Performs modified partially-mapped crossover between two individiuals of the population.

    Args:
        p1 (list): An individual representing a route.
        p2 (list): An individual representing a route.

    Returns:
        tuple: offsprings of crossover.
    '''
    # create two random crossover points
    xo_point_1 = random.randint(0, len(p1) - 4)
    xo_point_2 = random.randint(xo_point_1+1, len(p1) - 3)

    return (modified_pm_xo_one(p1, p2, xo_point_1, xo_point_2),
             modified_pm_xo_one(p2, p1, xo_point_1, xo_point_2))