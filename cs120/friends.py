"""
    File: friends.py
    Author: Elton Ho
    Course: CSC 120, Spring 2024
    This program has 1 function to implement a linked list of people and 
    friends from the inputted file. This is so that we can find the mutual 
    friends of two inputted people and print their names.
"""

from linked_list import *

def print_mutuals():
    """Implement a linked list of people and friends from an inputted file to 
       find the mutual friends of two inputted people and print their names.

       Parameters: None.

       Returns: None.
    """

    file_name = input('Input file: ')
    file = open(file_name)
    main_linked_list = LinkedList()
    for line in file:
        line_list = line.strip().split()

        # line_list[0] is one person and line_list[1] is another
        main_linked_list.update(line_list[0], line_list[1])
    name1 = input('Name 1: ')
    name2 = input('Name 2: ')
    main_linked_list.mutual_friends(name1,name2)  # print the mutuals
    file.close()

def main():
    print_mutuals()

main()