#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pandas as pd
import numpy as np
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# In[2]:


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
        city = input('Please input a city name (chicago, new york city, washington): ' ).lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print('invalid city name, please choose the city in chicago, new york city or washington')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Please input a month (all, january, february, ... , june): ' ).lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('invalid month, please choose the month in (all, january, february, ... , june)')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
            day = input('Please input a day of week (all, monday, tuesday, ... sunday): ' ).lower()
            if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                break
            else:
                print('invalid day of week, please choose the day of week in (all, monday, tuesday, ... sunday)')

    print('-'*40)
    return city, month, day


# In[3]:


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


# In[4]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month is: '+ str(df.groupby('month')['month'].count().idxmax()))

    # display the most common day of week
    print('The most common day of week is: ' + df.groupby('day_of_week')['day_of_week'].count().idxmax())

    # display the most common start hour
    df['hour_of_day'] = df['Start Time'].dt.hour
    print('The most common start hour is: ' + str(df.groupby('hour_of_day')['hour_of_day'].count().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[5]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is: '+ str(df.groupby('Start Station')['Start Station'].count().idxmax()))

    # display most commonly used end station
    print('The most commonly used end station is: '+ str(df.groupby('End Station')['End Station'].count().idxmax()))

    # display most frequent combination of start station and end station trip
    df['Start to End'] = df['Start Station'] + " -> " + df['End Station']
    print('The most common start to end combo is: ' + str(df.groupby('Start to End')['Start to End'].count().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[6]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time is: ' + str(df['Trip Duration'].sum() / 60) + ' min')

    # display mean travel time
    print('Average travel time is: ' + str(df['Trip Duration'].mean() / 60) + ' min')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[37]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCounts of user types are:')
    print(df['User Type'].value_counts())

    # Display counts of gender
    try:
        print('\nCounts of genters are:')
        print(df['Gender'].value_counts())
    except KeyError:
        print('Sorry, counts of gender data only supports in chicago and NYC')

    # Display earliest, most recent, and most common year of birth
    try:
        print('\nThe earliest year of birth is: ' + str(int(df['Birth Year'].min())))
        print('The most recent year of birth is: ' + str(int(df['Birth Year'].max())))
        print('The most common year of birth is: ' + str(int(df['Birth Year'].mode()[0])))
    except KeyError:
        print('Sorry, day of birth data only supports in chicago and NYC')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[38]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        n = 0
        while n < df['Start Time'].count():
            rawdata = input('\nWOuld you like to see individual trip data? Enter yes or no.\n')
            if rawdata.lower() == 'yes':
                print(df.loc[df.index[n:n+5]])
                n += 5
            else: break


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
