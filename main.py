from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional

class Status(Enum):
    PENDING = auto()
    ACCEPTED = auto()
    COMPLETED = auto()

@dataclass
class Ratings:
    rating: int
    receiver: 'Rider | Driver'
    giver: 'Rider | Driver'

@dataclass
class User:
    name: str
    user_id: str

@dataclass
class Driver(User):
    vehicle_info: str
    ratings: list = field(default_factory=list)

    def add_rating(self, rating: Ratings) -> None:
        self.ratings.append(rating)

    def accept_ride(self, ride: 'Ride'):
        if ride.driver is not None:
            raise Exception('Ride already accepted by another driver')
        ride.driver = self
        ride.mark_as_accepted()

    def rate_ride(self, ride: 'Ride', score: int) -> None:
        # only rate if you are the rider 
        if ride.driver != self:
            raise Exception('Can not rate rider when you are not the driver')
        # check if ride is completed
        if ride.status != Status.COMPLETED:
            raise Exception('Can not rate when it is not completed')
        rating = Ratings(score, ride.rider, self)
        ride.rider.add_rating(rating)

@dataclass
class Rider(User):
    ratings: list = field(default_factory=list)

    def add_rating(self, rating: Ratings) -> None:
        self.ratings.append(rating)

    def request_ride(self, destination: str, ride_manager: 'RideManager') -> 'Ride':
        ride = Ride(rider=self, destination=destination, status=Status.PENDING)
        ride_manager.add_ride(ride)
        return ride
    
    def rate_ride(self, ride: 'Ride', score: int) -> None:
        # only rate if you are the rider 
        if ride.rider != self:
            raise Exception('Can not rate driver when you are not the rider')
        # check if ride is completed
        if ride.status != Status.COMPLETED:
            raise Exception('Can not rate when it is not completed')
        rating = Ratings(score, ride.driver, self)
        ride.driver.add_rating(rating)

@dataclass
class Ride:
    rider: Rider
    destination: str
    status: Status
    driver: Optional[Driver] = None

    def mark_as_accepted(self):
        self.status = Status.ACCEPTED

    def mark_as_completed(self):
        self.status = Status.COMPLETED

class RideManager:
    """ track all rides and drivers
    """
    def __init__(self):
        self.rides = []
        self.drivers = []
    
    def add_driver(self, driver: Driver):
        self.drivers.append(driver)
    
    def add_ride(self, ride: Ride):
        self.rides.append(ride)
    
    def delete_ride(self, ride: Ride):
        # delete ride once completed
        if ride.status == Status.COMPLETED:
            self.rides = [r for r in self.rides if r != ride]
        else:
            raise Exception('Can not delete ride before it is completed')
    
    def __str__(self):
        return f"drivers: {self.drivers} \n rides: {self.rides}"

if __name__ == "__main__":
    rider = Rider("Alice", "r1")
    driver = Driver("Bob", "d1", "Toyota")
    rm = RideManager()
    rm.add_driver(driver)

    ride = rider.request_ride("123 Main St", rm)
    driver.accept_ride(ride)
    ride.mark_as_completed()
    rider.rate_ride(ride, 5)
    print(driver)
