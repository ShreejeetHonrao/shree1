"""
Design Prolog 

Karthik Nayak
Date: 5th Dec 2015

Purpose:  a simplified version of a database management system.  It will be able
to load a database file from secondary storage as a list, save the list as a database
file, display the list for the user, allow the user to manipulate the list in different
ways (query, sort, enter new data, remove data, change data in the list)

Preconditions:  filename(s) of the database files, menu choices from user, new record data from user, 
    change in record data from user, answers to prompts

Postconditions:  menu of choices, prompts for inputs, results of each database action, changed database list, external files

"""


"""
########################################################################
get_menu_choice
Purpose: displays main menu, gets user's choice and validates it, returns it
Precondition: no parameter, user's input of choice(s), 
Postcondition: returns choice as single character string "1" to "9"
"""
def get_menu_choice():
    
    #display main menu
    print("\nMain Menu\n")
    print("1. Load database")
    print("2. Save (close) database")
    print("3. Query (search)")
    print("4. Display database")
    print("5. Sort")
    print("6. Enter new item")
    print("7. Remove item")
    print("8. Change status and location of item")
    print("9. Exit")
    
    #ask for user choice
    choice = input("Choose item from menu: ")
    choice_list = ["1","2","3","4","5","6","7","8","9"]
    while choice not in choice_list:
        print("\nInvalid choice, please try again")
        choice = input("Choose item from menu:")
    return choice


"""
###########################################
load

Purpose: retrieve a database list from a file on secondary storage
Preconditions: no parameters, user enters filenames until a valid one is entered,
    user must hit Enter
Postconditions: returns the database (an organized list with no newlines), outputs prompts to user
  until valid filename is entered
"""
def load():
    print("\nLoading a database file\n")
    print("Filename will have a .db extension added, do not enter it")    
    
    ok = False
    #opens it if possible, asks user for another if the first won't open.
    while not ok:
        try:
            #asks the user for a filename and  adds the .db extension.
            filename = input("Enter filename:")
            filename += ".db"
            infile = open(filename, "r")
            ok = True
        except IOError:
            print("Error, Could not open", filename) 
    
    database = []
    contents = infile.read()
    infile.close()
    
    line_list = contents.split("\n")
    
    if line_list[-1] == "":
        del line_list[-1]   
    
    for line in line_list:
        elements = line.split(",")
        database.append(elements)
    print("Database loaded\n")
    input("Press Enter")   
    
    return database
    

"""
###########################################
save

Purpose: write out a database list to a file on secondary storage
Preconditions:  parameter is the database list, user must enter filename for writing to
    user must hit Enter
Postconditions:  list is written to file in form that can be read in by load function,
    user is informed that the file is written
    database is NOT changed
"""
def save(database):
    print("\nSaving a database file\n")
    print("Filename will have a .db extension added, do not enter it")
    filename = input("Enter filename:")
    filename += ".db"
    outfile = open(filename, "w")
    
    #writes the data in the database list to the file given in a way that could be read back in by the load function
    for i in range(len(database)):
        for j in range(len(database[i])):
            if j != (len(database[i])-1):
                print(database[i][j],",",end="",sep="", file=outfile)
            else:
                print(database[i][j],file=outfile)
    
    outfile.close()  
    print("\nFile saved\n")
    input("Press Enter")
    return
    

"""
###########################################

displayRecord 
Purpose:  display a record with 4 fields on the screen
Preconditions:  record (list with 4 elements) and width of column desired
Postconditions:  output to screen, no return value
   record is NOT changed
"""
def displayRecord(database_rec,width):
    
    #display each field, padded with spaces and trimmed to be width of column, on the same line
    for j in range(len(database_rec)):
        if j != (len(database_rec)-1):
            msg = database_rec[j]
            msg += " "*100
            msg = msg[:width]
            print(msg,end="")
        else:
            msg = database_rec[j]
            msg += " "*100
            msg = msg[:width]
            print(msg,end="\n")            
    return

"""
########################################################################
display_db 

Purpose:  to show all the records of the database list in readable form on
   the screen, with or without record numbers
Preconditions:  the database list and the flag for showing numbers (bool)
Postconditions: the database list contents in columns, with record numbers
   on the left side if showing numbers flag is True, no return value
   database will NOT be changed
"""
def display_db(database,show_num):
    width = 21
    if show_num == False:
        print("Display Database\n")
        print("Name                 Date Purchased       Status               Location")
    else:
        print("    Name                 Date Purchased       Status               Location")
    
    #print a record in the database list, formatting into columns
    for i in range(len(database)):
        
        #printing a record number on the left of each line if desired
        if show_num == True:
            print(i+1,end="   ")
        
        database_rec = database[i]
        displayRecord(database_rec,width)
    
    if show_num == False:
        print("\n",len(database),"records")
        input("\nPress Enter")
    
    return


