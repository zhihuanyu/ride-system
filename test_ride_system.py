import unittest
from main import Rider, Driver, Ride, RideManager, Status, Ratings

class TestRideSystem(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.rider = Rider("Alice", "r1")
        self.driver = Driver("Bob", "d1", "Toyota")
        self.ride_manager = RideManager()
        self.ride_manager.add_driver(self.driver)

    def test_ride_creation(self):
        """Test that a ride can be created and added to ride manager."""
        ride = self.rider.request_ride("123 Main St", self.ride_manager)
        self.assertEqual(ride.rider, self.rider)
        self.assertEqual(ride.destination, "123 Main St")
        self.assertEqual(ride.status, Status.PENDING)
        self.assertIsNone(ride.driver)
        self.assertIn(ride, self.ride_manager.rides)

    def test_ride_acceptance(self):
        """Test that a driver can accept a ride."""
        ride = self.rider.request_ride("123 Main St", self.ride_manager)
        self.driver.accept_ride(ride)
        self.assertEqual(ride.driver, self.driver)
        self.assertEqual(ride.status, Status.ACCEPTED)

    def test_ride_completion(self):
        """Test that a ride can be marked as completed."""
        ride = self.rider.request_ride("123 Main St", self.ride_manager)
        self.driver.accept_ride(ride)
        ride.mark_as_completed()
        self.assertEqual(ride.status, Status.COMPLETED)

    def test_ride_rating(self):
        """Test that a rider can rate a completed ride."""
        ride = self.rider.request_ride("123 Main St", self.ride_manager)
        self.driver.accept_ride(ride)
        ride.mark_as_completed()
        self.rider.rate_ride(ride, 5)
        self.assertEqual(len(self.driver.ratings), 1)
        self.assertEqual(self.driver.ratings[0].rating, 5)
        self.assertEqual(self.driver.ratings[0].receiver, self.driver)
        self.assertEqual(self.driver.ratings[0].giver, self.rider)

    def test_cannot_rate_incomplete_ride(self):
        """Test that a ride cannot be rated before completion."""
        ride = self.rider.request_ride("123 Main St", self.ride_manager)
        self.driver.accept_ride(ride)
        with self.assertRaises(Exception) as context:
            self.rider.rate_ride(ride, 5)
        self.assertTrue("Can not rate when it is not completed" in str(context.exception))

    def test_cannot_accept_taken_ride(self):
        """Test that a ride cannot be accepted by multiple drivers."""
        ride = self.rider.request_ride("123 Main St", self.ride_manager)
        self.driver.accept_ride(ride)
        another_driver = Driver("Charlie", "d2", "Honda")
        with self.assertRaises(Exception) as context:
            another_driver.accept_ride(ride)
        self.assertTrue("Ride already accepted by another driver" in str(context.exception))

    def test_cannot_rate_wrong_rider(self):
        """Test that only the actual rider can rate the ride."""
        ride = self.rider.request_ride("123 Main St", self.ride_manager)
        self.driver.accept_ride(ride)
        ride.mark_as_completed()
        another_rider = Rider("Charlie", "r2")
        with self.assertRaises(Exception) as context:
            another_rider.rate_ride(ride, 5)
        self.assertTrue("Can not rate driver when you are not the rider" in str(context.exception))

    def test_ride_manager_deletion(self):
        """Test that completed rides can be deleted from ride manager."""
        ride = self.rider.request_ride("123 Main St", self.ride_manager)
        self.driver.accept_ride(ride)
        ride.mark_as_completed()
        self.ride_manager.delete_ride(ride)
        self.assertNotIn(ride, self.ride_manager.rides)

    def test_cannot_delete_incomplete_ride(self):
        """Test that incomplete rides cannot be deleted."""
        ride = self.rider.request_ride("123 Main St", self.ride_manager)
        self.driver.accept_ride(ride)
        with self.assertRaises(Exception) as context:
            self.ride_manager.delete_ride(ride)
        self.assertTrue("Can not delete ride before it is completed" in str(context.exception))

if __name__ == '__main__':
    unittest.main() 