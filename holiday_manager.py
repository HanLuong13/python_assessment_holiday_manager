import json
from bs4 import BeautifulSoup as soup
import requests
from datetime import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager 
from splinter import Browser
from datetime import date as date_import

class Holiday:
    """Holiday class"""          
    def __init__(self, name, date):     
        self.name = name
        self.date = date 

    def __getitem__(self, name):
        return getattr(self, name)

    
    def __getitem__(self, date):
        return getattr(self, date)

    def __str__(self):
        # String output
        # Holiday output when printed.
        return (f'{self.name} ({self.date})')    
        
    def __eq__(self, other):
        if self.name == other.name and self.date == other.date:
            return True
        else:
            return False

          
           
# -------------------------------------------
# The Holiday_List class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class Holiday_List:

    """Holiday_List class"""   
    def __init__(self):
        self.inner_holidays = []
   
    def add_holiday(self, holiday_obj):
        # Make sure holiday_obj is an Holiday Object by checking the type
        # Use inner_holidays.append(holiday_obj) to add holiday
        # system adding holidays, not printing output

        if isinstance(holiday_obj, Holiday):
            if not holiday_obj in self.inner_holidays:
                holiday_obj.date = dt.strptime(holiday_obj.date, '%Y-%m-%d')
                holiday_obj.date = holiday_obj.date.date() #not keeping the time part.
                holiday_obj.date = str(holiday_obj.date)
                self.inner_holidays.append(holiday_obj)


    def user_add_holiday(self, holiday_obj):
        # Make sure holiday_obj is an Holiday Object by checking the type
        # Use inner_holidays.append(holiday_obj) to add holiday
        # print to the user that you added a holiday

        try:
            if isinstance(holiday_obj, Holiday):
                try:
                    if not holiday_obj in self.inner_holidays:
                        holiday_obj.date = dt.strptime(holiday_obj.date, '%Y-%m-%d')
                        holiday_obj.date = holiday_obj.date.date() #not keeping the time part.
                        holiday_obj.date = str(holiday_obj.date)
                        self.inner_holidays.append(holiday_obj)
                        print(f'\nSuccess: \n{holiday_obj} has been added to the holiday list.')
                    else: 
                        print(f'\n{holiday_obj} is already in the holiday list. Please try again')
                except ValueError:
                    print('\nError: \nInvalid date.  Please try again.')                
        except TypeError:
            print('\nNot a holiday')


    def scrape_holidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in inner_holidays array
        # Add non-duplicates to inner_holidays
        # Handle any exceptions - work on with more time

        global year_list
        try:
            executable_path = {'executable_path': ChromeDriverManager().install()}
            browser = Browser('chrome', **executable_path, headless=False)

            for year in year_list:
                holiday_url = 'https://www.timeanddate.com/holidays/us/'
                holiday_url = holiday_url + year
                browser.visit(holiday_url)
                html = browser.html
                html_soup = soup(html, 'html.parser')
                for tr in html_soup.find_all('tr', class_='showrow'):
                    title = tr.find('a')
                    date = tr.find('th', class_='nw')
                    if title != None and date != None:

                        title = title.text
                        date = date.text

                        str_date = str(date) + ' ' + year
                        date = dt.strptime(str_date, '%b %d %Y')
                        date = date.date() #not keeping the time part.
                        date = str(date)
                        new_obj = Holiday(title, date)
                        self.add_holiday(new_obj)
        except:
            print('Error in web scraping. Recheck and or retry.')

    def read_json(self, file_location):
        # Read in things from json file location
        # Use add_holiday function to add holidays to inner list.

        f = open(file_location)
        holiday_starter= json.load(f)
        for record in holiday_starter['holidays']:
            new_obj = Holiday(record['name'], record['date'])
            self.add_holiday(new_obj)

    def save_to_json(self, file_location):
        json_ver = {'holidays': []}
        # Write out json file to selected file.
        for item in self.inner_holidays:
            json_ver['holidays'].append({'name': item.name, 'date': item.date})
        with open(file_location, 'w') as f:
            json.dump(json_ver, f)

    def num_holidays(self):
        # Return the total number of holidays in inner_holidays
        count = 0
        for item in self.inner_holidays:
            count += 1
        return count

    def display_holidays(self):
        # Display holidays
        for item in self.inner_holidays:
            print(item)

    def find_holiday(self, holiday_obj):
        # Find Holiday in inner_holidays
        # Return Holiday
        holiday_exists = False
        
        if holiday_obj in self.inner_holidays:
            holiday_exists = True
        return holiday_exists

    def remove_holiday(self, holiday_obj):
        # Find Holiday in inner_holidays by searching the name and date combination.
        # remove the Holiday from inner_holidays
        # inform user you deleted the holiday

        if self.find_holiday(holiday_obj): 
            for holiday in self.inner_holidays:
                if holiday['name'] == holiday_obj.name and holiday['date'] == holiday_obj.date:
                    self.inner_holidays.remove(holiday)
                    print(f'\nSuccess: \n{holiday_obj} has been removed from the holiday list.')

        else:
            print(f'\nError: \n{holiday_obj} not found. Try again.')

    def filter_holidays_by_week(self, year_input, week_input):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on inner_holidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return filtered holidays 

        def find_week(date): 
            week = dt.strptime(date, '%Y-%m-%d').strftime('%U')
            if week == week_input:
                return True
            else:
                return False

        filtered_holidays = list(filter(lambda record: (year_input in record['date'] and find_week(record['date'])), self.inner_holidays))

        return filtered_holidays


    def get_weather(self):
        # Convert week_num to range between two days - done in main
        # Use Try / Except to catch problems - work on with more time
        # Query API for weather in that week range 
        # Added - only works for current week
        # Return weather as a list
        try:
            weather_list = []
            weather_url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"

            querystring = {"q":"minneapolis,us","lat":"35","lon":"139","cnt":"10","units":"imperial"}

            headers = {
                "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
                "X-RapidAPI-Key": "c0ae9adf37msh978e0eae2373a1dp173f69jsn731e4a7f9ad7"
            }

            response = requests.request("GET", weather_url, headers=headers, params=querystring)
            weather_response = response.json()
            for record in weather_response['list']:
                weather_date = dt.fromtimestamp(record['dt']).date()
                for record2 in record['weather']:
                    description = record2['description']
                    weather_list.append({'weather_date': weather_date.strftime('%Y-%m-%d'), 'description' : description})
        except:
            print('Error in web scraping. Recheck and or retry.')

        return weather_list


    def view_and_display_current_week(self, weather_list):
        # Look for weather description in weather list to match up with week's holiday
        # Print out holidays along with weather description
        
        print('\nThese are the holidays upcoming days in this week with weather.')
        for holiday_record in self.inner_holidays:
            for weather_record in weather_list:
                if weather_record['weather_date'] == holiday_record['date']:
                    description = weather_record['description']
                    print(f'{holiday_record} - {description}') 

    def create_filtered_holiday_list(self, filtered_holiday_list, year_input, week_input):
        #create holiday objects to add to holiday list object
        #prepare to display holidays in year and week

        if len(filtered_holiday_list) == 0:
            print('\nThere are no holidays in that week. :(')
        elif len(filtered_holiday_list) > 0: 
            for record in filtered_holiday_list:
                new_obj = Holiday(record['name'], record['date'])
                self.add_holiday(new_obj)
            print(f'\nThese are the holidays for Year {year_input} Week #{week_input}:')

