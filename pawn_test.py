from pawn import Pawn
import unittest

class PawnTest(unittest.TestCase):
    def test_pawn_init(self):
        loc = ("a", 1)
        pawn = Pawn(loc, "white")
        assert pawn.location == ("a", 1)
        assert pawn.has_moved == False
        assert pawn.board == None
        assert pawn.value == 1

    def test_pawn_move(self):
        loc = ("a", 1)
        pawn = Pawn(loc, "white")
        assert pawn.location == ("a", 1)
        assert pawn.has_moved == False
        pawn.move("a", 2)
        assert pawn.location == ("a", 2)
        assert pawn.has_moved == True
        with self.assertRaises(ValueError):
            pawn.move("Z", 2)

    def test_attack_range(self):
        pawn1 = Pawn(("a", 2), "white")
        pawn2 = Pawn(("b", 3), "black")
        pawn3 = Pawn(("d", 5), "white")

        assert pawn1.attack_range(pawn2) == True
        assert pawn2.attack_range(pawn1) == True
        with self.assertRaises(ValueError):
            pawn1.attack_range(pawn3)

    def test_attack(self):
        pawn1 = Pawn(("b", 2), "white")
        pawn2 = Pawn(("c", 3), "black")
        pawn3 = Pawn(("a", 3), "white")
        
        assert pawn1.attack(pawn2) == None
        assert pawn1.location == ("c", 3)
        assert pawn2.location == None
        assert pawn2.captured == True
        assert pawn1.captured == False
        with self.assertRaises(ValueError):
            pawn1.attack(pawn3)