import sys
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

from cars import CarStore, Car
from gui.cars import StoreDuplicateItem
from roads import Backroad, Highway, Route

PRICE = 1.48


class Table(Frame):
    """
    A simple table viewer implemented using a significant amount of jank
    """

    # Stores all of the rows that will be rendered
    __rows: list[list[str]] = []

    def add_row(self, row: list[str]) -> None:
        # Append and rerender
        self.__rows.append(row)
        self.render()

    def clear(self):
        """
        Clears all of the contents of the grid
        """

        self.__rows = []
        self.render_clear()

    def render_clear(self):
        """
        Hides the contents of the grid. THE CONTENTS IS STILL STORED
        """

        for widget in self.winfo_children():
            widget.grid_remove()
            widget.destroy()

    def render(self):
        # Start with a blank slate
        self.render_clear()

        # Loop through all of the columns
        for y, row in enumerate(self.__rows):
            # The default fonts for grid items
            # TODO: This should conform to system theme
            font = ('Arial', 12)

            # If this is the header, give it a bold font
            if y == 0:
                font = ('Arial', 12, 'bold')

            # Add all of the row items
            for x, column in enumerate(row):
                # We need to use tk labels, rather than ttk labels to set the
                # background color
                label = tk.Label(self, text=column.capitalize(), font=font)

                # Give the table headers a background color.
                # FIXME: This just ignores the system dark theme
                if y == 0:
                    label['background'] = '#d3d3d3'
                    label['foreground'] = '#000000'

                # Add the label to the grid
                label.grid(row=y, column=x, sticky="nswe")

    def write(self, text=""):
        # Write a label to the end of the grid with no particular regard for
        # formatting.

        length = len(self.winfo_children())
        label = Label(self, text=text)
        label.grid(row=length, column=0, sticky="nswe")


class AppStateEnum():
    SELECT = "Select an option"
    INDIVIDUAL_CAR = "Individual car"
    ALL_CARS = "All cars"
    INPUT_CAR = "Add a car"

    ALL = [SELECT, INDIVIDUAL_CAR, ALL_CARS, INPUT_CAR]


