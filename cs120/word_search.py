"""
    File: word_search.py
    Author: Elton Ho
    Course: CSC 120, Spring 2024
    Purpose: This program has 7 functions that return a list of valid words
    based on a text file, returns a grid based on a text file, checks if a 
    string is in the list of valid words, checks the grid horizontally for
    valid words, checks the grid vertically for valid words, checks the grid 
    diagonally for valid words, and prints out the valid words found in the
    grid.
"""

def get_word_list():
    """Takes the input for the name of the file with valid words and converts
    it into a list to be returned.
  
    Parameters: None.
  
    Returns: A list of strings representing valid words.
    """

    filename = input()
    f = open(filename)
    valid_words = [] 
    for line in f:

        # adds each line (each with one word per line) without "\n" to the list
        valid_words.append(line.strip())  
    return valid_words


def read_letters_file():
    """Takes the input for the name of the file representing the grid and
    converts it to a 2D list to be returned.
  
    Parameters: None.
  
    Returns: A 2D list of strings representing the grid.
    """

    filename = input()
    f = open(filename)
    grid = []
    for line in f:
        grid.append(line.strip().split())  # adds the inner list (grid's row) 
    return grid

def occurs_in(substr, word_list):
    """Checks if the case insensitive string (substr) is present in the list of 
    valid words(word_list).
  
    Parameters: substr is a string that is being checked.
    word list is the list of strings of valid words.
  
    Returns: A boolean depending on whether the case-insensitive string is in
    the list of valid words.
    """

    for x in word_list:

        # makes it case-insensitive and does the checking
        if substr.upper() == x.upper(): 
            return True
    return False
    
def horizontally(grid, valid_list, add_to):
    """Checks horizontally if a grid has valid words and append those words
    to a list(add_to).
  
    Parameters: grid is a 2D list representing the grid.
    valid list is the list of strings of valid words.
    add_to is the list that will get appended with the found valid words.  
  
    Returns: None. 
    """
    
    found = []  # list of valid found words 
    for row in grid:

        # left to right 
        for start in range(len(row) - 2):  # bounds for starting positions 
            end = start + 3 
            while end <= len(row):  # bounds for end position
                
                # creates the string starting from the start to the end
                string = ""
                for i in range(start,end):
                    string += row[i]
                
                # calls the function to test validity 
                if occurs_in(string, valid_list): 
                    found.append(string)
                end += 1

        # right to left (same as left to right except for the bounds)  
        for start in range(len(row) -1, 1, -1):  # bounds for start position 
            end = start - 2
            while end >= 0:  # bounds for end position

                string = ""
                for i in range(start,end -1, -1):
                    string += row[i]
                
                if occurs_in(string, valid_list):
                    found.append(string)
                end -= 1

    add_to.append(found)

def vertically(grid, valid_list, add_to):
    """Checks vertically if a grid has valid words and append those words
    to a list(add_to).
  
    Parameters: grid is a 2D list representing the grid.
    valid list is the list of strings of valid words.
    add_to is the list that will get appended with the found valid words.  
  
    Returns: None. 
    """

    found = []
    for x in range(len(grid)):

        # up down
        for start in range(len(grid) - 2):  # bounds for starting positions 
            end = start + 3
            while end <= len(grid):  # bounds for end position

                # creates the string starting from the start to the end
                string = ""
                for i in range(start,end):
                    string += grid[i][x]  # x stays the same for each column

                # calls the function to test validity 
                if occurs_in(string, valid_list):
                    found.append(string)
                end += 1
        
        # down up (same as up down besides the bounds)
        for start in range(len(grid) -1, 1, -1):  # bounds for start position 
            end = start - 2
            while end >= 0:  # bounds for end position

                string = ""
                for i in range(start,end -1, -1):
                    string += grid[i][x]

                if occurs_in(string, valid_list):
                    found.append(string)
                end -= 1
    add_to.append(found)

def diagonally(grid, valid_list, add_to):
    """Checks diagonally top left to bottom right if a grid has valid words
    and append those words to a list(add_to).
  
    Parameters: grid is a 2D list representing the grid.
    valid list is the list of strings of valid words.
    add_to is the list that will get appended with the found valid words.  
  
    Returns: None. 
    """
    found = []

    # positive offset 
    last = len(grid) -3  # last possible starting point 
    end = len(grid) - 1  # end of possible indexes

    # sets up the x and y for each start of a diagonal 
    for starting_x in range(len(grid)-2): 
        starting_y = 0 
        x = starting_x
        y = starting_y
        while y <= last:

            # other x and y are to continue the search on the same diagonal 
            other_y = y
            other_x = x
            x += 1
            y += 1 

            # makes a list of a possible consecutive combination on the 
            # diagonal 
            diagonal = []
            while other_y <= end:  
                diagonal.append(grid[other_y][other_x])

                # turns one of the possible combinations into a string 
                string = ""
                if len(diagonal) >= 3:
                    string += "".join(diagonal)

                # calls the function to test the validity
                if occurs_in(string, valid_list):
                    found.append(string)

                other_y += 1
                other_x += 1
            
        end -= 1
        last -= 1

    # negative offset (same as positive offset except x and y are switched)
    last = len(grid) -3 
    end = len(grid) - 1
    for starting_y in range(len(grid)-2):
        starting_x = 0
        x = starting_x
        y = starting_y
        
        while x <= last:
            other_y = y
            other_x = x
            x += 1
            y += 1 
            diagonal = []
            while other_x <= end:

                diagonal.append(grid[other_y][other_x])
                string = ""
                if len(diagonal) >= 3:
                    string += "".join(diagonal)

                if occurs_in(string, valid_list):
                    found.append(string)

                other_y += 1
                other_x += 1
            
        end -= 1
        last -= 1



    add_to.append(found)

def print_words_found(add_to):
    """Prints out in alphabetical order the valid words that got found without
    any duplicates.
  
    Parameters: add_to is the list that got appended with the found words.  
  
    Returns: None. 
    """

    # new list to be sorted alphabetically and have no duplicates 
    duplicate = []
    for inner_list in add_to:
        for word in inner_list:
            if word not in duplicate:  # makes sure it isn't a duplicate
                duplicate.append(word)
    duplicate.sort() 
    print("\n".join(duplicate))  # prints each word on a new line

def main():
    word_list = get_word_list()
    letters_grid = read_letters_file() 

    # a list used to accumulate the valid words found
    all_words = []  

    horizontally(letters_grid, word_list, all_words)

    vertically(letters_grid, word_list, all_words)

    diagonally(letters_grid, word_list, all_words)

    print_words_found(all_words)

main()
