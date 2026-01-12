"""
    File: linkedlist_sort.py
    Author: Elton Ho
    Course: CSC 120, Spring 2024
    This program has two classes to make a linked list and the nodes associated 
    with that linked list. This is so that we can read a file and convert a 
    line in that file into a linked list and be able to sort the linked list.
"""

class LinkedList:
    def __init__(self):
        self._head = None
    
    # sort the nodes in the list
    def sort(self):
        """Keeps removing the head of the linked list, adds it to a new linked 
        list in its sorted position, and copies the fully sorted to the old.    
  
        Parameters: None.

        Returns: None. 
        """
        
        sorted = LinkedList()  # link list that will be sorted
        curr_element = self._head
        while curr_element != None:
 # no changes have been made yet
            if sorted._head == None:  # if sorted is empty
                sorted._head = curr_element  # adds the curr_element to sorted
                self.remove()

            
            # not change prevents it from continuing after changing a link list
            elif sorted._head._value < curr_element._value:
                sorted.add(self.remove())
                change = True
            else:  # test for E and inserts immediately after E
                current_sorted = sorted._head  # go through sorted linked list
                while current_sorted != None:

                    # if statements find where E = current_sorted
                    if current_sorted._value >= curr_element._value:
                        if current_sorted._next == None or \
                        current_sorted._next._value < curr_element._value:
                            sorted.insert(current_sorted, self.remove())
                    current_sorted = current_sorted._next

            # After a node gets removed via the if statements, we point back to 
            # the head to continue on to a new node. 
            curr_element = self._head  
        self._head = sorted._head  # copies over the sorted to the old
    
    # add a node to the head of the list
    def add(self, node):
        node._next = self._head
        self._head = node
        
    # remove a node from the head of the list and return the node
    def remove(self):
        assert self._head != None
        _node = self._head
        self._head = _node._next
        _node._next = None
        return _node
    
    # insert node2 after node1
    def insert(self, node1, node2):
        assert node1 != None
        node2._next = node1._next
        node1._next = node2
    
    def __str__(self):
        string = 'List[ '
        curr_node = self._head
        while curr_node != None:
            string += str(curr_node)
            curr_node = curr_node.next()
        string += ']'
        return string

class Node:

    def __init__(self, value):
        self._value = value
        self._next = None
    
    def __str__(self):
        return str(self._value) + "; "
    
    def value(self):
        return self._value
    
    def next(self):
        return self._next
    
def main():
    file_name = input()
    file = open(file_name)
    linked_list = LinkedList()
    for line in file:
        line_list = line.strip().split()

        # for each number in the file, add it as a node for the linked list
        for number in line_list:
            node = Node(int(number))
            linked_list.add(node)
        linked_list.sort()
    print(linked_list)
    file.close

main()