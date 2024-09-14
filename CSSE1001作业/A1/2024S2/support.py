EMPTY_SQUARE = '~' # 没有船 默认初始设定 default square (no ship present)
MISS_SQUARE = '!'  # 攻击时为空的indicates the square was empty when hit
ACTIVE_SHIP_SQUARE = 'O'  # 活跃的有船的 indicates this is an active ship square
DEAD_SHIP_SQUARE = 'X'  # 被攻击的 indicates the square was hit

PLAYER_ONE = 'PLAYER 1'
PLAYER_TWO = 'PLAYER 2'

ROW_SEPARATOR = '|'
HEADER_SEPARATOR = ' /'

# graphics图形表示
GAME_OVER_GRAPHIC = '\n=========\nGAME OVER\n========='
NEXT_TURN_GRAPHIC = '\n-------Next_Turn--------'

# messages信息
P1_PLACEMENT_MESSAGE = 'PLAYER 1 SHIP PLACEMENT:'
P2_PLACEMENT_MESSAGE = 'PLAYER 2 SHIP PLACEMENT:'
DIVIDER_MESSAGE = '--------------------'
TURN_INPUT_MESSAGE = 'Enter a coordinate to attack: '


# Errors错误消息
INVALID_COORDINATE_LENGTH = 'Coordinates should be 2 characters long.'
INVALID_COORDINATE_LETTER = 'Invalid coordinate letter.'
INVALID_COORDINATE_NUMBER = 'Invalid coordinate number.'
INVALID_COORDINATE_SEQUENCE_LENGTH = 'Invalid coordinate sequence length.'
INVALID_SHIP_PLACEMENT = 'Ship placement would overlap another ship.'

# Errors for CSSE7030 students only (CSSE1001 students may ignore these two
# errors)
INVALID_SHIP_CONNECTIONS = 'Ship is not connected.\nThis would be a bad start.'
INVALID_BENDY_SHIP = 'Ships must be entirely vertical or horizontal.\nYour ship is bendy, which will make sailing difficult.'

# 类型别名 解释输入的提示 Type aliases (to be optionally used to further clarify type hints)
Position = tuple[int, int]
Result = tuple[bool, str]

SUCCESS: Result = (True, '')

def prompt_for_ship_coordinates(ship_length: int):
    """Returns the appropriate ship coordinate prompt for a given ship length.

    Parameters:
        ship_length: The length of the ship to prompt for

    Returns:
        The appropriate message.
    """
    return f'Enter a comma separated list of {ship_length} coordinates: '

# Functions below here are for use by CSSE7030 students only
# CSSE1001 students may ignore the function below this comment

def manhattan_distance(position: Position, other_position: Position) -> int:
    """Calculates the manhattan distance between two positions.

    Parameters:
        position: The first position
        other_position: The second position

    Returns:
        The manhattan distance between the two supplied positions.
    """
    row, col = position
    other_row, other_col = other_position

    row_difference = abs(row - other_row)
    col_difference = abs(col - other_col)

    return row_difference + col_difference


def add_positions(position: Position, other_position: Position) -> Position:
    """Sums and returns the supplied positions.

    Parameters:
        position: The first position
        other_position: The second position

    Returns:
        The element-wise sum of the first and second positions.
    """
    row, col = position
    other_row, other_col = other_position
    return row + other_row, col + other_col


def negate_position(position: Position) -> Position:
    """Returns the inverse of the supplied position.

    e.g. negate_position((1, 1)) -> (-1, -1)

    Parameters:
        position: The position to negate

    Returns the inverse of the supplied position.
    """
    row, col = position
    return -row, -col


def position_delta(start: Position, end: Position) -> Position:
    """Calculates the difference between two positions.

    Parameteres:
        start: The start position.
        end: The end position.

    Returns:
        The distance from start to end (end - start).
    """
    return add_positions(negate_position(start), end)
