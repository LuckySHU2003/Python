import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Callable, Optional

from support import *


def _add_positions(a: Position, b: Position) -> Position:
    """Helper function which adds two positions together element-wise.

    Parameters:
        a (Position): A position.
        b (Position): Another position.

    Returns:
        Position: The position resulting from adding a and b element-wise.
    """
    return (a[0] + b[0], a[1] + b[1])


class Weapon:
    """An abstract class representing a weapon."""

    WEAPON_NAME = "AbstractWeapon"
    WEAPON_SYMBOL = WEAPON_SYMBOL
    EFFECT = {}
    RANGE = 0

    def __init__(self) -> None:
        """Initializes a new weapon."""
        self._name = self.WEAPON_NAME
        self._effect = self.EFFECT

    def get_targets(self, position: Position) -> list[Position]:
        """Calculates the positions the weapon could reach from position.

        Parameters:
            position (Position): The current position of the weapon.

        Returns:
            list[Position]: A list of positions that the weapon can reach.
        """
        targets = []
        for i in range(1, self.RANGE + 1):
            deltas = [(0, i), (0, -i), (i, 0), (-i, 0)]
            targets.extend([_add_positions(position, delta)
                            for delta in deltas])
        return targets

    def get_effect(self) -> dict[str, int]:
        """Returns the effect of the weapon."""
        return self._effect

    def get_name(self) -> str:
        """Returns the name of the weapon."""
        return self._name

    def get_symbol(self) -> str:
        """Returns the symbol of the weapon."""
        return self.WEAPON_SYMBOL

    def __str__(self) -> str:
        return self.get_name()

    def __repr__(self) -> str:
        return self.__class__.__name__ + "()"


class PoisonDart(Weapon):
    """Reaches up to 2 squares away, and applies poison each time it hits."""

    WEAPON_NAME = "PoisonDart"
    WEAPON_SYMBOL = POISON_DART_SYMBOL
    EFFECT = {"poison": 2}
    RANGE = 2


class PoisonSword(Weapon):
    """Only reaches 1 square away but does damage and applies poison."""

    WEAPON_NAME = "PoisonSword"
    WEAPON_SYMBOL = POISON_SWORD_SYMBOL
    EFFECT = {"damage": 2, "poison": 1}
    RANGE = 1


class HealingRock(Weapon):
    """A weapon which heals its victim."""

    WEAPON_NAME = "HealingRock"
    WEAPON_SYMBOL = HEALING_ROCK_SYMBOL
    EFFECT = {"healing": 2}
    RANGE = 2


class Tile:
    """A tile, which can hold weapons and block player movement."""

    def __init__(self, symbol: str, is_blocking: bool) -> None:
        """Initializes a new tile.

        Parameters:
            symbol (str): The symbol representing the tile.
            is_blocking (bool): True iff the tile is blocking.
        """
        self._weapon = None
        self._symbol = symbol
        self._is_blocking = is_blocking

    def set_weapon(self, weapon: Weapon) -> None:
        """Fills the tile with the given weapon."""
        self._weapon = weapon

    def remove_weapon(self) -> None:
        """Removes the item from the tile."""
        self._weapon = None

    def get_weapon(self) -> Optional[Weapon]:
        """Returns the item in the tile."""
        return self._weapon

    def is_blocking(self) -> bool:
        """Returns True iff the tile is blocking."""
        return self._is_blocking

    def __str__(self) -> str:
        return self._symbol

    def __repr__(self) -> str:
        return self.__class__.__name__ + (f"('{self._symbol}',"
                                          f" {self._is_blocking})")


def create_tile(symbol: str) -> Tile:
    """Creates a tile based on the given symbol.

    Parameters:
        symbol (str): The symbol representing the tile.

    Returns:
        Tile: A new tile object based on the given symbol.
    """
    if symbol == WALL_TILE:
        return Tile(symbol, True)
    elif symbol in [GOAL_TILE, FLOOR_TILE]:
        return Tile(symbol, False)
    else:
        tile = Tile(FLOOR_TILE, False)
        if symbol in WEAPON_MAP:
            tile.set_weapon(WEAPON_MAP[symbol]())
        return tile


