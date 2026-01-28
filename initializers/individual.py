import random

areas = ['D', 'FC', 'G','QS', 'QG', 'CS', 'KS','RG', 'DV', 'SN']

def check_constraints(individual, points_matrix):
    '''Checks if individuals comply with all constraints: 
       - Routes that have Distant Village (DV) right after Queens Station (QS) can exclude Kings Station (KS).
       - Routes cannot have City Storerooms (CS) right after Queens Gardens (QG).
       - The Resting Grounds (RG) can only be reached in the last half of the session.
       - Each route goes through each area only once.
       - Routes can not have King Station (KS) and Place Holder (PH) at the same time.

    Args:
        individual (list): The individual representing a route.

    Returns:
        bool: True if constrainsts are being violated, False if not.      
    '''
    # Return True if CS comes right after QG
    if individual.index('CS') - individual.index('QG') == 1:
        return True
    if 'PH' in individual:
        if (individual.index('PH') - individual.index('QG') == 1) and (individual.index('CS') - individual.index('PH') == 1):
            return True

    # Return True if RG is in first half of route
    if individual.index('RG') <= len(individual)//2:
        return True
    
    # Return True if there are repeated areas in the route (excetp D)
    for i in range(1, len(individual) - 1):
        for j in range(1, len(individual) - 1):
            if individual[i] == individual[j] and i!=j:
                return True
        
    # Return True if a route has both KS and PH in it 
    if 'KS' in individual and 'PH' in individual:
        return True
    
    # Check if removing KS is better, if DV comes right after QS
    if (individual.index('DV') - individual.index('QS') == 1):
        # Create copy of individual to compare with and without KS
        ind_copy = individual.copy()

        # Replace KS with a placeholder (PH) in case fitness is better without it
        if 'KS' in individual:
            ind_copy[ind_copy.index('KS')] = 'PH'
            if route_geo_gains(ind_copy, points_matrix) > route_geo_gains(individual, points_matrix):
                individual[individual.index('KS')] = 'PH'

        # Put KS back in (after operators) in case fitness is better with it
        if 'PH' in individual:
            ind_copy[ind_copy.index('PH')] = 'KS'
            if route_geo_gains(ind_copy, points_matrix) > route_geo_gains(individual, points_matrix):
                individual[individual.index('PH')] = 'KS'

    # put KS back in (after operators) in case DV is not right after QS
    if (individual.index('DV') - individual.index('QS') != 1) and 'PH' in individual :
        individual[individual.index('PH')] = 'KS'

    return False 





def generate_individual(points_matrix):
    '''Creates an individual representing a route.

    Returns:
        list: A random order of the areas, representing a route (By default, routes include all areas once)
              All routes begin and end in Dirtmouth (D).
    '''
    shuffled_areas = areas[1:]  # Exclude 'D' from shuffling
    random.shuffle(shuffled_areas)

    # generate only acceptable individuals for the beginning of the population
    if check_constraints(shuffled_areas, points_matrix):
        return generate_individual(points_matrix)
    
    # Only returns acceptable individuals for the beginning of the population
    return ['D'] + shuffled_areas + ['D']


def route_geo_gains(individual, points_matrix):
    '''Calculate the total geo gains for a given route

    Args:
        individual (list): The individual representing a route.
        geo_gains_matrix (list): Matrix representing the points gained by moving from each area to all the other areas.

    Returns:
        int: Total geo gained from that route.
             Removes KS from route if DV comes right after QS and geo gains without it are greater.  
    '''
    id_to_count = individual.copy()
    if 'PH' in individual:
        id_to_count.remove('PH')
    
    gains = 0
    
    for i in range(len(id_to_count) - 1):
        current_area_index = areas.index(id_to_count[i])
        next_area_index = areas.index(id_to_count[i + 1])
        
        gains += points_matrix[current_area_index][next_area_index]
        
    return gains