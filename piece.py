from abc import abstractmethod

class Piece():
    """an Abstract class to be used to define the general attributes of a chess piece."""
    def __init__(self, location, color):
        """Initializes generic chess piece attributes. 
            args:
                location - tuple; the initial location of the piece
                color - string; the color of the piece"""
        self.color = color
        self.has_moved = False
        self.just_moved = False
        self.board = None
        self.location = location
        self.captured = False
        self.value = 0

    def _move(self, loc):
        """Helper function to move the piece to the given location
            args: 
                loc - tuple; the location of where to move the piece"""
        self.has_moved = True
        self.location = loc

    def attack(self, target):
        """Captures the Piece, if any, in the location 1 row and 1 column away from the pawn. 
            args: 
                target - Piece, or subclass of Piece
            return:
                None
            Raise:
                ValueError - if not within range"""
        if self.attack_range(target):
            target.captured = True
            self._move(target.location)
            target.location = None
        else:
            raise ValueError("Target not within range")

        @abstractmethod
        def attack_range(self, target):
            pass
