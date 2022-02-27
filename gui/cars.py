# Constants for readability. Nothing used regularly should be put here because
# it will slow down the program.
CAR_STORE_LOCATION = './cars.csv'


class StoreDuplicateItem(Exception):
    pass


class Car():
    """
    A class used to store all of the values for a car and keep intelisense happy
    """

    name: str
    kpl: float

    def __init__(self, name: str, kpl: float) -> None:
        self.name = name
        self.kpl = kpl

    def to_csv(self) -> str:
        return f'{self.name},{self.kpl}'


class CarStore():
    """
    This is responsible for loading and storing cars whilst allowing for us to
    make changes without introducing bugs
    """

    __cars: list[Car] = []

    def __init__(self) -> None:
        self.load()

    def load(self):
        # If the car file doesn't exist, we want to handle this gracefully rather
        # than crashing
        try:
            with open(CAR_STORE_LOCATION, 'r') as table:
                # All of the cars stored
                cars = table.readlines()

                for car in cars:
                    # Split the car into its parts
                    name, kpl = car.split(',')

                    # Create a new car. Note that we are avoiding self.add()
                    # to reduce IO throughput, which might be a touch slow on
                    # some computers (Cough, windows, cough, dos, cough)
                    self.__cars.append(Car(name, float(kpl)))
        except FileNotFoundError:
            # Console log for debugging. If the user is opening the program for
            # the first time, I expect that they will stumble accross the add
            # car dropdown before they see this message.
            print(
                'Car store was not found, there will be no cars in this program'
            )
            print(
                'Try adding cars using the "Add a car" option in the dropdown')

    def add(self, car: Car) -> None:
        """
        Adds a car to the store and saves it to the disk

        throws: StoreDuplicateItem
        """

        # If the car has the same name as another car, we should throw an error
        if self.get_car(car.name) != None:
            raise StoreDuplicateItem

        # Add the car to the internal array so that the program can use it latter
        self.__cars.append(car)

        # Create a place to store the new csv contents
        new_csv = ""

        # Write each car to the csv string
        for car in self.get():
            new_csv += car.to_csv() + "\n"

        # Write that car to disk
        with open(CAR_STORE_LOCATION, 'w') as table:
            table.write(new_csv)

    def get(self) -> list[Car]:
        """
        Returns the list of cars
        """
        return self.__cars

    def get_car(self, name: str) -> Car:
        """
        Finds a car with the matching name
        """

        for car in self.get():
            # Capitalization shouldn't mater
            if car.name.lower() == name.lower():
                return car