class App(Tk):
    sidebar_bg = "#7D7D7D"

    def __init__(self):
        Tk.__init__(self)

        self.car_store = CarStore()

        self.build_structure()

    def build_structure(self) -> None:
        # Basic grid structure that will be constructed
        #
        # |------------------------|--------------------------------------|
        # | |--------------------| | self.results                         |
        # | | self.sidebar_stack | |                                      |
        # | | self.quit_button   | |                                      |
        # | |--------------------| |                                      |
        # |------------------------|--------------------------------------|

        # This will hold the entire contents of the sidebar to reduce the
        # changes that need to be made to other widgets if I add a row
        self.sidebar_frame = ttk.Frame(self, width=200)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw", padx=8, pady=8)

        # State dropdown. Responsible for choosing the calculation that the user
        # wants to run. Defaults to a select value

        # Create a string variable to hold the state
        self.state = StringVar()
        self.state.set(AppStateEnum.SELECT)

        # Create the dropdown
        self.state_drop = OptionMenu(self.sidebar_frame,
                                     self.state,
                                     *AppStateEnum.ALL,
                                     command=self.update)

        # Tell the dropdown to fill the entire sidebar width
        self.state_drop.grid(row=0, column=0, sticky='ew')

        # This is where we will store everything in the sidebar
        self.sidebar_stack = Frame(self.sidebar_frame)
        self.sidebar_stack.grid(row=1, column=0, sticky='nwe')

        # Create the quit button and give it the self.destroy method
        self.quit_button = Button(self.sidebar_frame,
                                  text="Quit",
                                  command=self.destroy)
        self.quit_button.grid(row=2, column=0, sticky='sew')

        # Create a table to output the results
        self.results = Table(self)
        self.results.grid(row=0, column=1)

        # It works. Don't touch it. No clue what it does, but it works
        self.sidebar_frame.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Run the first UI build to make sure that the state is correct
        self.update()

    def update(self, *args) -> None:
        # HACK: Takes in *args to stop annoying type errors

        # Clear all of the elements that shouldn't persist
        for widget in self.sidebar_stack.winfo_children():
            widget.destroy()
        self.results.clear()

        # Grab the state for easy access
        state = self.state.get()

        # Run the appropriate method for the state
        if state == AppStateEnum.INDIVIDUAL_CAR:
            self.update_individual_car()
        elif state == AppStateEnum.ALL_CARS:
            self.update_all_cars()
        elif state == AppStateEnum.INPUT_CAR:
            self.update_input_car()

    # Constants for my sanity. Dont question my formatting decisions
    HIGHWAY = "Highway"
    COUNTRY = "Country roads"

    def get_road(self):
        """
        Creates a dropdown for the user to select the road type they want
        """

        # State variable for the road type
        car = StringVar()
        car.set("Select a road")

        # Create the widget
        car_selector = OptionMenu(self.sidebar_stack, car, "Select a road",
                                  self.HIGHWAY, self.COUNTRY)
        car_selector.pack()

        # Return it to the caller to handle
        return (car, car_selector)

    def update_individual_car(self) -> None:
        def calculate(car: str, road: str) -> None:
            """
            Function to find the car the user chose and display the calculation 
            in the table
            """

            # Clear the contents of the table
            self.results.clear()

            # Get the class objects that represent both the car and the road
            route = self.get_route(road)
            real_car = self.car_store.get_car(car)

            # Add the header row
            self.results.add_row(["Name", "Price", "Over $400"])

            # Generate the price based on the route
            price = route.get_cost(real_car.kpl, PRICE)
            # Add the calculated value to the table
            self.results.add_row([
                real_car.name, f"${price:.2f}", "Yes" if price > 400 else "No"
            ])

        # Get a list of all the car names
        car_names = [car.name.capitalize() for car in self.car_store.get()]

        # Select the car
        car = StringVar()
        car.set("Select a car")

        # Create the dropdown and pack it into the frame
        car_selector = OptionMenu(self.sidebar_stack, car, "Select a car",
                                  *car_names)
        car_selector.pack()

        # Add a road selector
        road, _road_selector = self.get_road()

        # Create the calculate button which calls the calculate method defined above
        button = Button(self.sidebar_stack,
                        text="Calculate",
                        command=lambda: calculate(car.get(), road.get()))
        button.pack()

    def update_all_cars(self) -> None:
        def calculate(road: str) -> None:
            """
            Calculate the price for all cars using the road of the user's choice
            """

            # Clear all the old results
            self.results.clear()

            # Get the route object
            route = self.get_route(road)

            # Add the header row
            self.results.add_row(["Name", "Price", "Over $400"])

            # Calculate the prices for all of the cars
            price = [(route.get_cost(car.kpl, PRICE), car.name)
                     for car in self.car_store.get()]

            for price, name in price:
                # Add the calculated value to the table
                self.results.add_row(
                    [name, f"${price:.2f}", "Yes" if price > 400 else "No"])

        # Summon a road selector
        road, _road_selector = self.get_road()

        # Summon a calculate button to trigger the above function
        button = Button(self.sidebar_stack,
                        text="Calculate",
                        command=lambda: calculate(road.get()))
        button.pack()

    def update_input_car(self) -> None:
        def save(name: str, raw_number: str) -> None:
            try:
                # Try to parse the users input
                number = float(raw_number)
            except ValueError:
                # If the number is invalid, we should provide an error to the
                # user and wait for another input
                self.results.write("Invalid number")
                return

            # The store may throw an error if there is already a car with that
            # name located somewhere within the store. We want to catch that error
            # and prevent the rest of that code from executing.
            try:
                # Give the car store a new car to have.
                self.car_store.add(Car(name, number))
            except StoreDuplicateItem:
                self.results.write("Two cars cannot have the same name")
                return

            # Dump the user back on the home screen for visual feedback. A bit
            # horrible, but it works
            self.state.set(AppStateEnum.SELECT)
            self.update()

        # Create the string variables for the entry box
        name = StringVar()
        kpl = StringVar()

        # Create the entry boxes
        name_entry = Entry(self.sidebar_stack, textvariable=name)
        kpl_entry = Entry(self.sidebar_stack, textvariable=kpl)

        # Pack the entry boxes into the layout
        name_entry.pack()
        kpl_entry.pack()

        # Summon confirm button that calls the save function with the required
        # parameters
        confirm = Button(self.sidebar_stack,
                         text="Add car",
                         command=lambda: save(name.get(), kpl.get()))
        confirm.pack()

    def get_route(self, road: str) -> Route:
        """
        Converts the road to a route object, which falls back to a backroad if 
        it cant find anything. Uses constants defined way up above in this class
        """

        if road == self.HIGHWAY:
            route = Highway()
        else:
            route = Backroad()

        return route

    # Terminate the python process
    # This exists because I am to lazy to replace all occupances and the
    # performance impact is non-existant
    def destroy(self) -> None:
        self.quit()

    def quit(self, code=0) -> None:
        """
        Exits the application with an optional, non-zero exit code
        """
        sys.exit(code)


# Only run this in the main file, otherwise print a warning
if __name__ == "__main__":
    app = App()
    app.title("Car comparison")
    app.mainloop()
else:
    print("Run 'main.py' as the main file")
