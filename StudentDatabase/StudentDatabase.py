import sqlite3, re

# creates table and imports CSV file
def importCSV():

    # creating Student Table
    query = '''
                CREATE TABLE IF NOT EXISTS Student(
                StudentId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                FirstName VARCHAR(50),
                LastName VARCHAR(50),
                GPA REAL,
                Major VARCHAR(30),
                FacultyAdvisor VARCHAR(50) DEFAULT "None",
                Address VARCHAR(75),
                City VARCHAR(50),
                State VARCHAR(30),
                ZipCode VARCHAR(20),
                MobilePhoneNumber VARCHAR(10),
                isDeleted INTEGER DEFAULT 0
                );
            '''
    connection.execute(query)
    connection.commit()

    # checking that the file has not already been imported
    cursor = connection.execute("SELECT * FROM Student;")
    cursor = cursor.fetchall()
    if len(cursor) >= 100:
        return

    # read cases file
    with open("students.csv") as f:
        columns = f.readline()
        data = f.readlines()

    records = []

    # get phone numbers only
    phones = [i.split(",")[6] for i in data]

    # cleaning up the phone numbers
    count = 0
    for j in phones:
        ind = j.find("x")
        j = j[:ind] if ind != -1 else j  # remove extension
        j = re.sub(r'\D', '', j)  # substitute non number characters with nothing
        if len(j) > 10:  # takes care of international dialing codes and grabs the last 10 digits
            j = j[-10:]
        phones[count] = j
        count += 1

    # adding each row to the records table as a tuple
    count = 0
    for i in data[:]:
        i = i.strip().split(",")
        i[6] = phones[count]
        records.append(tuple(i))
        count += 1

    # inserting each record into the database
    connection.executemany('INSERT INTO Student(FirstName, LastName, Address, City, State, ZipCode, MobilePhoneNumber, Major, GPA) VALUES(?,?,?,?,?,?,?,?,?);', records)
    connection.commit()

# prints the student in proper format given a tuple
def printStudent(stud):
    print("\nStudent ID:",stud[0])
    print("First Name:",stud[1])
    print("Last Name:",stud[2])
    print("GPA:", stud[3])
    print("Major:", stud[4])
    print("Faculty Advisor:", stud[5])
    print("Address:", stud[6])
    print("City:", stud[7])
    print("State:", stud[8])
    print("Zip Code:", stud[9])
    print("Mobile Phone Number:", stud[10])
    print("\n")

# takes an ID number and returns a boolean for whether it is in the database or not
def inDatabase(id):
    query = '''Select StudentId from Student
                        Where StudentId = ? AND isDeleted = 0'''
    cursor = connection.execute(query, [id])
    cursor = cursor.fetchall()

    if len(cursor) == 0:
        return False
    else:
        return True

# option 1 to print all student and their attributes
def option1():

    # selecting all students from the database
    query = '''
    SELECT *
    FROM Student;
    '''
    cursor = connection.execute(query)
    count = 1

    # printing all students that are not deleted
    for row in cursor:
        if inDatabase(row[0]):
            print("Student " + str(count) + "\n--------------------")
            printStudent(row)
            count += 1

# option 2 Add New Students
def option2():
    # verifying user input is a number
    while True:
        try:
            studID = int(input("Enter the Student ID: "))
            break
        except ValueError:
            print("Please enter a number.")

    if inDatabase(studID):
        print("\nThis ID already exists in the database.\n")
    else:
        # getting all attribute inputs from user
        fName = input('Student First Name: ')
        lName = input('Student Last Name: ')

        # verifying GPA is a number
        while (True):
            try:
                gpa = float(input('Student GPA: '))
                break
            except ValueError:
                print("Please enter a number.")

        major = input('Student Major: ')
        advisor = input('Student Faculty Advisor: ')
        address = input('Student address: ')
        city = input('City Name: ')
        state = input('State Name: ')
        zipCode = input('Student zipcode: ')
        phoneNum = input('Student phone number: ')

        # inserting student into the database
        query = '''INSERT INTO Student(StudentId, FirstName, LastName, 
                    GPA, Major,FacultyAdvisor,Address, City, State ,ZipCode, 
                    MobilePhoneNumber) VALUES(?,?,?,?,?,?,?,?,?,?,?)'''
        connection.execute(query, [studID, fName, lName, gpa, major, advisor, address, city, state, zipCode, phoneNum])
        connection.commit()


