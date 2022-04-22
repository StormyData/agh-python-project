import unittest
from src.Physics import Collider
from src.Vector import Vector

class ColliderTestCase(unittest.TestCase):
    def test_collides(self):
        a = Collider(Vector(0, 0), Vector(5, 5))
        b = Collider(Vector(3, 3), Vector(1, 1))
        self.assertTrue(a.collides(b), f"Colliders {a} and {b} did not collide")
        self.assertTrue(b.collides(a), f"Colliders {b} and {a} did not collide")

        c = Collider(Vector(5, 5), Vector(1, 1))
        self.assertFalse(a.collides(c), f"Colliders {a} and {c} did collide")
        self.assertFalse(c.collides(a), f"Colliders {c} and {a} did collide")
        self.assertFalse(b.collides(c), f"Colliders {b} and {c} did collide")
        self.assertFalse(c.collides(b), f"Colliders {c} and {b} did collide")

    def test_collide_offset(self):
        a = Collider(Vector(0, 0), Vector(5, 5))
        b = Collider(Vector(3, 3), Vector(1, 1))
        expected1 = Vector(0, -2)
        expected2 = Vector(0, 2)
        self.assertEqual(expected1, a.collide_offset(b), f"incorrect offset for {a} and {b}")
        self.assertEqual(expected2, b.collide_offset(a), f"incorrect offset for {b} and {a}")

        c = Collider(Vector(5, 5), Vector(1, 1))
        expected3 = Vector(0, 0)
        self.assertEqual(expected3, a.collide_offset(c), f"incorrect offset for {a} and {c}")
        self.assertEqual(expected3, c.collide_offset(a), f"incorrect offset for {c} and {a}")
        self.assertEqual(expected3, b.collide_offset(c), f"incorrect offset for {b} and {c}")
        self.assertEqual(expected3, c.collide_offset(b), f"incorrect offset for {c} and {b}")


if __name__ == '__main__':
    unittest.main()
