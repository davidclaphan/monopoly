# Author: David Claphan
# GitHub username: davidclaphan
# Date: 05/16/2022
# Description: This program is a simplified version of Monopoly, the Portfolio Project for CS162 - Introduction
#              to Computer Science II at Oregon State University. Instead of the classic properties you would find
#              in Monopoly, the properties in this program are all based on locations or landmarks in Chicago, IL.


class RealEstateGame:
    """
    Represents a board game, a simplified version of Monopoly. This class contains many of the methods that result
    in actions taken in the game (move/purchase space/etc.). It also has 'create' methods for the other classes to
    set up the board (Spaces) and Players at the beginning of the game.
    """

    def __init__(self):
        """
        Initializes data structures required for the game to work, such as lists to organize and hold Player and
        Space objects when they are created.
        """
        self._player_names = set()
        self._players = []
        self._game_board = []
        self._go_value = 0

    def create_spaces(self, go_value, rent_list):
        """
        Creates the spaces for the game board, taking as parameters the amount paid to a player for passing
        the "GO" space, and a list of rent values for the other 24 spaces on the board.
        """
        self._go_value = go_value

        space_counter = 1
        spaces = ["GO", "Falafel & Grill", "The Wormhole Coffee", "Revolution Brewing", "Pita Inn", "Ghareeb Nawaz",
                  "Small Cheval", "St. Lou's Assembly", "Clark St", "Wrigley Field", "Wicker Park Ave",
                  "United Center", "Northerly Island", "Lincoln Park", "River Shannon", "Lou Malnati's Pizzeria",
                  "Portillo's", "Chicago Ave", "Half Acre Beer Company", "Garfield Park Conservatory", "Metropolis",
                  "Division St", "The Loop", "Andy's Thai Kitchen", "Pompei Restaurant"]

        for rents in rent_list:
            # First, create the "GO" space
            if len(self._game_board) == 0:
                go_space = Space(spaces[0], 0)
                self._game_board.append(go_space)

            # After "GO" space created, create other spaces, 25 total (including "GO")
            if len(self._game_board) > 0:
                space = Space(spaces[space_counter], rents)
                self._game_board.append(space)
                space_counter += 1

    def create_player(self, name, starting_balance):
        """Creates a Player object for the game."""
        for names in self._player_names:
            if name.lower() == names.lower():
                raise PlayerNameError  # name entered should be unique from existing names

        player_object = Player(name, starting_balance)
        self._players.append(player_object)
        self._player_names.add(name)

    def get_player_account_balance(self, player_name):
        """Take a player name as a parameter and returns their account balance."""
        for player in self._players:
            if player.get_player_name() == player_name:
                return player.get_balance()

    def get_player_current_position(self, player_name):
        """
        Takes a player name as a parameter and returns their current position on the board. Position is
        returned as an integer, the "GO" space is value 0.
        """
        for player in self._players:
            if player_name == player.get_player_name():
                return player.get_position()

    def buy_space(self, player_name):
        """
        Updates the provided player as the owner of a space, given that specific criteria are met, such as the space
        not already having an owner and the player having enough money to purchase the space. Returns True if the
        purchase is successful, False if it is not.
        """
        for players in self._players:
            if player_name == players.get_player_name():  # identify player
                if players.get_balance() == 0:  # if player out of game, nothing happens
                    return False
                if players.get_position() == 0:  # if player is at "GO" space, nothing happens
                    return False
                # if player has a high enough balance and the space is not owned, player can buy space,
                # purchase price is deducted from their existing balance
                if players.get_balance() > self.get_board()[players.get_position()].get_purchase_price() and \
                        self.get_board()[players.get_position()].get_owner() is None:
                    self.get_board()[players.get_position()].set_owner(player_name)
                    players.set_balance(self.get_board()[players.get_position()].get_purchase_price() * -1)
                    return True
                return False
        return False

    def move_player(self, player_name, moves):
        """
        Moves the player forward on the game board equal to the number of spaces provided as the parameter (moves). This
        method calls multiple smaller methods for each action that occurs during a player move. If a player is out of
        the game, this method does nothing.
        """
        for players in self._players:
            if player_name == players.get_player_name():  # identify player
                if players.get_balance() == 0:  # if player out of game, nothing happens
                    return
                if players.get_position() + moves > 24:
                    players.set_balance(self.get_go_value())  # if a player passes "GO"

                players.set_position(moves)  # move the player

                # check if the space the player landed on is owned, if yes call pay_rent method
                if self._game_board[players.get_position()].get_owner() is not None and self._game_board[
                        players.get_position()] != 0:
                    self.pay_rent(player_name)  # call pay_rent

                    # include check for player newly out of game here
                    if players.get_balance() == 0:
                        for spaces in self._game_board:
                            if player_name == spaces.get_owner():
                                spaces.set_owner(None)  # reset previously owned spaces to None

                    return self.check_game_over()  # check's if the game is over after the player's turn is over
                return
        return

    def get_go_value(self):
        """
        Returns the amount associated with passing or landing on the "GO" space for the game. Used in the
        "move_player" method of RealEstateGame.
        """
        return self._go_value

    def pay_rent(self, player_name):
        """
        Called from move_player, if the space that the player moves to is owned, that moving player will have the
        amount of rent associated with that space deducted from their balance and given to the space owner. If the rent
        is greater than their account balance, their entire balance will be deducted and given to the space owner, and
        the moving player will be out of the game. This method also removes players from spaces they own if their
        balance is 0.
        """
        for players in self._players:
            if player_name == players.get_player_name():  # will look for player name
                if player_name == self._game_board[players.get_position()].get_owner():
                    return
                else:
                    if players.get_balance() >= self._game_board[players.get_position()].get_rent():
                        rent = self._game_board[players.get_position()].get_rent()  # assign rent value to variable
                        players.set_balance(rent * (-1))  # deduct from player landing on space
                        for owner in self._players:  # add to space owner
                            if owner.get_player_name() == self._game_board[players.get_position()].get_owner():
                                owner.set_balance(rent)

                    elif players.get_balance() < self._game_board[players.get_position()].get_rent():
                        rent = players.get_balance()
                        players.set_balance(rent * (-1))  # deduct remaining balance from player landing on space
                        for owner in self._players:  # add to space owner
                            if owner.get_player_name() == self._game_board[players.get_position()].get_owner():
                                owner.set_balance(rent)
                    return

    def check_game_over(self):
        """
        Check the account balances of all players. Once only one player has a balance >0, the game is over and
        this method will return the winner's name.
        """
        zero_balance_counter = 0
        for players in self._players:
            if players.get_balance() > 0:
                zero_balance_counter += 1

        if zero_balance_counter == 1:
            for players in self._players:
                if players.get_balance() > 0:
                    return players.get_player_name()  # return winners name, after term add print statement
        else:
            return ""  # return blank space if no winner yet

    def get_player_properties(self, player_name):
        """Returns the names of all properties owned by the player."""
        player_spaces = []
        for spaces in self.get_board():
            if spaces.get_owner() == player_name:
                player_spaces.append(spaces.get_name())  # check if player is space owner, if yes add to list

        return player_spaces

    def get_players(self):
        """Returns the list of Player objects in the RealEstateGame object. Used primarily for testing."""
        return self._players

    def get_player_names(self):
        """
        Returns the set of names for Player objects that have been created for the RealEstateGame object. Used
        primarily for testing.
        """
        return self._player_names

    def get_board(self):
        """
        Returns the list of Space objects that have been created for the RealEstateGame object. Used primarily for
        testing.
        """
        return self._game_board

    def get_space_owner(self, space):
        """Returns the owner of a specific space on the game board."""
        return self._game_board[space].get_owner()


