"""
    File: dates.py
    Author: Elton Ho
    Course: CSC 120, Spring 2024
    This program has 2 functions and 2 classes to store events on a date and 
    print those events based on an inputted file. The two classes make a date 
    with its events and store that date in a dictionary, and the two functions 
    convert an inputted file into the date objects while putting them into the 
    dictionary of dates and unifies the format for the dates.
"""

class Date:
    """This class represents a date and its events. 

       The class has a method to add events to the object. It is constructed 
       with two strings representing the date and the event to be passed in. 
       Note that the date gets canonicalized when the object is created.
    """

    def __init__(self, date, event):
        """Sets up the attributes for the object which are a string that is the 
           date and a list of strings that are the events for that date. 

           Parameters: date is a string representing the date for the object.
           event is a string that is the first event to be put in the list of 
           events for that date. 

           Returns: None.
        """
        # canonicalize_date(date) unifies the date format 
        # the function for it is at the bottom 
        self._date = canonicalize_date(date)
        self._event = [event]  
    
    def get_date(self):
        return self._date
    
    def get_event(self):
        return self._event
    
    def add_event(self, event):
        """Adds a string representing an event for that date to the list of 
           events.   

           Parameters: event is a string representing an event on that date to 
           be put in a list of other events.

           Returns: None.
        """

        self._event.append(event)
    
    def __str__(self):
        return self._date +  " : " + str(self._event)
        
class DateSet:
    """This class represents a collection of dates. 

       It has a method to add dates to the object. When constructing the 
       object, it doesn't need arguments but does have an dictionary attribute.
    """

    def __init__(self):
        """Sets up the attributes for the DateSet object which is a dictionary 
           of objects for dates and strings as the keys representing each date.  

           Parameters: None.

           Returns: None.
        """
        self._date_dictionary = {}
    
    def get_date_dictionary(self):
        return self._date_dictionary
    
    def add_date(self, date, event):
        """Adds an object representing a date to this object's dictionary after 
           creating that object or just adds the event to the Date object.

           Parameters: date is a string representing the date. 
           event is a string representing an event on that date.

           Returns: None.
        """ 

        # canonicalize_date(date) unifies the date format 
        # the function for it is at the bottom   
        if canonicalize_date(date) not in self._date_dictionary:
            date_object = Date(date, event.strip())  # creates the date object
            self._date_dictionary[canonicalize_date(date)] = date_object
        else:  # if the date object already exist 

            # add the event to the object for that date
            self._date_dictionary[canonicalize_date(date)].add_event\
            (event.strip())
    
    def __str__(self):
        return str(self._date_dictionary)
    
def convert_to_dateset():
    """Puts created date objects into a DateSet object and prints out the 
       events for a date based on the inputted file.    
  
    Parameters: None.
  
    Returns: None. 
    """

    file_name = input()
    file = open(file_name)
    calendar = DateSet()
    for line in file:
        line_list = line.strip().split(": ", 1)  # splits the ":" once

        # "I" means add that event to the DateSet object 
        if line_list[0][0] == "I":
            calendar.add_date(line_list[0], line_list[1])

        # "R" means print out the events for that date
        if line_list[0][0] == "R":
            date_canonical = canonicalize_date(line_list[0])
            if date_canonical in calendar.get_date_dictionary():

                # looks at the sorted list of events for that date
                for event in sorted(calendar.get_date_dictionary()\
                [date_canonical].get_event()):
                    print("{}: {}".format(date_canonical, event))

        # no valid operation for that line of the file
        if line_list[0][0] not in "IR":
            print("Error - Illegal operation.")
    file.close()


def canonicalize_date(date_str):
    """Converts a string with a date in it into its canonical representation. 
  
    Parameters: date_str is a string with the date that needs to get 
    canonicalized.
  
    Returns: A string that is the canonical representation of the date to 
    unify the format.
    """

    no_spaces = date_str.split()

    # numerical representation of each month for each abbreviation 
    letter_months = {"Jan": 1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6,\
                     "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}

    # deals with the format of mm/dd/yyyy
    if "/" in no_spaces[1]:
        dates = no_spaces[1].split("/")  # looks at just the date part
        year = dates[2]
        month = dates[0]
        day = dates[1]

    # deals with the format with the abbreviation
    if no_spaces[1] in letter_months:
        month = letter_months[no_spaces[1]]
        year = no_spaces[3]
        day = no_spaces[2]

    # deals with the format of mm-dd-yyyy
    if "-" in no_spaces[1]:
        dates = no_spaces[1].split("-")  # looks at just the date part
        year = dates[0]
        month = dates[1]
        day = dates[2]

    # int() is to remove any leading zeros
    return "{:d}-{:d}-{:d}".format(int(year), int(month), int(day))

def main():
    convert_to_dateset()

main()