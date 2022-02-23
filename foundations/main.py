# ==============================================================================
# "Database"
from email.policy import default

cars = {
    'porsche': 1,
    'jaguar': 2,
    'lotus': 4,
    'mercedes benz': 6,
    'rolls-royce': 8,
    'bugatti': 9,
    'lamborghini': 10,
    'aston martin': 10.5,
    'bmw': 11,
    'land rover': 11.1
}

# ==============================================================================
# Color enum


class TextColor:
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    magenta = '\033[35m'
    cyan = '\033[36m'
    white = '\033[37m'
    default = '\033[39m'


# ==============================================================================
# Abstract class

from abc import ABC, abstractmethod


class Route(ABC):
    @abstractmethod
    def get_distance(self) -> float:
        pass

    @abstractmethod
    def get_fuel_efficiency(self) -> float:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    def get_fuel_consumption(self, kpl: float) -> float:
        return self.get_distance() / (kpl * self.get_fuel_efficiency())

    def get_cost(self, kpl: float, fuel_price: float) -> float:
        return self.get_fuel_consumption(kpl) * fuel_price


class Backroad(Route):
    def get_fuel_efficiency(self) -> float:
        return 0.9

    def get_distance(self) -> float:
        return 2324.5

    def get_name(self) -> str:
        return "Country road"


class Highway(Route):
    def get_fuel_efficiency(self) -> float:
        return 1.1

    def get_distance(self) -> float:
        return 2558.3

    def get_name(self) -> str:
        return "Highway"


PRICE = 1.48
ROUTES: list[Route] = [Backroad(), Highway()]

while True:
    mode = input(
        "Do you want to:\n a) Check a singe car\n b) Check all cars\n c) Exit\n$ "
    )

    if mode == "a":
        # Ask user for input
        car = input('Enter the car brand you want to compare: ').lower()

        # If the car is not in the for object, terminate
        try:
            _car = cars[car]
        except KeyError:
            print('There is no such car in our database, try another one')
            continue

        for route in ROUTES:
            price = route.get_cost(cars[car], PRICE)
            print(f"{route.get_name()}: ${price:.2f}")

            if price > 400:
                print(
                    f"{TextColor.yellow} WARNING The price for driving via {route.get_name().lower()} is too high! {TextColor.default}"
                )

        print()
    elif mode == "b":
        for name, kpl in cars.items():
            print(f"{name.capitalize()}")
            print("-" * len(name))

            for route in ROUTES:
                price = route.get_cost(kpl, PRICE)
                warning = f"{TextColor.yellow} WARNING The price for driving via {route.get_name().lower()} is over $400!{TextColor.default}" if price >= 400 else ""
                print(f"{route.get_name()}: ${price:.2f} {warning}")

            print()
    elif mode == "c":
        # Exit out of the loop
        break
    else:
        print("Invalid input, try again. It should be a, b or c")