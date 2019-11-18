# ================================== V.02 ================================== #
# New method of creating header lines for separating exercise outputs
# Matplotlib formatting options removed
# ========================================================================== #

'''
1. Write a program that outputs ‘Hello World’ to the terminal
2. Write a program that outputs ‘Hello World’ 50 times using a for loop
3. Write a program with a for loop that iterates 50 times and outputs ‘Hello
World’ after every 5 iterations.
4. Write a program with a for loop with 50 iterations and outputs ‘Hello
World’ every odd value of the loop counter and, and ‘Goodbye World’
every even value.
5. Read in the text file ‘xy.txt’ and print the data to the terminal in 2 columns
6. Plot the data in ‘xy.txt’ with blue dots
7. Plot the data in ‘xy.txt’ with red crosses
8. Plot the data in ‘xy.txt’ as a line plot
9. Find the individual sums of the ‘x’ data and the ‘y’ data and print them to
the terminal
10. Determine the individual means for the ‘x’ and ‘y’ data and print them to
the terminal
11. Write a code that creates 3 variables called ‘day’, ‘month’, ‘year’. 
Get the code to ask the user to input values for each variable, and then 
output the values is the form "Today's date is:" dd/mm/yyyy.
Now run the code using today's date as the input.
'''

import datetime
import numpy as np
import matplotlib
# matplotlib.use('PDF')
import matplotlib.pyplot as plt

''' ======= EXERCISE ROUTINES ======='''
def exercise_1():
    print('hello world')

def exercise_2():
    for n in range(0, 50):
        print('foo bar ' + str(n))

def exercise_3():
    for n in range(0, 50):
        if n % 5 == 0:
            print('foo bar ' + str(n))

def exercise_4():
    for n in range(0, 50):
        if n % 2 == 0:
            print('good bye world ' + str(n))
        else:
            print('hello world ' + str(n))

def exercise_5():
    # Read in the text file ‘xy.txt’ and print the data to the terminal in 2 columns
    x, y = np.loadtxt('DATA/xy.txt', unpack=True)
    num_of_items = len(x)
    print('Number of data plots is ' + str(num_of_items))
    counter = 0
    print('===== BEGIN PRINT ITEMS =====')
    print('x', ' | ', 'y')
    while counter < num_of_items:
        print(x[counter], ' | ', y[counter])
        counter += 1
    print('===== END PRINT ITEMS =====')

def exercise_6():
    # Plot the data in ‘xy.txt’ with blue dots
    x, y = np.loadtxt('DATA/xy.txt', unpack=True)
    plt.plot(x, y, 'r+')
    plt.show()

def exercise_7():
    # Plot the data in ‘xy.txt’ with red crosses
    x, y = np.loadtxt('DATA/xy.txt', unpack=True)
    fig = plt.figure()  # Initialise the figure for plotting onto
    plt.plot(x, y, 'r+')
    # plt.show()
    filename = make_file_name_with_date(directory='Plots', name_stub='plot-exercise_7-', extension='.png')
    fig.savefig(filename)
    print('** Plot saved as ' + filename + ' **')

def exercise_8():
    # Plot the data in ‘xy.txt’ as a line plot
    x, y = np.loadtxt('DATA/xy.txt', unpack=True)
    fig = plt.figure()  # Initialise the figure for plotting onto
    plt.plot(x, y, '-m')
    # plt.show()
    filename = make_file_name_with_date(directory='Plots', name_stub='plot-exercise_8-', extension='.png')
    fig.savefig(filename)
    print('** Plot saved as ' + filename + ' **')

def exercise_9():
    print('''Task: Find the individual sums of the 'x' data and the 'y' data and
    print them to the terminal''')
    x, y = np.loadtxt('DATA/xy.txt', unpack=True)
    num_of_items = len(x)
    counter = 0
    while counter < num_of_items:
        temp_x = x[counter]
        temp_y = y[counter]
        print('{} + {} = {}'.format(str(temp_x), str(temp_y), temp_x + temp_y))
        counter += 1

def exercise_9_a():
    print('''Task: Find the individual sums of the ‘x’ data and the ‘y’ data and
    print them to the terminal''')
    x, y = np.loadtxt('DATA/xy.txt', unpack=True)
    x_and_y = np.vstack((x, y)).T
    print(np.sum(x_and_y, axis=1))

def exercise_10():
    print('''Task: 10. Determine the individual means for the ‘x’ and ‘y’ data and print them to
    the terminal''')
    x, y = np.loadtxt('DATA/xy.txt', unpack=True)
    x_and_y = np.vstack((x, y)).T
    print(np.mean(x_and_y, axis=1))


''' ===== END EXERCISE ROUTINES ====='''


list_of_exercises = [exercise_1, exercise_2, exercise_3, exercise_4,
                     exercise_5, exercise_6, exercise_7, exercise_8,
                     exercise_9, exercise_9_a, exercise_10]


def generate_current_date_str():
    date_format = 'yyyy-mm-dd'
    current_date = datetime.datetime.now()
    year = str(current_date.year)
    month = current_date.month
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)
    date = current_date.day
    if date < 10:
        date = '0' + str(date)
    else:
        date = str(date)

    # Get date format str and replace components
    current_date_str = date_format.replace('yyyy', year).replace('mm', month).replace('dd', date)

    return current_date_str


def make_file_name_with_date(directory, name_stub, extension):
    return directory + '/' + name_stub + generate_current_date_str() + extension


def headline(text, symbol, width):
    return f" {text} ".center(width, symbol)


''' ===== EXECUTION ====='''


def output_all():
    counter = 0
    while counter < len(list_of_exercises):
        print(headline(width=50, text='Start ' + list_of_exercises[counter].__name__, symbol='='))
        list_of_exercises[counter]()  # Run the exercise routine for this counter
        print(headline(width=50, text='End ' + list_of_exercises[counter].__name__, symbol='=') + '\n\n')
        counter += 1


valid_selection = False
while not valid_selection:
    user_selection = input('Do you want to run one exercise or all exercises?\nChoose "one" or "all": ')
    if user_selection != 'one' and user_selection != 'all':
        print('Invalid selection, type "one" or "all" only.  Please try again.\n\n')
    if user_selection == 'all':
        valid_selection = True
        output_all()
    if user_selection == 'one':
        valid_selection = True
        counter = 1
        for n in list_of_exercises:
            # Present a list of available exercises to the user for selection
            print(str(list_of_exercises.index(n) + 1) + ' : ' + str(n.__name__))
            counter += 1
        # New while loop to ensure valid exercise option is chosen
        valid_exercise = False
        while not valid_exercise:
            try:
                # User input is 1 indexed, list is 0 indexed so -1 to compensate
                user_selected_exercise = int(
                    input('Select the exercise to run by the corresponding number shown above: ')) - 1
                # Check that user input is in range of list
                if 0 <= user_selected_exercise < len(list_of_exercises):
                    valid_exercise = True
                else:
                    print('Invalid selection, type a number that is between 1 and ' +
                          str(len(list_of_exercises)) +
                          '.  Please try again.\n\n')
            except:
                print('Invalid selection, type only a number that is between 1 and ' +
                      str(len(list_of_exercises)) +
                      '.  Please try again.\n\n')

        print(headline(width=50, text='Start ' + list_of_exercises[user_selected_exercise].__name__, symbol='='))
        list_of_exercises[user_selected_exercise]()  # Run the exercise selected by user
        print(headline(width=50, text='End ' + list_of_exercises[user_selected_exercise].__name__, symbol='=') + '\n\n')

''' ===== END EXECUTION ====='''
