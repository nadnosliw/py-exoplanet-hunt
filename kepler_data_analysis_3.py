# ================================== V.03 ================================== #
# Removed auto save of plots in functions, now manual saving will be required
# this focuses saves onto only the plots that are useful.
# Refactored code to receive a shift_value estimate and iterate through a range of periods
# from that estimate showing plot for each for user to select best.
#
# ========================================================================== #


import datetime
import numpy as np
import matplotlib
# matplotlib.use('PDF')
import matplotlib.pyplot as plt
import csv


# ============================= FILE HANDLING ============================= #
def generate_system_filename(system_identifier):
    return 'KIC' + str(system_identifier) + '.tbl'


def make_file_name_with_date(directory, name_stub, extension):
    return directory + '/' + name_stub + generate_current_date_str() + extension


def get_kic_data_table_with_np(directory, filename):
    try:
        x, y, z = np.loadtxt(directory + '/' + filename, unpack=True, skiprows=3)
        # First column of data is not useful, ignore
        return y, z
    except:
        print('!! There was an error retrieving this data file: ' + filename + ' !!')
        return -1


def generate_data_plot(x, y, system_number, plot_type):
    fig = plt.figure()  # Initialise the figure for plotting onto
    plt.plot(x, y, 'r+')
    plt.show()

    # Plots will no longer be saved automatically
    '''
    filename = make_file_name_with_date(directory='Plots',
                                       name_stub=plot_type + ' plot for ' + system_number + ' - ',
                                       extension='.png')
    fig.savefig(filename)
    print('** Plot saved as "' + filename + '" **')
    '''


def write_to_csv(filename, path, data_list):
    # Transpose the data_list
    transposed_data = transpose_2d_columns_separate_array_into_rows(data_list)
    filename_and_path = path + '/' + filename + '.csv'
    csv_file = open(filename_and_path, 'w+')  # w+ means create new file if doesn't exist
    list_length = len(transposed_data)
    if list_length > 1:
        row_or_rows = 'rows'
    else:
        row_or_rows = 'row'
    with csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(transposed_data)
    print(headline(f'Data exported to {filename_and_path} with {str(list_length)} {row_or_rows}', '*', 100))


def import_csv_file(file_name, file_path):
    csv_file = open(file_path + '/' + file_name, 'r')
    output_array = []

    with csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            output_array.append(row)

    return output_array


# ============================= FORMATTING AND UI ============================= #
def headline(text, symbol, width):
    return f" {text} ".center(width, symbol)


def generate_current_date_str():
    date_format = 'yyyy-mm-dd'
    current_date = datetime.datetime.now()
    year = str(current_date.year)
    month = current_date.month
    date = current_date.day

    # Make month and day 2 digits
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)

    if date < 10:
        date = '0' + str(date)
    else:
        date = str(date)

    # Get date format str and replace components
    current_date_str = date_format.replace('yyyy', year).replace('mm', month).replace('dd', date)

    return current_date_str


# ============================= PHASE FOLDING ============================= #
def shift_data_plots_horizontally(data, shift_value):
    # Data is a 2D array
    operand_array = [[shift_value], [0]]  # Create a 2D array with shift_value and 0
    return np.subtract(data, operand_array)  # Subtracts shift_value from all data in first column


def perform_mod_on_array_np(data_array, period):
    # Data is a 2D array
    max_value = np.amax(data_array[1])
    # print(max_value)
    # Create a 2D array with shift_value and max value + 1 (modulo operation will return original num)
    operand_array = [[period], [max_value + 1]]
    return np.mod(data_array, operand_array)  # Calculates the division remainder of first column with shift_value


def perform_mod_on_time_data(data_array, period):
    # Data is a 2D array, sub arrays are columns not rows
    new_time_array = []
    # Iterate through first sub array, i.e. the time data
    for count, time_value in enumerate(data_array[0]):
        new_time_array.append(time_value % period)

    return [new_time_array, data_array[1]]


