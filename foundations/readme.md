## Entry 1 - Programming Foundations

The context of this programming assignment is free for you to choose. The goal here is to take a simple formula or concept and build an application that makes use of it to solve a problem. I will provide an example at the end to demonstrate this.
You should begin by outlining the formula you'll be building an application for. Then you should provide a scenario that will make use of that formula. Then you should add constraints that will require the programming components outlined below.
Your program will need to make use of the following in its solution:

- A compound decision structure (if-elif-else with multiple conditions).
- Looping control structures (while and for loops).
- Use of data types: strings, integers, floats and booleans.
- Use of data structures: lists, and dictionaries.

### Example

#### Isabelle’s Holliday

#### Formula

This project will make use of a simple cost of fuel/kilometre travelled formula:
cost = (distance⁄kilometres per litre) × Cost per litre of fuel
Scenario

Isabelle is planning a trip to visit Alice Springs. Since she lives in Canberra, ACT, she is concerned about the cost of fuel needed to make the trip. Using her GPS, she calculated that she could take the main highways (2558.3 [km]) or a series of country roads (2324.5 [km]) to reach her destination. Travelling on the highway, Isabelle’s car gets 110% of the kilometres per litre (KPL) listed below. If she travels via countryside roads, her car gets 90% of its listed kilometres per litre.
Estimating that the average cost of gas is $1.48 per litre (CPL), calculate how much money it will cost for her to travel to Alice Springs using the highway and the countryside roads. Applying the formula above, you can calculate the cost of travel by distance divided by KPL times CPL.
Isabelle also just happens to own 10 cars because she's extremely rich or something. These cars are presented below in order of highest to lowest consumption [km/lt].

1. Porsche (1 KPL)
1. Jaguar (2 KPL)
1. Lotus (4 KPL)
1. Mercedes Benz (6 KPL)
1. Rolls-Royce (8 KPL)
1. Bugatti (9 KPL)
1. Lamborghini (10 KPL)
1. Aston Martin (10.5 KPL)
1. BMW (11 KPL)
1. Land Rover (11.1 KPL)

Isabelle needs a program that will let her select a car, see how much it would cost to take that car, and be alerted if it would cost more than $400 in fuel.

#### How this addresses the criteria

- A compound decision structure (if-elif-else with multiple conditions).
  - There are 2 major decisions, if she takes the highways or backroads, and which car she takes. These two can be combined into an if-elif-else structure that will involve a compound conditional
- Looping control structures (while and for loops).
  - A while loop can be used to continually request input from the user in a command-line application, a for loop can be used to iterate over the data structures
- Use of data types: strings, integers, floats and booleans.
  - Strings will be used to output information, ints and floats will hold the KPL and CPL data, and bools will be in the conditionals for the while loop and if statements
- Use of data structures: lists, and dictionaries.
  - The cars can be stored in a dictionary to pair their name and KPL, the road distances can be stored in a list.
