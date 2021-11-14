from unittest import TestCase
from src.flight_booking.seating_plan import *


class TestSeatingPlan(TestCase):
    def setUp(self) -> None:
        self._a320 = read_plan("EasyJet", "A320", "1")
        self._a321 = read_plan("EasyJet", "A321", "neo")

    def test_read_plan(self):
        self.assertIsNotNone(self._a321)
        self.assertEqual(len(get_unallocated_seats(self._a321)), 235)

    def test_get_seating_row(self):
        row = get_seating_row(self._a320, "1A")
        self.assertIsNotNone(row)
        for letter in "ABCDEF":
            self.assertTrue(f"1{letter}" in row["seats"].keys())

    def test_get_invalid_seating_row(self):
        with self.assertRaises(ValueError):
            get_seating_row(self._a320, "100A")

    def test_get_allocated_seat(self):
        allocate_seat(self._a320, "5D", "id")
        self.assertEqual("5D", get_allocated_seat(self._a320, "id"))

    def test_allocated_seat_is_none_if_not_allocated(self):
        self.assertIsNone(get_allocated_seat(self._a320, "id"))

    def test_allocate_seat(self):
        self.assertIsNone(get_allocated_seat(self._a320, "id"))
        allocate_seat(self._a320, "5D", "id")
        self.assertEqual("5D", get_allocated_seat(self._a320, "id"))

    def test_allocate_seat_with_no_plan(self):
        with self.assertRaises(ValueError):
            allocate_seat(None, "5D", "id")

    def test_allocate_occupied_seat(self):
        with self.assertRaises(ValueError):
            allocate_seat(self._a320, "5D", "id")
            allocate_seat(self._a320, "5D", "other_id")

    def test_allocate_occupied_seat_to_occupant(self):
        allocate_seat(self._a320, "5D", "id")
        allocate_seat(self._a320, "5D", "id")
        self.assertEqual("5D", get_allocated_seat(self._a320, "id"))

    def test_get_unallocated_seats(self):
        self.assertEqual(len(get_unallocated_seats(self._a320)), 186)
        allocate_seat(self._a320, "5D", "id")
        unallocated = get_unallocated_seats(self._a320)
        self.assertEqual(185, len(unallocated))
        self.assertTrue("5D" not in unallocated)

    def test_copy_seat_allocations(self):
        # 28A exists in the A320 but not the A321neo so when we migrate the new seat
        # allocation should be 1A
        allocate_seat(self._a320, "28A", "id")
        self.assertEqual("28A", get_allocated_seat(self._a320, "id"))
        copy_seat_allocations(self._a320, self._a321)
        self.assertEqual("1A", get_allocated_seat(self._a321, "id"))

    def test_get_passengers_with_no_seat(self):
        allocate_seat(self._a320, "1A", "id-1")
        ids_with_no_allocation = get_passengers_with_no_seat(self._a320, {"id-1", "id-2"})
        self.assertEqual(1, len(ids_with_no_allocation))
        self.assertTrue("id-2" in ids_with_no_allocation)

    def test_can_clear_allocation(self):
        allocate_seat(self._a320, "1A", "id-1")
        clear_allocation(self._a320, "1A")
        self.assertIsNone(get_allocated_seat(self._a320, "id"))
