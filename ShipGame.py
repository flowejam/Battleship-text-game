## ====================================
## Class definitions:

class ShipGame:
    '''
    Represents a game of Battleship. 
    
    Methods: Initializes a ShipGame, with methods for representing the firing of a torpedo
    during the game, placing each player's ships on their grid, getting the number
    of ships remaining for a player, and the current state of the game, among other
    getter methods.

    Methods and data members utilize these classes: Player, Ship, Grid 

    It uses these classes because a ShipGame has two players (represented by the 
    Player class), and the Player class includes as a data member a list of Ship 
    objects, as well as a Grid object.
    '''
    def __init__(self):
        '''
        Initializes a ShipGame object.
        '''
        self._current_state = 'UNFINISHED'

        self._dict_of_players = {
                'first': Player(),
                'second': Player()
                }
        self._whose_turn = 'first'

    def place_ship(self, player: str, length: int, coordinates: str, orientation: str) -> bool:
        '''
        Signature: takes as parameters a string, integer, string, and a string, and 
        returns a boolean.

        Purpose: adds a ship of a certain length and orientation at a coordinate,
        as long as it is a valid position for the ship. 
        '''
        player_obj = self.get_player(player)
        ship_obj = Ship(length, coordinates, orientation)
        return player_obj.add_ship(ship_obj)


    def get_player(self, player: str):
        '''
        Signature: takes a string as a parameter.
        Purpose: Returns the '_dict_of_players' data member.
        '''
        return self._dict_of_players.get(player)

    def get_current_state(self) -> str:
        '''
        `get_current_state` returns the current state of the game: either 
        'FIRST_WON', 'SECOND_WON', or 'UNFINISHED'.
        '''
        return self._current_state

    def get_other_player(self, player: str) -> str:
        '''
        Signature: takes a string as a parameter, returns a string.

        Purpose: given a string (either 'first' or 'second'), returns the other
        player in this two player Battleship game.
        '''
        if player == 'first':
            other_player = 'second'
        elif player == 'second':
            other_player = 'first'
        return other_player


    def fire_torpedo(self, player: str, coordinates: str) -> bool:
        '''
        Signature: takes as paraemeters two strings, returns a boolean. 

        Purpose: represents a player taking a turn in a game of Battleship. If 
        it is the player's turn and the game is still in progress, (if it is a direct hit) 
        removes a point from the other player's ship mapping  and plots a zero 
        on the player's grid. 
        '''
        if self._whose_turn != player or self._current_state != 'UNFINISHED':
            return False

        else:
            point = translate_coordinates(coordinates)

            # record the move

            other_player = self.get_other_player(player)
            player_obj = self._dict_of_players[other_player]

            for ship_obj in player_obj.get_fleet():
                if point in ship_obj.get_mapping():
                    # remove point
                    ship_obj.get_mapping().discard(point)
                    #update grid
                    player_obj.get_grid().plot_on_grid(point, 0)
                    # update fleet
                    player_obj.update_fleet()
                    # update current state
                    if len(player_obj.get_fleet()) == 0:
                        if other_player == 'first':
                            self._current_state = 'SECOND_WON'
                        elif other_player == 'second':
                            self._current_state = 'FIRST_WON'
            # update turn
            self._whose_turn = other_player
            return True

    def get_num_ships_remaining(self, player: str) -> int:
        '''
        Signature: takes as a parameter a string, returns an integer.

        Purpose: `get_num_ships_remaining` takes as an argument either "first" 
        or "second" and returns how many ships the specified player has left.
        '''
        player_obj = self.get_player(player)
        return sum([1 for ship_obj in player_obj.get_fleet()])


class Ship:
    '''
    Represents a ship in a game of Battleship.

    Includes various getter methods, as well as a method for initializing a 
    mapping of letter-number coordinates to positions on a Grid object.
    '''
    MIN_SHIP_LENGTH = 2

    def __init__(self, length, coordinates, orientation):
        '''
        Initializes a Ship object with the length, coordinates, and orientation of 
        the ship. Also initializes the ship's mapping to positions on a Grid object.
        '''
        self._length = length
        self._coordinates = coordinates
        self._orientation = orientation
        self._mapping = None
        self.init_mapping()

    def __repr__(self):
        '''
        Purpose: prints a ship object.
        '''
        return 'Ship(' + repr(self._length) + ', ' + repr(self._coordinates) + ', ' + repr(self._orientation) + ')'

    def get_length(self) -> int:
        '''
        Returns the length of the ship object (an integer).
        '''
        return self._length

    def get_coordinates(self) -> str:
        '''
        Returns the coordinates for the ship object (a string).
        '''
        return self._coordinates

    def get_orientation(self) -> str:
        '''
        Returns the orientation of the ship object (a string, either a 'C' or 'R'). 
        '''
        return self._orientation

    def get_mapping(self):
        '''
        Returns the _mapping data member (a set of tuples).
        '''
        return self._mapping

    def add_mapping(self, translated_coordinates: tuple):
        '''
        Purpose: adds a tuple representing a point on a Grid object to the 
        _mapping data member of the ship object.
        '''
        if self._mapping is None:
            self._mapping = {translated_coordinates}

        else:
            self._mapping.add(translated_coordinates)

    def init_mapping(self):
        '''
        Purpose: a method for initializing the _mapping data member to a set of 
        points based on the coordinates closest to A1. 
        '''
        row, col = translate_coordinates(self._coordinates)
        if self._orientation == 'R':
            for col_val in range(col, (col + self._length)):
                self.add_mapping((row, col_val))

        elif self._orientation == 'C':
            for row_val in range(row, (row + self._length)):
                self.add_mapping((row_val, col))
                

