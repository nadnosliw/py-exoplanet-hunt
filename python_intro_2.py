
# INTRO TO PYTHON

# How does code work?


# Assign Variables
this_is_a_string = 'hello world'  # str
this_is_also_a_string = "hello world"  # str
integer = 5  # int
decimal = 6.5  # float

integer_as_a_string = str(integer)
str_as_int = int(integer_as_a_string)

a_tuple = (2, 4)
a_list = [0, 1, 2, 3, 4]
a_2d_list = [[0, 1, 2], ['a', 'b', 'c']]
boolean = True
boolean = False


# Get Python to say things to you - print
print('hello world')  # Prints hello world to the console
print(this_is_a_string)  # Prints the content of the variable "this_is_a_string"
print(f'This is a formatted string, integer = {integer}')


# Do math functions with number variables
mass = 60
acceleration = 2
net_force = mass * acceleration
print(f'net force = {net_force} N')

distance = 30
time = 5
speed = distance / time
print(f'speed = {speed} m/s')

# Use comments!
'''multi
line 
string
or comment'''

# Get Python to ask the user for input
# name = input('Hello, type your name: ')
# print(f'You said your name was: {name}')

'''
number = int(input('Hello, type a number: '))
result = number * 3
print(f'The number inputted was: {result}')


# Use logic
if result > 100:
    print('big')
elif result > 50:
    print('medium')
else:
    print('small')
'''

# Make and access arrays of data
a_list = [0, 1, 2, 3, 4]
first_item = a_list[2]
print(first_item)

a_list.append(5)
print(a_list)


# Loops for repeated tasks
for item in a_list:
    print(f'Calculation result: {item * 2}')


# Make and call functions - sub routines
def headline(message, symbol, width):
    return f" {message} ".center(width, symbol)


print(headline('Important message', '*', 100))
