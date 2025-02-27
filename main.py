from tkinter import *
from tkinter import filedialog

import os
import json
import datetime

running = True

timeLine = {

    "path":"",
    "entries":{},
    "files":[]

}

# ARRAY STRUCTURE FOR TIMELINE["FILES"]
# [ [FILE_NAME, CONTENTS, TIMESTAMP], [FILE_NAME, CONTENTS, TIMESTAMP], ... ]

def clearTimeline():

    tl = {

        "path":"",
        "entries":{},
        "files":[]

    }

    return tl

while(running):

    # displays main welcome message header
    print("timelinePreviewer\ndeveloped by florencio\n")

    # checks if timeLine["path"] is set
    # timeLine["path"] being set means that theres already loaded
    if timeLine["path"] == "":

        # displays the varies options the user can select
        print("[0] Load Timeline..")
        print("[1] Exit")

        # referenced in understanding how error handling works within python
        # https://www.geeksforgeeks.org/how-to-take-integer-input-in-python/
        try:
            # prompts the user to enter an int as their choice
            choice = int(input("\nPlease enter your choice: "))
        except ValueError:
            choice = -1

        # checks if choice is set to 0
        # "Load Timeline.." option
        if choice == 0:

            root = Tk()

            # referenced for hiding the main window from being displayed in order to only display the filedialog box
            # https://stackoverflow.com/questions/70725224/tkinter-not-working-the-first-time-it-runs-with-withdraw
            root.attributes('-topmost', True, '-alpha', 0)
            
            # displays directory select prompt, then saves selected folder location to timeLine["path"] variable
            timeLine["path"] = filedialog.askdirectory()

            root.destroy()
            
            # references python3 documentation for checking if file exists
            # https://docs.python.org/3/library/os.path.html
            # checks if entries.json exists in the directory selected by the user
            if os.path.exists(timeLine["path"]+"/entries.json"):

                # clears out timeLine["entries"] and timeLine["files"] variables
                timeLine["entries"] = {}
                timeLine["files"] = []

                # referenced for loading json files
                # https://www.geeksforgeeks.org/read-json-file-using-python/
                # parses and loads json file selected by user
                with open(timeLine["path"]+"/entries.json", "r") as file:
                    timeLine["entries"] = json.load(file)
                
                # loops through each entrie, adding each one to the timeLine["files"] array
                for i in timeLine["entries"]["entries"]:

                    # creates temporary entrie variable
                    entrie = []

                    # referenced for loading files
                    # https://www.w3schools.com/python/python_file_open.asp
                    f = open(f"{timeLine["path"]}/{i['id']}", "r")

                    # adds FILE_NAME, contents, and timestamp to entrie as an array
                    # [FILE_NAME, CONTENTS, TIMESTAMP]
                    entrie = [i["id"], f.read(), i["timestamp"]]
                    f.close()

                    timeLine["files"].append(entrie)
            
            # if entries.json doesn't exist, then clear out timeLine["path"], timeLine["entries"], and timeLine["files"]
            else:
                timeLine = clearTimeline()

        # checks if choice is set to 1
        elif choice == 1:
            print("Exiting..\n")
            running = False

        # if choice selected isn't part of the selection list, display error message and clear timeLine["path"], timeLine["entries"], and timeLine["files"]
        else:
            timeLine = clearTimeline()
            print("\nPlease enter a valid option\n")
    
    # if timeLine["path"] contains a string, then a project is loaded and runs under "else:"
    else:
        
        # loops through each entrie in timeLine["files"] array
        for i in range(0, len(timeLine["files"])):

            # referenced for converting and displaying unix timestamps
            # https://www.geeksforgeeks.org/fromtimestamp-function-of-datetime-date-class-in-python/

            # referenced for converting a timestamp from javascript to python, by dividing the original timestamp by 1000
            # https://stackoverflow.com/questions/37494983/python-fromtimestamp-oserror

            # converts timestamp from loaded entrie to a timestamp that python can understand by dividing by 1000
            date_time = datetime.datetime.fromtimestamp(float(timeLine["files"][i][2])/1000)

            # displays entrie in timeLine["files"] as a choice in prompt
            # [CHOICE] FILE_NAME MONTH/DAY/YEAR HOUR:MINUTE AM/PM
            print(f"[{i}] {timeLine["files"][i][0]} - {date_time.strftime('%m/%d/%Y %I:%M%p')}")

        # displays choice for closing file
        print(f"[{len(timeLine["files"])}] Close File")

        # displays choice for exiting the program
        print(f"[{len(timeLine["files"])+1}] Exit")

        try:
            # prompts user to enter an int as their choice, saved to the choice variable
            choice = int(input("\nPlease enter your choice: "))
        except ValueError:
            choice = -1

        print()
        
        # checks if the choice selected was the closing file option
        if choice == len(timeLine["files"]):
            timeLine = clearTimeline()

        # checks if the choice selected was the exiting program option
        elif choice == len(timeLine["files"])+1:
            print("Exiting..\n")
            running = False

        # checks if the choice selected was any of the entries from timeLine["files"]
        elif choice > -1 and choice < len(timeLine["files"])+1:

            # displays contents of the file selected
            print("\n----\tBEGINNING OF FILE\t----")
            print(timeLine["files"][choice][1])
            print("----\tEND OF FILE\t----\n")
            input("Press ENTER to continue\n")

        else:
            print("\nPlease enter a valid option\n")