"""A ride-sharing system implementation with rating functionality."""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional

class RideError(Exception):
    """Base exception for ride-related errors."""

class RideAlreadyAcceptedError(RideError):
    """Raised when trying to accept a ride that's already accepted."""

class RideNotCompletedError(RideError):
    """Raised when trying to rate a ride that's not completed."""

class InvalidRaterError(RideError):
    """Raised when someone tries to rate who shouldn't."""

class Status(Enum):
    """Represents the possible states of a ride."""
    PENDING = auto()
    ACCEPTED = auto()
    COMPLETED = auto()

@dataclass
class Ratings:
    """Represents a rating given by one user to another."""
    rating: int
    receiver: 'Rider | Driver'
    giver: 'Rider | Driver'

@dataclass
class User:
    """Base class for all users in the system."""
    name: str
    user_id: str

@dataclass
class Driver(User):
    """Represents a driver in the ride-sharing system."""
    vehicle_info: str
    ratings: list = field(default_factory=list)

    def add_rating(self, rating: Ratings) -> None:
        """Add a new rating to the driver's rating list."""
        self.ratings.append(rating)

    def accept_ride(self, current_ride: 'Ride'):
        """Accept a ride request if it hasn't been accepted by another driver."""
        if current_ride.driver is not None:
            raise RideAlreadyAcceptedError('Ride already accepted by another driver')
        current_ride.driver = self
        current_ride.mark_as_accepted()

    def rate_ride(self, current_ride: 'Ride', score: int) -> None:
        """Rate a rider after completing a ride."""
        if current_ride.driver != self:
            raise InvalidRaterError('Can not rate rider when you are not the driver')
        if current_ride.status != Status.COMPLETED:
            raise RideNotCompletedError('Can not rate when it is not completed')
        rating = Ratings(score, current_ride.rider, self)
        current_ride.rider.add_rating(rating)

@dataclass
class Rider(User):
    """Represents a rider in the ride-sharing system."""
    ratings: list = field(default_factory=list)

    def add_rating(self, rating: Ratings) -> None:
        """Add a new rating to the rider's rating list."""
        self.ratings.append(rating)

    def request_ride(self, destination: str, ride_manager: 'RideManager') -> 'Ride':
        """Request a new ride to a destination."""
        new_ride = Ride(rider=self, destination=destination, status=Status.PENDING)
        ride_manager.add_ride(new_ride)
        return new_ride

    def rate_ride(self, current_ride: 'Ride', score: int) -> None:
        """Rate a driver after completing a ride."""
        if current_ride.rider != self:
            raise InvalidRaterError('Can not rate driver when you are not the rider')
        if current_ride.status != Status.COMPLETED:
            raise RideNotCompletedError('Can not rate when it is not completed')
        rating = Ratings(score, current_ride.driver, self)
        current_ride.driver.add_rating(rating)

@dataclass
class Ride:
    """Represents a ride in the system."""
    rider: Rider
    destination: str
    status: Status
    driver: Optional[Driver] = None

    def mark_as_accepted(self):
        """Mark the ride as accepted by a driver."""
        self.status = Status.ACCEPTED

    def mark_as_completed(self):
        """Mark the ride as completed."""
        self.status = Status.COMPLETED

class RideManager:
    """Manages all rides and drivers in the system."""
    def __init__(self):
        self.rides = []
        self.drivers = []

    def add_driver(self, driver: Driver):
        """Add a new driver to the system."""
        self.drivers.append(driver)

    def add_ride(self, ride: Ride):
        """Add a new ride to the system."""
        self.rides.append(ride)

    def delete_ride(self, current_ride: Ride):
        """Delete a completed ride from the system."""
        if current_ride.status == Status.COMPLETED:
            self.rides = [r for r in self.rides if r != current_ride]
        else:
            raise RideNotCompletedError('Can not delete ride before it is completed')

    def __str__(self):
        """Return a string representation of the ride manager."""
        return f"drivers: {self.drivers} \n rides: {self.rides}"

if __name__ == "__main__":
    test_rider = Rider("Alice", "r1")
    test_driver = Driver("Bob", "d1", "Toyota")
    rm = RideManager()
    rm.add_driver(test_driver)

    test_ride = test_rider.request_ride("123 Main St", rm)
    test_driver.accept_ride(test_ride)
    test_ride.mark_as_completed()
    test_rider.rate_ride(test_ride, 5)
    print(test_driver)
