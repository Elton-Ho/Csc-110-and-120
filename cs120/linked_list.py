"""
    File: linked_list.py
    Author: Elton Ho
    Course: CSC 120, Spring 2024
    This program has 2 classes to create a "main" linked list of people and 
    within each person node, a friends list as a linked list. This is so that 
    we can ultimately find the mutual friends of two people in the "main" 
    linked list and print their names. 
"""

class Node():
    """This class represents a node for a linked list and information about
       who a person is friends with. 

       The class has a method to update a linked list of friends and various 
       setter and getter methods. It is constructed with a string representing 
       the name of the person, a linked list of the person's friends, and a 
       pointer to the next node. 
    """

    def __init__(self, name):
        """Sets up the attributes for the object as a string for the name of a 
           person, a linked list of friends pointer and _next pointer to None.

           Parameters: name is a string representing the name of a person in 
           the file. 

           Returns: None.
        """

        self._name = name
        self._friends = None
        self._next = None

    def name(self):
        return self._name

    def friends(self):
        return self._friends

    def update_node(self, name):
        """Creates the linked list of friends with the name in it or adds the 
           name to the existing linked list.

           Parameters: name is a string representing the name of a person in 
           the file. 

           Returns: None.
        """

        if self._friends == None:  # no linked list yet
            self._friends = LinkedList()
            self._friends.add(Node(name))
        else:
            self._friends.add(Node(name))
        self._friends.sort() 

    def next(self):
        return self._next

    def set_next(self, target):
        self._next = target

    def __str__(self):
        return self._name

class LinkedList():
    """This class represents a linked list for a list of people.

       The class has a method to update the linked list with people, add or 
       remove a node from the head, insert a node after another node, sort the 
       linked list, and find and print the mutual friends of two people. It is 
       constructed with a pointer to the head of the linked list. Note that the 
       __str__ is a little different than a typical linked list's __str__ to 
       match the project's desired output. 
    """

    def __init__(self):
        """Sets up the attributes for the object as a _head pointer to None.

           Parameters: None.

           Returns: None.
        """

        self._head = None
    
    def update(self, name1, name2):
        """Adds a node to the "main" linked list if it doesn't already exist or
           updates that node's linked list of friends with a node if it does.

           Parameters: name1 is a string that is one of the names in the file.
           name2 is a string that is another name in the file.

           Returns: None.
        """

        current = self._head

        # look for name1/name2
        found1 = False
        found2 = False
        while current != None:
            if current.name() == name1:

                # add the other name as a friend
                current.update_node(name2)
                found1 = True 
            if current.name() == name2:
                current.update_node(name1)
                found2 = True 
            current = current.next()

        # name1/name2 not in the "main" linked list
        if not found1:
            self.add(Node(name1))
            self._head.update_node(name2)
        if not found2:
            self.add(Node(name2))
            self._head.update_node(name1)

    def mutual_friends(self, name1, name2):
        """Creates an alphabetically sorted linked list of the mutual friends 
           of two people and prints it if it exists.

           Parameters: name1 is a string that is one of the names in the file.
           name2 is a string that is another name in the file.

           Returns: None.
        """

        current = self._head

        # look for name1 and name2 in the main linked list
        found1 = None
        found2 = None
        while current != None:
            if current.name() == name1:
                found1 = current
            if current.name() == name2:
                found2 = current
            current = current.next()
        if found1 == None:  # prints an error message if a name wasn't found
            print("ERROR: Unknown person " + name1)
        elif found2 == None:
            print("ERROR: Unknown person " + name2)
        else:
            mutuals = LinkedList()
            current1 = found1.friends()._head
            current2 = found2.friends()._head
            while current1 != None:  # go through both friends list
                while current2 != None:
                    if current1.name() == current2.name():  # found a mutual

                        # adds in reverse order so that it is alphabetical 
                        mutuals.add(Node(current1.name()))
                    current2 = current2.next()
                current2 = found2.friends()._head  # resets inner while loop
                current1 = current1.next()
            if mutuals._head != None:
                print(mutuals)

    # add a node to the head of the list
    # source: long problem for sorting a linked list 
    def add(self, node):
        node.set_next(self._head)
        self._head = node 

    # remove a node from the head of the list and return the node
    # source: long problem for sorting a linked list 
    def rm_from_hd(self):
        assert self._head != None
        removed = self._head
        self._head = removed.next() 
        removed.set_next(None)
        return removed
    
    # insert node2 after node1
    # source: long problem for sorting a linked list
    def insert_after(self, node_a, node_b):
        assert node_a != None
        node_b.set_next(node_a.next())
        node_a.set_next(node_b)

    # source: long problem for sorting a linked list 
    def sort(self):
        """Keeps removing the head of the linked list, adds it to a new linked 
           list in its sorted position, and copies the fully sorted to the old.    

           Parameters: None.

           Returns: None. 
        """

        sorted = LinkedList()
        curr_element = self._head
        while curr_element != None:
            change = False  # no changes have been made yet 
            if sorted._head == None:  
                sorted._head = curr_element
                self.rm_from_hd()
                change = True
            if sorted._head.name() < curr_element.name() and not change:
                sorted.add(self.rm_from_hd())
                change = True
            if not change:  # test for E and inserts immediately after E
                current_sorted = sorted._head 
                while current_sorted != None and not change:

                    # if statements find where E = current_sorted
                    if current_sorted.name() >= curr_element.name():
                        if current_sorted.next() == None or \
                        current_sorted.next().name() < curr_element.name():
                            sorted.insert_after(current_sorted, \
                            self.rm_from_hd())
                            change = True
                    current_sorted = current_sorted.next()
            curr_element = self._head  
        self._head = sorted._head

    # prints in the desired format of the project 
    # source: based on long problem for sorting a linked list
    def __str__(self):
        string = "Friends in common:\n"
        curr_node = self._head
        while curr_node != None:
            string += str(curr_node) + "\n"
            curr_node = curr_node.next()
        return string