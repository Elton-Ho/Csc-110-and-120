"""
    File: huffman.py
    Author: Elton Ho
    Course: CSC 120, Spring 2024
    Purpose: This program has one Tree class and two functions to create a 
    (Binary) Tree based on the inputted preorder and inorder transversal of a 
    tree and decode a sequence of values based on the created tree using 
    Huffman coding. This is so we can print out the postorder transversal of a 
    Tree and the decoded sequence.
"""

class Tree:
    """This class represents a node for a binary tree.

        The class has getter and setter methods, and its string representation 
        is the postorder transversal version. It is constructed with a string 
        representing the value of the node and a pointer to its left and right 
        child.
    """

    def __init__(self, value):
        """Sets up the attributes for the object as a string for the value of 
           the node and its left and right child pointer to None.

           Parameters: value is a string for the value of the node.

           Returns: None.
        """

        self._value = value
        self._left = None
        self._right = None
    
    def get_value(self):
        return self._value
    
    def get_left(self):
        return self._left
    
    def get_right(self):
        return self._right

    def set_left(self, node):
        self._left = node

    def set_right(self, node):
        self._right = node

    # source: inspired by ica24 answer's inorder_str but changed for postorder
    def __str__(self):
        return_string = ""
        if self._left != None:
            return_string += str(self._left) + " "
        if self._right != None:
            return_string += str(self._right)+ " " + self._value
        else:
            return_string += self._value
        return return_string

def create_tree(preorder, inorder):
    """Creates the binary tree using recursion and the inputted strings that 
       are the preorder and inorder transversal of the tree. 

       Parameters: preorder is a string representing the inputted preorder 
       transversal of the tree. 
       inorder is a string representing the inputted inorder transversal of the 
       tree.

       Returns: An object which is the root node for a completed tree. 
    """

    if preorder == []:
        return
    root = Tree(preorder[0])

    # setting left to create_tree(preorder_left, inorder_left)
    root.set_left(create_tree(preorder[1:inorder.index(preorder[0]) + 1],\
    inorder[:inorder.index(preorder[0])]))

    # setting right to create_tree(preorder_right, inorder_right)
    root.set_right(create_tree(preorder[inorder.index(preorder[0]) + 1:],\
    inorder[inorder.index(preorder[0]) + 1:]))
    return root

def decode(root, input):
    """Uses Huffman coding to decode the encoded string via a binary tree.  

       Parameters: root is an object representing the root node of the binary 
       tree. 
       input is a string representing the inputted encoded sequence. 

       Returns: A string that represents the decoded sequence. 
    """

    # goes through the tree using the same method for a linked list
    current = root
    decoded = ""
    for number in input:
        if number == "0" and current.get_left() != None:
            current = current.get_left()
        if number == "1" and current.get_right() != None:
            current = current.get_right()

        # found the needed value
        if current.get_left() == None and current.get_right() == None:
            decoded += current.get_value()
            current = root  # reset 
    return decoded

def main():
    file_name = open(input('Input file: '))
    file = file_name.readlines()
    preorder_list = file[0].strip().split()
    inorder_list = file[1].strip().split()
    encoded  = file[2].strip()
    print(create_tree(preorder_list, inorder_list))
    print(decode(create_tree(preorder_list, inorder_list), encoded))
    file_name.close() 

main()