class Entity:
    """An abstract class representing a generic entity."""

    NAME = "Entity"
    SYMBOL = ENTITY_SYMBOL

    def __init__(self, max_health: int) -> None:
        """Initializes a new entity. Entities start with maximum health.

        Parameters:
            max_health (int): The maximum health of the entity.
        """
        self._max_health = max_health
        self._health = max_health
        self._poison = 0
        self._weapon = None

    def get_symbol(self) -> str:
        """Returns the symbol of the entity."""
        return self.SYMBOL

    def get_name(self) -> str:
        """Returns the name of the entity."""
        return self.NAME

    def get_health(self) -> int:
        """Returns the current health of the entity."""
        return self._health

    def get_poison(self) -> int:
        """Returns the current poison of the entity."""
        return self._poison

    def get_weapon(self) -> Optional[Weapon]:
        """Returns the weapon equipped by the entity, or None."""
        return self._weapon

    def get_weapon_targets(self, position: Position) -> list[Position]:
        """Returns the positions the entity can attack with its weapon from
            the given position.

        Parameters:
            position (Position): The position to attack from

        Returns:
            list[Position]: A list of positions that the entity can attack.
        """
        if self._weapon is None:
            return []
        return self._weapon.get_targets(position)

    def get_weapon_effect(self) -> dict[str, int]:
        """Returns the effects of the entity's weapon."""
        if self._weapon is None:
            return {}
        return self._weapon.get_effect()

    def equip(self, weapon: Weapon) -> None:
        """Equips the given weapon."""
        self._weapon = weapon

    def _apply_damage(self, damage: int) -> None:
        """Reduces the entity's health by the given damage amount, then caps
            the entity's health to sit in the range [0, max_health].

        Parameters:
            damage (int): The amount of damage to apply to the entity.
        """
        self._health -= damage
        self._health = min(max(0, self._health), self._max_health)

    def apply_effects(self, effects: dict[str, int]) -> None:
        """Applies all effects in the given dictionary to the entity.

        Parameters:
            effects (dict[str, int]): Maps type of each effect to the amount.
        """
        self._poison += effects.get("poison", 0)
        self._apply_damage(-effects.get("healing", 0))
        self._apply_damage(effects.get("damage", 0))

    def apply_poison(self) -> None:
        """Handles changes to the entity at the end of a turn."""
        self._apply_damage(self._poison)
        self._poison = max(0, self._poison - 1)

    def is_alive(self) -> bool:
        """Returns True iff the entity is alive."""
        return self._health > 0

    def __str__(self) -> str:
        return self.get_name()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._max_health})"


class Player(Entity):
    """A player, which starts with no weapon."""

    NAME = "Player"
    SYMBOL = PLAYER_SYMBOL


class Slug(Entity):
    """An abstract class representing a monster."""

    NAME = "Slug"
    SYMBOL = SLUG_SYMBOL
    TURNS_PER_MOVE = 2

    def __init__(self, max_health: int) -> None:
        """Initializes a new Slug.

        Parameters:
            max_health (int): The maximum health of the slug.
        """
        super().__init__(max_health)
        self._move_counter = 0

    def choose_move(
        self,
        candidates: list[Position],
        current_position: Position,
        player_position: Position,
    ) -> Position:
        """Chooses the next move.

        Parameters:
            candidates (list[Position]): A list of valid positions to move to.
            current_position (Position): The current position of the monster.
            player_position (Position): The (previous) position of the player.

        Returns:
            Position: The chosen position to move to.
        """

        raise NotImplementedError(
            "Slug subclasses must implement a choose_move method."
        )

    def can_move(self) -> bool:
        """Returns True iff the entity can move this turn."""
        return self._move_counter % self.TURNS_PER_MOVE == 0

    def end_turn(self) -> None:
        """Handles changes to the entity at the end of a turn."""
        self._move_counter += 1


