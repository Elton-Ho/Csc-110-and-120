'''
Elton Ho 
CSC110 Fall 2023
1 p.m. Class
Programming Project 3
This program has four separate functions that find the mean, variance,
standard deviation, and range of a list of numeric values.
'''

def mean(numbers):
    '''
    This function returns a float rounded to two decimals that represents the
    mean of the list of values called "numbers".
    Args:
            numbers: a list of integers or floats. 
    Returns:
            A float rounded to two decimals that represents the mean of the
            list of values called "numbers."
    '''

    # starts at the beginning of the list
    index = 0

    # starts with a total of 0
    total = 0

    # deals with empty lists
    if len(numbers) > 0: 

        # adds every number in the list and assigns that value to "total"
        while index < len(numbers):
            total += numbers[index]
            index += 1

        # calculation for mean    
        return round(total / len(numbers), 2)
    
    # return 0 if the list is empty
    return 0

def variance(numbers):
    '''
    This function returns a float rounded to two decimals that represents the
    variance of the list of values called "numbers".
    Args:
            numbers: a list of integers or floats. 
    Returns:
            A float rounded to two decimals that represents the variance of the
            list of values called "numbers."
    '''

    # starts at the beginning of the list
    index = 0

    # starts with a total of 0
    total = 0

    # deals with empty lists
    if len(numbers) > 0:

        # adds up all the (individual numbers - mean) ** 2 and assigns it to
        # "total" and calls the mean function for the mean
        while index < len(numbers):
            total += (numbers[index] - mean(numbers)) ** 2
            index += 1

        # rounds the last part of the calculation for variance to two decimals
        return round (total / (len(numbers) - 1), 2)        
    
    # return 0 if the list is empty
    return 0    

def sd(numbers):
    '''
    This function returns a float rounded to two decimals that represents the
    standard deviation of the list of values called "numbers".
    Args:
            numbers: a list of integers or floats. 
    Returns:
            A float rounded to two decimals that represents the standard 
            deviation of the list of values called "numbers."
    '''
    # calculates the standard deviation by calling the variance function and
    # rounds to two decimal places
    return round(variance(numbers) ** .5, 2) 

def list_range(numbers):
    '''
    This function returns a float or integer that represents the range of the
    list of values called "numbers".
    Args:
            numbers: a list of integers or floats. 
    Returns:
            A float or integer that represents the range of the list of values
            called "numbers."
    '''

    # deals with empty lists
    if len(numbers) > 0:

        # starts at the beginning of the list
        index = 0

        # assumes the maximum is the first item in the list
        maximum = numbers[0]

        # assumes the minimum is the first item in the list
        minimum  = numbers[0]

        # checks the whole list
        while index < len(numbers):

            # checks for a new value as the maximum
            if numbers[index] > maximum:
                maximum = numbers[index]

            # checks for a new value as the minimum
            if numbers[index] < minimum :
                minimum  = numbers[index]
            index += 1

        # calculates the range
        return maximum - minimum 
    
    # return 0 if the list is empty
    return 0      
