# Magic python modules
from abc import ABC, abstractmethod


class Route(ABC):
    """
    The base for each Route. Contains all of the math logic to prevent it from
    being duplicated
    """
    @abstractmethod
    def get_distance(self) -> float:
        """
        Implemented by child classes, returns the distance of the route
        """
        pass

    @abstractmethod
    def get_fuel_efficiency(self) -> float:
        """
        Implemented by child classes, returns the fuel efficiency of the route
        """

        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        Implemented by child classes, returns the name of the route
        """

        pass

    def get_fuel_consumption(self, kpl: float) -> float:
        """
        Returns the fuel consumption of a car with the given kpl when driving on
        this route
        """

        return self.get_distance() / (kpl * self.get_fuel_efficiency())

    def get_cost(self, kpl: float, fuel_price: float) -> float:
        """
        Returns the price of a car with a given kpl and fuel price when driving
        on this route
        """

        return self.get_fuel_consumption(kpl) * fuel_price


# ==============================================================================
# Implement all of the Routes


class Backroad(Route):
    # The following methods are required by the Route abstract class

    def get_fuel_efficiency(self) -> float:
        return 0.9

    def get_distance(self) -> float:
        return 2324.5

    def get_name(self) -> str:
        return "Country road"


class Highway(Route):
    # The following methods are required by the Route abstract class

    def get_fuel_efficiency(self) -> float:
        return 1.1

    def get_distance(self) -> float:
        return 2558.3

    def get_name(self) -> str:
        return "Highway"