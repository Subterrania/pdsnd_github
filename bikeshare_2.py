import time
import pandas as pd
import numpy as np

#Import colored logs and set the variables if the module is installed
try:
    import coloredlogs, logging
    color = 'yes'
except ModuleNotFoundError:
    color = None

if color is not None:
    coloredlogs.install(level='DEBUG')

    NOC = '\033[m'
    RED = '\033[1;31;40m'
    GREEN = '\033[1;32;40m'
    GREY = '\033[1;30;40m'
    CYAN = '\033[1;36;40m'
    YELLOW = '\033[1;33;40m'
else:
    print('To experience this program in more color, please install the coloredlog and logging modules.')
    NOC = ''
    RED = ''
    GREEN = ''
    GREY = ''
    CYAN = ''
    YELLOW = ''


#Define dictionaries with the possible month and day filters
months_dict = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}

days_dict = {
    'Mo': 1,
    'Tu': 2,
    'We': 3,
    'Th': 4,
    'Fr': 5,
    'Sa': 6,
    'Su': 7
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    def specify_filter(choice_str, choice, list_of_options):
        """
        Helper function that can be used to go through each filter in turn

        Args:
            (str) choice_str - name of the filter as a string to fill print()
            (var) choice - the filter variable that the user has to make a choice about, defaulted to None
            (list) list_of_options - the list the user gets to chose from concerning the filter
        """
        print('\nWhich ' + choice_str + ' are you interested in?\n')
        for elem in list_of_options:
            print(CYAN + elem, NOC)
        while choice not in list_of_options:
            choice = input('\nPlease select:').title()
            if choice in list_of_options:
                print('You selected {}'.format(choice))
            else:
                print('\nPlease select an option from the list.')
                for elem in list_of_options:
                    print(CYAN + elem, NOC)
        return choice

    print(GREEN + '-'*40, NOC)
    print(GREEN + 'Hello! Let\'s explore some US bikeshare data!', NOC)
    print(GREEN + '-'*40, NOC)

    city = None
    month = None
    day = None

    cities = ['Chicago', 'Washington', 'New York City']
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','All']
    days = ['Mo','Tu','We','Th','Fr','Sa','Su','All']

    city = specify_filter("city", city, cities)
    month = specify_filter("month", month, months)
    day = specify_filter("day", day, days)

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


    file = '{}.csv'.format(city.lower().replace(' ', '_'))

    print('loading {} data...'.format(file))

    df = pd.read_csv(file)

    if month != 'All':
        is_selected_month = pd.DatetimeIndex(df['Start Time']).month == months_dict[month]
        #print(is_selected_month)
        df = df[is_selected_month]

    if day != 'All':
        is_selected_day = pd.DatetimeIndex(df['Start Time']).dayofweek + 1 == days_dict[day]
        #print(is_selected_day)
        df = df[is_selected_day]


    return df



def time_stats(df):
    #Displays statistics on the most frequent times of travel.

    print(GREEN + '\nCalculating The Most Frequent Times of Travel...\n', NOC)
    start_time = time.time()

    # display the most common month and day of week
    df['Month'] = pd.DatetimeIndex(df['Start Time']).month
    df['Day of Week'] = pd.DatetimeIndex(df['Start Time']).dayofweek + 1
    df['Hour'] = pd.DatetimeIndex(df['Start Time']).hour

    try:
        most_freq_month = [month for month, id in months_dict.items() if id == df['Month'].value_counts().idxmax()][0]
        most_freq_day_of_week = [day for day, id in days_dict.items() if id == df['Day of Week'].value_counts().idxmax()][0]
    except ValueError:
        print('The selection you have made is empty.')
        print('-'*40)
        return

    print('Most common month for the selected time frame: {}'.format(most_freq_month))
    print(YELLOW + '-'*20, NOC)
    print('\nMost common day for the selected time frame: {}'.format(most_freq_day_of_week))
    print(YELLOW + '-'*20, NOC)

    # display the most common start hour
    most_freq_hour = df['Hour'].value_counts().idxmax()
    print('\nMost journeys were started between {}:00 and {}:00'.format(most_freq_hour, most_freq_hour + 1))

    print(GREY + '\nThis took %s seconds.' % round((time.time() - start_time),2), NOC)
    print('-'*40)


def station_stats(df):
    #Displays statistics on the most popular stations and trip.

    print(GREEN + '\nCalculating The Most Popular Stations and Trip...\n', NOC)
    start_time = time.time()

    try:
        # display most commonly used start station
        most_freq_start_station = df['Start Station'].value_counts().idxmax()
        print('The most common start station for the selected time frame was {}.'.format(most_freq_start_station))
        print(YELLOW + '-'*20, NOC)
        # display most commonly used end station
        most_freq_end_station = df['End Station'].value_counts().idxmax()
        print('\nThe most common end station for the selected time frame was {}.'.format(most_freq_end_station))
        print(YELLOW + '-'*20, NOC)
        # display most frequent combination of start station and end station trip
        df['Route'] = np.where(df['Start Station'] == df['End Station'], 'a roundtrip starting and ending at ' + df['Start Station'], df['Start Station'] + ' to ' + df['End Station'])
        most_freq_route = df['Route'].value_counts().idxmax()
        print('\nThe most frequently traveled route for the selected time frame was {}.'.format(most_freq_route))
    except ValueError:
        print('The selection you have made is empty.')
        print('-'*40)
        return

    print(GREY + '\nThis took %s seconds.' % round((time.time() - start_time),2), NOC)
    print('-'*40)


def trip_duration_stats(df):
    #Displays statistics on the total and average trip duration.

    print(GREEN + '\nCalculating Trip Duration...\n', NOC)
    start_time = time.time()


    df['Travel Time'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
    df2 = df[['Start Time', 'End Time', 'Travel Time']]
    df2 = df2[df['Travel Time'].dt.days>=0]

    try:
        # display mean travel time
        mean_tt = df2['Travel Time'].mean().round('S')
        print('The average journey in the selected time frame took {} days {} hours {} minutes and {} seconds.'.format(mean_tt.days, round(mean_tt.seconds/3600), round((mean_tt.seconds%3600)/60), (mean_tt.seconds%3600)%60))
        print(YELLOW + '-'*20, NOC)
        # display total travel time
        sum_tt = df2['Travel Time'].sum()
        print('\nThe journeys in the selected time frame amount to a total travel time of {} days {} hours {} minutes and {} seconds.'.format(sum_tt.days, round(sum_tt.seconds/3600), round((sum_tt.seconds%3600)/60), (sum_tt.seconds%3600)%60))
    except ValueError:
        print('The selection you have made is empty.')
        print('-'*40)
        return

    print(GREY + '\nThis took %s seconds.' % round((time.time() - start_time),2), NOC)
    print('-'*40)


def user_stats(df):
    #Displays statistics on bikeshare users.

    print(GREEN + '\nCalculating User Stats...\n', NOC)
    start_time = time.time()

    # Display counts of user types
    print('Types of users:\n')
    user_types = df['User Type'].value_counts()
    for user_type, amount in user_types.iteritems():
        print(user_type, amount)
    print(YELLOW + '-'*20, NOC)

    # Display counts of gender
    print('\nGender of users:\n')
    try:
        genders = df['Gender'].fillna('Unknown').value_counts()
        for gender, amount in genders.iteritems():
            print(gender, amount)
        print(YELLOW + '-'*20, NOC)
    except KeyError:
        print('There is no gender data available for your selection.')
        print(YELLOW + '-'*20, NOC)

    # Display earliest, most recent, and most common year of birth
    print('\nBirth year of users:\n')
    try:
        oldest_user = int(df['Birth Year'].dropna().min())
        youngest_user = int(df['Birth Year'].dropna().max())
        most_common_year = int(df['Birth Year'].dropna().value_counts().idxmax())
        print('The oldest user in your selection was born in {} and the youngest in {}. Most users in your selection were born in {}.'.format(oldest_user, youngest_user, most_common_year))
        print(YELLOW + '-'*20, NOC)
    except KeyError:
        print('There is no data about birth year available for your selection.')
        print(YELLOW + '-'*20, NOC)

    print(GREY + '\nThis took %s seconds.' % round((time.time() - start_time),2), NOC)
    print('-'*40)

def display_data(df):
    # Displays the raw data from the dataset to the user in 5 row increments
    print(YELLOW + 'Would you like to see the raw data?' + NOC + '\n')
    incrementer = 0
    df_length = len(df.index)
    while True:
        show_data = input('Press "Enter" to see 5 lines of raw data or type' + RED + ' "end" ' + NOC + 'to stop looking at data.\n').lower()
        if(show_data == 'end'):
            break
        incrementer += 5
        print(df.iloc[incrementer-5:incrementer])
        if(incrementer - df_length >= 0):
            print('You have reached the end of the dataset.')
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        print('\nWould you like to restart? Enter' + CYAN + ' yes ' + NOC + 'to restart.\n')
        restart = input('')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
