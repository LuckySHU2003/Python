from typing import Optional
from support import *


def num_hours() -> float:
    """
    Gives the number of hours spent on the assignment 1.
    
    Returns:
        the total time spent on the assignment 1.
    """
    return 20.0


def create_empty_board(board_size: int) -> list[str]:
    """
    Generates the empty board.

    Parameter:
        board_size: the size of the board 

    Returns:
        An empty board where each string represents a row.
    """
    board = []
    for _ in range(board_size): 
        new_row = EMPTY_SQUARE * board_size
        board.append(new_row)
    return board


def get_square(board: list[str], position: tuple[int, int]) -> str:
    """
    Returns the character present at the give(row, column)position
    within the given board.

    Parameters:
        board: The current game board represented as
            a list of strings.

        position: The characters from the position(row,column)

    Returns:
        str: The characters at the position
        
    Pre-condition:
        Position must exist on board.
    """
    row, col = position
    return board[row][col]


def change_square(board: list[str], position: tuple[int, int],
                  new_square: str) -> None:
    """
    Replaces the character at the given(row,column)position with
    new_square.

    Parameters:
        board: The current game board represented as a list of strings.

        position: tuple[int, int] - A tuple (row, column)
                  indicating the position to change.

        new_square: The new character to place at the specified position.
        
    Pre-condition:
        Position must exist on board.
    """
    row, col = position
    board[row] = board[row][:col] + new_square + board[row][col+1:]


def coordinate_to_position(coordinate: str) -> tuple[int, int]:
    """
    Gets the coordinate corresponding position tuple(row,column).

    Parameter:
        coordinate: The string entered by user to represent
                    a (row,column) position on the board
        
    Returns:
        tuple: The tuple corresponds to the coordinate.
        
    Pre-conditions:
        The coordinate must consist of exactly two characters.
        
        First character is an uppercase letter from 'A' to 'I'

        Second character is a single digit character.
    """
    column_letter, row_number = coordinate
    col = ord(column_letter) - ord('A')
    row = int(row_number) - 1
    return (row, col)


def can_place_ship(board: list[str], ship: list[tuple[int, int]]) -> bool:
    """
    Checks if the ship can be placed on the board.

    Parameters:
        board: list[str] - The current game board represented
               as a list of strings.

        ship: The list of position of ship

    Returns:
        True if the ship can be placed, otherwise False
    """
    for position in ship:
        row, col = position
        if board[row][col] != EMPTY_SQUARE:
            return False
    return True


def place_ship(board: list[str], ship: list[tuple[int, int]]) -> None:
    """
    Places the ship on the board. 

    Parameters:
        board: The current game board represented as a list of strings.

        ship: The list of position of ship

    Pre-condition:
        position must exist on board according to can_place_ship.
    """
    for position in ship:
        row, col = position
        change_square(board, (row, col), ACTIVE_SHIP_SQUARE)


def attack(board: list[str], position: tuple[int, int]) -> None:
    """
    Attempts to attack the cell at the (row,column)position within the board.

    Parameters:
        board: list[str] - The current game board represented
               as a list of strings.

        position: The position (row, column)

    Pre-condition:
        position must exist on board.
    """
    row, col = position
    if board[row][col] == ACTIVE_SHIP_SQUARE:
        change_square(board, position, DEAD_SHIP_SQUARE)
    elif board[row][col] == EMPTY_SQUARE:
        change_square(board, position, MISS_SQUARE)


def display_board(board: list[str], show_ships: bool) -> None:
    """
    Prints the board in a human-readable format.

    Parameters:
        board: The current game board represented
               as a list of strings.
        
        show_ships:
            True: all squares should be shown as they are.
            False: ships are not shown.
    """
    header = HEADER_SEPARATOR + ''.join(
        chr(i) for i in range(ord('A'), ord('A') + len(board))
    )
    print(header)
    for i, row in enumerate(board):
        if not show_ships:
            row = row.replace(ACTIVE_SHIP_SQUARE, EMPTY_SQUARE)
        print(f"{i + 1}{ROW_SEPARATOR}{row}")


def get_player_hp(board: list[str]) -> int:
    """
    Gets the players current HP,
    which is equal to the total number of active ship squares
    remaining in the board.

    Parameter:
        board: The current game board represented
               as a list of strings.

    Returns:
        The total number of active ship squares remaining in their board.
    """
    total_count = 0
    for row in board:
        total_count += row.count(ACTIVE_SHIP_SQUARE)
    return total_count


def display_game(p1_board: list[str], p2_board: list[str],
                 show_ships: bool) -> None:
    """
    Prints the overall game state.
    The game state consists of player 1`s health and board state,
    followed by player 2`s health and board state.

    Parameters:
        p1_board: The board of player1
        p2_board: The board of player2
        show_ships: Whether show ships
    """
    p1_hp = get_player_hp(p1_board)
    p2_hp = get_player_hp(p2_board)

    # Choose correct word
    if p1_hp == 1:
        p1_life_word = 'life'
    else:
        p1_life_word = 'lives'

    if p2_hp == 1:
        p2_life_word = 'life'
    else:
        p2_life_word = 'lives'

    # Prints Players state
    print(f"{PLAYER_ONE}: {p1_hp} {p1_life_word} remaining")
    display_board(p1_board, show_ships)
    
    print(f"{PLAYER_TWO}: {p2_hp} {p2_life_word} remaining")
    display_board(p2_board, show_ships)


