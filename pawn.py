from piece import Piece

class Pawn(Piece):
    """Creates a pawn object, subclass of Piece, inherits from the Piece class"""
    
    def __init__(self, location, color):
        """Initializes Pawn class as a subclass of Piece"""
        super().__init__(location, color)
        self.value = 1
    
    def move(self, column, row):
        """moves the pawn to the desired space.
            args:
                column - string; the location of the row that the pawn is to be moved.
                row      - int; the row to move the pawn to.
            return:
                None
            raise:
                error - Value Error, if the piece cant move to that area."""
        if self.captured == True:
            raise ValueError("Not a valid move")
        elif row == 9 or "Z" > column > 'h':
            raise ValueError("out of bounds")
        
        if column == self.location[0]:
            if self.color == "white":
                if row - self.location[1] == 1:
                    self._move((column, row))
                else:
                    raise ValueError("Cant Move to that location")
            elif self.color == "black":
                if self.location[1] - row == 1:
                    self._move((column, row))
                else:
                    raise ValueError("Cant Move to that location")
        else: 
            raise ValueError("Cant move to that location")

    def attack_range(self, target):
        """Checks if the target piece is within range. Raises value error if trying to attack your own piece.
            args:
                target - Piece subclass Object
            return:
                bool - Indication whether the target can be attacked or not
            raise:
                error - ValueError """
        pawn_column, pawn_row = ord(self.location[0]), self.location[1]
        target_column, target_row = ord(target.location[0]), target.location[1]

        if self.color == target.color:
            raise ValueError("Can not attack your own piece.")

        if pawn_column - 1 == target_column or pawn_column + 1 == target_column:
            if self.color == "white" and target_row == pawn_row + 1:
                return True
            elif self.color == "black" and pawn_row == target_row + 1:
                return True
            else:
                return False
        else:
            return False