class NiceSlug(Slug):
    """A nice but lazy slug that doesn't move and can heal the player."""

    NAME = "NiceSlug"
    SYMBOL = NICE_SLUG_SYMBOL
    MAX_HEALTH = 10

    def __init__(self) -> None:
        """Initializes a new NiceSlug."""
        super().__init__(self.MAX_HEALTH)
        self.equip(HealingRock())

    def choose_move(
        self,
        candidates: list[Position],
        current_position: Position,
        player_position: Position,
    ) -> Position:
        return current_position

    def __repr__(self) -> str:
        return "NiceSlug()"


def _euclidean_rank(candidate_position: Position,
                    player_position: Position) -> int:
    """Returns a number proportional to the Euclidean distance between the
        positions.
    """
    row1, col1 = candidate_position
    row2, col2 = player_position
    return (row1 - row2) ** 2 + (col1 - col2) ** 2


class AngrySlug(Slug):
    """An angry slug that moves quickly and has a sword."""

    NAME = "AngrySlug"
    SYMBOL = ANGRY_SLUG_SYMBOL
    MAX_HEALTH = 5

    def __init__(self) -> None:
        """Initializes a new AngrySlug."""
        super().__init__(self.MAX_HEALTH)
        self.equip(PoisonSword())

    def choose_move(
        self,
        candidates: list[Position],
        current_position: Position,
        player_position: Position,
    ) -> Position:
        ordered = sorted(
            candidates + [current_position],
            key=lambda x: (_euclidean_rank(x, player_position), x),
        )
        return ordered[0] if ordered else current_position

    def __repr__(self) -> str:
        return "AngrySlug()"


class ScaredSlug(Slug):
    """A scared slug that tries to run away from the player."""

    NAME = "ScaredSlug"
    SYMBOL = SCARED_SLUG_SYMBOL
    MAX_HEALTH = 3

    def __init__(self) -> None:
        """Initializes a new ScaredSlug."""
        super().__init__(self.MAX_HEALTH)
        self.equip(PoisonDart())

    def choose_move(
        self,
        candidates: list[Position],
        current_position: Position,
        player_position: Position,
    ) -> Position:
        ordered = sorted(
            candidates + [current_position],
            key=lambda x: (_euclidean_rank(x, player_position), x),
        )
        return ordered[-1] if ordered else current_position

    def __repr__(self) -> str:
        return "ScaredSlug()"


WEAPON_MAP = {
    POISON_DART_SYMBOL: PoisonDart,
    POISON_SWORD_SYMBOL: PoisonSword,
    HEALING_ROCK_SYMBOL: HealingRock,
}
SLUG_MAP = {
    SCARED_SLUG_SYMBOL: ScaredSlug,
    ANGRY_SLUG_SYMBOL: AngrySlug,
    NICE_SLUG_SYMBOL: NiceSlug,
}


