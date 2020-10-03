from typing import Any

import numpy as np
import pandas as pd
import time
import statistics as st
import json

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
          'September', 'October', 'November',
          'December']

DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

TIME_FILTERS = ['month', 'day', 'both', 'none']


def print_counts(df, index_header):
    measurer = np.vectorize(len)
    index_cell_size = measurer(df.index.astype(str)).max(axis=0)
    value_cell_size = max(measurer(df.values.astype(str)).max(axis=0), len('Count'))
    print_index_header = index_header.ljust(index_cell_size)
    print_count_header = 'Count'.ljust(value_cell_size)
    header_seperator = '=' * (index_cell_size + value_cell_size + 7)
    line_seperator = '-' * (index_cell_size + value_cell_size + 7)
    print(header_seperator)
    print('| {} | {} |'.format(print_index_header, print_count_header))
    print(header_seperator)
    for ind in range(0, df.index.size):
        print_index = df.index[ind].ljust(index_cell_size)
        print_value = df.values[ind].astype(str).ljust(value_cell_size)
        print('| {} | {} |'.format(print_index, print_value))
        print(line_seperator)
    print('\n')


def read_input(user_message, input_type):
    """
    Reads the user data and validates it according the input type.
    If user data is invalid according to the input type, the use is requested to enter data again

    Input:
        user_message: The message to present to the user
        input_type: The type of data the user chose

    Returns:
        The user's input data

    """
    while True:
        user_input = input(user_message)
        if input_type == 'city':
            user_data = str(user_input).lower()
            if user_data in CITY_DATA.keys():
                return user_data
        if input_type == 'time filter':
            user_data = str(user_input).lower()
            if user_data in TIME_FILTERS:
                return user_data
        elif input_type == 'month':
            try:
                user_data = int(user_input)
                month_range = range(1, 12)
                if user_data in month_range:
                    return MONTHS[user_data - 1].lower()
            except ValueError:
                user_data = str(user_input).lower()
                if user_data.title() in MONTHS:
                    return user_data
                elif user_data == 'all':
                    return user_data
        else:
            try:
                user_data = int(user_input)
                day_range = range(1, 7)
                if user_data in day_range:
                    return DAYS[user_data - 1].lower()
            except ValueError:
                user_data = str(user_input).lower()
                if user_data.title() in DAYS:
                    return user_data
                elif user_data == 'all':
                    return user_data
        print('Incorrect {} provided, please try again\n'.format(input_type))


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        Data returned is always in lowercase to avoid further checks
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington).
    city = read_input('Would you like to see data for Chicago, New York City or Washington?\n', 'city')

    filter = read_input(
        'Would you like to filter the data by month, day, both or not at all? Type "none" for no time filter\n',
        'time filter')

    month = 'all'
    day = 'all'

    # No time filter - get data for all months and days
    if filter == 'none':
        print('You requested data for {} with no time filter.'.format(city.title()))
        return city, 'all', 'all'

    if filter.lower() == 'both' or filter.lower() == 'month':
        month = read_input('Which month do you want to filter by: {} or All? (You can use month\' index)\n'.format(
            str(MONTHS).strip('[]')), 'month')

    if filter.lower() == 'both' or filter.lower() == 'day':
        day = read_input(
            'Which day do you want to filter by: {} or All? (You can use days\' index)\n'.format(str(DAYS).strip('[]')),
            'day')

    if month != 'all':

        month_msg = month.title()
    else:
        month_msg = 'All months'

    if day != 'all':
        day_msg = day.title()
    else:
        day_msg = 'All days'

    print('You requested data for {}, at {} for {}.'.format(city.title(), month_msg, day_msg))

    print('-' * 80)
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
    df = pd.read_csv(CITY_DATA[city], low_memory=False)
    df.drop(axis=0, index=0, inplace=True)
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    if month != 'all':
        df['month'] = pd.DatetimeIndex(df['Start Time']).month_name()
        df = df[df['month'] == month.title()]

    if day != 'all':
        df['week_day'] = pd.DatetimeIndex(df['Start Time']).day_name()
        df = df[df['week_day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = pd.DatetimeIndex(df['Start Time']).month_name()
    month_counts = df['month'].value_counts()
    common_month = month_counts.index[0]
    common_month_count = month_counts.values[0]

    # display the most common day of week
    df['week_day'] = pd.DatetimeIndex(df['Start Time']).day_name()
    weekday_counts = df['week_day'].value_counts()
    common_week_day = weekday_counts.index[0]
    common_week_day_count = weekday_counts.values[0]

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    hour_counts = df['hour'].value_counts()
    common_hour = hour_counts.index[0]
    common_hour_count = hour_counts.values[0]

    print("Most frequent month is '{}' with {} counts.".format(common_month, common_month_count))
    print("Most frequent week day is '{}' with {} counts.".format(common_week_day, common_week_day_count))
    print("Most frequent hour is '{}' with {} counts.".format(common_hour, common_hour_count))

    elapsed_time = round(float(time.time() - start_time), 2)
    print("\nThis took %s seconds." % elapsed_time)
    print('-' * 80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_counts = df['Start Station'].value_counts()
    common_start_station = start_station_counts.index[0]
    common_start_station_count = start_station_counts.values[0]

    # display most commonly used end station
    end_station_counts = df['End Station'].value_counts()
    common_end_station = end_station_counts.index[0]
    common_end_station_count = end_station_counts.values[0]

    # display most frequent combination of start station and end station trip
    df['station_combination'] = df['Start Station'] + ',' + df['End Station']
    station_combination_counts = df['station_combination'].value_counts()
    common_station_combination = station_combination_counts.index[0]
    common_station_combination_count = station_combination_counts.values[0]
    station_combination_names = common_station_combination.split(',')

    print("Most popular start station is '{}' with {} counts.".format(common_start_station, common_start_station_count))
    print("Most popular end station is '{}' with {} counts.".format(common_end_station, common_end_station_count))
    print("Most popular start and end station combination is: start at '{}' and end at '{}' with {} counts."
          .format(station_combination_names[0], station_combination_names[1], common_station_combination_count))

    elapsed_time = round(float(time.time() - start_time), 2)
    print("\nThis took %s seconds." % elapsed_time)
    print('-' * 80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Trip Duration'] = df['Trip Duration'].astype(float)

    # display total travel time
    avg_trip_duration = round(sum(df['Trip Duration']) / len(df), 2)
    print("Average travel duration is '{}' sec.".format(avg_trip_duration))

    # display mean travel time
    mean_trip_duration = round(st.mean(df['Trip Duration']), 2)
    print("The travel mean duration is '{}' sec.".format(mean_trip_duration))

    elapsed_time = round(float(time.time() - start_time), 2)
    print("\nThis took %s seconds." % elapsed_time)
    print('-' * 80)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].fillna('No Information').value_counts()
    print_counts(user_types, 'User types')

    # Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].fillna('No Information').value_counts()
        print_counts(genders, 'Gender')
    else:
        print("\nNo Gender information provided")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        recent_birth_year = int(pd.DataFrame.max(df['Birth Year']))
        earliest_birth_year = int(pd.DataFrame.min(df['Birth Year']))
        most_common_birth_year = int(df['Birth Year'].value_counts().index[0])
        most_common_birth_year_count = df['Birth Year'].value_counts().values[0]

        print("Birth Year information:")
        print("Most Recent Birth Year is: {}".format(recent_birth_year))
        print("Most Earliest Birth Year is: {}".format(earliest_birth_year))
        print("Most Common Birth Year is: {} with {} counts.".format(most_common_birth_year,
                                                                     most_common_birth_year_count))
    else:
        print("\nNo Birth Year information provided")

    elapsed_time = round(float(time.time() - start_time), 2)
    print("\nThis took %s seconds." % elapsed_time)
    print('-' * 80)


def trip_data(df):
    """Display trip data - shows 5 records each time."""

    data_limit = 5
    start_data = 0
    total_line_number = len(df.index)
    while True:
        show_trip_data = input('\nWould you like to see trip data (showing 5 records at a time)? Enter yes or no.\n')
        if show_trip_data.lower() != 'yes':
            break
        elif start_data < total_line_number:
            limit = start_data + data_limit
            if (start_data + data_limit) > total_line_number:
                limit = total_line_number - start_data
            df_to_print = df.iloc[start_data:limit, 1:]
            json_records = df_to_print.to_json(orient="records")
            json_records_parsed = json.loads(json_records)
            print('Showing trip data for rows {} to {}.'.format(start_data + 1, limit))
            print(json.dumps(json_records_parsed, indent=4))
            start_data += limit


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        trip_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
