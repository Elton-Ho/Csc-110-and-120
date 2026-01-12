"""
    File: word_grid.py
    Author: Elton Ho
    Course: CSC 120, Spring 2024
    Purpose: This program has 3 functions that take the input for grid size
    and seed and returns the grid size and changes the seed, make a grid of 
    random letters, and prints out the grid.
"""

import random

def init():
    """Takes the input for grid size and seed and returns an integer 
    representing the grid size inputed and changes the seed to the inputed
    seed.
  
    Parameters: None.
  
    Returns: An integer that is the inputed grid size.
    """
    grid_size = int(input())
    seed_value = input()
    random.seed(seed_value)  # changes the seed to what was inputed 
    return grid_size

def make_grid(grid_size):
    """Creates a grid of random letters based on what the grid size is and 
    returns the grid which is a 2D list. 
  
    Parameters: grid_size is an integer representing the size of the grid. 
  
    Returns: A 2D list of random letters representing the grid. 
    """
    
    grid = []

    # makes a string of letters to be randomly selected 
    letters = "abcdefghijklmnopqrstuvwxyz"

    # makes the grid the correct size vertically 
    for x in range(grid_size): 
        grid.append([])  # creates the inner list 

        # makes the grid the correct size horizontally 
        for y in range(grid_size):

            # appends a random letter to the inner list
            grid[x].append(letters[random.randint(0,25)])
    return grid

def print_grid(grid):
    """Iterates through the grid and prints it in the correct format. 
  
    Parameters: grid is the 2D list that represents the grid to be printed 
  
    Returns: None. 
    """
    for row in grid:
        print(",".join(row))  # prints the row in x1,x2,x3... format 

def main():
    print_grid(make_grid(init()))  # prints the created grid based on inputs

main()
