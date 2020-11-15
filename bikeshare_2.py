import time
import pandas as pd
import numpy as np

# attachment name and directory
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # user input for city (chicago, new york city, washington).
    # while loop to handle invalid inputs, break when input match key from CITY_DATA
    while True:
        city = input('Please enter city name (chicago, new york city, washington): ').lower()
        if city in CITY_DATA.keys():
            break
        else:
            print('Invalid input')

    # user input for month (all, january, february, ... , june)
    # while loop to handle invalid inputs, break when input match key from months

    while True:
        month = input(
            'To filter by certain month, enter month name. Enter all for no filter (all, january, february, ... , june): ').lower()
        if month in months:
            break
        else:
            print('Invalid input')

    # user input for day of week (all, monday, tuesday, ... sunday)
    # while loop to handle invalid inputs, break when input match key from days

    while True:
        day = input('To filter by certain day, enter day name. Enter all for no filter (all, monday, tuesday, ... , sunday): ').lower()
        if day in days:
            break
        else:
            print('Invalid input')

    print('\nFiltering with: \nCity: {}, Month: {}, Day: {}'.format(city.title(), month.title(), day.title()))

    # return valid input
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # return filtered DataFrame
    return df


def display_raw_data(df):
    """
    Asks user if he wants to show the raw data,
    if yes, show 5 rows then asks show more rows
        if showed data then user don't want to see more rows, asks if he wants to see stats about the data, return True or False to continue rest of code
    if no, proceed directly to show stats about the data, return True
    Parameters
    ----------
    df : DataFrame
        the loaded data.

    Returns
    -------
    is_run_rest : Bool
        Continue rest of the functions or not.

    """
    # i, row counter
    i = 0

    # input to show data or directly to stats and convert it to lower case using lower() function
    raw = input("Do you want to show the data table (yes or no): ").lower()
    pd.set_option('display.max_columns', 200)

    # initial values if raw data are displayed, if user want to continue with rest of function
    raw_displayed = False
    is_run_rest = False

    while True:
        # if user input is no, check if data were displayed before or not
        if raw == 'no':
            # if data were displayed, check if user want to stop or show stats
            if raw_displayed:
                print('-' * 40)
                run_rest = input('do you want to show stats about the station: ').lower()

                if run_rest == 'yes':
                    is_run_rest = True
                else:
                    is_run_rest = False
            # if data were not displayed, proceed to show data stats without asking the user
            else:
                is_run_rest = True
            break
            # if user input is yes, show 5 rows and ask to show more or stop
        elif raw == 'yes':
            print(df[i:i + 5])
            raw = input('want to show more rows: ')  # then convert the user input to lower case using lower() function
            i += 5
            raw_displayed = True
        else:
            raw = input('Invalid input, please use yes or no: ').lower()

    # return to run rest of code or skip it
    return is_run_rest


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # TODO- don't show this if filtering by month
    travel_month_name = months[df['month'].mode()[0]].title()
    print('Most common travel month is: {}'.format(travel_month_name))

    # display the most common day of week
    print('Most common travel day is: {}'.format(df['day_of_week'].mode()[0].title()))

    # display the most common start hour
    print('Most common starting travel hour is: {}'.format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    # TODO: add count / total
    print('Most common starting station: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    # TODO: add count / total
    print('Most common end station: {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    # TODO: add count / total
    df['route'] = df['Start Station'] + ' -to- ' + df['End Station']
    print('Most common travel route : {}'.format(df['route'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time is: {} seconds'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('Average travel time is: {} seconds'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # Try Except to avoid if missing users info
    try:
        user_types = df['User Type'].value_counts()
        # print each type in separate line
        for i in range(user_types.size):
            print('Total number of {}s are: {}'.format(user_types.index[i], user_types[i]))
    except:
        print('No information about users found')

    # Display counts of gender
    # Try, Except to avoid if missing gender info
    try:
        print('')
        user_genders = df['Gender'].value_counts()
        # print each gender in separate line
        for i in range(user_genders.size):
            print('Total number of {}s are: {}'.format(user_genders.index[i], user_genders[i]))
    except:
        print('No information about gender found')

    # Display earliest, most recent, and most common year of birth
    try:
        print('')
        print('Oldest user birth year is: {}'.format(int(df['Birth Year'].min())))
        print('Youngest user birth year is: {}'.format(int(df['Birth Year'].max())))
        print('Most users birth year is: {}'.format(int(df['Birth Year'].mode()[0])))
    except:
        print('No information about birth year found')

    # End calculations
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        start_time = time.time()
        df = load_data(city, month, day)

        # df = load_data('chicago', 'all', 'all')
        print("\nLoading took %s seconds." % (time.time() - start_time))
        print('-' * 40)

        # run display_raw_data then return check to display rest of functions
        if display_raw_data(df):
            print('-' * 40)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        restart = input('\nWould you like to restart?  (yes or no):.\n').lower()
        if restart == 'no':
            print('Thanks and goodbye')
            print('-' * 60)
            break


if __name__ == "__main__":
    main()
