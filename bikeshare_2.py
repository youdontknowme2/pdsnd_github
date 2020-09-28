import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input('Which city would you like to see the data? (Chicago, Washington, New York City): ')).lower()
            if city in ('chicago', 'new york city', 'washington'):
                print('\nWe\'ll get the data for {}.\n'.format(city.title()))
                break
            else:
                print('\nInvalid input: please use the name of the city shown in the brackets.\n')
        except:
            print('\nInvalid input: please use the name of the city shown in the brackets.\n')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input('Which month would you like to see the data? (All, January, February, March, April, May, June): ')).lower()
            if month in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
                print('\nWe\'ll get the data for {}.\n'.format(month.title()))
                break
            else:
                print('\nInvalid input: please use the name of the month shown in the brackets.\n')
        except:
            print('\nInvalid input: please use the name of the month shown in the brackets.\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input('Which day would you like to see the data? (All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday): ')).lower()
            if day in ('all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'):
                print('\nWe\'ll get the data for {}.\n'.format(day.title()))
                break
            else:
                print('\nInvalid input: please use the name of the day shown in the brackets.\n')
        except:
            print('\nInvalid input: please use the name of the day shown in the brackets.\n')

    print('-'*40)
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
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # display the most common month
    popular_month = df['month'].mode()[0]
    if popular_month == 1:
        month_name = 'January'
    elif popular_month == 2:
        month_name = 'February'
    elif popular_month == 3:
        month_name = 'March'
    elif popular_month == 4:
        month_name = 'April'
    elif popular_month == 5:
        month_name = 'May'
    elif popular_month == 6:
        month_name = 'June'
    print('The most popular month is {}.'.format(month_name))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most popular day is {}.'.format(popular_day))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular hour is {}:00.'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most popular start station is: ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most popular end station is: ', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_start_end_station = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('The most popular combination of start and end station is: ', popular_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time_hours = df['Trip Duration'].sum() / 60 / 60
    print('Total trip duration is {} hours.'.format(total_travel_time_hours))

    # display mean travel time
    mean_travel_time_hours = df['Trip Duration'].mean() / 60 / 60
    print('Average trip duration is {} hours.'.format(mean_travel_time_hours))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts()
    print(user_count)

    # Display counts of gender
    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print(user_gender)
    else:
        print('No gender data')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_yob = int(df['Birth Year'].min())
        most_recent_yob = int(df['Birth Year'].max())
        most_common_yob = int(df['Birth Year'].mode())
        print('The earliest birth year is {}.\nThe most recent birth year is {}. \nThe most common birth year is {}.'.format(earliest_yob, most_recent_yob, most_common_yob))
    else:
        print('No birth year data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Ask users if they want to see raw data until users indicate no
        raw_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if raw_data.lower() == 'yes':
            i = 0
            while True:
                print(df.iloc[i:i+5])
                i += 5
                more_data = input('\nWould you like to see 5 more lines of raw data? Enter yes or no.\n')
                if more_data.lower() != 'yes':
                    break
        elif raw_data.lower() != 'yes':
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