class SlugDungeonModel:
    """A class representing the model for the slug dungeon game."""

    def __init__(
        self,
        tiles: list[list[Tile]],
        slugs: dict[Position, Slug],
        player: Player,
        player_position: Position,
    ) -> None:
        """Initializes a new SlugDungeonModel.

        Parameters:
            tiles (list[list[Tile]]): The tiles of the map.
            monsters (dict[Position, Slug]): A dictionary mapping positions of
                                             monsters to the monsters at those
                                             positions.
            player (Player): The player.
            player_position (Position): The starting position of the player.
        """
        self._tiles = tiles
        self._slugs = slugs
        self._player = player
        self._player_position = player_position
        self._last_player_position = player_position

    def get_tiles(self) -> list[list[Tile]]:
        """Returns the tiles of the map."""
        return self._tiles

    def get_slugs(self) -> dict[Position, Slug]:
        """Returns a dictionary mapping positions of monsters to the monsters
        at those positions."""
        return self._slugs

    def get_player(self) -> Player:
        """Returns the player."""
        return self._player

    def get_player_position(self) -> Position:
        """Returns the current position of the player."""
        return self._player_position

    def get_tile(self, position: Position) -> Tile:
        """Returns the tile at the given position."""
        return self._tiles[position[0]][position[1]]

    def get_dimensions(self) -> tuple[int, int]:
        """Returns the dimensions of the map."""
        return len(self._tiles), len(self._tiles[0])

    def _get_monster_position(self, monster: Slug) -> Position:
        """
        Returns the position of the given monster. Precondition is that the
        monster is in the model.
        """
        for position, candidate in self._slugs.items():
            if candidate == monster:
                return position

    def get_valid_slug_positions(self, slug: Slug) -> list[Position]:
        """Returns a list of valid positions for the given monster to move to.

        Parameters:
            slug (Slug): The slug to move.

        Returns:
            list[Position]: Valid positions for the monster to move to.

        Pre-condition:
            - The given slug is alive and exists in the game.
        """
        if not slug.can_move():
            return []

        position = self._get_monster_position(slug)
        valid = [position]
        for delta in POSITION_DELTAS:
            candidate = _add_positions(position, delta)
            if (self._is_valid_position(candidate)
                    and candidate != self._player_position):
                valid.append(candidate)
        return valid

    def _is_valid_position(self, position: Position) -> bool:
        """
        Determines if a position is valid for a move.

        Parameters:
            position (Position): The position to check.

        Returns:
            True iff the given position exists and contains a non-blocking tile.
        """
        row, col = position
        if row < 0 or row >= len(self._tiles):
            return False
        if col < 0 or col >= len(self._tiles[0]):
            return False

        return (not self._tiles[row][col].is_blocking()
                and not self._slugs.get(position))

    def perform_attack(self, entity: Entity, position: Position) -> None:
        """Allows an entity to make an attack from a particular position.

        Parameters:
            entity (Entity): The entity making the attack.
            position (Position): The position to attack from.
        """
        # Entity makes an attack on all squares they can with their weapon
        targets = entity.get_weapon_targets(position)
        player_pos = self._player_position

        # Allow entity to try to attack each target
        for target_pos in targets:
            if entity is self._player and target_pos in self._slugs:
                self._slugs[target_pos].apply_effects(
                    entity.get_weapon_effect())
            elif entity in self._slugs.values() and target_pos == player_pos:
                self._player.apply_effects(entity.get_weapon_effect())

    def _tick_monsters(self) -> None:
        """Handles a tick for all monsters, including deleting them from
        the game and replacing them with their weapon if they die."""
        result = {}
        for position, monster in self.get_slugs().items():
            monster.apply_poison()
            if monster.is_alive():
                result[position] = monster
            else:
                tile = self.get_tile(position)
                tile.set_weapon(monster.get_weapon())
        self._slugs = result

    def _move_monster(self, position: Position, monster: Slug) -> None:
        """
        Move a single monster to the chosen position

        Parameters:
            position (Position): the current position of the monster.
            monster (Slug): the monster to be moved.
        """
        valid_positions = self.get_valid_slug_positions(monster)
        next_position = monster.choose_move(
            valid_positions, position, self._last_player_position
        )
        if not monster.can_move():
            return

        self._slugs.pop(position)
        self._slugs[next_position] = monster

    def _move_monsters(self) -> None:
        """Move all monsters to their chosen positions."""
        for position, monster in list(self.get_slugs().items()):
            self._move_monster(position, monster)

    def _perform_monster_attacks(self) -> None:
        """Performs attacks for all monsters."""
        for position, monster in self.get_slugs().items():
            self.perform_attack(monster, position)
            monster.end_turn()

    def end_turn(self) -> None:
        """Ends the turn for the player and monsters, including movement, ticks,
        and attacks."""
        self._player.apply_poison()
        self._tick_monsters()
        self._move_monsters()
        self._perform_monster_attacks()

    def handle_player_move(self, position_delta: Position) -> None:
        """Moves the player in the given direction if the move is valid, then
            handles the end of the turn (attacks, monster movement, etc.).

        Parameters:
            position_delta (Position): The change in position to apply to the
                                        player's position.
        """
        new_position = _add_positions(self._player_position, position_delta)
        if not self._is_valid_position(new_position):
            return

        # Player moves
        self._last_player_position = self._player_position
        self._player_position = new_position

        # Pick up any weapon on the new tile
        tile = self.get_tile(new_position)
        weapon = tile.get_weapon()
        if weapon is not None:
            self._player.equip(weapon)
            tile.remove_weapon()

        # Attack
        self.perform_attack(self._player, self._player_position)
        self.end_turn()

    def has_won(self) -> bool:
        """Returns True iff the player has reached the goal."""
        tile_symbol = str(self.get_tile(self._player_position))
        return not self._slugs and tile_symbol == "G"

    def has_lost(self) -> bool:
        """Returns True iff the player has died."""
        return not self._player.is_alive()


