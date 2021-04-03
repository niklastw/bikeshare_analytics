import time
import pandas as pd
import datetime

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    print("Please enter the name of the \033[4mcity\033[0m (Chicago, New York City, Washington) to filter by")
    while True:
        city = input().lower()
        if city not in CITY_DATA.keys():
            print("Please enter a valid city")
        else:
            break

    # get user input for month (all, january, february, ... , june)

    print("Please enter the name of the \033[4mmonth\033[0m (January - June) to filter by, or 'all' to apply no month filter")
    while True:
        month = input().lower()
        if month not in months:
            print("Please enter a valid month")
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)

    print("Please enter the name of the \033[4mday\033[0m to filter by, or 'all' to apply no day filter")
    while True:
        day = input().lower()
        if day not in days:
            print("Please enter a valid day")
        else:
            break

    print("You chose:\n")

    print("City: {}".format(city.title()))
    print("Month: {}".format(month.title()))
    print("Day: {}\n".format(day.title()))

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
        df - pandas DataFrame containing city data filtered by month and day
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

    # display the most common month
    print("Most Common Month: {}".format(df['month'].mode()[0]))

    # display the most common day of week
    print("Most Common Day: {}".format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print("Most Common Start Hour: {}".format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most Commonly Used Start Station: {}".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("Most Commonly Used End Station: {}".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' \033[4mto\033[0m ' + df['End Station']
    print("Most Frequent Combination of Start Station And End Station Trip: {}".format(df['Trip'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total Travel Time: {}".format(datetime.timedelta(seconds=df['Trip Duration'].sum().item())))

    # display mean travel time
    print("Mean Travel Time: {}".format(datetime.timedelta(seconds=df['Trip Duration'].mean().item())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of User Types:\n{}".format(df['User Type'].value_counts()))

    # Display counts of gender
    try:
        print("Counts of Gender:\n{}".format(df['Gender'].value_counts()))
    except:
        print("No Data of Gender Available")
    # Display earliest, most recent, and most common year of birth
    try:
        print("Earliest Year of Birth: {}".format(int(df['Birth Year'].min())))
        print("Most Recent Year of Birth: {}".format(int(df['Birth Year'].max())))
        print("Most Common Year of Birth: {}".format(int(df['Birth Year'].mode()[0])))
    except:
        print("No Data of Birth Year available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw(df):
    counter = 5
    print("Would You Like to See 5 Lines of Raw Data? Yes/No")
    while True:
        decision = input().lower()
        if decision == 'yes':
            print(df.head())
            break
        elif decision == 'no':
            break
        else:
            print("Please Enter a Valid Answer")
    while decision == 'yes':
        decision = input("Would You Like to See 5 more Lines? Yes/No\n").lower()
        if decision == 'yes':
            print(df[counter:counter + 5])
            counter += 5
        elif decision == 'no':
            break
        else:
            print("Please Enter a Valid Answer")
            decision = 'yes'


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
