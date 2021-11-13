import unittest
from .helpers import create_test_flight, create_test_passenger, fill_test_flight


class TestFlightSeatingPlan(unittest.TestCase):
    def setUp(self) -> None:
        self._flight = create_test_flight()
        self._passenger = create_test_passenger()

    def test_flight_with_no_plan_has_0_capacity(self):
        self.assertIsNone(self._flight.seating_plan)
        self.assertEqual(0, self._flight.capacity)

    def test_can_load_seating_plan(self):
        self._flight.load_seating("A321", "neo")
        self.assertIsNotNone(self._flight.seating_plan)
        self.assertEqual(235, self._flight.capacity)
        self.assertEqual(235, self._flight.available_capacity)

    def test_can_get_seating_plan(self):
        self._flight.load_seating("A321", "neo")
        self.assertIsNotNone(self._flight.seating_plan)
        self.assertEqual(235, self._flight.capacity)
        self.assertEqual(235, self._flight.available_capacity)

    def test_can_allocate_seat(self):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)
        pid = self._passenger["id"]
        self.assertIsNone(self._flight.get_allocated_seat(pid))

        self._flight.allocate_seat("5D", pid)
        self.assertEqual("5D", self._flight.get_allocated_seat(pid))
        self.assertEqual(234, self._flight.available_capacity)

    def test_can_allocate_next_seat(self):
        self._flight.load_seating("A321", "neo")
        expected = ["1A", "1B", "1C", "2A", "2B"]
        for i in range(5):
            passenger = create_test_passenger()
            self._flight.add_passenger(passenger)
            self._flight.allocate_next_empty_seat(passenger["id"])
            self.assertEqual(expected[i], self._flight.get_allocated_seat(passenger["id"]))
        self.assertEqual(230, self._flight.available_capacity)

    def test_can_fill_the_flight(self):
        self._flight.load_seating("A321", "neo")
        fill_test_flight(self._flight)
        self.assertEqual(self._flight.capacity, len(self._flight.passengers))
        self.assertEqual(0, self._flight.available_capacity)

    def test_cannot_add_passenger_to_a_full_flight(self):
        self._flight.load_seating("A321", "neo")
        fill_test_flight(self._flight)
        with self.assertRaises(ValueError):
            passenger = create_test_passenger()
            self._flight.add_passenger(passenger)

    def test_cannot_allocate_seat_to_missing_passenger(self):
        with self.assertRaises(ValueError):
            self._flight.allocate_seat("1A", "not_on_the_flight")

    def test_can_move_passenger(self):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)

        pid = self._passenger["id"]
        self._flight.allocate_seat("5D", pid)
        self.assertEqual("5D", self._flight.get_allocated_seat(pid))

        pid = self._passenger["id"]
        self._flight.allocate_seat("7F", pid)
        self.assertEqual("7F", self._flight.get_allocated_seat(pid))

    def test_can_reload_seating_plan(self):
        self._flight.load_seating("A321", "neo")
        self._flight.add_passenger(self._passenger)

        pid = self._passenger["id"]
        self._flight.allocate_seat("5D", pid)

        self._flight.load_seating("A320", "1")
        self.assertEqual("5D", self._flight.get_allocated_seat(pid))
        self.assertEqual(185, self._flight.available_capacity)

    def test_can_reload_seating_plan_with_no_allocations(self):
        self._flight.load_seating("A320", "1")
        self.assertEqual(186, self._flight.capacity)
        self.assertEqual(186, self._flight.available_capacity)

        self._flight.load_seating("A321", "neo")
        self.assertEqual(235, self._flight.capacity)
        self.assertEqual(235, self._flight.available_capacity)

    def test_cannot_load_plan_with_insufficient_seats(self):
        self._flight.load_seating("A321", "neo")
        fill_test_flight(self._flight)
        self.assertEqual(0, self._flight.available_capacity)
        with self.assertRaises(ValueError):
            self._flight.load_seating("A320", "1")