def transpose_2d_columns_separate_array_into_rows(data_array):
    transposed_array = []
    for n in range(0, len(data_array[0])):
        transposed_array.append([data_array[0][n], data_array[1][n]])
    return transposed_array


def transpose_2d_rows_separated_array_into_columns(rows_separated_array):
    transposed_array = []
    # Get number of columns from the first row
    number_of_columns = len(rows_separated_array[0])
    for column in range(0, number_of_columns):
        # Add empty list for each column to the transposed array
        transposed_array.append([])

    for row in rows_separated_array:
        # Iterate through the rows in the input array
        for column, data in enumerate(row):
            # For each row track the number of items which is the column number
            # Add the data point to the correct column list in the transposed array
            transposed_array[column].append(data)

    return transposed_array


def time_period_iterator(catalogue_number, data_array, coordinate_1, coordinate_2, resolution):
    time_period = (coordinate_2 - coordinate_1) / 9
    time_period = float(str(time_period)[0:7])  # Tidy up time_period to 7 s.f. value

    # Subtract 5 x resolution from the time_period and iterate adding the resolution from there
    time_period -= resolution * 5
    while time_period < time_period + 5 * resolution:
        # Shift all data points so that the first transit occurs at time_period/2 from 0
        # Subtract (first_transit_coordinate - time_period/2) from all data points
        zeroed_data = shift_data_plots_horizontally(data_array, coordinate_1 - time_period/2)

        phase_folded_data = perform_mod_on_time_data(zeroed_data, time_period)

        shifted_phase_folded_data = shift_data_plots_horizontally(phase_folded_data, time_period / 2)

        # write_to_csv("shifted_phase_folded_data", 'Data_Exports', shifted_phase_folded_data)

        generate_data_plot(shifted_phase_folded_data[0],
                           shifted_phase_folded_data[1],
                           catalogue_number,
                           'Phase folded')

        # Ask user if they want to save the time period, continue iterating, or exit
        next_step = handle_phase_fold_next_step(time_period, resolution)

        if next_step == 'Get next plot':
            time_period += resolution
        elif next_step == 'Increase resolution':
            # Subtract resolution value to account for overshoot
            time_period -= resolution
            resolution /= 10  # Make resolution smaller by factor of ten
            time_period -= resolution * 5  # Offset time_period by half of the resolution range
        elif next_step == 'Exit':
            # Subtract resolution value to account for overshoot
            time_period -= resolution
            return time_period

    return 'N/A'


def phase_fold_single_time_period(catalogue_number, data_array, coordinate_1, time_period):
    time_period = float(str(time_period)[0:7])  # Tidy up time_period to 7 s.f. value

    # Shift all data points so that the first transit occurs at time_period/2 from 0
    # Subtract (first_transit_coordinate - time_period/2) from all data points
    zeroed_data = shift_data_plots_horizontally(data_array, coordinate_1 - time_period/2)

    phase_folded_data = perform_mod_on_time_data(zeroed_data, time_period)

    shifted_phase_folded_data = shift_data_plots_horizontally(phase_folded_data, time_period / 2)

    # write_to_csv("shifted_phase_folded_data", 'Data_Exports', shifted_phase_folded_data)

    generate_data_plot(shifted_phase_folded_data[0],
                       shifted_phase_folded_data[1],
                       catalogue_number,
                       'Phase folded')


