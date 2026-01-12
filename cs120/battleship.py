"""
    File: battleship.py
    Author: Elton Ho
    Course: CSC 120, Spring 2024
    Purpose: This program has three classes and one function to create a legal 
    battleship board with all its positions and pieces in those positions. This 
    is to use the board to process guesses in an inputted file to determine if 
    the move would hit, miss, sink, win, or be illegal.
"""

import sys

class GridPos:
    """This class represents a position in the battleship grid.

       The class has getter and setter methods. It is constructed with a tuple 
       representing the coordinate it takes up on the grid, what is occupied in 
       that coordinate, and a boolean showing whether this position has been 
       guessed or not.
    """

    def __init__(self, position):
        """Sets up the attributes for the object as a tuple for the position, 
           None as what's occupied, and False for it already being guessed.  

           Parameters: position is a tuple representing the coordinate on the 
           grid it takes up.

           Returns: None.
        """

        self._position = position
        self._occupied = None
        self._guessed = False

    def set_occupied(self, piece):
        self._occupied = piece

    def set_guessed(self):
        self._guessed = True

    def guessed(self):
        return self._guessed

    def occupied(self):
        return self._occupied
    
    def position(self):
        return self._position

    def __str__(self):
        if self._occupied == None:
            return "*" 
        return str(self._occupied) 
    
class Board:
    """This class represents the battleship board with the grid and its pieces.

       The class has a helper method to create the grid, a method to place 
       pieces on the board, and a method to process guesses. It is constructed 
       with a 2D list representing the grid, a list of ship objects, and a 
       boolean showing whether there was an overlap of pieces.  
    """

    def __init__(self):
        """Sets up the attributes for the object as a 2D list grid, an empty 
           list for ship objects, and False for an overlap in pieces present.  

           Parameters: None.

           Returns: None.
        """

        self._grid = self.grid_helper()
        self._ships = []
        self._overlap = False
    
    def grid_helper(self):
        """Creates a 10x10 battleship grid represented by a 2D list of position 
           objects.

           Parameters: None.

           Returns: Returns a 2D list of position objects for the grid.
        """

        grid = []
        for row_number in range(10):
            row = []
            for position_number in range(10):
                row.append(GridPos((position_number,row_number)))
            grid.append(row)
        return grid
    
    def ships(self):
        return self._ships
    
    def grid(self):
        return self._grid
    
    def overlap(self):
        return self._overlap
            
    def place_piece(self, piece, coord1, coord2):
        """Places ship pieces onto the grid by finding which of the two coords 
           are the start and altering the three objects for placing.

           Parameters: piece is a ship object representing the piece that needs 
           to be placed. 
           coord1 is a tuple that is either the start or end coordinate.
           coord2 is a tuple is the other coordinate.

           Returns: Returns an integer representing the number of times the 
           position object was altered. 
        """

        # number of times a part of the ship is added to verify sizing
        count = 0 

        # finds which of the coordinates is the start and stop
        start = coord1
        stop = coord2
        if coord1[0] > coord2[0] and coord2[1] == coord2[1]:
            start = coord2
            stop = coord1
        if coord1[1] > coord2[1] and coord1[0] == coord2[0]:
            start = coord2
            stop = coord1

        # go through all the coordinates between the start and stop
        for x_position in range(start[0], stop[0] + 1):
            for y_posistion in range(start[1], stop[1] + 1):

                # the position object there is not occupied so add the piece
                if self._grid[y_posistion][x_position].occupied() == None:
                    piece.add_position((x_position, y_posistion))
                    self._grid[y_posistion][x_position].set_occupied(piece)
                    count += 1
                else:
                    self._overlap = True
                    break
        self._ships.append(piece)
        return count
    
    def process_guess(self, line_lst):
        """Processes an inputted file of guesses to determine if the game is 
           over, a ship has sunk, a ship was only hit, or a guess was a miss. 

           Parameters: line_lst is a list of strings that is a line of the 
           inputted file of guesses.

           Returns: None. 
        """

        # not within the bounds of the board
        if not 0 <= int(line_lst[0]) <= 9 or not 0 <= int(line_lst[1]) <= 9:
            print("illegal guess")
        else:
            guess_position = self.grid()[int(line_lst[1])][int(line_lst[0])]
            piece = guess_position.occupied()
            if piece == None:
                if guess_position.guessed():  # have already guessed this coord
                    print("miss (again)")
                else:
                    guess_position.set_guessed()
                    print("miss")
            else:
                if guess_position.guessed():
                    print("hit (again)")
                else:
                    piece.rm_position(guess_position.position())
                    guess_position.set_guessed()
                    if piece.not_hit() > 0:  # ship hasn't sunk yet
                        print("hit")
                    else: 
                        self._ships.remove(piece)
                        print("{} sunk".format(piece))
                        if len(self.ships()) == 0:  # all ships have sunk
                            print("all ships sunk: game over")
                            sys.exit(0)

    def __str__(self):
        string = ""

        # backwards because of the difference in 2D lists and y-axis of grids
        for row in range(len(self._grid) - 1, -1, -1):
            for position in self._grid[row]:
                string += str(position)
            string += "\n"
        return string

