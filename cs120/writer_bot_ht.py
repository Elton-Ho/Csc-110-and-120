"""
    File: writer_bot_ht.py
    Author: Elton Ho
    Course: CSC 120, Spring 2024
    Purpose: This program has three functions and one hash table class to 
    create a list of words from an inputted file, create a hash table for that 
    list of words using Markov's algorithm, and create a list of words based on 
    the table, the inputted prefix size, and the inputted number of words. This 
    is so that we can print strings following Markov's algorithm.
"""

import sys
import random
SEED = 8
random.seed(SEED)

class Hashtable:
    """This class represents a hash table ADT that uses linear probing.

       The class has methods for hashing, putting a key value pair into the 
       hash table, getting the value of a key in the table, and checking if a 
       key is in the table. It is constructed with an integer representing the 
       size of the hash table and a list for the table.
    """

    def __init__(self, size):
        """Sets up the attributes for the object as an integer for the size of 
           the hash table and a list that size of None's as the hash table.

           Parameters: size is an integer representing the hash table's size.

           Returns: None.
        """

        self._size = size
        self._pairs = [None] * self._size 

    def _hash(self, key):
        """Uses Horner's rule for polynomials with 31 as the value of x to hash 
           a key for the hash table.

           Parameters: key is a string representing a key in the hash table.

           Returns: an integer resulting in the hashing of the key string.
        """
        
        p = 0
        for c in key:
            p = 31*p + ord(c)
        return p % self._size
    
    def put(self, key, value):
        """Uses the hashing of a key and linear probing for collisions to put a 
           key value pair into the hash table.

           Parameters: key is a string representing a key in the hash table.
           value is a list representing the value for the key. 

           Returns: None.
        """
        
        index = self._hash(key)
        while self._pairs[index] != None:
            index -= 1
            if index == 0:  # wrap around to the end
                index = self._size - 1
        self._pairs[index] = [key, value]
        
    def get(self, key):
        """Uses the concept of linear probing and the hashing of a key to get 
           the value of a key in the hash table.

           Parameters: key is a string representing a key in the hash table.

           Returns: An empty list or a list of strings which is the value for 
           that key or None if the key isn't in the hash table. 
        """
                
        index = self._hash(key)
        while self._pairs[index] != None and self._pairs[index][0] != key:
            index -= 1
            if index == 0:  # wrap around to the end
                index = self._size - 1

        # found an empty slot so key doesn't exist in the hash table
        if self._pairs[index] == None:
            return None
        return self._pairs[index][1]
    
    def __contains__(self, key):
        """Uses the concept of linear probing and the hashing of a key to see 
           if a key exists in the hash table.

           Parameters: key is a string representing a key in the hash table.

           Returns: A boolean True if the key is in the hash table and False 
           otherwise. 
        """
                
        index = self._hash(key)
        while self._pairs[index] != None and self._pairs[index][0] != key:
            index -= 1
            if index == 0:  # wrap around to the end
                index = self._size - 1

        # found an empty slot so key doesn't exist in the hash table
        if self._pairs[index] == None:
            return False
        return self._pairs[index][0] == key
    
    def __str__(self):
        return str(self._pairs)

def inputs_list():
    """Creates a list of strings for the words in an inputted file and takes 
       the inputs for the file name, hash table size, and prefix size. 

       Parameters: None.

       Returns: A tuple containing the list of strings for the inputted file, 
       an integer as the inputted hash table size, and an integer representing 
       the inputted prefix size.
    """

    file_name = input()
    hash_size = int(input())
    size = int(input())
    if size < 1:
        print("ERROR: specified prefix size is less than one")
        sys.exit(0)
    file = open(file_name)
    line_list = []
    nonword = "@" 
    for line in file:
        line_list += line.strip().split()
    for times in range(size):
        line_list.insert(0, nonword)
    file.close()
    return line_list, hash_size, size 

def markov_algorithm(file_list, hash_size, prefix_size):
    """Creates a hash table of strings as keys and a list of strings as values 
       to make the table for Markov's algorithm.  

       Parameters: file_list is a list of strings of all the words in the 
       inputted file.
       hash_size is an integer representing the size of the hash table. 
       prefix_size is an integer for the inputted prefix size. 

       Returns: A hash table of strings as keys and a list of strings as values 
       to make the table for Markov's algorithm.
    """

    markov = Hashtable(hash_size)
    for words in range(0,len(file_list) - prefix_size):
        prefix = " ".join(file_list[words:words + prefix_size])
        if prefix not in markov:
            markov.put(prefix, [])  # empty list as the key 

        # append the suffix to the key that is a list
        markov.get(prefix).append(file_list[words+prefix_size])
    return markov

def generated_text(algorithm, wordlist, size):
    """Creates a list of strings based on Markov's algorithm, the inputted 
       prefix size, and the inputted number of words needed. 

       Parameters: algorithm is a hash table of strings as keys and a list of 
       strings as values representing the table for Markov's algorithm.
       wordlist is a list of strings for the words in the inputted file.
       size is an integer for the inputted prefix size. 

       Returns: A list of strings representing the generated text. 
    """

    num_words = int(input())
    if num_words < 1:
        print("ERROR: specified size of the generated text is less than one")
        sys.exit(0)
    text_list = wordlist[size: size+size]
    prefix = " ".join(wordlist[size: size+size])
    num_words -= size  # already added the first n amount of words to the list
    while prefix in algorithm and num_words > 0:
        if len(algorithm.get(prefix)) > 1:
            suffix = algorithm.get(prefix)[random.randint(0,\
            len(algorithm.get(prefix))- 1)]
        else:
            suffix = algorithm.get(prefix)[0]
        text_list.append(suffix)

        # change the prefix string by moving it one over 
        prefix = " ".join(prefix.split()[1:] + [suffix])
        num_words -= 1
    return text_list

def main():
    file_list = inputs_list()
    generated = generated_text(markov_algorithm(file_list[0], file_list[1],\
    file_list[2], ), file_list[0], file_list[2])
    for index in range(len(generated)//10):

        # ten words each line
        print(" ".join(generated[index * 10: (index * 10) + 10]))

    # last line still needs to be printed
    if len(generated) % 10 != 0:
        print(" ".join(generated[(index + 1) * 10:]))

main()