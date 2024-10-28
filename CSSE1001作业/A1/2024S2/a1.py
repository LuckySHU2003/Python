from typing import Optional
from support import *


def create_empty_board(board_size: int) -> list[str]:
    """Generates an initial empty board

    Parameter:
        board_size (int): the size of the game board

    Returns:
        (list[str]): The empty board
    """
    board = []
    for _ in range(board_size):
        board.append(EMPTY_SQUARE * board_size)

    return board


def get_square(board: list[str], position: Position) -> str:
    """Gets the character at the given position on the board.

    Parameters:
        board (list[str]): The board state you wish to get a square from
        position (Position): The position to inspect

    Returns:
        (str): The square at the supplied position
    """
    row, col = position
    return board[row][col]


def change_square(board: list[str], position: Position, character: str) -> None:
    """Mutates the given board such that the character at the given position
        is replaced with new_square.

    Parameters:
        board (list[str]): The board to update
        position (Position): The position to update
        character (str): The character to set at the supplied position on board
    """
    row, col = position
    board[row] = board[row][:col] + character + board[row][col + 1 :]


def coordinate_to_position(coordinate: str) -> Position:
    """Converts the given game coordinate (e.g. A1) into the corresponding
        position (e.g. (0, 0)).

    Parameters:
        coordinate (str): The coordinate i.e. of form 'A1'

    Returns:
        (Position): The corresponding position
    """
    letter, number = coordinate
    return int(number) - 1, ord(letter) - ord('A')


def can_place_ship(board: list[str], ship: list[Position]) -> bool:
    """Checks if the board has room on the proposed squares for a ship to be
        placed

    Parameters:
        board (list[str]): the current board state
        ship (list[Position]): The positions which make up a potential ship
                               placement

    Returns:
        (bool): True iff the ship can be placed without overlapping existing
                non-blank squares
    """
    for position in ship:
        if get_square(board, position) != EMPTY_SQUARE:
            return False
    return True


def place_ship(board: list[str], ship: list[Position]) -> None:
    """Places the ship consisting of the given squares on the board.

    Parameters:
        board (list[str]): The current board state
        ship (list[Position]): The proposed squares to place on
    """
    for position in ship:
        change_square(board, position, ACTIVE_SHIP_SQUARE)


def attack(board: list[str], position: Position) -> None:
    """Attempts to fire upon the supplied square within the given board.

    Parameters:
        board (list[str]): The board to attack
        position (Position): The position to target in this attack
    """
    target_square = get_square(board, position)
    if target_square == ACTIVE_SHIP_SQUARE:
        change_square(board, position, DEAD_SHIP_SQUARE)
        return

    if target_square == EMPTY_SQUARE:
        change_square(board, position, MISS_SQUARE)


def display_board(board: list[str], show_ships: bool) -> None:
    """Prints a representation of the gameboard to the screen.

    Parameters:
        board (list[str]): the current board state
        show_ships (bool): True iff active ships should be displayed
    """

    # Print the header
    header = HEADER_SEPARATOR + 'ABCDEFGHI'[: len(board)]
    print(header)

    # Print the board
    for row_index, row in enumerate(board):
        result = f'{row_index + 1}{ROW_SEPARATOR}'
        for letter in row:
            if letter == ACTIVE_SHIP_SQUARE and not show_ships:
                result += EMPTY_SQUARE
            else:
                result += letter

        print(result)


def get_player_hp(board: list[str]) -> int:
    """Determines how many unhit squares a given board has left, i.e. how much
        hp is left on the board.

    Parameters:
        board: The current board state

    Returns:
        (int): The total amount of hp the player has
    """
    total_hp = 0
    for row in board:
        total_hp += row.count(ACTIVE_SHIP_SQUARE)
    return total_hp


def _display_player_state(
    board: list[str], player_name: str, show_ships: bool
) -> None:
    """Displays the current game state for a single player.

    Note that this is a helper method not specified in the task sheet, which
    reduces duplication in display_game.

    Parameters:
        board (list[str]): The player's current board state
        player_name (str): The name to display for this player
        show_ships (bool): True iff active ships should be made visible
    """
    lives = get_player_hp(board)
    if lives == 1:
        unit = 'life'
    else:
        unit = 'lives'

    print(f'{player_name}: {lives} {unit} remaining')
    display_board(board, show_ships)


def display_game(
    p1_board: list[str], p2_board: list[str], show_ships: bool
) -> None:
    """Displays the current game state.

    Parameters:
        p1_board (list[str]): The board state for player 1.
        p2_board (list[str]): The board state for player 2.
        show_ships (bool): True iff active ships should be made visible
    """
    _display_player_state(p1_board, PLAYER_ONE, show_ships)
    _display_player_state(p2_board, PLAYER_TWO, show_ships)


