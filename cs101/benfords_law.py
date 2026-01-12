'''
Elton Ho 
CSC110 Fall 2023
1 p.m. Class
Programming Project 5
This program has 4 separate functions that make a list of the numbers in a file,
count the amount of numbers that start with a certain digit, find the percentage 
of a list of numbers that start with a certain digit, and check if a data set 
follows Benford's law. 
'''

def csv_to_list(file_name):
    '''
    This function returns a list of strings of the numbers in a file.
    Args:
            file_name: a string representing the name of the file to be opened.
    Returns:
            A list of strings of the numbers in a file.
    '''

    # opens a file in read mode 
    file = open(file_name, "r")

    # creates an empty list
    list = []

    # goes through each line of the file, strip("\n") and split(",") each line,
    # and adds only the numbers from the new list to the list to be returned. 
    for x in file:
        csv_list= x.strip("\n").split(",")
        for y in csv_list:
            if y[0] in "1234567890":
                list.append(y)

    # returns the list 
    return list 

def count_start_digits(numbers):
    '''
    This function returns a dictionary of integers with the count of numbers that
    start with a certain digit as the value and that certain digit as the key.
    Args:
            numbers: a list of strings that represents the numbers in a file.
    Returns:
            A dictionary of integers with the count of numbers that start with
            a certain digit as the value and that certain digit as the key.
    '''

    # creates the initial count 
    dictionary = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

    # goes through the numbers list and adds to the count depending on what the
    # number started with after it was converted to an integer to compare
    for x in numbers:
        if int(x[0]) in dictionary:
            dictionary[int(x[0])] += 1
        
    # returns the dictionary of the count 
    return dictionary

def digit_percentages(counts):
    '''
    This function returns a dictionary with a float representing the percentage
    of the list of numbers that starts with a certain number as the value and
    that certain number as the key. 
    Args:
            counts: a dictionary of integers representing the count of a number
            that starts with a certain digit.
    Returns:
            A dictionary with a float representing the percentage of the list of
            numbers that start with a certain number as the value and that 
            certain number as the key. 
    '''

    # creates the template for the new dictionary 
    dictionary = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

    # sums up all the values
    sum = 0
    for x in counts:
        sum += int(counts[x])

    # calculates the percentages and adds them to the dictionary as values
    for x in counts:
        dictionary[x] += round(int(counts[x]) / sum * 100, 2)

    # return the new dictionary     
    return dictionary

def check_benfords_law(percentages_per_digit):
    '''
    This function returns True if a dictionary representing a data set follows
    Benford's law within the margin and False if it doesn't. 
    Args:
            percentages_per_digit: a dictionary with the value as floats 
            representing the percentage of a list that starts with a certain 
            digit and that certain digit as an integer for the key.
    Returns:
            True if a dictionary representing a data set follows
            Benford's law within the margin and False if it doesn't. 
    '''

    # dictionary representing the percentages that follow Benford's law
    benfords_law = {1: 30, 2: 17, 3: 12, 4:9, 5: 7, 6: 6, 7: 5, 8: 5, 9: 4}

    # checks whether the argument follows Benford's law's percentages within
    #  margin  
    for x in percentages_per_digit:
        if percentages_per_digit[x] >= benfords_law[x] + 10 or \
        percentages_per_digit[x] <= benfords_law[x] - 5:
            return False
    return True 
