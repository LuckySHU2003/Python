from typing import Optional
from a1_support import *

FORWARD_DELTA = (1, 1)
BACKWARD_DELTA = (-1, 1)
HELP_COMMAND = ["h", "H"]
QUIT_COMMAND = ["q", "Q"]
SPECIAL_COMMANDS = HELP_COMMAND + QUIT_COMMAND
ADD_COMMAND = ["a", "A"]
REMOVE_COMMAND = ["r", "R"]
ACTIONS = ADD_COMMAND + REMOVE_COMMAND

def num_hours() -> float:
    """
    Give an estimation of the time spent on the assignment
    
    Returns:
        (float): the total time spent on the assignment
    """
    return 3.5

def generate_initial_board() -> list[str]:
    """
    Generate the initial state of the game
    
    Returns:
        (list[str]): an empty board as the initial of the game
    """
    board = []
    for _ in range(BOARD_SIZE): #_是占位符
        new_col = BLANK_PIECE * BOARD_SIZE
        board.append(new_col)
        
    return board

def is_column_full(column: str) -> bool:
    """
    Check if a column in the board is full or not
    
    Parameter:
        column (str): a column in the board
    
    Returns:
        (bool): True if the column is full of pieces, otherwise False
    """
    return (column[0] == PLAYER_1_PIECE) or (column[0] == PLAYER_2_PIECE)

def is_column_empty(column: str) -> bool:
    """
    Check if a column in the board is empty or not
    
    Parameter:
        column (str): a column in the board
    
    Returns:
        (bool): True if the column is empty, otherwise False
    """
    return column[-1] == BLANK_PIECE

def display_board(board: list[str]) -> None:
    """
    Display the game board in a human friendly format
    
    Parameter:
        board (list[str]): the current game state
    """
    display = ""

    # Construct the board
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            display = display + COLUMN_SEPARATOR + board[j][i] 
        display = display + COLUMN_SEPARATOR + "\n"
    
    # Column number
    display = display + " "
    for i in range(BOARD_SIZE):
        display = display + str(i+1) + " "

    print(display)

def check_input(command: str) -> bool:
    """
    Validate the user input command. A valid command format is 
    1. "{action}{column}", where {action} may be "a", "A", "r" or "R"
    and {column} is an integer with in the range of the board.
    2. "h" or "H" or "q" or "Q"
    
    Parameter:
        command (str): the user's input 
    
    Returns:
        (bool): True if the command is well-fromatted, otherwise False
    """
    if command == "":
        print(INVALID_FORMAT_MESSAGE)
        return False
    
    # Special commands
    if command in SPECIAL_COMMANDS:
        return True
    
    if command[0] in ACTIONS:
        # Columns must be integers within the valid range
        if command[1:].isdigit():
            column_index = int(command[1:])
            if (1 <= column_index) and (column_index <= BOARD_SIZE):
                return True
            else:
                print(INVALID_COLUMN_MESSAGE)
                return False
            
    print(INVALID_FORMAT_MESSAGE)
    return False

def get_action() -> str:
    """
    Prompt the user until obtain a valid command
    
    Returns:
        (str): the valid input command
    """
    command = input(ENTER_COMMAND_MESSAGE)
    while not check_input(command):
        command = input(ENTER_COMMAND_MESSAGE)
        
    return command


def add_piece(board: list[str], piece: str, column_index: int) -> bool:
    """
    Add a piece to the top of a specific column in the board, 
    if the column is not full
    
    Parameters:
        board (list[str]): the current game state
        piece (str): the type of piece to be added
        column_index (int): The index of the column to be added with a piece
    
    Returns:
        (bool): True if the piece is sucessfully added to the top of 
        the column, otherwise False
    """
    old_col = board[column_index]
    
    if is_column_full(old_col):
        print(FULL_COLUMN_MESSAGE)
        return False
    
    # Extract old pieces in the column
    old_pieces = ""
    for old_piece in old_col:
        if old_piece in PLAYER_1_PIECE + PLAYER_2_PIECE:
            old_pieces += old_piece
            
    new_pieces = piece + old_pieces 
    new_col = (BOARD_SIZE - len(new_pieces)) * BLANK_PIECE + new_pieces
    
    board[column_index] = new_col
    return True

def remove_piece(board: list[str], column_index: int) -> bool:
    """
    Remove the bottom piece from a specific column, if the column is not empty
    
    Parameters:
        board (list[str]): the current game state
        column_index (int): the index of the column to be removed
            the bottom piece
    
    Returns:
        (bool): True if the bottom piece is sucessfully removed from 
            the column, otherwise False
    """
    old_col = board[column_index]
    if is_column_empty(old_col):
        print(EMPTY_COLUMN_MESSAGE)
        return False
    
    new_col = BLANK_PIECE + old_col[:-1]
    board[column_index] = new_col
    return True

def _get_rows(board: list[str]) -> list[str]:
    """
    Get every row of the game board
    
    Parameter:
        board (list[str]): the current game state
    
    Returns:
        (list[str]): all rows of the game board
    """
    
    rows = []
    for i in range(BOARD_SIZE):
        row = ""
        for col in board:
            row += col[i]
        rows.append(row)
    return rows
     