def is_valid_coordinate(coordinate: str, board_size: int) -> Result:
    """Determines whether a coordinate string is valid.

    Parameters:
        coordinate (str): The raw coordinate string to check
        board_size (int): The dimension of the game board

    Returns:
        (Result): A result tuple detailing validity and error message (if any)
    """
    if len(coordinate) != 2:
        return False, INVALID_COORDINATE_LENGTH

    letter, number = coordinate
    if not 0 <= ord(letter) - ord('A') < board_size:
        return False, INVALID_COORDINATE_LETTER

    if not number.isnumeric() or int(number) < 1 or int(number) > board_size:
        return False, INVALID_COORDINATE_NUMBER

    return SUCCESS


def is_valid_coordinate_sequence(
    coordinate_sequence: str, ship_length: int, board_size: int
) -> Result:
    """Checks if the supplied raw coordinate sequence is valid.

    Parameters:
        coordinate_sequence (str): A comma separated sequence of raw coordinates
        ship_length (int): The required ship length for this sequence
        board_size (int): the dimension of the game board

    Returns:
        (Result): A result tuple detailing validity and error message (if any)
    """

    coordinates = coordinate_sequence.split(',')
    if len(coordinates) != ship_length:
        return False, INVALID_COORDINATE_SEQUENCE_LENGTH

    for coordinate in coordinates:
        is_valid, reason = is_valid_coordinate(coordinate, board_size)
        if not is_valid:
            return False, reason

    return SUCCESS


def build_ship(coordinate_sequence: str) -> list[Position]:
    """Converts a valid coordinate sequence into a ship.

    Parameters:
        coordinate_sequence (str): A valid coordinate sequence

    Returns:
        (list[Position]) The corresponding ship
    """
    ship = []
    for coordinate in coordinate_sequence.split(','):
        ship.append(coordinate_to_position(coordinate))
    return ship


def setup_board(board_size: int, ship_sizes: list[int]) -> list[str]:
    """Allows a user to place all their ships on a new board.

    Parameters:
        board_size (int): the dimension of the game board
        ship_sizes (list[int]): the size of each ship to be constructed

    Returns:
        (list[str]) The new board state with players ships placed on it
    """
    board = create_empty_board(board_size)
    ships_placed = 0
    while ships_placed < len(ship_sizes):
        next_ship_size = ship_sizes[ships_placed]
        display_board(board, show_ships=True)

        # retrieve ship coordinates
        raw_coordinates = input(prompt_for_ship_coordinates(next_ship_size))
        is_valid, reason = is_valid_coordinate_sequence(
            raw_coordinates, next_ship_size, board_size
        )
        if not is_valid:
            print(reason)
            continue

        # ship construction
        ship = build_ship(raw_coordinates)
        if not can_place_ship(board, ship):
            print(INVALID_SHIP_PLACEMENT)
            continue

        place_ship(board, ship)
        ships_placed += 1

    return board


def get_winner(p1_board: list[str], p2_board: list[str]) -> Optional[str]:
    """Determines who (if anyone) has won the game.

    Parameters:
        p1_board (list[str]): Player 1's board
        p2_board (list[str]): Player 2's board

    Returns:
        The name of the player who has won (if any), otherwise None.
    """
    if get_player_hp(p2_board) == 0:
        return PLAYER_ONE

    if get_player_hp(p1_board) == 0:
        return PLAYER_TWO


def make_attack(target_board: list[str]) -> None:
    """Performs a single turn against the target board.

    Parameters:
        target_board (list[str]): The target player's board
    """
    while True:
        raw_coordinate = input(TURN_INPUT_MESSAGE)
        is_valid, reason = is_valid_coordinate(
            raw_coordinate, len(target_board)
        )
        if not is_valid:
            print(reason)
            continue

        position = coordinate_to_position(raw_coordinate)
        attack(target_board, position)
        return


def play_game():
    """Plays through an entire game of battleships."""
    board_size = int(input('Enter board size: '))
    ship_sizes = []
    for item in input('Enter ships sizes: ').split(','):
        ship_sizes.append(int(item))

    # Board placement phase
    print(DIVIDER_MESSAGE)
    print(P1_PLACEMENT_MESSAGE)
    p1_board = setup_board(board_size, ship_sizes)

    print(P2_PLACEMENT_MESSAGE)
    p2_board = setup_board(board_size, ship_sizes)

    is_player_ones_turn = True
    while True:
        # Check win conditions
        winner = get_winner(p1_board, p2_board)
        if winner is not None:
            break

        if is_player_ones_turn:
            target_board = p2_board
            player = PLAYER_ONE
        else:
            target_board = p1_board
            player = PLAYER_TWO

        # Display game state
        print(NEXT_TURN_GRAPHIC)
        display_game(p1_board, p2_board, show_ships=False)

        print(f"\n{player}'s turn!")
        # Perform turn and switch
        make_attack(target_board)
        is_player_ones_turn = not is_player_ones_turn

    print(GAME_OVER_GRAPHIC)
    print(f'{winner} won!')
    display_game(p1_board, p2_board, show_ships=True)


if __name__ == '__main__':
    play_game()