def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize Holiday_List Object
    # 2. Load JSON file via Holiday_List read_json function
    # 3. Scrape additional holidays using your Holiday_List scrape_holidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the Holiday_List object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 
    
    global year_list
    year_list = ['2020', '2021', '2022', '2023', '2024']

    # Start of main
    holiday_list = Holiday_List()
    holiday_list.read_json('starting_holiday_json.json')
    holiday_list.scrape_holidays()

    #Read in menu related texts
    file = open('text.txt')
    texts = file.read().splitlines()
    
    #Start up display
    for x in range(0,4,1):
        print((texts[x]).format(num = holiday_list.num_holidays()))

    still_menu = True
    while still_menu: 
        # #Main Menu - Holiday Management display
        input_invalid = True

        for x in range(4, 13, 1):
            print(texts[x])
        
        while input_invalid: 
            try:
                user_input = int(input('Enter choice: '))

                # if 1. add a holidary
                if user_input == 1:
                    for x in range(12, 16, 1):
                        print(texts[x])

                    holiday_input = input('Holiday: ')
                    date_input = input('Date: ')
                    new_holiday = Holiday(holiday_input, date_input)
                    holiday_list.user_add_holiday(new_holiday)

                # if 2. remove a holiday
                elif user_input == 2:
                    for x in range(15, 19, 1):
                        print(texts[x])

                    holiday_input = input('Holiday: ')
                    date_input = input('Date: ') 
                    new_holiday = Holiday(holiday_input, date_input)
                    holiday_list.remove_holiday(new_holiday)      
   
                # if 3. save changes
                elif user_input == 3:
                    for x in range(18, 22, 1):
                        print(texts[x])

                    user_input = input('Are you sure you want to save your changes? [y/n]: ').lower()
                    if user_input == 'y':
                        holiday_list.save_to_json('holiday_list.json')
                        for x in range(24, 27, 1):
                            print(texts[x])
                    elif user_input == 'n':
                        for x in range(21, 24, 1):
                            print(texts[x])
                    else:
                        print('Invalid choice. Try again')
                    
                # if 4. view holidays
                elif user_input == 4:
                    for x in range(30, 34, 1):
                        print(texts[x])
                 
                    year_input = input('Which year? Choose from 2020-2024: ')
                    week_input = input('Which week? #[1-52, Leave blank for the current week - if year is current year]: ')                       
                    week_input = week_input.zfill(2)

                    current_year = date_import.today().strftime('%Y')                                             
                    filtered_holidays = Holiday_List()

                    # valid inputs
                    if year_input in year_list:
                        if 1 <= int(week_input) <= 52:
                            filtered_holiday_list = holiday_list.filter_holidays_by_week(year_input, week_input)
                            filtered_holidays.create_filtered_holiday_list(filtered_holiday_list, year_input, week_input)
                            filtered_holidays.display_holidays()

                        # current week
                        elif week_input == '00' and year_input == current_year:
                            week_input = date_import.today().strftime('%U')
                            weather_valid = False
                            while not weather_valid:
                                user_input = input('Would you like to see this week\'s weather? (only upcoming holidays in the week) [y/n]: ').lower()

                                # if y. view weather with holidays
                                if user_input == 'y':
                                    weather_valid = True
                                    filtered_holiday_list = holiday_list.filter_holidays_by_week(year_input, week_input)
                                    filtered_holidays.create_filtered_holiday_list(filtered_holiday_list, year_input, week_input)
                                    weather_list = filtered_holidays.get_weather()
                                    filtered_holidays.view_and_display_current_week(weather_list)
                        
                                # if n. no weather
                                elif user_input == 'n':
                                    weather_valid = True
                                    filtered_holiday_list = holiday_list.filter_holidays_by_week(year_input, week_input)
                                    filtered_holidays.create_filtered_holiday_list(filtered_holiday_list, year_input, week_input)
                                    filtered_holidays.display_holidays()
                                
                                # invalid choise for weather 
                                else:
                                    print(' (y) or (n) to see weather. Try again')

                        # invalid current week for wrong year            
                        elif week_input == '00' and year_input != current_year:
                            print('Invalid inputs. Try again')

                    # invalid inputs for either year or week        
                    else:
                        print('Invalid inputs. Try again')

                # if 5. exit menu and program
                elif user_input == 5:
                    for x in range(27, 31, 1):
                        print(texts[x])      

                    exit_input = input('Are you sure you want to exit? [y/n] ').lower()
                    if exit_input == 'y':
                        exit_input2 = input('Your changes will be lost. [y/n] ').lower()
                        if exit_input2 == 'y':
                            print('Goodbye!')
                            quit()
                        elif exit_input2 == 'n':
                            input_invalid = False
                        else:
                            print('Invalid choice. Try again')
                    elif exit_input == 'n':
                        input_invalid = False
                    else:
                        print('Invalid choice. Try again')          

            except ValueError:
                print('Not a valid choice. Try again.')

            input_invalid = False
            


if __name__ == "__main__":
    main();
