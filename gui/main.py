import sys
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

from cars import CarStore, Car
from roads import Backroad, Highway, Route

PRICE = 1.48


class Grid(Frame):
    def __init__(self, parent) -> None:
        Frame.__init__(self, parent)

        self.current_row = 0
        self.config()

    def config(self, columns=1, expand_last_item=True):
        self.columns = columns
        self.expand_last_item = expand_last_item

        return self

    def clear(self):
        self.current_row = 0

        for widget in self.winfo_children():
            widget.destroy()

        return self

    def append(self, *widgets):
        if len(widgets) > self.columns:
            raise ValueError("Too many items in grid")

        for index, widget in enumerate(widgets):
            span = 1

            if index == len(
                    widgets
            ) - 1 and self.expand_last_item and self.columns > len(widgets):
                span = self.columns - len(widgets)

            widget.grid(row=self.current_row,
                        column=index,
                        columnspan=span,
                        sticky="nswe",
                        pady=(0, 4))

        self.current_row += 1

        return self


class TextFrame(Frame):
    """
  This is a sort of replacement for `ttk.Text` that doesn't insist on ignoring
  the size of its contents
  """
    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def write(self, text=""):
        label = Label(self, text=text)
        label.pack()


class Table(Frame):
    """
    A simple table viewer implemented using a significant amount of jank
    """

    __rows: list[list[str]] = []

    def add_row(self, row: list[str]) -> None:
        self.__rows.append(row)
        self.render()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def render(self):
        # Start with a blank slate
        self.clear()

        # Loop through all of the columns
        for y, row in enumerate(self.__rows):
            font = ('Arial', 12)

            # If this is the header, give it a bold font
            if y == 0:
                font = ('Arial', 12, 'bold')

            # Add all of the row items
            for x, column in enumerate(row):
                # We need to use tk labels, rather than ttk labels to set the
                # background color
                label = tk.Label(self, text=column, font=font)

                # Give the table headers a background color.
                # FIXME: This just ignores the system dark theme
                if y == 0:
                    label['background'] = '#d3d3d3'
                    label['foreground'] = '#000000'

                label.grid(row=y, column=x, sticky="nswe")

    def write(self, text=""):
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
        # FIXME: There w
        car_names = []

        for car in self.car_store.get():
            car_names.append(car.name)

        # Select the car
        car = StringVar()
        car.set("Select a car")

        car_selector = Combobox(self.sidebar_stack, textvariable=car)
        car_selector['values'] = tuple(car_names)
        car_selector.pack()

        road, road_selector = self.get_road()

        button = Button(self.sidebar_stack,
                        text="Calculate",
                        command=lambda: calculate(car.get(), road.get()))
        button.pack()

    def update_all_cars(self) -> None:
        def calculate(road: str) -> None:
            self.results.clear()
            route = self.get_route(road)

            # Add the header row
            self.results.add_row(["Name", "Price", "Over $400"])

            for car in self.car_store.get():
                # Generate the price based on the route
                price = route.get_cost(car.kpl, PRICE)
                # Add the calculated value to the table
                self.results.add_row([
                    car.name, f"${price:.2f}", "Yes" if price > 400 else "No"
                ])

        road, _road_selector = self.get_road()

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

            # Give the car store a new car to have.
            self.car_store.add(Car(name, number))

            # Dump the user back on the home screen for visual feedback. A bit
            # horrible, but it works
            self.state.set(AppStateEnum.SELECT)
            self.update()

        name = StringVar()
        kpl = StringVar()

        name_entry = Entry(self.sidebar_stack, textvariable=name)
        kpl_entry = Entry(self.sidebar_stack, textvariable=kpl)

        name_entry.pack()
        kpl_entry.pack()

        confirm = Button(self.sidebar_stack,
                         text="Add car",
                         command=lambda: save(name.get(), kpl.get()))
        confirm.pack()

    def get_route(self, road: str) -> Route:
        if road == self.HIGHWAY:
            route = Highway()
        else:
            route = Backroad()

        return route

    def check_car(self, name: str, road: str) -> None:
        route: Route = self.get_route(road)

        price = route.get_cost(self.car_store.get_car(name).kpl, PRICE)

        self.results.write(f"{route.get_name()}: ${price:.2f}")

        if price > 400:
            self.results.write(
                f"WARNING The price for driving via {route.get_name().lower()} is too high!"
            )

    # Terminate the python process
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