"""

###########################################
verifyYN
Purpose: ask the user a question, get an answer and
   make sure it is only Yes or No ("Y" or "N")

Precondition:  prompt string to ask the user
Postcondition: user's answer as either "Y" or "N"
"""
def verifyYN(question):
    #ask user the question
    ans = input(question)
    answers = ["y","n"]
    
    while ans.lower() not in answers:
        print("invalid input")
        ans = input(question)
    return ans.lower()
    

"""
###########################################
change_status

Purpose:  allow the user to choose a record, enter new information for the record's
  location field, validate it, make sure the user wants to change the database and
  follow the user's instructions
Preconditions: parameter is the database list, user must enter record number and new location,
  user must enter Y or N to "are you sure?" question, user must hit Enter
Postconditions: no return value, database list is changed if user oks it
"""
def change_status(database):
    print("\nChange an item's status\n")
    
    #display records in database, with record numbers
    show_num = True
    display_db(database,show_num)
    
    #asks the user which record they want and verifies the input
    flag = True
    while (flag == True):
        try:
            record_no = int(input("\nWhich record? "))
            while record_no not in range(1,len(database)+1):
                print("Invalid input")
                record_no = int(input("\nWhich record? "))
            flag = False
        except:
            print("Invalid input")
    record_no -= 1
    
    temp1 = database[record_no][2]
    if database[record_no][2] == "IN":
        database[record_no][2] = "OUT"
    else:
        database[record_no][2] = "IN"
        
    #The user is asked for the new location (which is checked for commas)
    location = input("New location? ")
    if "," in location:
        location = location.replace(',',' ')
        
    temp2 = database[record_no][3]
    database[record_no][3] = location
    
    #The user is asked to verify that they do want to change the record as given
    width = 21
    database_rec = database[record_no]
    displayRecord(database_rec,width)
    question = "Do you want to make the change? (y/n)"
    ans = verifyYN(question)
    if ans == "n":
        database[record_no][2] = temp1
        database[record_no][3] = temp2  
        print("\nStatus and location did NOT change")
    else:
        print("\nStatus and location changed")
    
    input("\nPress Enter")
    return
        

"""
###########################################
remove_data 
Purpose:  allows user to choose one record to be removed from database list,
  verifies that user wants to do it, then removes it from the list
Preconditions: parameter: the database list, the user hits Enter
Postconditions:  database records displayed, user prompts, no return value,
   database MAY be changed
"""
def remove_data(database):
    print("\nRemove a record\n")
    
    #display the records in the database, with record numbers
    show_num = True
    display_db(database,show_num)        
    
    #asks the user which record and verifies it 
    flag = True
    while (flag == True):
        try:
            record_no = int(input("\nWhich record? "))
            while record_no not in range(1,len(database)+1):
                print("Invalid input")
                record_no = int(input("\nWhich record? "))
            flag = False
        except:
            print("Invalid input")
    record_no -= 1  
    
    #display that record (only)
    database_rec = database[record_no]
    width = 21
    displayRecord(database_rec,width)
    
    #ask the user to verify that they do want to remove.
    question = "Do you want to delete this record? (y/n)"
    ans = verifyYN(question)
    if ans == "y":
        del database[record_no]
        print("\nRemoved removed")
    else:
        print("\nNo changes were made")
    input("\nPress Enter")
    return
     
        
"""
########################################################################

get_field_choice
purpose:  to ask the user which field they want to use, validate the response and return it
preconditions:  no parameter, display list of 4 fields, ask user for choice,
    error message if necessary
postconditions: returns the user's choice "1" through "4"
"""
def get_field_choice():
    print("Which field to query?")
    print("1. Item name")
    print("2. Date bought")
    print("3. Status")
    print("4. Location")
    choice = input("Which field? ")
    answers = ["1","2","3","4"]
    while choice not in answers:
        print("Invalid input")
        choice = input("Which field? ")
    choice = int(choice)
    choice -= 1
    return choice
   
   
"""
###########################################
query
Purpose:  allow the user to ask for records matching given value in chosen field
    to be displayed
Preconditions:  parameter database list, user enters field choice, value to search for
    user hits Enter
Postconditions: database records may or may not be displayed, 
     record count of hits displayed, waits for Enter
    database is NOT changed, no return value
"""
def query(database):
    print("\nQuerying the Database\n")
    
    #ask the user which field they want to query about (validated)
    choice = get_field_choice()
    
    #ask the user what value to search for
    value = input("What value to look for? ")
    count = 0 
    width = 21
    for i in range(len(database)):
        if value.lower() == database[i][choice].lower():
            database_rec = database[i]
            displayRecord(database_rec,width)    
            count += 1
    
    print("\n",count,"record found")
    input("\nPress Enter")      
    return
   
   