def is_valid_coordinate(coordinate: str, board_size: int) -> tuple[bool, str]:
    """
    Checks if the provided coordinate represents a valid coordinate string.

    Parameters:
        coordinate: The string of the coordinate
        board_size: The size of the board

    Returns:
        True if coordinate valid, otherwise False,
        and describes the message about possible issues with coordinate.
    """
    if len(coordinate) != 2:
        return (False, INVALID_COORDINATE_LENGTH) 

    col, row = coordinate[0], coordinate[1]

    if col < 'A' or col >= chr(ord('A') + board_size):
        return (False, INVALID_COORDINATE_LETTER)  

    if not row.isdigit() or int(row) < 1 or int(row) > board_size:
        return (False, INVALID_COORDINATE_NUMBER)

    return SUCCESS


def is_valid_coordinate_sequence(
    coordinate_sequence: str,
    ship_length: int,
    board_size: int
) -> tuple[bool, str]:
    """
    Checks if the provided coordinate sequence represents a sequence of
    exactly ship length comma-separated valid coordinate strings. 

    Parameters:
        coordinate_sequence: The sequence of coordinate
        ship_length: The length of the ship
        board_size: The size of the board

    Returns:
        tuple:containing a bool and corresponding messages
            bool: True if there are exactly ship_length coorinates
                  which are all valid, otherwise False.
        
    """
    coordinates = coordinate_sequence.split(',')
    if len(coordinates) != ship_length:
        return (False, INVALID_COORDINATE_SEQUENCE_LENGTH)

    for coordinate in coordinates:
        valid, message = is_valid_coordinate(coordinate.strip(), board_size)
        if not valid:
            return (valid, message)

    return SUCCESS


def build_ship(coordinate_sequence: str) -> list[tuple[int, int]]:
    """
    Gives the list of (row,column) positions
    corresponding to the coordinate_sequence.

    Parameters:
        coordinate_sequence: A string of comma-separated coordinates

    Returns:
        A list of (row, column) positions matching the given coordinates.

    Pre-condition:
        coordinate_sequence must represent a valid coordinate sequence.
    """
    coordinates = coordinate_sequence.split(',')
    positions = []

    for coordinate in coordinates:
        stripped_coordinate = coordinate.strip()
        position = coordinate_to_position(stripped_coordinate)
        positions.append(position)
    return positions


def setup_board(board_size: int, ship_sizes: list[int]) -> list[str]:
    """
    Allows the user to set up a new board by placing ships.

    Parameters:
        board_size: The size of the board
        ship_sizes: A list of ship sizes to be placed

    Returns:
        The fully set-up board.
    """
    board = create_empty_board(board_size)
    
    for ship_size in ship_sizes:
        while True:
            display_board(board, True)
            coordinate_sequence = input(
                prompt_for_ship_coordinates(ship_size)
            )

            is_valid, message = is_valid_coordinate_sequence(
                coordinate_sequence,
                ship_size,
                board_size)

            if not is_valid:
                print(message)
                continue

            ship_positions = build_ship(coordinate_sequence)

            if not can_place_ship(board, ship_positions):
                print(INVALID_SHIP_PLACEMENT)
                continue

            place_ship(board, ship_positions)
            break

    return board


def get_winner(p1_board: list[str], p2_board: list[str]) -> Optional[str]:
    """
    Returns which player has won (their opponent’s HP is 0),
    or None if neither player has won yet.

    Parameters:
        p1_board: Player 1's board
        p2_board: Player 2's board

    Returns:
        The name of the winning player, or None if no player has won.
    """
    if get_player_hp(p2_board) == 0:
        return PLAYER_ONE
    elif get_player_hp(p1_board) == 0:
        return PLAYER_TWO
    return None


def make_attack(target_board: list[str]) -> None:
    """
    Performs a single turn against the target board.

    Parameter:
        target_board: The board that is being attacked by player.
    """
    while True:
        coordinate = input(TURN_INPUT_MESSAGE)
        valid, message = is_valid_coordinate(coordinate, len(target_board))

        if not valid:
            print(message)
            continue
        
        position = coordinate_to_position(coordinate)
        attack(target_board, position)
        break


def play_game() -> None:
    """
    Coordinates gameplay of a single game of Battleships from start to finish.

    This function manages all operations from the start to the end of the game,
    including setting up the boards, taking turns, and declaring the winner.
    """
    
    # Remind user to input board size
    board_size_input = input("Enter board size: ")
    board_size = int(board_size_input)

    # Remind user to input ship size
    ship_sizes_input = input("Enter ships sizes: ")
    ship_sizes_strings = ship_sizes_input.split(',')  
    ship_sizes = []  # initialize

    # Add to size
    for size_str in ship_sizes_strings:
        size = int(size_str.strip()) 
        ship_sizes.append(size)  
        
    # Set boards of players
    print(DIVIDER_MESSAGE)
    print(P1_PLACEMENT_MESSAGE)
    p1_board = setup_board(board_size, ship_sizes)
    
    print(P2_PLACEMENT_MESSAGE)
    p2_board = setup_board(board_size, ship_sizes)

    # Game Loop 
    current_player = PLAYER_ONE
    current_board = p1_board
    opponent_board = p2_board

    while True:
        print(NEXT_TURN_GRAPHIC)
        display_game(p1_board, p2_board, False)
        print()
        print(f"{current_player}'s turn!")
        make_attack(opponent_board)
        
        # Check if player win 
        winner = get_winner(p1_board, p2_board)
        if winner:
            print(GAME_OVER_GRAPHIC)
            print(f"{winner} won!")
            display_game(p1_board, p2_board, True)
            break

        # Exchange current player and opponent
        if current_player == PLAYER_ONE:
            current_player = PLAYER_TWO
            current_board = p2_board
            opponent_board = p1_board
            
        else:
            current_player = PLAYER_ONE
            current_board = p1_board
            opponent_board = p2_board


if __name__ == "__main__":
    play_game()
