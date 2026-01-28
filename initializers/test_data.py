import random

# geo points matrix example
gains_matrix = [[0, 10, 120, -230, 342, 10, 101, 432, -20, 243], 
                    [47, 0, 82, 103, 96, 231, -10, 34, 136, 109],
                    [18, 2, 0, 621, 64, 107, 3, 97, 71, 234],
                    [166, 336, 409, 0, 352, 49, 100, 392, 184, 249],
                    [-38, 202, 213, 210, 0, 14, -17, 216, 141, 215],
                    [284, 275, 394, 350, 285, 0, 340, 292, 330, 296],
                    [451, 494, 48, 381, 335, 269, 0, 550, 845, 173],
                    [342, -55, -76, 377, 12, 38, 56, 0, -81, 229],
                    [228, 219, 129, 346, 172, 222, 257, 213, 0, 146],
                    [39, 98, 76, 69, 43, 66, 58, 45, 59, 0]]

# the geo points are always integer values


def generate_points_matrix():
    '''Creates a random geo gains matrix, taking into account that the points gained by passing from G to FC  
        must be at least 3.2 % less than the minimum between all the other positive Geo gains

    Returns:
        list: Random geo gains matrix.
    '''
    # generate random matrix
    data = [[random.randint(-500, 500) for _ in range(10)] for _ in range(10)]
    
    # find all positive values in the matrix (except points of moving from G to FC)
    positive_values = [value for row in data for value in row if value > 0 and (data.index(row), row.index(value)) != (2, 1)]
    
    # make sure points of moving from G to FC are at least 3.2% less than the minimum positive value
    if positive_values:
        
        min_positive_value = min(positive_values)
        adjustment = 0.032 * min_positive_value
        
        data[2][1] = max(data[2][1] - adjustment, 0) 
    
    return data