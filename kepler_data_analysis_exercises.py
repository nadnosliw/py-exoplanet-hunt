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


def generate_data_plot(x, y, system_number):
    fig = plt.figure()  # Initialise the figure for plotting onto
    plt.plot(x, y, 'r+')
    plt.show()

    filename = make_file_name_with_date(directory='Plots', name_stub='plot for ' + system_number + ' - ', extension='.png')
    fig.savefig(filename)
    print('** Plot saved as "' + filename + '" **')


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


# =============================== EXECUTION =============================== #
def main():
    print(headline('Process Started', '=', 100) + '\n')
    valid_input = False
    while not valid_input:
        catalogue_number = input('Type the Kepler Input Catalogue (KIC) number of the system (e.g. 002571238) : ')
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
            
            if data != -1:
                # Data was extracted
                generate_data_plot(data[0], data[1], catalogue_number)
                valid_input = True

    print('\n' + headline('Process Complete', '=', 100))


'002571238'
main()