# option 3 for updating Students by StudentId
def option3():
    # verifying user input is a number
    while True:
        try:
            studID = int(input("Enter the Student ID: "))
            break
        except ValueError:
            print("Please enter a number.")

    # checking id student ID is in database
    if not inDatabase(studID):
        print("\nThis ID does not exist in the database.")
    else:
        # print the student for user reference
        cursor = connection.execute("SELECT * FROM Student WHERE StudentId = ?", [studID])
        for row in cursor:
            printStudent(row)

        print("What would you like to update?")
        print("1. Major")
        print("2. Faculty Advisor")
        print("3. Phone Number")

        # verifying user input is a number
        while (True):
            try:
                userChoice = int(input("select an option: "))
            except ValueError:
                print("Please enter a number between 1 and 3.")
                continue

            # Update major
            if userChoice == 1:
                major = input("Enter the major you would like to update the student to: ").title()
                query = ''' Update Student
                            set Major = ?
                            Where StudentId = ?'''
                connection.execute(query, [major, studID])
                connection.commit()
                print("\nStudent Major Successfully Updated.")
                break

            # Update advisor
            elif userChoice == 2:
                advisor = input("Enter the faculty advisor you would like to update the Student to: ").title()
                query = ''' Update Student
                            set FacultyAdvisor = ?
                            Where StudentId = ?'''
                connection.execute(query, [advisor, studID])
                connection.commit()
                print("\nStudent Faculty Advisor Successfully Updated.")

                break

            # Update phone number
            elif userChoice == 3:
                while(True):
                    phone = input("Enter the phone number you would like to update the student record to: ").title()

                    # cleaning input to see if it's a valid phone number
                    ind = phone.find("x")
                    phone = phone[:ind] if ind != -1 else phone  # remove extension if given
                    phone = re.sub(r'\D', '', phone)  # substitute non number characters with nothing
                    if len(phone) > 10:  # takes care of international dialing codes and grabs the last 10 digits
                        phone = phone[-10:]

                    if len(phone) != 10:
                        print("Please enter a valid 10 digit phone number.")
                        continue
                    else:
                        break
                query = ''' Update Student
                            set MobilePhoneNumber = ?
                            Where StudentId = ?'''
                connection.execute(query, [phone, studID])
                connection.commit()
                print("\nStudent Phone Number Successfully Updated.")

                break
            else:
                print("Please enter a number between 1 and 3.")
                continue





# option 4 for deleting Students by StudentId
def option4():
    while True:
        print("Enter the Student ID of the Student you want to delete: ")
        try:
            userId = int(input())
            break
        except ValueError:
            print("Please enter a number.")

    # soft deleting student if they are in the database
    if inDatabase(userId):
        query = '''
                    UPDATE Student
                    SET isDeleted = 1
                    WHERE StudentId = ?'''
        cursor = connection.cursor()
        cursor.execute(query, [userId])
        print("\nStudent Successfully Deleted.\n")
    else:
        print("\nStudent ID " + str(userId) + " is not in the database.\n")

    connection.commit()

# Option 5 to search by Major, GPA, City, State, or Advisor
def option5():
    print("\nSelect an option to search:")
    print("1. Major")
    print("2. GPA")
    print("3. City")
    print("4. State")
    print("5. Advisor")

    # verifying input is a number
    while True:
        try:
            userChoice = int(input("Enter a number: "))
            break
        except ValueError:
            print("Please enter a number.")

    # Search by major
    if userChoice == 1:
        major = input("Enter the major you would like to search: ").title()
        query = ''' Select *
                    from Student
                    where Major = ?;'''
        cursor = connection.execute(query, [major])
        cursor = cursor.fetchall()

        if len(cursor) == 0:
            print("\nThere are no students with this major.")
        else:
            for row in cursor:
                printStudent(row)

    # Search by GPA
    elif userChoice == 2:
        gpa = round(float(input("Enter the GPA (to 1 decimal point) that you would like to search: ")), 1)
        query = ''' Select *
                    from Student
                    where GPA = ?;'''
        cursor = connection.execute(query, [gpa])
        cursor = cursor.fetchall()

        if len(cursor) == 0:
            print("\nThere are no students with this GPA.")
        else:
            for row in cursor:
                printStudent(row)

    # Search by city
    elif userChoice == 3:
        city = input("Enter the city you would like to search: ").title()
        query = ''' Select *
                    from Student
                    where city = ?;'''
        cursor = connection.execute(query, [city])
        cursor = cursor.fetchall()

        if len(cursor) == 0:
            print("\nThere are no students in this city.")
        else:
            for row in cursor:
                printStudent(row)

    # Search by state
    elif userChoice == 4:
        state = input("Enter the State you would like to search: ").title()
        query = ''' Select *
                    from Student
                    where State = ?;'''
        cursor = connection.execute(query, [state])
        cursor = cursor.fetchall()

        if len(cursor) == 0:
            print("\nThere are no students in this state.")
        else:
            for row in cursor:
                printStudent(row)

    # Search by advisor
    elif userChoice == 5:
        advisor = input("Enter the Advisor you would like to search: ").title()
        query = ''' Select *
                    from Student
                    where FacultyAdvisor = ?;'''
        cursor = connection.execute(query, [advisor])
        cursor = cursor.fetchall()

        if len(cursor) == 0:
            print("\nThere are no students with this advisor.")
        else:
            for row in cursor:
                printStudent(row)

# connecting to SQLite db - need to change path for each device
connection = sqlite3.connect("/Users/nikitashetty/Desktop/College/CPSC_Courses/CPSC_408/sqlite3/chinook.db")

# creating database and importing csv file
importCSV()

# menu loop to ask user until they exit the program
while True:
    # user options
    print("\n\t\tOptions\n------------------------")
    print("1. Display all students and their attributes.")
    print("2. Add a new student.")
    print("3. Update student by student id.")
    print("4. Delete student by student id.")
    print("5. Search and display students by Major, GPA, City, State, or Advisor.")
    print("6. Exit the program")

    try:
        user_choice = int(input("Enter option here: "))
    except ValueError:
        print("Please enter a number.\n")
        continue

    if user_choice == 1:
        option1()
    elif user_choice == 2:
        option2()
    elif user_choice == 3:
        option3()
    elif user_choice == 4:
        option4()
    elif user_choice == 5:
        option5()
    elif user_choice == 6:
        print("\nAll done.")
        break
    else:
        print("\nPlease enter a number between 1 and 6.")


connection.close()
