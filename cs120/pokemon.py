"""
    File: pokemon.py
    Author: Elton Ho
    Course: CSC 120, Spring 2024
    Purpose: This program has 3 functions so that a solution for a user-inputed 
    query related to Pokemon can be printed out. These three functions convert 
    an inputted text file of Pokemon stats to a 2D dictionary, find the 
    averages for each type's stats, and compare the average stats of each type
    to find the largest.  
"""

def convert_to_dictionary():
    """Converts an inputed text file of Pokemon stats to a 2D dictionary of
    types and then the names of the Pokemon with the stats as the value. 
  
    Parameters: None. 
  
    Returns: A 2D dictionary of strings organized by type and then the name of
    the Pokemon with the stats as the value for the name of the Pokemon.
    """

    file_name = input()
    file = open(file_name)
    pokemon = {}
    for line in file:
        if line[0] != "#":  # skips the first line 
            pokemon_list = line.strip().split(',')

            # Creates an inside dictionary with the type as the key on the
            # first level
            if pokemon_list[2] not in pokemon:
                pokemon[pokemon_list[2]] = {}

            # Puts the name as the key of the inside dictionary and the
            # stats as the value 
            pokemon[pokemon_list[2]][pokemon_list[1]] = pokemon_list[4:]
    file.close()
    return pokemon

def avg(Pokemon):
    """Finds the averages for each type's stats.

    Parameters: Pokemon is a 2D dictionary of strings organized by type and 
    then the name of the Pokemon with the stats as the value for the name 
    of the Pokemon. 
  
    Returns: A dictionary of a string representing the Pokemon's type as
    the key and a list of either floats or integers as the averages of 
    each stat for that type as the value.
    """

    avg_stat = {}
    for Type in Pokemon:
        index = 0

        if Type not in avg_stat:  # makes the key as the type
            avg_stat[Type] = []

        # This loops is so that it stays on the same stat for each Pokemon 
        # and only moves on after finding the average 
        while index < 7:
            total = 0
            avg = 0 
            for Name in Pokemon[Type]:
                total += int(Pokemon[Type][Name][index])
            avg = total / len(Pokemon[Type])
            avg_stat[Type].append(avg)
            index += 1
    return avg_stat

def max_average(avg_stat):
    """Finds the largest average for a stat and the type associated with it. 
  
    Parameters: avg_stat is a dictionary of a string representing the Pokemon's 
    type as the key and the averages of each stat for that type as the value 
    which is either a float or an integer.
  
    Returns: A dictionary with integers as the key representing each stat and 
    the value being a 2D list with the largest average for that stat and the 
    type(s) associated with that average in the inside list. 
    """

    index = 0

    # each stat is represented by the index 
    max_stat = {0:[],1:[],2:[],3:[],4:[],5:[],6:[]}

    # This loops is so that it stays on the same stat for each type and only 
    # moves on after finding the max average stat and the type
    while index < 7:

        # finds the max average for a stat and one type associated with it 
        max = None
        max_type = None
        for Type in avg_stat:
            if max == None or max < avg_stat[Type][index]:
                max = avg_stat[Type][index]
                max_type = Type
        max_stat[index]= [max,[max_type]]

        # Second for loop is to see if there are other types with the same max 
        # average for a stat and appending that type to the inner list 
        for Type in avg_stat:
            if avg_stat[Type][index] == max and Type not in max_stat[index][1]:
                max_stat[index][1].append(Type)
            max_stat[index][1].sort()  # sorts the types by alphabetical order 

        index += 1
    return max_stat

def main():
    max_avg = max_average(avg(convert_to_dictionary()))

    # allows for a string of the name of each stat to represent it 
    max_dictionary = {'TOTAL':max_avg[0],'HP':max_avg[1],'ATTACK':max_avg[2], \
                      'DEFENSE':max_avg[3],'SPECIALATTACK':max_avg[4], \
                        'SPECIALDEFENSE':max_avg[5],'SPEED':max_avg[6]}
    
    # keeps asking for an input unless an empty line is inputed
    queries = None
    while queries != "":
        queries = input().upper()  # makes it case-insensitive 
        if queries in max_dictionary:

            # Prints each type with the same max average for that stat 
            # on its own line
            # max_dictionary[queries][1] = inner list of types
            # max_dictionary[queries][0] = max average for that stat 
            for index in range(len(max_dictionary[queries][1])):
                print("{}: {}".format(max_dictionary[queries][1][index], \
                                       max_dictionary[queries][0]))
main()