"""
###########################################
find_min 
purpose:  to find the location of the lowest value in the database
     list, in the chosen field
pre-conditions:  parameters: database list and choice of field (1-4)
post-conditions: returns location of minimum value in field chosen
   database does NOT change

"""
def find_min(database,choice):
    location = 0 
    
    #for each entry in the database list
    for i in range(len(database)):
        
        #if the current value of the chosen field is less than the lowest value of the field seen so far       
        if database[i][choice] < database[location][choice]:
            
            #change location to be the current location
            location = i
            
    return location


"""
###########################################
sort
Purpose: to allow the user to choose which field to sort by, and which
  direction to sort the records in the database
Preconditions:  database list, user choice of fields, user choice of direction (A/D)
Postconditions:   display of field choices, ask user direction, ask user to verify
   that they want to do this, wait for Enter, database MAY be changed
"""
def sort(database):
    show_num = False
    print("\nSorting the Database\n")
    
    #ask the user which field to sort by (validated)
    choice = get_field_choice()
    
    #ask direction (Ascending or Descending) (validated)
    order = input("Ascending(A) or Descending(D)? ")
    answers = ["a","d"]
    while order.lower() not in answers:
        print("Invalid input")
        order = input("Ascending(A) or Descending(D)? ")
    
    #ask the user if they are sure they want to sort the database
    question = "\nAre you sure you want to sort the database? (y/n)"
    ans = verifyYN(question)
    show_num = True
    if ans == "y":
        
        #sort using the selection sort algorithm ascending
        for i in range(len(database)):
            temp_database = database[i:]
            pos = find_min(temp_database,choice)
            database[i][choice],temp_database[pos][choice] = temp_database[pos][choice], database[i][choice] 
    
        #adjust the database for the direction desired (reverse for descending)
        if order.lower() == "d":
            database.reverse()
        print("\nDatabase sorted")
    
    else:
        print("\nDatabase not sorted")
    
    input("\nPress enter")   
    return


"""
###########################################
get_new_entry
Purpose: allow the user to enter the data for all four fields of a record,
   validate them, verify that the user wants to add the record to the database
   and perform the user's instruction
Preconditions:  database list, user inputs for fields
Postconditions:  prompts for inputs, verify user wants to add the record,
   waits for Enter, no return value, database MAY be changed
"""
def get_new_entry(database):   
    print("\nCreate new record\n")
    
    #ask the user for the data of a record and validating all of them 
    
    name = input("Item name? ")
    if "," in name:
        name = name.replace(',',' ') 

    flag = True
    while flag == True:
        date = input("Date bought (YYYY/MM/DD) ? ")
        date = date.split("/")
        try:
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
            flag = False
            msg = False
            if len(date) > 3:
                msg = True
                flag = True
            if not(0 < month < 13):
                msg = True
                flag = True 
            if not(0 < day < 32):
                msg = True
                flag = True   
            if msg == True:
                print("Invalid input")
        except:
            print("invalid input")
    date = '/'.join(date)

    status = input("Status (IN/OUT)? ")
    status_input = ["IN","OUT"]
    while status.upper() not in status_input:
        print("Invalid input")
        status = input("Status (IN/OUT)? ")
    
    location = input("Location? ")
    if "," in location:
        location = location.replace(',',' ')  
    
    record = [name,date,status.upper(),location]   
    
    #display the record  made from user inputs
    print()
    width = 21
    displayRecord(record,width)

    #ask if they really want to add it to the database
    question = "\nDo you want to add this record? (y/n)"
    ans = verifyYN(question)
    
    #if they say yes, add it to the end of the database
    if ans == "y":
        database.append(record)
        print("\nRecord added")
    else:
        print("\nNo changes were made")    
        
    input("\nPress Enter")
    return
   
    
def main():
    
    #set database list to empty
    database=[]
    
    choice = get_menu_choice()
    while choice != "9":
        if choice == "1":
            database = load()
        elif choice == "2":
            save(database)
        elif choice == "3":
            if len(database) != 0:
                query(database)
            else:
                input("\nDatabase empty, please load a database")     
        elif choice == "4":
            show_num = False
            display_db(database,show_num)
        elif choice == "5":
            sort(database)
        elif choice == "6":
            get_new_entry(database)
        elif choice == "7":
            if len(database) != 0:
                remove_data(database)
            else:
                input("\nDatabase empty, please load a database")            
        else:
            if len(database) != 0:
                change_status(database)
            else:
                input("\nDatabase empty, please load a database") 

        choice = get_menu_choice()
        
main()