def load_level(filename: str) -> SlugDungeonModel:
    """Initializes the dungeon model based on the file with the given name.

    Parameters:
        filename (str): The name of the file to read.

    Returns:
        SlugDungeonModel: The initialized dungeon model.
    """
    tiles = []
    monsters = {}
    player_position = None

    with open(filename) as file:
        player = Player(int(file.readline()))
        for row_num, line in enumerate(file):
            row = []
            for col_num, char in enumerate(line.strip()):
                position = (row_num, col_num)
                row.append(create_tile(char))

                # Process any entities
                if char == PLAYER_SYMBOL:
                    player_position = position
                elif char in SLUG_MAP:
                    monsters[position] = SLUG_MAP[char]()

            tiles.append(row)

    return SlugDungeonModel(tiles, monsters, player, player_position)


class DungeonMap(AbstractGrid):
    """A simple view for the dungeon map."""

    TILE_TO_COLOR = {
        GOAL_TILE: GOAL_COLOUR,
        FLOOR_TILE: FLOOR_COLOUR,
    }

    def _draw_tiles(self, tiles: list[list[Tile]]) -> None:
        """
        Draws the tiles on the map.

        Parameters:
            tiles (list[list[Tile]]): The tiles of the map.
        """
        for row_num, row in enumerate(tiles):
            for col_num, tile in enumerate(row):
                # Draw initial tile
                bbox = self.get_bbox((row_num, col_num))
                color = self.TILE_TO_COLOR.get(str(tile), WALL_COLOUR)
                self.create_rectangle(bbox, fill=color)

                # Draw symbol for item (weapon) if any
                weapon = tile.get_weapon()
                if weapon:
                    position = (row_num, col_num)
                    self.annotate_position(position, weapon.get_symbol())

    def _draw_entity(
        self, position: Position, entity_name: str, is_player: bool = True
    ):
        """
        Draws an entity on the map.

        Parameters:
            position (Position): the position of the entity
            entity_name (str): the name of the entity
            is_player (bool): True if the entity is the player, otherwise false
        """
        colour = PLAYER_COLOUR if is_player else SLUG_COLOUR
        self.create_oval(self.get_bbox(position), fill=colour)
        if entity_name.endswith("Slug"):
            entity_name = entity_name[:-4] + "\nSlug"
        self.annotate_position(position, entity_name)

    def redraw(
        self,
        tiles: list[list[Tile]],
        player_position: Position,
        slugs: dict[Position, Slug],
    ) -> None:
        """Clears and redraws the map.

        Parameters:
            tiles (list[list[Tile]]): The tiles of the map.
            player_position (Position): The position of the player.
            monsters (dict[Position, Slug]): A list of monsters to draw.
        """
        self.clear()
        self._draw_tiles(tiles)

        for (position, monster) in slugs.items():
            self._draw_entity(position, monster.get_name(), is_player=False)
        self._draw_entity(player_position, "Player")


class DungeonInfo(AbstractGrid):
    """A simple view for some dungeon info."""

    def redraw(self, entities: dict[Position, Entity]) -> None:
        """Clears and redraws the info with the given entities.

        Parameters:
            entities (dict[Position, Entity]): Maps positions to entities.
        """
        self.clear()

        # Draw header
        for column, header in enumerate(
            ["Name", "Position", "Weapon", "Health", "Poison"]
        ):
            self.annotate_position((0, column), header, font=TITLE_FONT)

        # Draw monster info
        for i, (position, entity) in enumerate(entities.items()):
            weapon = None
            if entity.get_weapon():
                weapon = entity.get_weapon().get_name()
            name = entity.get_name()
            health = entity.get_health()
            poison = entity.get_poison()
            for j, value in enumerate(
                [name, position, weapon, health, poison]
            ):
                self.annotate_position((i + 1, j), text=str(value))


