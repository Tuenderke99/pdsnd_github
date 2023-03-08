# Import necessary libraries
import time
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Define dictionary for city data files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Define function to get user inputs for city, month, and day
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Loop until valid city name is entered
    while True:
        city = input('Enter the name of the city you are looking for (chicago, new york city, washington):').lower()
        if city in CITY_DATA:
            break
        else:
            print('Oops, guess you have choosen an invalid input. Please enter a valid city name.')
        
    # Loop until valid month is entered
    while True:
        month = input('Now enter the name of the month you are looking for (all, january, february, ... , june):').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('Invalid input. "\U0001F605" Please enter a valid month name.')

    # Loop until valid day is entered
    while True:
        day = input('Last enter the name of the day of the week you want to analyze (all, monday, tuesday, ... sunday): ').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print('Please enter a valid day of the week like "firday"')

    print('-'*40)
    return city, month, day

# Define function to load data for specified city and filter by month and day
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
    # Load data from file based on city name
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)
    
    # Filter data by month if applicable
    if month != 'all':
        # Convert Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # Extract month from Start Time column
        df['month'] = df['Start Time'].dt.month_name()

        # Filter data by selected month
        df = df[df['month'] == month.title()]

    # Filter data by day of week if applicable
    if day != 'all':
        # Convert Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # Extract day of week from Start Time column
        df['day of week'] = df['Start Time'].dt.day_name()

        # Filter data by selected day of week
        df = df[df['day of week'] == day.title()]
    
    return df

# Define time_stats function
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # Convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract month, day of week, and start hour from Start Time column
    df['month'] = df['Start Time'].dt.month_name()
    df['day of week'] = df['Start Time'].dt.day_name()
    df['start hour'] = df['Start Time'].dt.hour
    
    # Calculate and print most common month, day of week, and start hour
    common_month = df['month'].mode()[0]
    print('Most Common month:', common_month)
    common_day = df['day of week'].mode()[0]
    print('Most Common day of week:', common_day)
    common_hour = df['start hour'].mode()[0]
    print('Most Commonstart hour:', common_hour)
    
    # Promt user to display raw data
    raw_data_index = 0
    while True:
        raw_data = input('\nDo you want to see some raw data? Enter yes or no.\n').lower()
        if raw_data == 'yes':
            print(df.iloc[raw_data_index:raw_data_index + 5])
            raw_data_index += 5
        elif raw_data == 'no':
            break
        else:
            print('Invalid input. Please enter yes or no.')
            pd.set_option("display.max_columns", 200)
            
    # Create bar chart of trip counts by month
    trip_counts = df['month'].value_counts()
    trip_counts = trip_counts.reindex(['January', 'February', 'March', 'April', 'May', 'June'])
    
    trip_counts.plot(kind='bar')
    plt.title('Number of trips by month')
    plt.xlabel('Month')
    plt.ylabel('Number of trips')
    plt.show()
            
    # Print total execution time of function
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
# Define station_stats function
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Calculate the most common start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station: {}'.format(most_common_start_station))

    # Calculate the most common end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station: {}'.format(most_common_end_station))

    # Calculate the most frequent combination of start and end stations
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    most_common_trip = df['Trip'].mode()[0]
    print('The most frequent combination of start station and end station trip: {}'.format(most_common_trip))
    
    # Print the time taken to complete this calculation
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
# Define trip_duration_stats function
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_hours = total_travel_time / 3600
    print('Total travel time: {:.2f} hours'.format(total_travel_time_hours))

    # Calculate mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time_minutes = mean_travel_time / 60
    print('Mean travel time: {:.2f} minutes'.format(mean_travel_time_minutes))
    
    # Print how long the function took to run
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

# Define user_stats function
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Calculating and displaying the number of user types
    user_types = df['User Type'].value_counts()
    print('Number of user types:\n{}'.format(user_types))

    # Calculate and display the counts of genders, if 'Gender' column exists
    try:
        gender_counts = df['Gender'].value_counts()
        print('\nCounts of genders:\n{}'.format(gender_counts))
    except KeyError:
        print('No data available for the selected city')

    # Calculate and display earliest, most recent, and most common birth years, if 'Birth Year' column exists
    try:
        earliest_birth_year = df['Birth Year'].min()
        print('\nEarliest birth year: {}'.format(int(earliest_birth_year)))
        most_resent_birth_year = df['Birth Year'].max()
        print('\nMost resent birth year: {}'.format(int( most_resent_birth_year)))
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('\nMost common birth year: {}'.format(int(most_common_birth_year)))
    except KeyError:
        print('Sorry no data available')
        
    # Displaying the time taken for the calculations to complete
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Define main function
def main():
    while True:
        city, month, day = get_filters()    # User input and filters 
        df = load_data(city, month, day)    # Loading data
        time_stats(df)                      # Statistics on the most frequent times of travel 
        station_stats(df)                   # Statistics on the most popular stations and trip
        trip_duration_stats(df)             # Statistics on the total and average trip duration
        user_stats(df)                      # Statistics on bikeshare users

        restart = input('\nWould you like to restart? Enter yes or no.\n') # Restart prompt and loop
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
