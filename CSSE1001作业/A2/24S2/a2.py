import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Callable, Optional, Union

from support import *


# Model -----------------------------------------------------------------------
class Weapon:
    """
    An abstract class providing base functionality for all weapons.
    """

    def __init__(self):
        """
        Construct a new abstract weapon with default attributes.
        """
        self._name = "AbstractWeapon"
        self._symbol = WEAPON_SYMBOL
        self._effect = {}

    def get_name(self) -> str:
        """Returns the name of this weapon."""
        return self._name

    def get_symbol(self) -> str:
        """Returns the symbol of this weapon."""
        return self._symbol

    def get_effect(self) -> dict[str, int]:
        """Returns a dictionary representing the effect of the weapon."""
        return self._effect

    def get_targets(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Returns a list of all positions within range for this weapon.

        Parameters:
            position (tuple[int, int]): The current position of the weapon.

        Returns:
            list[tuple[int, int]]: Positions within the weapon's range.
        """
        return []

    def __str__(self) -> str:
        """Returns the name of the weapon in a user-friendly format."""
        return self._name

    def __repr__(self) -> str:
        """Returns a string representation to create an identical instance."""
        return f"{self.__class__.__name__}()"


class PoisonDart(Weapon):
    """A specific weapon that adds poison to its target."""

    def __init__(self):
        """Constructs a new Poison Dart weapon."""
        super().__init__()
        self._name = "PoisonDart"
        self._symbol = POISON_DART_SYMBOL
        self._effect = {"poison": 2}

    def get_targets(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        """Returns a list of all positions within range for this weapon.

        Parameters:
            position(tuple[int, int]) : The current position of the weapon.

        Returns:
            list[tuple[int, int]]: A list of positions within the weapon's
                range.
        """
        row, col = position
        targets = []
        
        for delta_row, delta_col in POSITION_DELTAS:
            for i in range(1, 3):
                new_row = row + delta_row * i
                new_col = col + delta_col * i
                targets.append((new_row, new_col))
        return targets


class PoisonSword(Weapon):
    """A weapon dealing damage and adding poison."""

    def __init__(self):
        """Constructs a new Poison Sword weapon."""
        super().__init__()
        self._name = "PoisonSword"
        self._symbol = POISON_SWORD_SYMBOL
        self._effect = {"damage": 2, "poison": 1}

    def get_targets(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Returns a list of all positions within range for this weapon.

        Parameters:
            position(tuple[int, int]):The current position of the weapon.

        Returns:
            list[tuple[int, int]:A list of positions within the weapon's range.
        """
        row, col = position
        targets = [
            (row + delta_row, col + delta_col)
            for delta_row, delta_col in POSITION_DELTAS
        ]
        return targets


class HealingRock(Weapon):
    """A weapon that restores health."""

    def __init__(self):
        """Constructs a new Healing Rock weapon."""
        super().__init__()
        self._name = "HealingRock"
        self._symbol = HEALING_ROCK_SYMBOL
        self._effect = {"healing": 2}

    def get_targets(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        """Returns a list of all positions within range for this weapon.

        Parameters:
            position(tuple[int, int]): The current position of the weapon.

        Returns:
            list[tuple[int, int]]: List of positions within the weapon's range.
        """
        row, col = position
        targets = []
        for delta_row, delta_col in POSITION_DELTAS:
            for i in range(1, 3):
                new_row = row + delta_row * i
                new_col = col + delta_col * i
                targets.append((new_row, new_col))
        return targets


class Tile:
    """
    Base class for tiles. A tile may block movement and may contain a weapon.
    """

    def __init__(self, symbol: str, is_blocking: bool) -> None:
        """
        Initializes a Tile instance.
        
        Parameters:
            symbol(str): The symbol of the tile.
            is_blocking(bool): Whether the tile is blocking.
        """
        self._symbol = symbol
        self._is_blocking = is_blocking
        self._weapon = None

    def is_blocking(self) -> bool:
        """Returns whether the tile blocks movement."""
        return self._is_blocking

    def get_weapon(self) -> Optional[Weapon]:
        """Returns the weapon on this tile or None if none."""
        return self._weapon

    def get_symbol(self) -> str:
        """Returns the symbol of the tile."""
        return self._symbol

    def set_symbol(self, symbol: Optional[str] = None) -> None:
        """Sets the symbol of the tile."""
        self._symbol = symbol

    def set_weapon(self, weapon: Weapon) -> None:
        """
        Sets the weapon on the tile.
        
        Parameters:
            weapon: The weapon to set.
        """
        self._weapon = weapon

    def remove_weapon(self) -> None:
        """Removes the weapon from the tile."""
        self._weapon = None

    def __str__(self) -> str:
        """Returns the symbol as a string."""
        return self._symbol

    def __repr__(self) -> str:
        """Returns a string representation of the tile."""
        return f"Tile('{self._symbol}', {self._is_blocking})"


def create_tile(symbol: str) -> Tile:
    """
    Creates and returns a tile based on the provided symbol.

    Parameters:
        symbol (str): The symbol representing the tile or weapon.

    Returns:
        Tile: An instance of Tile with appropriate attributes.
    """
    tile_mapping = {
        WALL_TILE: (WALL_TILE, True),
        FLOOR_TILE: (FLOOR_TILE, False),
        GOAL_TILE: (GOAL_TILE, False),
        PLAYER_SYMBOL: (PLAYER_SYMBOL, True),
    }
    
    weapon_mapping = {
        POISON_DART_SYMBOL: PoisonDart(),
        POISON_SWORD_SYMBOL: PoisonSword(),
        HEALING_ROCK_SYMBOL: HealingRock(),
    }

    if symbol in tile_mapping:
        tile_symbol, is_blocking = tile_mapping[symbol]
        return Tile(tile_symbol, is_blocking)

    if symbol in weapon_mapping:
        tile = Tile(FLOOR_TILE, False)
        tile.set_weapon(weapon_mapping[symbol])
        return tile

    return Tile(FLOOR_TILE, False)


class Entity:
    """
    A base class providing base functionality for all entities.
    """

    def __init__(self, max_health: int) -> None:
        """
        Constructs an Entity.
        
        Parameters:
            max_health(int): The maximum health of the entity.
        """
        self._name = "Entity"
        self._symbol = ENTITY_SYMBOL
        self._health = max_health
        self._max_health = max_health
        self._poison = 0
        self._weapon = None

    def get_symbol(self) -> str:
        """Returns the symbol of the entity."""
        return self._symbol

    def get_name(self) -> str:
        """Returns the name of the entity."""
        return self._name

    def get_health(self) -> int:
        """Returns the current health of the entity."""
        return self._health

    def get_poison(self) -> int:
        """Returns the poison value affecting the entity."""
        return self._poison

    def get_weapon(self) -> Optional[Weapon]:
        """Returns the weapon held by the entity or None."""
        return self._weapon

    def equip(self, weapon: Weapon) -> None:
        """
        Equips the given weapon.

        Parameters:
            weapon(Weapon): The weapon to equip.
        """
        if weapon is None or isinstance(weapon, Weapon):
            self._weapon = weapon
        else:
            raise TypeError("Invalid weapon provided.")

    def get_weapon_targets(self, position: Position) -> list[Position]:
        """
        Returns the positions the entity can attack with its weapon
        from the given position.
        
        Parameters:
            position(Position): The current position of the entity.
        
        Returns:
            A list of positions the entity can attack.
            If the entity doesn't have a weapon, returns an empty list.
        """
        if self._weapon is None:
            return []  
        return self._weapon.get_targets(position)

    def get_weapon_effect(self) -> dict[str, int]:
        """
        Returns the effect of the entity's weapon.
        
        Returns:
            A dictionary representing the effect of the weapon. If the entity
            doesn't have a weapon, returns an empty dictionary.
        """
        if self._weapon is None:
            return {}  
        return self._weapon.get_effect()
    
    def apply_effects(self, effects: dict[str, int]) -> None:
        """Applies the effects from a weapon to the entity."""
        self._health = max(0, min(self._max_health,
                                  self._health +
                                  effects.get("healing", 0) -
                                  effects.get("damage", 0)))
        self._poison += effects.get("poison", 0)

    def apply_poison(self) -> None:
        """Applies poison effects on the entity."""
        if self._poison > 0:
            self._health = max(0, self._health - self._poison)
            self._poison = max(0, self._poison - 1)

    def is_alive(self) -> bool:
        """Returns True if the entity is alive."""
        return self._health > 0

    def __str__(self) -> str:
        """Returns the name of the entity."""
        return self._name

    def __repr__(self) -> str:
        """Returns a string representation to create an identical entity."""
        return f"{self.__class__.__name__}({self._max_health})"


class Player(Entity):
    """
    Player class that inherits from Entity.
    """

    def __init__(self, max_health: int):
        """
        Constructs a Player.

        Parameters:
            max_health (int): The maximum health of the player.
        """
        super().__init__(max_health)
        self._name = "Player"
        self._symbol = PLAYER_SYMBOL


class Slug(Entity):
    """
    Abstract base class for slugs, inherits from Entity.
    """

    def __init__(self, max_health: int, position: tuple[int, int] = (0, 0)):
        """
        Constructs a Slug.

        Parameters:
            max_health (int): The maximum health of the slug.
            position (tuple[int, int]): The starting position of the slug.
        """
        super().__init__(max_health)
        self._name = "Slug"
        self._can_move = True
        self._symbol = SLUG_SYMBOL
        self._position = position

    def choose_move(self, candidates: list[tuple[int, int]], 
                    current_position: tuple[int, int], 
                    player_position: tuple[int, int]) -> tuple[int, int]:
        """
        Abstract method to choose the slug's movement. Must be implemented
        by subclasses.

        Parameters:
            candidates (list): List of possible positions.
            current_position (tuple): The slug's current position.
            player_position (tuple): The player's current position.

        Returns:
            tuple: The chosen position.
        """
        raise NotImplementedError("Slug subclasses must implement a "
                                  "choose_move method.")

    def get_position(self) -> tuple[int, int]:
        """Returns the current position of the slug."""
        return self._position

    def can_move(self) -> bool:
        """Returns whether the slug can move."""
        return self._can_move

    def end_turn(self) -> None:
        """Toggles the slug's ability to move."""
        self._can_move = not self._can_move


class NiceSlug(Slug):
    """
    Constructs a NiceSlug, inherits from Slug.
    """

    def __init__(self, position: tuple[int, int] = (0, 0)):
        """Constructs a NiceSlug."""
        super().__init__(10, position)
        self._name = "NiceSlug"
        self._weapon = HealingRock()
        self._symbol = NICE_SLUG_SYMBOL

    def choose_move(self, candidates: list[Position],
                    current_position: Position, player_position: Position) \
            -> Position:
        """
        NiceSlug does not move and stays at its current position.

        Parameters:
            candidates(list[Position]): List of possible positions
                the slug can move to.
            current_position(Position): The current position of the slug.
            player_position(Position): The player's current position.

        Returns:
            position: Current position
        """
        return current_position

    def __repr__(self) -> str:
        """Returns a string representation of the NiceSlug."""
        return f"{self.__class__.__name__}()"


class AngrySlug(Slug):
    """
    A hostile slug that moves towards the player.
    """

    def __init__(self, position: tuple[int, int] = (0, 0)):
        """Constructs an AngrySlug."""
        super().__init__(5, position)
        self._name = "AngrySlug"
        self._weapon = PoisonSword()
        self._symbol = ANGRY_SLUG_SYMBOL

    def choose_move(self, candidates: list[Position],
                    current_position: Position, player_position: Position) \
            -> Position:
        """
        AngrySlug Moves towards the player.
        
        Parameters:
            candidates(list[Position]): List of possible positions
                the slug can move to.
            current_position(Position): The current position of the slug.
            player_position(Position): The player's current position.

        Returns:
            Position: The candidate position closest to the player.
        """
        if not candidates:
            return current_position
        return min(candidates,
                   key=lambda pos: distance_to_player(pos, player_position))

    def __repr__(self) -> str:
        """Returns a string representation of the AngrySlug."""
        return f"{self.__class__.__name__}()"


class ScaredSlug(Slug):
    """
    A timid slug that moves away from the player.
    """

    def __init__(self, position: tuple[int, int] = (0, 0)):
        """Constructs a ScaredSlug."""
        super().__init__(3, position)
        self._name = "ScaredSlug"
        self._weapon = PoisonDart()
        self._symbol = SCARED_SLUG_SYMBOL

    def choose_move(self, candidates, current_position, player_position):
        """Moves away from the player."""
        if not candidates:
            return current_position
        return max(candidates,
                   key=lambda pos: distance_to_player(pos, player_position))

    def __repr__(self) -> str:
        """Returns a string representation of the ScaredSlug."""
        return f"{self.__class__.__name__}()"


def distance_to_player(candidate: tuple[int, int],
                       player_position: tuple[int, int]) -> float:
    """
    Calculates the Euclidean distance between a candidate position and the
    player's position.

    Parameters:
        candidate (tuple[int, int]): The candidate position.
        player_position (tuple[int, int]): The player's position.

    Returns:
        float: The Euclidean distance between the two positions.
    """
    return ((candidate[0] - player_position[0]) ** 2 + 
            (candidate[1] - player_position[1]) ** 2) ** 0.5


class SlugDungeonModel:
    """
    Represents the logical state of a SlugDungeon game.
    """

    def __init__(self, tiles: list[list[Tile]], slugs: dict[Position, Slug], 
                 player: Player, player_position: Position) -> None:
        """
        Initializes the SlugDungeonModel.

        Parameters:
            tiles (list[list[Tile]]): A 2D list representing the game's tiles.
            slugs (dict[Position, Slug]): A dictionary mapping positions to
                slug instances.
            player (Player): The player instance.
            player_position (Position): The initial position of the player.
        """
        self._tiles = tiles
        self._slugs = slugs
        self._slugs_len = len(slugs)
        self._player = player
        self._player_position = player_position

    def get_tiles(self) -> list[list[Tile]]:
        """
        Returns the 2D list of tiles representing the dungeon.

        Returns:
            list[list[Tile]]: The tiles of the dungeon.
        """
        return self._tiles

    def get_slugs(self) -> dict[Position, Slug]:
        """
        Returns a dictionary mapping slug positions to the Slug instances at
        those positions.

        Returns:
            dict[Position, Slug]: A dictionary mapping positions to
                slug instances.
        """
        return self._slugs

    def get_slugs_len(self) -> int:
        """
        Returns the number of slugs.

        Returns:
            int: The number of slugs.
        """
        return self._slugs_len

    def get_player(self) -> Player:
        """
        Returns the player instance.

        Returns:
            Player: The player instance.
        """
        return self._player

    def get_player_position(self) -> Position:
        """
        Returns the player's current position.

        Returns:
            Position: The current position of the player.
        """
        return self._player_position

    def get_tile(self, position: Position) -> Tile:
        """
        Returns the tile at a given position.

        Parameters:
            position (Position): The position to query.

        Returns:
            Tile: The tile at the given position.
        """
        row, col = position
        return self._tiles[row][col]

    def get_dimensions(self) -> tuple[int, int]:
        """
        Returns the dimensions of the dungeon.

        Returns:
            tuple[int, int]: The number of rows and columns in the dungeon.
        """
        return len(self._tiles), len(self._tiles[0])

    def get_valid_slug_positions(self, slug: Slug) -> list[Position]:
        """
        Returns a list of valid positions that the slug can move to.

        Parameters:
            slug (Slug): The slug instance.

        Returns:
            list[Position]: A list of valid positions for the slug.
        """
        if not slug.can_move():
            return [slug.get_position()]

        valid_positions = []
        rows, cols = self.get_dimensions()
        row, col = slug.get_position()

        for delta_row, delta_col in POSITION_DELTAS:
            new_row, new_col = row + delta_row, col + delta_col
            # Check Bounds
            if 0 <= new_row < rows and 0 <= new_col < cols:
                tile = self._tiles[new_row][new_col]
                # Check tile is valid or not
                if not tile.is_blocking() and (new_row, new_col) \
                        not in self._slugs\
                        and (new_row, new_col) != self.get_player_position():
                    valid_positions.append((new_row, new_col))

        return valid_positions or [slug.get_position()]

    def perform_attack(self, entity: Entity, position: Position) -> None:
        """
        Executes an attack from the given entity at the specified position.

        Parameters:
            entity (Entity): The attacking entity.
            position (Position): The position to attack from.
        """
        if not entity.get_weapon():
            return

        weapon = entity.get_weapon()
        targets = weapon.get_targets(position)  

        # Player attack Slugs
        if isinstance(entity, Player):  
            for target_pos in targets:  
                target_entity = self._slugs.get(target_pos)
                if target_entity and isinstance(target_entity, Slug):
                    target_entity.apply_effects(
                        weapon.get_effect())
    
        # Slugs only attack Player
        elif isinstance(entity, Slug):  
            for target_pos in targets:
                if target_pos == self._player_position:
                    self._player.apply_effects(weapon.get_effect()) 
        
    def end_turn(self) -> None:
        """
        Handles the steps at the end of a player's turn,
        including applying poison,moving slugs, and handling slug attacks.
        """
        self._player.apply_poison()

        # Track slugs to remove and to move
        slugs_to_remove = []
        slugs_to_move = {}

        # The player's previous position (used for slug movement decisions)
        previous_position = self._player_position
        
        # Loop through all slugs to apply poison and determine moves
        for position, slug in list(self._slugs.items()):
            slug.apply_poison()
            # If the slug is dead, mark for removal
            if not slug.is_alive():
                slugs_to_remove.append(position)
            # Move alive Slugs in the turn when Slugs can move
            elif slug.can_move():
                new_position = slug.choose_move(
                    self.get_valid_slug_positions(slug), position,
                    previous_position
                )
                if new_position != position:
                    slugs_to_move[position] = new_position
                    
        # Move slugs to new positions
        for old_pos, new_pos in slugs_to_move.items():
            self._slugs[new_pos] = self._slugs.pop(old_pos)
            
        # Remove dead slugs and place their weapons
        for position in slugs_to_remove:
            dead_slug = self._slugs.pop(position)
            self.get_tile(position).set_weapon(dead_slug.get_weapon())

        # All remaining slugs make attack
        for position, slug in self._slugs.items():
            self.perform_attack(slug, position)

        # Set up for slugs
        for slug in self._slugs.values():
            slug.end_turn()

    def handle_player_move(self, position_delta: Position) -> None:
        """
        Moves the player in the specified direction.

        Parameters:
            position_delta (Position):
                The change in position to move the player.
        """
        new_row = self._player_position[0] + position_delta[0]
        new_col = self._player_position[1] + position_delta[1]
        num_rows, num_cols = self.get_dimensions()

        # Check Bounds:
        if 0 <= new_row < num_rows and 0 <= new_col < num_cols:
            tile = self._tiles[new_row][new_col]
            # Check position is valid or not
            if not tile.is_blocking() and (new_row, new_col) not in self._slugs:
                self._player_position = (new_row, new_col)
                # Player get  new weapon, replace the old weapon if any
                if tile.get_weapon():
                    self._player.equip(tile.get_weapon())
                    tile.remove_weapon()
                # Player makes attack and Slugs do what they should do
                self.perform_attack(self._player, self._player_position)
                self.end_turn()

    def has_won(self) -> bool:
        """
        Checks if the player has won the game.

        Returns:
            bool: True if the player has won, otherwise False.
        """
        current_tile = self.get_tile(self._player_position)

        if current_tile.get_symbol() == GOAL_TILE and len(self._slugs) == 0:
            return True
        return False
    
    def has_lost(self) -> bool:
        """
        Checks if the player has lost the game.

        Returns:
            bool: True if the player has lost, otherwise False.
        """
        return not self._player.is_alive()


def load_level(filename: str) -> SlugDungeonModel:
    """
    Loads the level from the specified file.

    Parameters:
        filename (str): The path to the level file.

    Returns:
        SlugDungeonModel: The initialized game model based on the level data.

    Raises:
        ValueError: If there is an error loading the level.
    """
    try:
        with open(filename, 'r') as file:
            # First line gives the max health of player
            max_health = int(file.readline())
            
            tiles, slugs, player_position = [], {}, None
            player = Player(max_health)

            slug_mapping = {
                NICE_SLUG_SYMBOL: NiceSlug,
                ANGRY_SLUG_SYMBOL: AngrySlug,
                SCARED_SLUG_SYMBOL: ScaredSlug,
            }

            # Read rest lines to load entities and create tiles
            for row, line in enumerate(file):
                tile_row = []
                for col, char in enumerate(line.strip()):
                    if char in slug_mapping:
                        if len(slugs) >= MAX_SLUGS:
                            raise ValueError("Too many slugs in the level.")
                        tile_row.append(create_tile(FLOOR_TILE))
                        slugs[(row, col)] = slug_mapping[char]((row, col))
                    elif char == PLAYER_SYMBOL:
                        tile_row.append(create_tile(FLOOR_TILE))
                        player_position = (row, col)
                    else:
                        tile = create_tile(char)
                        if tile is None:
                            raise ValueError(f"Invalid tile at ({row}, {col})")
                        tile_row.append(tile)
                tiles.append(tile_row)

            return SlugDungeonModel(tiles, slugs, player, player_position)

    except Exception as e:
        raise ValueError(f"Error loading level from {filename}: {e}")


# View------------------------------------------------------------------------
class DungeonMap(AbstractGrid):
    """
    Displays the dungeon with tiles, the player, and slugs. Tiles are drawn as 
    colored rectangles, and entities (player and slugs) are drawn as colored 
    ovals with their names annotated on the map.
    """

    def __init__(self, root: Union[tk.Tk, tk.Frame], 
                 dimensions: tuple[int, int], size: tuple[int, int]) -> None:
        """
        Initializes the DungeonMap instance.

        Parameters:
            root (Union[tk.Tk, tk.Frame]): The root window or frame.
            dimensions (tuple[int, int]): The number of rows and columns in the
                dungeon.
            size (tuple[int, int]): The size of the map in pixels.
        """
        super().__init__(root, dimensions, size)
        self.pack(side=tk.LEFT, padx=10, pady=10)

    def clear(self) -> None:
        """
        Clears all the drawings from the canvas.
        """
        self.delete("all")

    def redraw(self, tiles: list[list[Tile]], player_position: Position, 
               slugs: dict[Position, Slug]) -> None:
        """
        Redraws the dungeon map with updated tiles, player, and slugs.

        Parameters:
            tiles (list[list[Tile]]): The layout of tiles in the dungeon.
            player_position (Position): The current position of the player.
            slugs (dict[Position, Slug]): A dictionary of slug positions
                and instances.
        """
        self.clear()

        # Display tiles
        for row in range(len(tiles)):
            for col in range(len(tiles[row])):
                self._draw_tile(tiles[row][col], (row, col))

        # Display player
        self._draw_entity(player_position, PLAYER_COLOUR, "Player")

        # Display slugs
        for position, slug in slugs.items():
            self._draw_entity(position, SLUG_COLOUR, str(slug))

    def _draw_tile(self, tile: Tile, position: Position) -> None:
        """
        Draws a tile and annotates its weapon, if any.

        Parameters:
            tile (Tile): The tile to draw.
            position (Position): The position of the tile.
        """
        bbox = self.get_bbox(position)

        # Colour tile based on type
        symbol_colour_mapping = {
            WALL_TILE: WALL_COLOUR,
            FLOOR_TILE: FLOOR_COLOUR,
            GOAL_TILE: GOAL_COLOUR
        }
        
        tile_colour = symbol_colour_mapping.get(tile.get_symbol(), FLOOR_COLOUR)
        self.create_rectangle(bbox, fill=tile_colour)
        
        if tile.get_weapon():
            self.annotate_position(position, tile.get_weapon().get_symbol())

    def _draw_entity(self, position: Position,
                     colour: str, symbol: str) -> None:
        """
        Draws an entity at the given position.

        Parameters:
            position (Position): The entity's position.
            colour (str): The color to fill the entity.
            symbol (str): The symbol representing the entity.
        """
        bbox = self.get_bbox(position)
        self.create_oval(bbox, fill=colour)
        self.annotate_position(position, symbol)

    def remove_player(self, player_position: Position) -> None:
        """
        Removes the player's representation from the map.

        Parameters:
            player_position (Position): The current position of the player.
        """
        bbox = self.get_bbox(player_position)
        self.create_rectangle(bbox, fill=WALL_COLOUR)


class DungeonInfo(AbstractGrid):
    """
    Displays the status information of entities like the player and slugs,
    including health, weapon, and poison status.
    """

    def __init__(self, root: Union[tk.Tk, tk.Frame], 
                 dimensions: tuple[int, int], size: tuple[int, int], 
                 width: int = None) -> None:
        """
        Initializes the DungeonInfo instance.

        Parameters:
            root (Union[tk.Tk, tk.Frame]): The root window or frame.
            dimensions (tuple[int, int]): The number of rows and columns.
            size (tuple[int, int]): The size of the component in pixels.
            width (int, optional): The width of the component.
        """
        super().__init__(root, dimensions, size)
        if width:
            self.config(width=width)
        self.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

    def redraw(self, entities: dict[Position, Entity]) -> None:
        """
        Redraws the status information of the entities.

        Parameters:
            entities (dict[Position, Entity]): A dictionary of entities
                and their positions.
        """
        self.clear()
        headers = ["Name", "Position", "Weapon", "Health", "Poison"]

        # Display headings
        for col, header in enumerate(headers):
            self.annotate_position((0, col), header, font=TITLE_FONT)

        # Display info of entities
        for row, (position, entity) in enumerate(entities.items(), start=1):
            weapon = entity.get_weapon()
            weapon_name = weapon.get_name() if weapon else "None"
            entity_info = [
                entity.get_name(), f"{position}", weapon_name, 
                str(entity.get_health()), str(entity.get_poison())
            ]
            self._draw_row(row, entity_info)

    def _draw_row(self, row: int, data: list[str],
                  is_header: bool = False) -> None:
        """
        Draws a row of information on the grid.

        Parameters:
            row (int): The row number to draw.
            data (list[str]): The information to display in the row.
            is_header (bool, optional): Whether the row is a header row.
        """
        font = TITLE_FONT if is_header else REGULAR_FONT
        for col, text in enumerate(data):
            self.annotate_position((row, col), text, font=font)


class ButtonPanel(tk.Frame):
    """
    Displays control buttons for loading a new game and quitting the game.
    """

    def __init__(self, root: tk.Tk, on_load: Callable, 
                 on_quit: Callable) -> None:
        """
        Initializes the ButtonPanel.

        Parameters:
            root (tk.Tk): The root window.
            on_load (Callable): The callback function to load a new game.
            on_quit (Callable): The callback function to quit the game.
        """
        super().__init__(root, width=900)
        self._load_button = tk.Button(self, text="Load Game", command=on_load)
        self._load_button.pack(side=tk.LEFT, expand=tk.TRUE)
        self._quit_button = tk.Button(self, text="Quit", command=on_quit)
        self._quit_button.pack(side=tk.LEFT, expand=tk.TRUE)


# Controller-----------------------------------------------------------------
class SlugDungeon:
    """
    Controls the game initialization, display, and event handling
    for the SlugDungeon.
    """

    def __init__(self, root: tk.Tk, filename: str) -> None:
        """
        Initializes the game, including the model and view components,
        and handles event bindings.

        Parameters:
            root (tk.Tk): The root instance of the tkinter window.
            filename (str): The filename containing the level data.
        """
        root.title("Slug Dungeon")
        self._root = root

        self._model = load_level(filename)
        self._tiles = self._model.get_tiles()
        map_dimensions = self._model.get_dimensions()

        # Display DungeonMap and DungeonInfo
        self._main_frame = tk.Frame(root)
        self._main_frame.pack(expand=tk.TRUE)
        self._top_frame = tk.Frame(self._main_frame,
                                   width=DUNGEON_MAP_SIZE[0] + 400)
        self._top_frame.pack(side=tk.TOP, expand=tk.TRUE)
        self._dungeon_map = DungeonMap(self._top_frame, map_dimensions,
                                       DUNGEON_MAP_SIZE)
        self._dungeon_map.pack(side=tk.LEFT, expand=tk.TRUE)
        self._slug_info = DungeonInfo(self._top_frame, (7, 5),
                                      SLUG_INFO_SIZE, width=SLUG_INFO_SIZE[0])
        self._slug_info.pack(side=tk.RIGHT, expand=tk.TRUE, fill=tk.Y)

        # Display PlayerInfo
        self._bottom_frame = tk.Frame(self._main_frame,
                                      width=PLAYER_INFO_SIZE[0])
        self._bottom_frame.pack(side=tk.BOTTOM, expand=tk.FALSE)
        self._player_info = DungeonInfo(self._bottom_frame, (2, 5),
                                        PLAYER_INFO_SIZE, width=900)
        self._player_info.pack(side=tk.TOP, expand=tk.TRUE)

        # Display buttons
        self._button_panel = ButtonPanel(self._root, self.load_level,
                                         self._root.destroy)
        self._button_panel.pack(fill=tk.X, ipady=10)

        self.redraw()
        root.bind("<KeyPress>", self.handle_key_press)

    def quit_game(self) -> None:
        """Quits the game by closing the Tkinter window."""
        self._root.destroy()

    def redraw(self) -> None:
        """Redraws the game view based on the current model state."""
        tiles = self._model.get_tiles()
        player_position = self._model.get_player_position()
        slugs = self._model.get_slugs()
        player = self._model.get_player()
        self._dungeon_map.redraw(tiles, player_position, slugs)
        self._slug_info.redraw(slugs)
        self._player_info.redraw({player_position: player})

    def load_level(self) -> None:
        """Loads a new level and redraws the view."""
        filename = filedialog.askopenfilename(
            title="Choose level file", filetypes=[("Text files", "*.txt")])
        if filename:
            try:
                self._model = load_level(filename)
                self._dungeon_map.set_dimensions(self._model.get_dimensions())
                self.redraw()
            except Exception as e:
                print(f"Error loading level: {e}")

    def handle_key_press(self, event: tk.Event) -> None:
        """
        Handles a key press event from the user. If the key corresponds to
        a valid movement, the player's movement is processed and
        the view is redrawn.

        Parameters:
            event (tk.Event): The tkinter event object.
        """
        key_directions = {
            'w': POSITION_DELTAS[3],
            'a': POSITION_DELTAS[1],
            's': POSITION_DELTAS[2],
            'd': POSITION_DELTAS[0],
            'space': (0, 0)
        }
        # Get direction based on key press
        direction = key_directions.get(event.keysym)

        # Handle player movement and redraw the view
        if direction:
            self._model.handle_player_move(direction)
            self.redraw()
 
            # Check if the game has been won or lost
            if self._model.has_won():
                self._show_message(WIN_TITLE, WIN_MESSAGE)
            elif self._model.has_lost():
                self._show_message(LOSE_TITLE, LOSE_MESSAGE)

    def remove_player_from_map(self) -> None:
        """
        Removes the player's symbol from the map.
        """
        player_position = self._model.get_player_position()
        tile = self._tiles[player_position[0]][player_position[1]]
        tile.set_symbol(None)

    def _show_message(self, title: str, message: str) -> None:
        """
        Displays a messagebox with a title and message. Allows the user to
        reload the level or quit.

        Parameters:
            title (str): The title of the messagebox.
            message (str): The message content.
        """
        if messagebox.askyesno(title, message):
            self.load_level()
        else:
            self._root.destroy()


def play_game(root: tk.Tk, file_path: str) -> None:
    """
    Starts the game by loading the specified level file.

    Parameters:
        root (tk.Tk): The root window instance.
        file_path (str): The file path of the level to load.
    """
    SlugDungeon(root, file_path)
    root.mainloop()


def main() -> None:
    """
    The entry point for the game. Creates the root window and starts the game.
    """
    root = tk.Tk()
    file_path = filedialog.askopenfilename(title="Choose level file",
                                           filetypes=[("Text files", "*.txt")])

    if file_path:
        play_game(root, file_path)
    else:
        print("No file selected. Exiting game.")
        root.destroy()


if __name__ == "__main__":
    main()