class Ship:
    """This class represents a ship piece on the battleship board.

       The class has two methods to add or remove a position in the list of 
       coordinates occupied. It is constructed with a string for its type of 
       ship, an integer for the size of the ship, a list of tuples for 
       positions occupied, and an integer of how many parts of it haven't been 
       hit yet.
    """
        
    def __init__(self, kind, size):
        """Sets up the attributes as a string for the kind, an integer for its 
           size and parts not hit, and an empty list for occupied positions. 

           Parameters: kind is a string representing the type of ship it is.
           size is an integer that is the size of the ship. 

           Returns: None.
        """

        self._kind = kind
        self._size = size
        self._position = []
        self._not_hit = size

    def add_position(self, position):
        """Adds a tuple to the list of occupied positions. 

           Parameters: position is a tuple representing a position on the grid.

           Returns: None.
        """

        self._position.append(position)

    def rm_position(self, position):
        """Removes a tuple from the list of occupied positions and updates the 
           count for parts hit. 

           Parameters: position is a tuple representing a position on the grid.

           Returns: None.
        """

        self._position.remove(position)
        self._not_hit -= 1

    def not_hit(self):
        return self._not_hit
    
    def size(self):
        return self._size
    
    def position(self):
        return self._position

    def __str__(self):
        return self._kind[0]
    
def create_board():
    """Creates a legal board of pieces or exits the program if the placement of 
       a piece is illegal. 

       Parameters: None.

       Returns: A board object that represents the battleship board.
    """
    
    board = Board()
    file = open(input())
    pieces_dict = {"A":(5 , "Aircraft carrier"), "B":(4, "Battleship"), "S":\
    (3, "Submarine"), "D":(3, "Destroyer"),  "P":(2, "Patrol boat")}
    type_sets = set()  # for checking that one of each type is on the board
    for line in file:
        line_lst = line.strip().split()
        type_sets.add(line_lst[0])
        piece = Ship(pieces_dict[line_lst[0]][1], pieces_dict[line_lst[0]][0])
        coord1 = (int(line_lst[1]), int(line_lst[2]))
        coord2 = (int(line_lst[3]), int(line_lst[4]))
        if not 0 <= coord1[0] <= 9 or not 0 <= coord1[1] <= 9 or not 0 <=\
        coord2[0] <= 9 or not 0 <= coord2[1] <= 9:  # check x and y for both
            print("ERROR: ship out-of-bounds: " + line)
            sys.exit(0)
        if coord1[0] != coord2[0] and coord1[1] != coord2[1]:
            print("ERROR: ship not horizontal or vertical: " + line)
            sys.exit(0)
        # pieces get placed in the if statement
        if board.place_piece(piece, coord1, coord2) != piece.size():
            if board.overlap():  # size is wrong too when overlapping
                print("ERROR: overlapping ship: " + line)
            else:
                print("ERROR: incorrect ship size: " + line)
            sys.exit(0)
    file.close()
    if len(type_sets) != 5 or len(board.ships()) != 5:
        print("ERROR: fleet composition incorrect")
        sys.exit(0)  # extra ships or not one of each so exit
    return board

def main():
    board = create_board()
    file = open(input())  # the file for guesses
    for line in file:
        line_lst = line.strip().split()
        board.process_guess(line_lst)
    file.close()

main()