from pawn import Pawn
import string
import pprint
from os import system, name
from time import sleep

class Board(dict):
    """Creates an empty chess board object"""
    def __init__(self):
        """Initializes board class with general attributes."""
        # uses strings.ascii_lowercase to copy the first 8 letters of the alphabet, used for notation.
        self.columns = [char for char in string.ascii_lowercase[:8]]

        # instantiates two teams, white and black
        self.white = Team("white")
        self.black = Team("black")

        # used to determine wether or not the game should continue.
        self.should_continue = True

        # for every column, create an array of empty strings. this is used to store the location of the pieces
        for char in self.columns:
            self[char] = ["" for i in range(8)]

        # sets the board with the pieces
        self.set_board()

    def set_board(self):
        """Initially sets the chess board with the pieces in the appropriate area.
            args:
                None
            return:
                None"""
        pieces = self.white.create()
        pieces.extend(self.black.create())

        for piece in pieces:
            key = piece.location[0]
            i = piece.location[1] - 1
            self[key][i] = piece

    def show_board(self):
        """Displays the board in a very basic format.
            args:
                None
            return:
                None"""
        # use the ordinal ascii code to increment or decrement the alphabet letter.
        column = ord("a")
        
        # iterate 8 times and display the board with appropriate terms to define the pieces.
        for i in range(8):
            # create an array of 8 _ characters
            row = ["_"]*8

            # iterate through every column and update the row with the appropriate piece.
            # reverses the ascii code back into the appropriate character
            for j, item in enumerate(self[chr(column + i)]):

                # initially used a dunder method to display the string of the pawn, but was encountering errors. 
                # for time sake I used this quick hack.
                # checks to see if the item is not an empty string,
                # if it isn't then set item to equal either wp for White pawn or bp for Black Pawn
                if item != "":
                    if item.color == "white":
                        item = "wp"
                    elif item.color == "black":
                        item = "bp"
                    row[j] = str(item)

            # print out each rown individually
            print(chr(column + i),": ", " ".join(row))

    def make_move(self, piece, column, row):
        """Moves the desired piece to the desired location, if possible.
            args:
                piece - Pawn object; the piece that you want to move
                column - string; the column you would like to move the piece to
                row- int; the row that you would like to move the piece to.
            return:
                bool; True if the piece captured another piece on this move."""
        spot = self[column][row - 1]

        # checks to see if the spot is occupied, if it is attempt to attack
        # if it is not, move to that location
        if spot != "":
            self[piece.location[0]][piece.location[1] - 1] = ''
            piece.attack(spot)
            self[piece.location[0]][piece.location[1] - 1] = piece
            return True
        else:
            self[piece.location[0]][piece.location[1] - 1] = ''
            piece.move(column, row)
            self[piece.location[0]][piece.location[1] - 1] = piece
            return False

    def get_pawn(self, current):
        """Gets the pawn at the desired location.
            args:
                current - string; the current color of the pawn to be returned
            return
                pawn - Pawn; the pawn that is to be moved."""
        # uses custom input handler to handle bad input.
        piece = input_handler("What Piece would you like to move? (i.e e2) ")

        # gets the column and row of the pawn from the input
        column, row = piece[0], int(piece[1]) - 1

        # gets the item at that location
        pawn = self[column][row]

        # checks to see if the pawn is a valid piece or an empty space. 
        # also checks to see if the pawn was just moved after a capture
        if pawn == "":
            print("There is no pawn in that spot! Try again...")
            return self.get_pawn(current)
        elif pawn.color != current:
            print("You have to move your own piece! Try again...")
            return self.get_pawn(current)
        elif pawn.just_moved == True:
            print("You just moved that pawn, choose a different piece...")
            return self.get_pawn(current)
        
        return pawn
    
    def get_location_and_move(self, pawn):
        """Gets the location of the pawn and then moves it to the desired location
            args:
                pawn - Pawn Object; the pawn to be moved
            return:
                capture - bool; wether or not the pawn made a capture on its previous move."""
        location = input_handler("Where would you like to move? (i.e. e3) ")
        column, row = location[0], int(location[1])

        if row > 8 or row < 1:
            print("sorry you can't move there, try again... ")
            self.get_location_and_move(pawn)

        try:
            capture = self.make_move(pawn, column, row)
            if pawn.color == "white" and pawn.location[1] == 8:
                self.should_continue = False
            elif pawn.color == "black" and pawn.location[1] == 1:
                self.should_continue = False
            return capture
        except ValueError:
            print("sorry you can't move there, try again...")
            self.get_location_and_move(pawn)

    def run(self):
        """Runs the EverChess game until a pawn reaches the end."""
        previous = "black"
        current = "white"

        previous_pawn = None
        self.set_board()

        print("Welcome! Lets play a game of EverChess ")
        print("White starts, input your move using chess notation.")

        while self.should_continue:
            if previous_pawn != None:
                previous_pawn.just_moved = False
            self.show_board()
            print(f"{current}'s turn!")

            pawn = self.get_pawn(current)
            previous_pawn = pawn
            capture = self.get_location_and_move(pawn)

            if capture == True:
                print(f"{current} captured {previous}'s pawn!'")
                if current == "white":
                    self.white.points += 1
                else:
                    self.black.points += 1
                sleep(1)

            else:
                current, previous = previous, current
            clear()

        self.show_board()
        print(f"{previous} wins!! Congratulations. Better luck next time {current}! ")

class Team:
    """Team class to create a team of pieces, used to track points."""
    def __init__(self, color):
        """Initializes general team attributes
            args:
                color - string; the color that will be assigned to the team"""
        self.color = color
        self.size = 8
        self.points = 0
        self.pieces = []

    def create(self):
        """Creates the team based off the size.
            Time Complexity:
                O(1) - it only creates a team based off of the size, and the size is always 8. 
                          only ever iterates a constant 8 amount of times.
            Space Complexity:
                O(1) - Only creates a list of 8 items, this is always constant and doesnt change.
            args:
                None
            return:
                self.pieces - dynamic array; an array of all the pieces on the team."""
        column = ord("a")

        if self.color == "black":
            pawn_row = 7
        else:
            pawn_row = 2

        for i in range(self.size):
            location = (chr(column + i), pawn_row)
            pawn = Pawn(location, self.color )
            self.pieces.append(pawn)

        return self.pieces
            
def clear():
    """Function to clear the terminal after each move. 
        Checks the type of system and runs the appropriate command, then sleeps for .01 seconds.
        Sleeps so that the terminal has time to clear before more input is added.
        args:
            None
        return:
            None"""
    if name == "nt":
        system("cls")
    else:
        system("clear")

    sleep(.01)

def input_handler(prompt):
    """Function to recursively handle user input for chess notation.
        Handles base cases and exceptions.
        args:
            prompt - string; what you want to say to the user.
        return:
            user_input - string; the valid users response"""
    user_input = input(prompt)

    if user_input == '':
        print('you must provide some information!')
        return input_handler(prompt)
    elif len(user_input) == 1 or len(user_input) >= 3 or user_input[0] > "h":
        print("Invalid input, Try again... ")
        return input_handler(prompt)

    try: 
        int(user_input[1])
        if int(user_input[1]) > 8 or int(user_input[1]) == 0:
            print("Invalid input, Try again... ")
            return input_handler(prompt)
    except ValueError:
        print("Invalid input, Try again... ")
        return input_handler(prompt)

    return user_input

if __name__ == "__main__":
    board = Board()
    
    board.run()