class Player:
    '''
    Represents a player in a game of battleship.

    Includes data members for a Grid object and a list of Ship objects (initialized
    to be an empty list). 

    Includes methods for adding a ship to the player's fleet, and getter methods
    for the grid and fleet data members. 
    '''
    def __init__(self):
        '''
        Initializes a Player object instance.
        A player fleet is a list of Ship objects.
        '''
        self._fleet = []
        self._grid = Grid()

    def add_ship(self, a_ship: Ship) -> bool:
        '''
        Signature: takes as a parameter a Ship object, returns a boolean.

        Purpose: adds a ship to the player's fleet.
        '''
        if self._valid_add(a_ship):
            self._grid.update_grid(a_ship)
            self._fleet.append(a_ship)
            return True

        else:
            return False

    def _valid_add(self, a_ship: Ship) -> bool:
        '''
        Signature: takes as a parameter a Ship object, returns a boolean.

        Purpose: private helper method for determining if it is a valid ship placement
        '''
        if a_ship.get_length() < Ship.MIN_SHIP_LENGTH:
            return False
        elif not self._grid.fits_grid(a_ship):
            return False
        elif self.overlaps(a_ship):
            return False
        else:
            return True

    def overlaps(self, a_ship: Ship):
        '''
        Signature: takes as a parameter a Ship object.

        Purpose: determines if a ship to be added overlaps with any other ship 
        object on the player's grid.
        '''
        for ship_obj in self._fleet:
            set_intersect_result = (a_ship.get_mapping() & ship_obj.get_mapping())
            if len(set_intersect_result) != 0:
                return True
        return False

    def update_fleet(self):
        '''
        Removes ship objects from the _fleet data member if the ship object's 
        _mapping data member is empty (i.e., if all points have been removed by
        torpedoes).
        '''
        for index, ship_obj in enumerate(self._fleet):
            if len(ship_obj.get_mapping()) == 0:
                del self._fleet[index]

    def get_fleet(self):
        '''
        Returns the _fleet data member for the Player instance. 
        '''
        return self._fleet

    def get_grid(self):
        '''
        Returns the _grid data member for the Player instance. 
        '''
        return self._grid


class Grid:
    '''
    Represents a player's grid in a game of Battleships.

    Includes data members for setting up the grid as a list of lists, initialized
    with all values set to 0. 

    Includes methods for plotting on the grid, printing the grid, and determining
    whether or not a ship fits on the grid.
    '''
    GAME_SIZE = 10
    def __init__(self):
        '''
        Initializes a Grid object. 
        The '_grid_map' attribute is made up of 0's (where no ships are) and 1's (where there is a ship).
        '''
        self._row_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

        self._row_label_dict = dict(zip(self._row_labels, [i for i in range(Grid.GAME_SIZE)]))

        self._col_labels = [i for i in range(1, 11)]

        self._grid_map = [[0 for x in range(Grid.GAME_SIZE)] for y in range(Grid.GAME_SIZE)] 

    def plot_on_grid(self, translated_coordinates: tuple, val: int):
        '''
        Signature: takes as parameters a tuple and an integer. 

        Purpose: plot point on grid from coordinates with the given value ('val'). 
        '''
        row, col = translated_coordinates
        self._grid_map[row][col] = val 

    def update_grid(self, a_ship: Ship):
        '''
        Signature: takes as a parameter a ship object.

        Purpose: plots all positions in the ship object's _mapping data member
        on the grid.
        '''
        for point in a_ship.get_mapping():
            self.plot_on_grid(point, 1)

    def get_grid(self):
        '''
        Returns an object representing the grid.
        '''
        return self._grid_map

    def print_grid(self):
        '''
        Prints the grid object.
        '''

        grid_str = ' '

        for label in self._col_labels:
            grid_str += (' ' + str(label))

        grid_str += '\n'

        for index, row in enumerate(self._grid_map):
            row_str = self._row_labels[index] + ' '
            for value in row:
                if value == 0:
                    row_str += '  '
                else:
                    row_str += 'x '
            row_str += '\n'
            grid_str += row_str

        print(grid_str)
        

    def fits_grid(self, a_ship: Ship) -> bool:
        '''
        Signature: takes as a parameter a Ship object, returns a boolean.

        Purpose: returns True if the ship object fits on the grid, False otherwise.
        '''
        for point in a_ship.get_mapping():
            row, col = point

            if row < 0:
                return False
            elif row > (Grid.GAME_SIZE - 1):
                return False
            elif col < 0:
                return False
            elif col > (Grid.GAME_SIZE - 1): 
                return False
        return True


## ===================================
## Function definitions:


def translate_coordinates(coordinates: str) -> tuple:
    '''
    Signature: takes as a parameter a string representing coordinates for 
    a ship object in a ShipGame, returns a tuple representing a point on a Grid
    object. 
    (coordinates are a letter from A-J followed by a number)

    Purpose: converts the given coordinates to a set of indices for a Grid object.
    '''
    row_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    row_label_dict = dict(zip(row_labels, [i for i in range(Grid.GAME_SIZE)]))

    letter = coordinates[0]
    number = int(coordinates[1:]) - 1
    return (row_label_dict.get(letter), number)

