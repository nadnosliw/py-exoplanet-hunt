
# INTRO TO PYTHON

# How does code work?


# Assign Variables
this_is_a_string = 'hello world'  # str
this_is_also_a_string = "Daniel's world"  # str
integer = 5  # int
decimal = 5.7  # float

integer_as_a_string = str(integer)
str_as_an_integer = int(integer_as_a_string)

a_tuple = (2, 4)
a_list = [0, 1, 2, 3, 4, 5]
another_list = ['a', 'b', 'c', 'd', ['abc', 'xyz']]
a_2d_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

boolean = True
boolean_false = False  # bool


# Get Python to say things to you - print
# print(f'The value of integer_as_a_string is {integer_as_a_string}')


# Do math functions with number variables
mass = 60
acceleration = 2
net_force = mass * acceleration

# print(f'The value of net force is {net_force} N')

distance_travelled = 30
time_for_leg_one = 5
speed = distance_travelled / time_for_leg_one

# print(f'The value of speed is {speed} m/s')

radius = 3
area_of_circle = 3.142 * radius**2

# print(f'The area of the circle is {area_of_circle} m^2')


# Use comments!
'''multi
line
string or comment'''


# Get Python to ask the user for input
# name = input('Please type your name: ')
# number = int(input('Please type a number: '))
# result = number * 2

# print(f'Your number is: {result}')

# Use logic
'''
number = 49
if number > 100:
    print('big')
elif number > 50:
    print('medium')
else:
    print('small')
'''

# Make and access arrays of data
a_2d_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# print(a_2d_list[2][2])

# Loops for repeated tasks
'''
a_2d_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
for row in a_2d_list:
    print(f'The first item, doubled, is: {row[0] * 2}')
'''


# Make and call functions - sub routines
def headline(message, symbol, width):
    return f' {message} '.center(width, symbol)


print(headline('Important Message', '=', 50))


