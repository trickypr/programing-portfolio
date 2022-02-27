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