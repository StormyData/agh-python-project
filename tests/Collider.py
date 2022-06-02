import unittest
from src.Physics import Collider
from src.Vector import Vector, get_sized_box


class ColliderTestCase(unittest.TestCase):
    def test_collides(self):
        a = Collider([Vector(0, 0) + v for v in get_sized_box(Vector(5, 5))])
        b = Collider([Vector(3, 3) + v for v in get_sized_box(Vector(1, 1))])
        self.assertTrue(a.collides(b), f"Colliders {a} and {b} did not collide")
        self.assertTrue(b.collides(a), f"Colliders {b} and {a} did not collide")

        c = Collider([Vector(6, 6) + v for v in get_sized_box(Vector(1, 1))])
        self.assertFalse(a.collides(c), f"Colliders {a} and {c} did collide")
        self.assertFalse(c.collides(a), f"Colliders {c} and {a} did collide")
        self.assertFalse(b.collides(c), f"Colliders {b} and {c} did collide")
        self.assertFalse(c.collides(b), f"Colliders {c} and {b} did collide")

    def test_collide_offset(self):
        a = Collider([Vector(0, 0) + v for v in get_sized_box(Vector(5, 5))])
        b = Collider([Vector(3, 3) + v for v in get_sized_box(Vector(1, 1))])
        expected1 = Vector(0, -2)
        expected2 = Vector(0, 2)
        self.assertEqual(expected1, a.collide_offset(b), f"incorrect offset for {a} and {b}")
        self.assertEqual(expected2, b.collide_offset(a), f"incorrect offset for {b} and {a}")

        c = Collider([Vector(6, 6) + v for v in get_sized_box(Vector(1, 1))])
        expected3 = Vector(0, 0)
        self.assertEqual(expected3, a.collide_offset(c), f"incorrect offset for {a} and {c}")
        self.assertEqual(expected3, c.collide_offset(a), f"incorrect offset for {c} and {a}")
        self.assertEqual(expected3, b.collide_offset(c), f"incorrect offset for {b} and {c}")
        self.assertEqual(expected3, c.collide_offset(b), f"incorrect offset for {c} and {b}")

    def test_collider_move(self):
        a = Collider([Vector(0, 0) + v for v in get_sized_box(Vector(5, 5))])
        b = Collider([Vector(3, 3) + v for v in get_sized_box(Vector(1, 1))])
        c = Collider([Vector(6, 6) + v for v in get_sized_box(Vector(1, 1))])
        c.move_by(Vector(-1.5, -1.5))
        self.assertTrue(a.collides(c), f"Colliders {a} and {c} did not collide")
        self.assertTrue(c.collides(a), f"Colliders {c} and {a} did not collide")
        self.assertFalse(b.collides(c), f"Colliders {b} and {c} did collide")
        self.assertFalse(c.collides(b), f"Colliders {c} and {b} did collide")
        expected3 = Vector(0, 0)
        expected4 = Vector(0, 0.5)
        self.assertEqual(-expected4, a.collide_offset(c), f"incorrect offset for {a} and {c}")
        self.assertEqual(expected4, c.collide_offset(a), f"incorrect offset for {c} and {a}")
        self.assertEqual(expected3, b.collide_offset(c), f"incorrect offset for {b} and {c}")
        self.assertEqual(expected3, c.collide_offset(b), f"incorrect offset for {c} and {b}")

    def test_collider_slanted(self):
        a = Collider([Vector(0, 0), Vector(4, 0), Vector(4, 4), Vector(0, 2)])
        b = Collider([Vector(0, 3) + v for v in get_sized_box(Vector(3, 1))])
        expected = Vector(-0.2, 0.4)
        calculated = b.collide_offset(a)
        self.assertAlmostEqual(expected.x, calculated.x, msg=f"expected={expected}, calculated={calculated}")
        self.assertAlmostEqual(expected.y, calculated.y, msg=f"expected={expected}, calculated={calculated}")

        a = Collider(list(reversed([Vector(0, 0), Vector(4, 0), Vector(4, 4), Vector(0, 2)])))
        calculated = b.collide_offset(a)
        self.assertAlmostEqual(expected.x, calculated.x, msg=f"expected={expected}, calculated={calculated}")
        self.assertAlmostEqual(expected.y, calculated.y, msg=f"expected={expected}, calculated={calculated}")


if __name__ == '__main__':
    unittest.main()
