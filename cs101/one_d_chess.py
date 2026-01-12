'''
Elton Ho 
CSC110 Fall 2023
1 p.m. Class
Programming Project 4
This program has eight separate functions that creates the initial 1D 
chessboard list, represents the chessboard graphically, checks if a move is
valid, moves the king, moves the knight, makes sure the right move function is
called, checks if the game is over, and returns the winner of the game. 
'''

def create_board():
    '''
    This function returns a list of strings acting as the initial 1D chessboard.
    Args:
            None.
    Returns:
            A list of strings acting as the initial 1D chess board.
    '''

    # returns the list that is the initial 1D chessboard
    return ["WKi", "WKn", "WKn", 
            "EMPTY", "EMPTY", "EMPTY",
            "BKn", "BKn", "BKi"]

def printable_board(board):
    '''
    This function replaces the "EMPTY" in the list called board with "   " and
    returns a string that represents the board graphically.
    Args:
            board: the list of strings that represents the 1D chessboard.
    Returns:
            A string that represents the board graphically.
    '''

    # replaces all the "Empty" in the list with "   " for the sake of
    # graphically representing the board 
    for i in range(len(board)):
        if board[i] == "EMPTY":
            board[i] = "   "

    # returns a string to represent the board in a more visually appealing
    # and graphical manner than a list         
    return "+-----------------------------------------------------+\n| "\
         + board[0] + " | " + board[1] + " | "+ board[2] + " | " + board[3]\
         +" | " + board[4] + " | " + board[5]+ " | " + board[6] + " | " +\
         board[7] + " | " + board[8] +  \
        " |\n+-----------------------------------------------------+"

def is_valid_move(board, position, player):
    '''
    This function returns a True boolean if the desired move is valid and
    False otherwise.
    Args:
            board: the list of strings that represents the 1D chessboard.
            position: an integer representing the index of the piece the player
            wants to move.
            player: a string of either "WHITE" or "BLACK" representing the side.
    Returns:
            A True boolean if the desired move is valid and False otherwise.
    '''

    # returns True if the position is a valid index on the board and if at that
    #  index it's a piece they own
    if 0 <= position <= len(board) - 1 and board[position][0] == player[0]:
        return True
    
    # returns False otherwise 
    return False

def move_king(board, position, direction):
    '''
    This function alters the board list so that the king can move in the desired
    direction until it takes a piece or reaches the end of the board.
    Args:
            board: the list of strings that represents the 1D chessboard.
            position: an integer representing the index of the piece the player
            wants to move.
            direction: a string of either "LEFT" or "RIGHT" representing the
            direction the player wants to move the king.
    Returns:
            None.
    '''

    # no move has been made yet
    change = False

    # for moving left
    if direction == "LEFT":

        # looks at the board from right to left 
        for i in range(len(board) - 1, -1, -1):

            # it will move the king left legally until it takes a piece or 
            # reaches the end and accounts for incorrectly deleting the king

            # the EMPTY and "   " is included to account for when the 
            # printable_board function hasn't or has been called
            if board[i] not in "EMPTY   " and change == False and board[i] \
            != board[position] and position != 0:
                board[i] = board[position]
                board[position] = "EMPTY"

                # indicate a change has been made to stop moving the piece so
                # that only one turn is made
                change = True

    # for moving right            
    if direction == "RIGHT":

        # looks at the board from left to right 
        for i in range(len(board)):

            # it will move the king right legally until it takes a piece or 
            # reaches the end and accounts for incorrectly deleting the king

            # the EMPTY and "   " is included to account for when the 
            # printable_board function hasn't or has been called
            if board[i] not in "EMPTY   " and change == False and board[i] \
            != board[position] and position != len(board) -1:
                board[i] = board[position]
                board[position] = "EMPTY"

                # indicate a change has been made to stop moving the piece so
                # that only one turn is made
                change = True

def move_knight(board, position, direction):
    '''
    This function alters the board list so that the knight can move in the 
    desired direction for two spaces if in bounds.
    Args:
            board: the list of strings that represents the 1D chessboard.
            position: an integer representing the index of the piece the player
            wants to move.
            direction: a string of either "LEFT" or "RIGHT" representing the
            direction the player wants to move the knight.
    Returns:
            None.
    '''

    # moves the knight two spaces to the left if in bounds
    if direction == "LEFT":
        if position > 1:
            board[position - 2] = board[position]
            board[position] = "EMPTY"

    # moves the knight two spaces to the right if in bounds           
    if direction == "RIGHT":
        if position < len(board) - 1:
            board[position + 2] = board[position]
            board[position] = "EMPTY"

def move(board, position, direction):
    '''
    This function calls either the move_king function or move_knight function
    depending on what the piece on the position index is so that it can move it
    in the desired direction.
    Args:
            board: the list of strings that represents the 1D chessboard.
            position: an integer representing the index of the piece the player
            wants to move.
            direction: a string of either "LEFT" or "RIGHT" representing the
            direction the player wants to move the piece.
    Returns:
            None.
    '''

    # calls the move_king function if it is a king ("i" is the 3rd character
    # of the piece) on the position index
    if board[position][2] ==  "i":
        move_king(board, position, direction)

    # calls the move_knight function if it is a knight ("n" is the 3rd character
    # of the piece) on the position index
    if board[position][2] ==  "n":
        move_knight(board, position, direction)

def is_game_over(board):
    '''
    This function returns a True boolean if the game is over and False if it
    isn't.
    Args:
            board: the list of strings that represents the 1D chessboard.
    Returns:
            A True boolean if the game is over and False if it isn't.
    '''

    # the count of kings starts as 0
    number_of_kings = 0

    # adds to the count if there is a black or white king on the board
    for pieces in board:
        if pieces in "BKiWKi":
            number_of_kings += 1
    
    # if there are two kings on the board the game hasn't ended
    if number_of_kings == 2:
        return False
    
    # the game has ended because there is only 1 king left
    return True 

def whos_the_winner(board):
    '''
    This function returns None if there isn't a winner yet or a string of
    either "White" if white is the winner or "Black" if black is the winner.
    Args:
            board: the list of strings that represents the 1D chessboard.
    Returns:
            None if there isn't a winner yet or a string of either "White"
            if white is the winner or "Black" if black is the winner.
    '''
    
    # assumes there is no winner yet
    winner = None

    # tests if the game is over
    if is_game_over(board) == True:

        for pieces in board:

            # there is a white king left at the end of the game so white wins
            if pieces == "WKi":
                winner = "White"

            # there is a black king left at the end of the game so black wins
            if pieces == "BKi":
                winner = "Black"

    # returns the winner or None if the game hasn't ended yet 
    return winner
board = create_board()
print( printable_board(board) )

move_king(board, 8, "LEFT")
print(board)


move_king(board, 7, "LEFT")
print(board)


move_king(board, 6, "LEFT")
print(board)