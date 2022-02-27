# Constants for readability. Nothing used regularly should be put here because
# it will slow down the program.
CAR_STORE_LOCATION = './cars.csv'


class Car():
    def __init__(self, name: str, kpl: float) -> None:
        self.name = name
        self.kpl = kpl


class CarStore():
    """
    This is responsible for loading and storing cars whilst allowing for us to
    make changes without introducing bugs
    """

    __cars: list[Car] = []

    def __init__(self) -> None:
        self.load()

    def load(self):
        try:
            with open(CAR_STORE_LOCATION, 'r') as table:
                # All of the cars stored
                cars = table.readlines()

                for car in cars:
                    # Split the car into its parts
                    name, kpl = car.split(',')

                    # Create a new car
                    self.__cars.append(Car(name, float(kpl)))
        except FileNotFoundError:
            print(
                'Car store was not found, there will be no cars in this program'
            )

    def add(self, car: Car) -> None:
        self.__cars.append(car)

        new_csv = ""

        for car in self.get():
            new_csv += f"{car.name},{car.kpl}\n"

        with open(CAR_STORE_LOCATION, 'w') as table:
            table.write(new_csv)

        self.load()

    def get(self) -> list[Car]:
        return self.__cars

    def get_car(self, name: str) -> Car:
        for car in self.get():
            if car.name == name:
                return car