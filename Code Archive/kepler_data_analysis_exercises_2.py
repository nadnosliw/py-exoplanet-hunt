# ================================== V.01 ================================== #
#
#
#
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

    filename = make_file_name_with_date(directory='Plots',
                                        name_stub=plot_type + ' plot for ' + system_number + ' - ',
                                        extension='.png')
    fig.savefig(filename)
    print('** Plot saved as "' + filename + '" **')


def write_to_csv(filename, path, data_list):
    # Transpose the data_list
    # transposed_data = list(zip(data_list))
    transposed_data = transpose_2d_data(data_list)
    filename_and_path = path + '/' + filename + '.csv'
    csv_file = open(filename_and_path, 'w+')  # w+ means create new file if doesn't exist
    list_length = len(transposed_data)
    with csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(transposed_data)
    print(headline(f'Data exported to {filename_and_path} with {str(list_length)} rows', width=100, symbol='*'))


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
def shift_data_by_half_period(data, period):
    # Data is a 2D array
    operand_array = [[period/2], [0]]  # Create a 2D array with half shift_value and 0
    return np.subtract(data, operand_array)  # Subtracts half shift_value from all data in first column


def perform_mod_on_array(data_array, period):
    # Data is a 2D array
    max_value = np.amax(data_array[1])
    # print(max_value)
    # Create a 2D array with shift_value and max value + 1 (modulo operation will return original num)
    operand_array = [[period], [max_value + 1]]
    return np.mod(data_array, operand_array)  # Calculates the division remainder of first column with shift_value


def transpose_2d_data(data_array):
    transposed_array = []
    for n in range(0, len(data_array[0])):
        transposed_array.append([data_array[0][n], data_array[1][n]])
    return transposed_array


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


def handle_phase_fold_input():
    valid_input = False
    while not valid_input:
        time_period = float(input(
            'Type the orbital time shift_value of the system (e.g. 3.117, 5.632) : '))

        # Check that the time_period is a valid float and greater than 0
        if time_period != '' and str(type(time_period)) == "<class 'float'>" and time_period > 0:
            # Something was typed and it is a valid float larger than 0
            valid_input = True
        else:
            print('\nInvalid time shift_value for the system.  Please try again.\n\n')

    return time_period


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

    if task_options['Phase fold']:
        time_period = handle_phase_fold_input()
        #print('shift_value: ' + str(time_period))
        data = catalogue_number_and_data[1]
        #print('data: ' + str(data))
        shifted_data = shift_data_by_half_period(data, time_period)
        #print('shifted data: ' + str(shifted_data))
        write_to_csv("shifted_data", '../Data_Exports', shifted_data)
        phase_folded_data = perform_mod_on_array(shifted_data, time_period)
        print('folded data: ' + str(phase_folded_data))
        write_to_csv("phase_folded_data", '../Data_Exports', phase_folded_data)
        shifted_phase_folded_data = shift_data_by_half_period(phase_folded_data, time_period)
        #print('shifted data 2: ' + str(shifted_phase_folded_data))
        write_to_csv("shifted_phase_folded_data", '../Data_Exports', shifted_phase_folded_data)
        generate_data_plot(shifted_phase_folded_data[0],
                           shifted_phase_folded_data[1],
                           catalogue_number_and_data[0],
                           'Phase folded')

    print('\n' + headline('Process Complete', '=', 100))


'test system: 006922244'
'002571238'
main()