# ============================= HANDLE INPUTS ============================= #
def handle_catalogue_number_input(get_plot):
    valid_input = False
    while not valid_input:
        # User will remain in this loop until some data has been successfully extracted and plot generated
        catalogue_number = input(
            'Type the Kepler Input Catalogue (KIC) number of the system (e.g. 006922244, 002571238) : ')
        data = -1
        filename = ''
        if len(catalogue_number) != 0:
            # If catalogue number is valid then a valid filename will be generated
            filename = generate_system_filename(catalogue_number)
        else:
            print('\nInvalid catalogue number for the system.  Please try again.\n\n')

        if filename:
            # Filename exists
            data = get_kic_data_table_with_np(directory='DATA', filename=filename)  # data = -1 if file not found

            if data != -1 and get_plot:
                # Data was extracted and plot requested
                generate_data_plot(data[0], data[1], catalogue_number, 'Raw')
                valid_input = True
            elif data != -1:
                # Data was extracted and plot not requested
                valid_input = True
            else:
                print('\nInvalid catalogue number for the system.  Please try again.\n\n')

    return catalogue_number, data


def handle_time_coordinate_input(message):
    # Ask for coordinates of first and last transits
    valid_input = False
    while not valid_input:
        coordinate = float(input(
            f'Type the coordinate estimate for the {message} (e.g. 131.697 or 163.391) : '))
        # coordinate_2 = float(input(
        #     'Type the coordinate estimate for the tenth transit (e.g. 163.391) : '))

        # time_period = (coordinate_2 - coordinate) / 9

        # Check that the coordinate is a valid float and greater than 0
        if coordinate != '' and str(type(coordinate)) == "<class 'float'>" and coordinate > 0:
            # Something was typed and it is a valid float larger than 0
            valid_input = True
        else:
            print('\nInvalid coordinate value entered.  Please try again.\n\n')

    return coordinate


def handle_phase_fold_next_step(time_period, resolution):
    print(f'\n\nThe time period for the last plot was {str(time_period)}')
    print(f'The current resolution being used is {str(resolution)}\n')
    valid_input = False
    # task_options = {'Get next plot': False, 'Increase resolution': False, 'Exit': False}
    while not valid_input:
        # print('Select the next step to take: ')
        for option_number, option in enumerate(phase_fold_next_step_options, 1):
            print(option_number, option.get('Name'))  # , f'[More information, {option.get("Info")}]')
            print('    I.e. ' + option.get('Info'))
        selected_option = int(input('\nSelect the next step to take from the options above (1, 2 or 3): '))

        if str(type(selected_option)) == "<class 'int'>":
            if 1 <= selected_option <= len(phase_fold_next_step_options):
                valid_input = True
                selected_option -= 1  # -1 to account for zero indexing

    return phase_fold_next_step_options[selected_option].get('Name')


def handle_saving_time_period_to_csv(time_period, catalogue_number):
    print(f'Do you want to save the time period ({str(time_period)}) for system {str(catalogue_number)}?')
    valid_input = False
    while not valid_input:
        user_selection = input('''y Save time period to csv\nn Do not save time period to csv\nRespond y/n: ''')
        if user_selection == 'y' or user_selection == 'n':
            valid_input = True

    if user_selection == 'y':
        # Get existing file, check for the catalogue number in column 1, update or add the time period in column 2
        try:
            existing_array = import_csv_file(system_parameters_csv_file_name + '.csv', 'Data_Exports/')
            transposed_array = transpose_2d_rows_separated_array_into_columns(existing_array)
            try:
                system_row_number = transposed_array[0].index(catalogue_number)
                # This system already has a value, update the time period
                transposed_array[1][system_row_number] = time_period
                # Write data back to csv
                write_to_csv(system_parameters_csv_file_name, 'Data_Exports', transposed_array)
            except ValueError:
                # This system does not already has a value, add a new row
                transposed_array[0].append(catalogue_number)
                transposed_array[1].append(time_period)
        except (OSError, IOError):
            # The file does not yet exist, write a new array to the csv
            write_to_csv(system_parameters_csv_file_name, 'Data_Exports', [[catalogue_number], [time_period]])

    return


