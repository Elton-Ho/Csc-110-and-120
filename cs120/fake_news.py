
"""
    File: fake_news.py
    Author: Elton Ho
    Course: CSC 120, Spring 2024
    This program has 1 function and 2 classes to process a csv file of possible 
    fake news titles and implement a linked list to store the words of the 
    titles and their count. This is so we can see the words that reoccur for at 
    least the same time as a selected word. 
"""

import csv
import string

class Node():
    """This class represents a node for a linked list and information about a
       word.

       The class has a method to set the _next attribute to a target and 
       increase the count. It is constructed with a string representing the 
       word in a title, an integer representing the number of times the word 
       appears, and a pointer for the next node. 
    """

    def __init__(self, word):
        """Sets up the attributes for the object as a string for a word in the 
           title, the integer 1 as its count, and a _next pointer to None.

           Parameters: word is a string for one of the words that occur in a 
           news title.

           Returns: None.
        """

        self._word = word
        self._count = 1
        self._next = None

    def word(self):
        return self._word
    
    def count (self):
        return self._count 
    
    def next(self):
        return self._next
    
    def set_next(self, target):
        """Assigns the _next attribute to a target which is a node or None.

           Parameters: target is a node or None that needs the _next attribute.

           Returns: None.
        """
        self._next = target

    def incr(self):
        """Increases the value of _count by one.

           Parameters: None.

           Returns: None.
        """
        self._count += 1

    def __str__(self):
        return self._word + ":" + str(self._count) + " " 

class LinkedList():
    """This class represents a linked list for words in news titles.

       The class has a method to add or remove a node from the head, check if 
       the lists are empty, update the count for a word, insert a node after 
       another node, sort the linked list, get the count for the node in a 
       desired position, and print the words with at least the count of a 
       desired word. It is constructed with a pointer to the head of the linked 
       list. 
    """

    def __init__(self):
        """Sets up the attributes for the object as a _head pointer to None.

           Parameters: None.

           Returns: None.
        """

        self._head = None

    def is_empty(self):
        """Returns a boolean based on whether the linked list is empty or not. 

           Parameters: None.

           Returns: A boolean that is True if the list is empty and False if it 
           isn't.
        """
        return self._head == None
    
    def head(self):
        return self._head

    # add a node to the head of the list
    # source: long problem for sorting a linked lists
    def add(self, node):
        node.set_next(self._head)
        self._head = node

    def update_count(self, word):
        """Creates a node for a word if it doesn't already exist in the linked 
           list, otherwise, it increases the count for that word.

           Parameters: word is a string for one of the words that occur in a 
           news title.

           Returns: None.
        """

        current = self._head
        change = False  # keeps track of changes made 
        if self.is_empty():  # empty linked list
            node = Node(word)
            self.add(node)
        else:
            while current != None and not change:
                if current.word() == word:  # node does exist so increment
                    current.incr()
                    change = True
                current = current.next()

            # the node doesn't already exist so it needs to create it
            if not change:  
                node = Node(word)
                self.add(node)

    # remove a node from the head of the list and return the node
    # source: long problem for sorting a linked lists 
    def rm_from_hd(self):
        assert self._head != None
        _node = self._head
        self._head = _node.next()
        _node.set_next(None)
        return _node

    # insert node2 after node1
    # source: long problem for sorting a linked lists
    def insert_after(self, node1, node2):
        assert node1 != None
        node2.set_next(node1.next())
        node1.set_next(node2)

    # source: long problem for sorting a linked lists 
    def sort(self):
        """Keeps removing the head of the linked list, adds it to a new linked 
           list in its sorted position, and copies the fully sorted to the old.    

           Parameters: None.

           Returns: None. 
        """

        sorted = LinkedList()  # link list that will be sorted
        curr_element = self._head
        while curr_element != None:
            change = False  # no changes have been made yet
            if sorted._head == None:  # if sorted is empty
                sorted._head = curr_element  # adds the curr_element to sorted
                self.rm_from_hd()
                change = True

            # not change prevents it from continuing after changing a link list
            if sorted._head.count() < curr_element.count() and not change:
                sorted.add(self.rm_from_hd())
                change = True
            if not change:  # test for E and inserts immediately after E
                current_sorted = sorted._head  # go through sorted linked list
                while current_sorted != None and not change:

                    # if statements find where E = current_sorted
                    if current_sorted.count() >= curr_element.count():
                        if current_sorted.next() == None or \
                        current_sorted.next().count() < curr_element.count():
                            sorted.insert_after(current_sorted, \
                            self.rm_from_hd())
                            change = True
                    current_sorted = current_sorted.next()

            # After a node gets rm_from_hdd via the if statements, we point 
            # back to the head to continue on to a new node. 
            curr_element = self._head  
        self._head = sorted._head  # copies over the sorted to the old

    def get_nth_highest_count(self, n): 
        """Returns a integer which is the count for the node in the n position 
           of a linked list.    

           Parameters: n is an integer which is the inputted position for a 
           node in the linked list. 

           Returns: An integer which is the count for the node in the inputted 
           position. 
        """

        current = self._head
        while current != None and n != 0:
            current = current.next()
            n -= 1
        return current.count()
    
    def print_upto_count(self, n):
        """Prints the words and their count that have at least the count of n    

           Parameters: n is an integer which is the count for a node/word

           Returns: None.
        """

        current = self._head
        while current != None:
            if current.count() >= n:  
                print("{} : {:d}".format(current.word(), current.count()))
            current = current.next()

    # source: long problem for sorting a linked lists
    def __str__(self):
        string = 'List[ '
        curr_node = self._head
        while curr_node != None:
            string += str(curr_node)
            curr_node = curr_node.next()
        string += ']'
        return string

def process_and_print():
    """It processes an inputted csv formatted file to get the important words 
    of a news title and print words with at least the count of a selected word.

    Parameters: None.

    Returns: None.
    """

    file_name = input()
    file = open(file_name)
    linked_list = LinkedList()
    csvreader = csv.reader(file)  # spits at the proper commas of a csv
    for line in csvreader:
        if "#" not in line[0]:

            # gets rid of the punctuation
            new_list = []
            for char in line[4]:
                if char not in string.punctuation:
                    new_list.append(char.lower())
                else:
                    new_list.append(" ")

            # gets rid of the spaces and characters with lengths > 2 
            no_spaces = "".join(new_list).split()
            for char in no_spaces:
                if len(char) > 2:
                    linked_list.update_count(char)

    linked_list.sort()
    print(linked_list)
    integer_n = int(input())  # n is a word's linked list inputted position 

    # prints out the words with at least the count as the selected word 
    linked_list.print_upto_count(linked_list.get_nth_highest_count(integer_n))
    file.close

def main():
    process_and_print()

main()