class PlayerNameError(Exception):
    pass


# Will cause an issue with grader in course, implement this after course is over.
class CannotPurchaseGoSpace(Exception):
    pass


class Space:
    """
    Represents one of the spaces/properties that exists on the board. A space should be created using the
    create_spaces method in the RealEstateGame class and will have data members for space name, rent, purchase price,
    and owner (from Player object).
    """

    def __init__(self, name, rent):
        """Initializes a space on the game board taking name and rent amount as parameters."""
        self._space_name = name
        self._rent = rent
        self._purchase_price = rent * 5
        self._owner = None

    def get_rent(self):
        """Returns the amount of rent that a player will pay if they land on this space and another player owns it."""
        return self._rent

    def get_owner(self):
        """Returns the name of the player that currently owns the space. If nobody owns it, it is FOR SALE!"""
        return self._owner

    def get_purchase_price(self):
        """Returns the amount it costs to purchase this space when it is not owned by another player."""
        return self._purchase_price

    def get_name(self):
        """Returns the name of the space."""
        return self._space_name

    def set_owner(self, player_name):
        """
        Updates the owner of a space. Used with the buy_space method and when a player is out of the game and
        can no longer be a space owner.
        """
        self._owner = player_name


class Player:
    """
    Represents a player in the RealEstateGame. Players have a name, account balance, and position on the board. They
    are created using the create_player method in the RealEstateGame class. Players will move around the board and
    depending on the result of their moves they may add to or deduct from their account balance. They may also
    be owners of Spaces on the game board.
    """

    def __init__(self, name, account_balance):
        """Initializes a player at the "GO" space with a name and starting account balance."""
        self._name = name
        self._account_balance = account_balance
        self._current_position = 0

    def get_player_name(self):
        """Returns a player's name."""
        return self._name

    def get_balance(self):
        """Returns a player's current account balance."""
        return self._account_balance

    def get_position(self):
        """Returns a players current position on the game board."""
        return self._current_position

    def set_balance(self, amount):
        """
        Used to update the account balance of a player. Can be used to increase if receiving rent or passing the
        "GO" space or to decrease if paying rent or buying a Space on the game board.
        """
        self._account_balance += amount

    def set_position(self, moves):
        """
        Used to move a player around the game board. Called as part of the move_player method in the RealEstateGame
        class. The position after the 25th space is back to the first space (position 0) which is the "GO" space.
        """
        if (self._current_position + moves) > 24:  # check if player has gone past the last space on the board
            self._current_position = (self._current_position + moves) - 25
        else:
            self._current_position += moves