def handle_time_period_input(catalogue_number):
    # Ask for time period
    valid_input = False
    while not valid_input:
        # Amend this to look up the time period from the csv file
        time_period = float(input(
            f'Input the accurate time period for system {catalogue_number} (e.g. 3.52254) : '))

        # Check that the period is a valid float and greater than 0
        if time_period != '' and str(type(time_period)) == "<class 'float'>" and time_period > 0:
            # Something was typed and it is a valid float larger than 0
            valid_input = True
        else:
            print('\nInvalid time period value entered.  Please try again.\n\n')

    return time_period


def handle_phase_fold_input_option():
    print(f'\n\nChoose an option from below')
    valid_input = False
    while not valid_input:
        for option_number, option in enumerate(phase_fold_input_options, 1):
            print(option_number, option.get('Name'))  # , f'[More information, {option.get("Info")}]')
            print('    I.e. ' + option.get('Info'))
        selected_option = int(input('\nSelect an option above (1 or 2): '))

        if str(type(selected_option)) == "<class 'int'>":
            if 1 <= selected_option <= len(phase_fold_input_options):
                valid_input = True
                selected_option -= 1  # -1 to account for zero indexing

    return phase_fold_input_options[selected_option].get('Name')


# ============================= GLOBAL VARIABLES ============================= #
phase_fold_input_options = [
    {'Name': 'Iterate period estimates', 'Info': 'Start with rough estimate for period and find accurate value'},
    {'Name': 'Phase fold accurate period',
     'Info': 'You already have an accurate period and just need a phase folded plot'}
]
phase_fold_next_step_options = [
    {'Name': 'Get next plot', 'Info': 'Get the next plot at the same resolution'},
    {'Name': 'Increase resolution',
     'Info': 'Increase resolution by factor of 10 and get plots around the previous value of the time period'},
    {'Name': 'Exit', 'Info': 'Exit the iteration'}
]
system_parameters_csv_file_name = 'System_Parameters'


# =============================== EXECUTION =============================== #
def main():
    print(headline('Process Started', '=', 100) + '\n')
    valid_input = False
    task_options = {'Get plot': False, 'Phase fold': False}
    while not valid_input:
        task_selection = int(input('''Specify task(s): \n1 Get a plot of a system only
2 Phase fold a plot only
3 Get a plot and phase fold it
Select an option from above by number (1, 2 or 3): '''))
        if str(type(task_selection)) == "<class 'int'>":
            if 1 <= task_selection <= 3:
                valid_input = True
                if task_selection == 3:
                    task_options['Get plot'] = True
                    task_options['Phase fold'] = True
                elif task_selection == 2:
                    task_options['Phase fold'] = True
                else:
                    task_options['Get plot'] = True

    # Use the Get plot value in dict to define whether user wants to plot
    # Data array is needed regardless of whether they want the plot
    catalogue_number_and_data = handle_catalogue_number_input(get_plot=task_options['Get plot'])

    if task_options.get('Phase fold'):
        catalogue_number = catalogue_number_and_data[0]
        data = catalogue_number_and_data[1]
        phase_fold_option = handle_phase_fold_input_option()
        if phase_fold_option == 'Iterate period estimates':
            time_coordinate_1 = handle_time_coordinate_input('first transit')
            time_coordinate_2 = handle_time_coordinate_input('last transit')

            finalised_time_period = time_period_iterator(
                catalogue_number,
                data,
                time_coordinate_1,
                time_coordinate_2,
                0.01
            )

            if finalised_time_period != 'N/A':
                finalised_time_period = float(str(finalised_time_period)[0:7])  # Shorten to 7 s.f.
                print('\n' + headline(f'Phase folding complete, finalised time period = {finalised_time_period}', '=', 100))
                handle_saving_time_period_to_csv(finalised_time_period, catalogue_number)
            else:
                print('\n' + headline(f'Phase folding ended', '=', 100))
        elif phase_fold_option == 'Phase fold accurate period':
            time_coordinate_1 = handle_time_coordinate_input('first transit')
            accurate_time_period = handle_time_period_input(catalogue_number)

            phase_fold_single_time_period(catalogue_number, data, time_coordinate_1, accurate_time_period)


main()
