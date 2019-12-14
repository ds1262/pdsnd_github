import time
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
    cities = ('chicago', 'new york city', 'washington')
    months = ('January', 'February', 'March', 'April', 'May', 'June')
    days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
    filter = ('month', 'day', 'not at all')

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington)
    print("Would you like to see data for chicago, new york city, washington?")
    while True:
        city = input("Choose City > ")
        if city not in cities:
            pass
        else:
            break
    print("You have chosen:", city)

    # get user input to filter the data by month, day, or not at all
    print("Would you like to filter the data by month, day, or not at all?")
    while True:
        filter_choice = input("Choose Data Filter > ")
        if filter_choice not in filter:
            pass
        else:
            break
    print("You have chosen:", filter_choice)

    # get user input for month (january, february, ... , june)
    if filter_choice == filter[0]:
        print("Which month - January, February, March, April, May or June?")
        while True:
            month = input("Choose Month > ")
            if month not in months:
                pass
            else:
                break
        day = "all"
        print("You have chosen:", month)

    # get user input for day of week (monday, tuesday, ... sunday)
    if filter_choice == filter[1]:
        print("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?")
        while True:
            day = input("Choose Day > ")
            if day not in days:
                pass
            else:
                break
        month = "all"
        print("You have chosen:", day)

    if filter_choice == filter[2]:
        month = 'all'
        day = 'all'
    
    print("Data will be filtered by: ",city," ",month," ",day)
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
    #Load chosen data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    #Convert the Start time column to date time
    df['Start Time']=pd.to_datetime(df['Start Time'])

    #Create new columns for month and day
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #Filter dataframe by month if chosen
    if month != 'all':
        # use the index of the months list to get the month integer
        months = ('January', 'February', 'March', 'April', 'May', 'June')
        month=months.index(month) + 1
        df = df[df['month'] == month]
    
    #Filter dataframe by day if chosen
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Display the most common month, a way to describe the most common value in a column is the mode
    month_common = df['month'].mode()[0]
    print('Most common month #: ', month_common)

    #Display the most common day of week, a way to describe the most common value in a column is the mode
    day_common = df['day_of_week'].mode()[0]
    print('Most common day of the week: ', day_common)

    #Display the most common start hour
    #Extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    #Find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most common Start Station: ', start_station)

    #Display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most common End Station: ', end_station)

    #Display most frequent combination of start station and end station trip
    #Create a new column for combined start and end station
    df['Combined Station'] = df['Start Station'] + ' to ' + df['End Station']
    combined_station = df['Combined Station'].mode()[0]
    print('Most common Start and End Station combination: ', combined_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Display total trip duration
    total_trip = df['Trip Duration'].sum()
    print('Total trip duration: ', total_trip) 

    #Display mean travel time
    mean_trip = df['Trip Duration'].mean()
    print('Mean trip duration: ', mean_trip) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of each User Type:/n', user_types)

    #Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print('Count of each Gender:\n', gender)
    else:
        print('Count of each Gender:\n Sorry, Gender is not available for this city')

    #Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        year_earliest = df['Birth Year'].min()
        print('Earliest birth year: ', year_earliest)
    else:
        print('Earliest birth year: Sorry, Birth Year is not available for this city')
    
    if 'Birth Year' in df:
        year_recent = df['Birth Year'].max()
        print('Most recent birth year: ', year_recent)
    else:
        print('Most recent birth year: Sorry, Birth Year is not available for this city')
    
    if 'Birth Year' in df:
        year_common = df['Birth Year'].mode()
        print('Common birth year: ', year_common)
    else:
        print('Common birth year: Sorry, Birth Year is not available for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    #Display first five rows of data
    while True:
        view_data = input('Would you like to view the first five rows of data? Enter yes or no > ').lower()
        if view_data == 'yes':
            print('First five rows of data\n', df.head())
            break
        elif answer == 'no':
            break
        else:
            True

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()