class ButtonPanel(tk.Frame):
    """ A simple view for the functional buttons in the game"""

    def __init__(self, root: tk.Tk, on_load: Callable,
                 on_quit: Callable) -> None:
        """Initializes a new ButtonPanel.

        Parameters:
            root (tk.Tk): The root window for the game.
            on_load (Callable): A method for handling loading new games
            on_quit (Callable): A method for handling exit the game
        """
        super().__init__(root)
        tk.Button(self, text="Load Game", command=on_load).pack(
            side=tk.LEFT, expand=True
        )
        tk.Button(self, text="Quit", command=on_quit).pack(side=tk.LEFT,
                                                           expand=True)


class SlugDungeon:
    """A class representing the Slug Dungeon game."""

    KEY_TO_DELTA = {
        "w": (-1, 0),
        "s": (1, 0),
        "a": (0, -1),
        "d": (0, 1),
        "space": (0, 0),
    }

    def __init__(self, root: tk.Tk, filename: str) -> None:
        """Initializes a new SlugDungeon.

        Parameters:
            root (tk.Tk): The root window for the game.
            filename (str): The name of the file to load the level from.
        """
        self._root = root
        self._root.title("Slug Dungeon")
        self._current_filename = filename
        self._model = load_level(filename)

        frame = tk.Frame(root)
        frame.pack(expand=True, fill=tk.X)

        self._map = DungeonMap(frame, self._model.get_dimensions(),
                               DUNGEON_MAP_SIZE)
        self._map.pack(side=tk.LEFT)

        self._monster_info = DungeonInfo(frame, (MAX_SLUGS + 1, 5),
                                         SLUG_INFO_SIZE)
        self._monster_info.pack(side=tk.LEFT)

        self._player_info = DungeonInfo(root, (2, 5),
                                        PLAYER_INFO_SIZE)
        self._player_info.pack(fill=tk.X)

        self._buttons = ButtonPanel(root, self.load_level, root.destroy)
        self._buttons.pack(fill=tk.X, ipady=10)

        self._root.bind("<KeyPress>", self.handle_key_press)
        self.redraw()

    def redraw(self) -> None:
        """Redraws the game."""
        tiles = self._model.get_tiles()
        player_position = self._model.get_player_position()
        monsters = self._model.get_slugs()
        player = self._model.get_player()

        self._map.redraw(tiles, player_position, monsters)
        self._monster_info.redraw(monsters)
        self._player_info.redraw({player_position: player})

        self._root.update_idletasks()

    def handle_key_press(self, event: tk.Event) -> None:
        """Handles a key press event.

        Parameters:
            event (tk.Event): The event to handle.
        """
        if event.keysym not in self.KEY_TO_DELTA:
            return
        self._model.handle_player_move(self.KEY_TO_DELTA[event.keysym])
        self.redraw()

        if self._model.has_won():
            title, message = WIN_TITLE, WIN_MESSAGE
        elif self._model.has_lost():
            title, message = LOSE_TITLE, LOSE_MESSAGE
        else:
            return

        # Handle game win/loss
        if messagebox.askyesno(title, message):
            self._load_from_file(self._current_filename)
        else:
            self._root.destroy()

    def _load_from_file(self, filename: str) -> None:
        """Loads a new level from the given filename.

        Parameters:
            filename (str): The name of the file to load.
        """
        self._model = load_level(filename)
        self._current_filename = filename
        self._map.set_dimensions(self._model.get_dimensions())
        self.redraw()

    def load_level(self) -> None:
        """Loads a new level."""
        filename = filedialog.askopenfilename()
        if filename:
            self._load_from_file(filename)


def play_game(root: tk.Tk, filename: str) -> None:
    """Plays the Slug Dungeon game.

    Parameters:
        root (tk.Tk): The root window for the game.
        filename (str): The name of the file to load the level from.
    """
    dungeon = SlugDungeon(root, filename)
    root.mainloop()


def main():
    root = tk.Tk()
    play_game(root, "./levels/level1.txt")


if __name__ == "__main__":
    main()
