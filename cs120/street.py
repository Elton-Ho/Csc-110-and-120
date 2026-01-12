"""
    File: street.py
    Author: Elton Ho
    Course: CSC 120, Spring 2024
    Purpose: This program has nine functions that generate the street at each 
    height, generate the street horizontally depending on the input, generate 
    the building, generate the empty loot, generate the park, find the max 
    height, find the max width, find the numbers in the input, and find the 
    symbols in the input. These nine functions work together to create a 
    rendering of a street using recursion. 
"""

def verticle(input, height, max_height, max_width): 
    """Iterates through the height of the street to render the city at each 
    height. 
  
    Parameters: input is a list of strings representing parts of the input.
    height is an integer to keep track of the current height being rendered.
    max_height is an integer representing the max height for comparing with the 
    current height.
    max_width is an integer representing the max width of the street. 
  
    Returns: A string representing the rendering of the whole street. 
    """

    # for the bottom of the border 
    if height == 0:
        return "+" + "-" * max_width + "+\n"
    
    # for the padding on top 
    if max_height == height: 
        return "+" + "-" * max_width + "+\n" + "|" + " " * max_width + "|\n" +\
        verticle(input, height - 1, max_height, max_width)
    
    return "|" + horizontal(input, max_width, height) +\
    verticle(input, height - 1, max_height, max_width)

def horizontal(input, width, height):
    """Iterates left to right on input, renders all on one line the detected 
    infrastructure, and subtracts from the max width to know when to stop.
  
    Parameters: input is a list of strings representing parts of the input.
    width is an integer representing the width that still needs to be rendered. 
    height is an integer to represent the current height being rendered.
  
    Returns: A string representing the horizontal rendering of the street at a 
    certain height. 
    """

    # end of horizontal has a |
    if width == 0:
        return "|\n"
    inputted_width = find_numbers(input[0])[0]

    # looks at the first letter of parts of input for detecting 
    if input[0][0] == "b":
        inputted_height = find_numbers(input[0])[1]

        # input[0][-1]) is the brick
        return building(inputted_width, inputted_height, height, input[0][-1])\
        + horizontal(input[1:], width - inputted_width, height)
    if input[0][0] == "e":

        # find_symbol(input[0]) is the trash
        return empty_lot(inputted_width, height, find_symbol(input[0]),\
        find_symbol(input[0])) + horizontal(input[1:], width - inputted_width,\
        height)
    if input[0][0] == "p":

        # find_symbol(input[0]) is the foliage 
        return park(inputted_width, height, find_symbol(input[0])) +\
        horizontal(input[1:], width - inputted_width, height)

def building(width, height, current_height, brick):
    """Renders the correct string representing the building depending on the 
    height it's on.
  
    Parameters: width is an integer representing the width of the building.
    height is an integer representing the height a part of the building exists 
    on. 
    current_height is an integer representing the height being rendered.
    brick is a string representing the symbol the building is made of.  
  
    Returns: A string representing the horizontal rendering of a building at a 
    certain height. 
    """

    # checking if it's at a height a part of the building needs to be rendered
    if height >= current_height:
        return brick * width
    return " " * width

def empty_lot(width, current_height, current_trash, trash):
    """Renders the correct string representing the empty lot depending on the 
    height it's on.
  
    Parameters: width is an integer representing the width of the empty lot.
    current_height is an integer representing the height being rendered.
    current_trash is a string representing the part of the trash pattern being 
    rendered.
    trash is a string representing the symbols of the whole trash pattern. 
  
    Returns: A string representing the horizontal rendering of an empty lot at 
    a certain height. 
    """

    if current_height == 1:
        if width == 0:
            return ""
        if current_trash != "":
            
            # returns " " in place of "_"
            if current_trash[0]== "_":
                return " " + empty_lot(width - 1, current_height,\
                current_trash[1:], trash)
            
            return current_trash[0] + empty_lot(width - 1, current_height,\
            current_trash[1:], trash)
        else: 

            # reset the current_trash
            return empty_lot(width, current_height, trash, trash)
    return " " * width

def park(width, current_height, foliage):
    """Renders the correct string representing the park depending on the 
    height it's on.
  
    Parameters: width is an integer representing the width of the park.
    current_height is an integer representing the height being rendered.
    foliage is a string representing what the foliage is made of. 
  
    Returns: A string representing the horizontal rendering of a park at a 
    certain height. 
    """

    if current_height == 5:
        return (width//2) * " " + foliage + (width//2) * " "
    if current_height == 4:
        return (width//2-1) * " " + foliage* 3 + (width//2-1) * " "
    if current_height == 3:
        return (width//2 - 2) * " " + foliage * 5 + (width//2 - 2) * " "
    if current_height <= 2:
        return (width//2) * " " + "|" + (width//2) * " "
    return " " * width

def find_numbers(input_string):
    """Finds the number parts of a part of the input.
  
    Parameters: input_string is a string representing part of the input.
  
    Returns: A list of integers representing the number parts of a part of the 
    input.  
    """

    if input_string == "":
        return []
    if not input_string[0].isnumeric():
        return find_numbers(input_string[1:])
    
    # found two digit number
    if input_string[0].isnumeric() and input_string[1].isnumeric():
        return [int(input_string[0] + input_string[1])] + \
            find_numbers(input_string[2:])
    
    # found one digit number
    if input_string[0].isnumeric() and not input_string[1].isnumeric():
        return [int(input_string[0])] + find_numbers(input_string[1:])
    
def find_height(input):
    """Finds the max height of the input of the infrastructure in the street.
  
    Parameters: input is a list of strings representing parts of the input.
  
    Returns: An integer representing the max height of the input. 
    """
    
    if input == []:
        return 0
    if input[0][0] == "b":

        # building height is the second number so index 1 of find_numbers
        return max(find_numbers(input[0])[1], find_height(input[1:]))
    if input[0][0] == "p":
        return max(5, find_height(input[1:]))
    if input[0][0] == "e":
        return max(1, find_height(input[1:]))

def find_width(input):
    """Finds the max width of the input of the infrastructure in the street.
  
    Parameters: input is a list of strings representing parts of the input.
  
    Returns: An integer representing the max width of the input. 
    """

    if input == []:
        return 0
    
    # for all, width is always the first number so index 0 of find_numbers
    return find_numbers(input[0])[0] + find_width(input[1:])

def find_symbol(input_string):
    """Finds the symbol parts of a part of the input.
  
    Parameters: input_string is a string representing part of the input.
  
    Returns: A string representing the symbol parts of a part of the input. 
    """

    if input_string == "":
        return []
    if input_string[0] == "," and find_symbol(input_string[1:]) != "," :
        return input_string[1:]  # everything after the "," are the symbols
    return find_symbol(input_string[1:])

def main():
    input_list = input("Street: ").split()
    max_height = find_height(input_list) + 1  # + 1 is to account for padding
    print(verticle(input_list, max_height, max_height, find_width(input_list)))

main()