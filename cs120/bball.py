"""
    File: bball.py
    Author: Elton Ho
    Course: CSC 120, Spring 2024
    This program has 1 function and 3 classes to store teams into its 
    conference and those conferences into a set based on an inputted file. This 
    is so that we can ultimately find the conferences with the best average win 
    rate.
"""

class Team():
    """This class represents information about a team's name, conference, and 
       win ratio. 

       The class has a method to calculate the win ratio of the team. It is 
       constructed with a list representing the line from the file read.
    """
    def __init__(self, line):
        """Sets up the attribute for the object which is a list of strings that
           represents a line in a file containing needed info about the team. 

           Parameters: line is a list of strings pulled from the inputted file 
           that contains different information about the team in each index 
           which are its name, the conference the team is in, the amount of 
           wins, and the amount of losses it has.

           Returns: None.
        """
        self._line = line 

    def name(self):
        return self._line[0]
    
    def conf(self):
        return self._line[1]
    
    def win_ratio(self):
        """Calculates the win ratio of the team based on the passed in file and 
           returns it. 

           Parameters: None.

           Returns: A float which is the calculated win ratio using the list 
           representing a line from the file.
        """

        # win / (win + lose)
        return float(self._line[2]) / (float(self._line[2]) +\
        float(self._line[3]))
    
    def __str__(self):
        return "{} : {}".format(self.name(), self.win_ratio())

class Conference():
    """This class represents a conference that a group of teams belongs to. 

       The class has methods to add team objects to the list of teams and 
       calculate the average win ratio of the conference. It is constructed 
       with a string representing the name of the conference and a list of 
       team objects of that conference.
    """

    def __init__(self, conf):
        """Sets up the attributes for the object which are a string that is the
           conference's name and a list of the conference's team objects.

           Parameters: conf is a string that represents the name of the 
           conference that is taken from the list of strings representing the 
           line from the file. 

           Returns: None.
        """

        self._conf = conf
        self._teams = []

    def get_conf(self):
        return self._conf
    
    def __contains__(self, team):
        return team in self._teams
    
    def name(self):
        return self._conf
    
    def add(self, team):
        """Appends the team object to a list of other team objects for that 
           conference. 

           Parameters: team is an object that represents information about 
           a team's name, conference, and win ratio.

           Returns: None.
        """

        self._teams.append(team)

    def win_ratio_avg(self):
        """Calculates the average win ratio of the conference and returns that 
           float. 

           Parameters: None.

           Returns: A float representing the average win ratio of the 
           conference.
        """

        # adds all the win ratio of the teams in a conference
        total_win_ratio = 0
        for team in self._teams:
            total_win_ratio += team.win_ratio()
        return total_win_ratio / len(self._teams)
     
    def __str__(self):
        return "{} : {}".format(self.name(), self.win_ratio_avg())
    
class ConferenceSet():
    """This class represents a set of conferences. 

       The class has methods to add conference objects to the list of 
       conferences and find the conferences in the list with the highest 
       average win ratio. It is constructed with a list representing the set of 
       conferences.
    """

    def __init__(self):
        """Sets up the attributes for the object which is a list of conference 
        objects.

        Parameters: None.

        Returns: None.
        """
        self._conferences = []

    def add(self, team):
        """Adds conferences to the list, creates conferences, and adds teams to 
        conferences depending on what's already in the list. 

        Parameters: team is an object that represents information about 
        a team's name, conference, and win ratio.

        Returns: None.
        """

        index = 0 

        # the set is empty so it makes a new conference and adds it to the set 
        if len(self._conferences) == 0:
            conference = Conference(team.conf())
            conference.add(team)
            self._conferences.append(conference)
        else:

            # prevents duplicates by stopping if there's a change
            change = False  
            while index < len(self._conferences) and not change:

                # Finds the matching conference and make sure the team isn't 
                # already in the conference.
                if team.conf() == self._conferences[index].get_conf():
                    if team not in self._conferences[index]:
                        self._conferences[index].add(team)
                        change = True

                # If it went through the whole set without finding a matching 
                # conference and a change hasn't been made, it makes a new one.
                if index == len(self._conferences) - 1 and not change:
                    conference = Conference(team.conf())
                    conference.add(team)
                    self._conferences.append(conference)
                    change = True
                index += 1

    def best(self):
        """Finds the highest average win ratio and finds a list of conferences 
        with that average and returns the list sorted. 

        Parameters: None.

        Returns: a sorted list of strings that represents the conferences with 
        the highest win ratio average.
        """

        highest_avg = 0
        highest_conferences = []

        # finds the highest average win ratio
        for conference in self._conferences:
            if conference.win_ratio_avg() > highest_avg:
                highest_avg = conference.win_ratio_avg()

        # finds the matching conferences for that average
        for conference in self._conferences:
            if conference.win_ratio_avg() == highest_avg:
                highest_conferences.append(str(conference))
        return sorted(highest_conferences)

def find_best_conference(file, conference_set):
    """Converts the inputted file into a list usable by the objects to return
    the sorted list of conferences with the best average win ratio. 

    Parameters: file is a string that represents the name of the file.
    conference_set is an object that represents a set of conferences. 

    Returns: a sorted list of strings that represents the conferences with 
    the highest win ratio average.
    """

    for line in file:
        if line[0] != '#':  # ignores the first line with a #
            count = 0  # accounts for when there are () in the team name
            for char in line:
                if char == "(":
                    count += 1
            if count > 1:  # there are () in the team name 
                # ) separates the team from the conference and numbers
                line_list = line.strip().split(")")
                conference = line_list[1].strip(" (")  # removes the extra  (
                if line[0][0].isnumeric():  # random number and spaces in front
                    # + ")" adds back the lost ) from split 
                    team = " ".join(line_list[0].split()[1:]) + ")"
                else:
                    team = line_list[0] + ")"
            if count == 1:  # slight difference because there are no ()
                # ( separates the team from the conference 
                line_list = line.strip().split("(") 

                # ) separates the numbers from the conference
                conference = line_list[1].split(")")[0]
                if line[0][0].isnumeric():
                    team = " ".join(line_list[0].split()[1:])
                else:
                    team = line_list[0].strip()
            line_list = [team,conference] + line_list[-1].strip().split()[-2:]    
            conference_set.add(Team(line_list))
    file.close()
    return conference_set.best()

def main():
    file_name = input()
    file = open(file_name)
    conference_set = ConferenceSet()
    for best in find_best_conference(file, conference_set):
        print(best)

main()