def _get_a_diagonal(board: list[str], point: tuple[int, int],
                    delta: tuple[int, int]) -> str:
    """
    Get the diagonal in the board of a given point followed in a direction

    Parameters:
        board (list[str]): the current game state
        point (tuple[int, int]): the start point of the diagonal
        delta (tuple[int, int]): diagonal moving offsets

    Returns:
        (str): The diagonal from the point in the direction of delta
    """
    
    i, j = point
    delta_i, delta_j = delta
    
    d = ""
    while 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE:
        d += board[i][j]
        i += delta_i
        j += delta_j
        
    return d 

def _get_diagonals(board: list[str]) -> list[str]:
    """
    Get all diagonals in the board

    Parameter:
        board (list[str]): the current game state

    Returns:
        list[str]: all diagonals in the board
    """
    diagonals = []
    
    for i in range(BOARD_SIZE):
        # forward direction
        diagonals.append(_get_a_diagonal(board, (i, 0), FORWARD_DELTA))
        diagonals.append(_get_a_diagonal(board, (0, i), FORWARD_DELTA))
        
        #backward direction
        diagonals.append(_get_a_diagonal(board, (i, 0), BACKWARD_DELTA))
        diagonals.append(_get_a_diagonal(board, (BOARD_SIZE - 1, i),
                                         BACKWARD_DELTA))
    
    return diagonals

def check_win(board: list[str]) -> Optional[str]:
    """
    Validate the current game state into 
    1. player1 wins: there are REQUIRED_WIN_LENGTH number of PLAYER_1_PIECE
        consecutively in any row, columns, or diagonal
    2. player2 wins: there are REQUIRED_WIN_LENGTH number of PLAYER_2_PIECE
        consecutively in any row, columns, or diagonal
    3. draw: player1 and player2 win at the same time
    4. no one has won: other than the above 3 cases
    
    Parameter:
        board (list[str]): the current game state

    Returns:
        Optional[str]: PLAYER_1_PIECE if player1 wins, PLAYER_2_PIECE 
        if player2 wins, BLANK_PIECE if it is a draw
    """
    player1_win = False
    player2_win = False
    
    for line in board + _get_rows(board) + _get_diagonals(board):
        if REQUIRED_WIN_LENGTH * PLAYER_1_PIECE in line:
            player1_win = True
        if REQUIRED_WIN_LENGTH * PLAYER_2_PIECE in line:
            player2_win = True
    
    if player1_win and player2_win:
        return BLANK_PIECE
    elif player1_win:
        return PLAYER_1_PIECE
    elif player2_win:
        return PLAYER_2_PIECE
    
####################################################################
# Another way to approach the check_win by checking all neighbours #
####################################################################
# def check_win(board: list[str]) -> Optional[str]:
#     victor = None

#     # Only need to check half the valid directions at each piece
#     DELTAS = [(1,0),(0,1),(1,1),(1,-1)]
    
#     for curr_col in range(BOARD_SIZE):
#         for curr_row in range(BOARD_SIZE):
#             candidate = board[curr_col][curr_row]
#             # No point checking an empty space
#             if not candidate == BLANK_PIECE: 
                
#                 # Check victory along 4 potential vectors
#                 for delta in DELTAS: 
#                     won = True
#                     for i in range(REQUIRED_WIN_LENGTH - 1):
#                         check_col = curr_col + ((i+1) * delta[0])
#                         check_row = curr_row + ((i+1) * delta[1])
#                         if (not check_col in range(BOARD_SIZE)) or \
#                                 (not check_row in range(BOARD_SIZE)) or \
#                                 (not board[check_col][check_row] == \
#                                   candidate):
#                                     won = False
#                                     break
#                     if won:
#                         if victor == None:
#                             victor = candidate
#                         elif victor != candidate:
#                             victor = BLANK_PIECE
#                             return victor
    
#     return victor

def play_game() -> None:
    """
    Play one exact game until reaching a win condition or a player wants
    to quit
    """
    # Set up the game
    board = generate_initial_board()
    turn_count = 0
    winning_player = None
    successful_move = True
    
    while winning_player is None:
        # Set to current player
        if turn_count % 2 == 0:
            player_move = PLAYER_1_MOVE_MESSAGE
            piece = PLAYER_1_PIECE
        else:
            player_move = PLAYER_2_MOVE_MESSAGE
            piece = PLAYER_2_PIECE
        
        if successful_move:
            display_board(board)
            print(player_move)

        command = get_action()

        if command in HELP_COMMAND:
            print(HELP_MESSAGE)

        elif command in QUIT_COMMAND:
            break
        
        else: # handle adding and removing the piece
            successful_move = False
            target_col = int(command[1:]) - 1
            if command[0] in ADD_COMMAND:
                successful_move = add_piece(board, piece, target_col)

            elif command[0] in REMOVE_COMMAND:
                successful_move = remove_piece(board, target_col)

            if successful_move:
                turn_count += 1

        winning_player = check_win(board)

    # Someone has won (Or the game was quit)
    if not winning_player == None:
        display_board(board)
    if winning_player == PLAYER_1_PIECE:
        print(PLAYER_1_VICTORY_MESSAGE)
    elif winning_player == PLAYER_2_PIECE:
        print(PLAYER_2_VICTORY_MESSAGE)
    elif winning_player == BLANK_PIECE:
        print(DRAW_MESSAGE)

def main() -> None:
    """
    Run Connect 4 (ish) game and enable the replay option
    """
    play_on = True
    while play_on:
        play_game()

        # Handle replay
        user_response = input(CONTINUE_MESSAGE)
        if user_response not in "Yy":
            play_on = False

if __name__ == "__main__":
    main()
