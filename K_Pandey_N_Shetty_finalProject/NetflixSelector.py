import mysql.connector
from random import randint
import csv
import time

# connects to Netflix Database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    auth_plugin='mysql_native_password',
    passwd="ssSS!5152541",
    database="Netflix"
)
cursor = db.cursor()


# returns the number of titles in the database
def getNumTitles():
    cursor.execute("SELECT COUNT(*) FROM Titles;")
    crsr = cursor.fetchall()

    if len(crsr) > 0:
        return crsr[0][0]
    else:
        return -1


# takes an id number and returns boolean for whether it is in the db or not
def userRecordInDatabase(id):
    query = '''Select UserID from User_Record
                Where UserID = %d AND isDeleted = 0'''
    cursor.execute(query, id)
    crsr = cursor.fetchall()

    if len(crsr) == 0:
        return -1
    else:
        return crsr


# takes a name and email and returns boolean for whether it is in the db or not
def userInDatabase(name, email):
    query = '''Select UserID from Users
                Where Name = %s AND Email = %s AND isDeleted = 0'''
    cursor.execute(query, [name, email])
    crsr = cursor.fetchall()

    if len(crsr) == 0:
        return False
    else:
        return True


# helper function to get User ID given the name and email of the user
def getUserID(name, email):
    cursor.execute("Select UserID from Users Where Name = %s AND Email = %s", [name, email])
    crsr = cursor.fetchall()

    if len(crsr) > 0:
        return crsr[0][0]
    else:
        return -1


# helper function to check if id is in user's future list
def inFutureList(userID, titleID):
    cursor.execute("select FutureList from User_Record where UserID = %d and TitleID = %d" % (userID, titleID))
    crsr = cursor.fetchall()

    if len(crsr) > 0:
        if crsr[0][0] == 1:
            return True

    return False


# adds a title to the future list given the id of the user and id of the title
def addToFutureList(userID, titleID):
    cursor.execute("select userID from User_Record where userID = %d and TitleID = %d" % (userID, titleID))
    crsr = cursor.fetchall()

    # either updates record or creates new record
    if len(crsr) > 0:
        if inFutureList(userID, titleID):
            print("This title is already in your Future List.")
        else:
            query = ''' update User_Record
                        set FutureList = 1
                        where userID = %d and titleId = %d'''
            cursor.execute(query % (userID, titleID))
            print("\nTitle successfully added to future list.")

    else:
        query = '''insert into User_Record (TitleID, UserID, FutureList) 
                    values (%d, %d, %d)'''
        cursor.execute(query % (titleID, userID, 1))
        print("\nTitle successfully added to future list.")

    time.sleep(.5)
    db.commit()


# print all titles and info 10 at a time
def printAllTitles(userID):
    cursor.execute("select * from Titles")
    while True:
        titles = cursor.fetchmany(10)

        print("--------Titles---------")
        if len(titles) > 0:
            for row in titles:
                print("ID:", row[0])
                print("Title:", row[1])
                print("Year Released:", row[2])
                print("Duration:", row[3])
                print("Content Rating:", row[4])
                print("Type:", row[5])
                print("Description:", row[6])
                print("\n")

            # second menu for what to do with the titles
            print("Would you like to:")
            print("1) See more titles")
            print("2) Add a title to your Future List")
            print("3) Rate a title")
            print("4) Go back to Menu")
            while True:
                try:
                    user_choice = int(input("Enter your choice: "))
                    break
                except ValueError:
                    print("Please enter a number.\n")

            if user_choice == 1:
                pass
            elif user_choice == 2:
                cursor.fetchall()
                while True:
                    try:
                        titleID = int(input("Enter the ID of the title you would like to add:"))
                        break
                    except ValueError:
                        print("Please enter a number.\n")

                addToFutureList(userID, titleID)
            elif user_choice == 3:
                cursor.fetchall()
                while True:
                    try:
                        titleID = int(input("Enter the ID of the title you would like to rate:"))
                        break
                    except ValueError:
                        print("Please enter a number.\n")
                rateTitle(userID, titleID)

            elif user_choice == 4:
                cursor.fetchall()
                break
        else:
            print("No more titles to view. Back to menu")
            break


# prints one title given an id
def printTitle(id):
    cursor.execute("select * from Titles Where TitleID = %d" % id)
    title = cursor.fetchall()

    for row in title:
        print("ID:", row[0])
        print("Title:", row[1])
        print("Year Released:", row[2])
        print("Duration:", row[3])
        print("Content Rating:", row[4])
        print("Type:", row[5])
        print("Description:", row[6])

    db.commit()


# helper function to get media type given the title id
def isMovie(id):
    cursor.execute("select Type from Titles where TitleID = %d" % id)
    crsr = cursor.fetchall()

    if len(crsr) > 0:
        if crsr[0][0] == "Movie":
            return True

    return False


# helper function to get actor id from name
def getActorID(name):
    cursor.execute("select ActorID from Actors where Name = %s", [name])
    crsr = cursor.fetchall()

    if len(crsr) > 0:
        return crsr[0][0]
    else:
        return -1


# helper function to get director id from name
def getDirectorID(name):
    cursor.execute("select DirectorID from Directors where Name = %s", [name])
    crsr = cursor.fetchall()

    if len(crsr) > 0:
        return crsr[0][0]
    else:
        return -1


# def deleteRecord():
def rateTitle(userID, titleID):
    while True:
        try:
            rating = int(input("Enter your rating (1-5): "))
            if rating < 1 or rating > 5:
                print("Please enter a number between 1 and 5.")
                continue
            break
        except ValueError:
            print("Please enter a number.\n")

    cursor.execute("select userID from User_Record where userID = %d and TitleID = %d" % (userID, titleID))
    crsr = cursor.fetchall()

    if len(crsr) > 0:
        query = ''' update User_Record
                    set UserRating = %d, UserWatched = 1
                    where UserID = %d and TitleId = %d'''
        cursor.execute(query % (rating, userID, titleID))

    else:
        query = '''insert into User_Record (TitleID, UserID, UserRating, UserWatched) 
                    values (%d, %d, %d, %d)'''
        cursor.execute(query % (titleID, userID, rating, 1))

    print("\nRating successfully added.")
    time.sleep(.5)


# generate random movie title from available movies
def getRandomMovie(userID):
    while True:
        # generate some integers
        movieID = randint(1, getNumTitles())
        if isMovie(movieID):
            print("\n-----Your Random Movie------\n")
            printTitle(movieID)
            print()
            time.sleep(.5)
        else:
            continue

        # second menu for what to do with the title or to generate a new show/movie
        while True:
            print("Would you like to: ")
            print("1) Add this movie to your Future List")
            print("2) Rate this Movie")
            print("3) Generate a New Random Movie")
            print("4) Generate a New Random TV Show")
            print("5) Go back to menu")
            stop = True
            try:
                user_choice = int(input("Enter option here: "))
            except ValueError:
                print("Please enter a number.\n")
                time.sleep(.5)

            if user_choice == 1:
                addToFutureList(userID, movieID)
            elif user_choice == 2:
                rateTitle(userID, movieID)
            elif user_choice == 3:
                stop = False
            elif user_choice == 4:
                getRandomShow(userID)
            elif user_choice == 5:
                pass
            else:
                print("Please enter a number between 1 and 5.")

            break

        if stop:
            break


# generates a random tv show for the user to watch
def getRandomShow(userID):
    while True:
        # generate some integer
        showID = randint(1, getNumTitles())
        if not isMovie(showID):
            print("\n-----Your Random Show------\n")
            printTitle(showID)
            print()
            time.sleep(.5)
        else:
            continue

        # second menu for what to do with the title or to generate a new show/movie
        while True:
            print("Would you like to: ")
            print("1) Add this show to your Future List")
            print("2) Rate this Show")
            print("3) Generate a New Random Show")
            print("4) Generate a New Random Movie")
            print("5) Go back to menu")
            stop = True

            try:
                user_choice = int(input("Enter option here: "))
            except ValueError:
                print("Please enter a number.\n")

            if user_choice == 1:
                addToFutureList(userID, showID)
            elif user_choice == 2:
                rateTitle(userID, showID)
            elif user_choice == 3:
                stop = False
            elif user_choice == 4:
                getRandomMovie(userID)
            elif user_choice == 5:
                pass
            else:
                print("Please enter a number between 1 and 5.")
                time.sleep(.5)
            break

        if stop:
            break


# allows the user to search for a title by the name
def searchByTitleName(userID):
    while True:
        # asking the user for title name input
        titleName = input("\nEnter the title name: ").title()
        query = '''Select TitleID from Titles
                    where title = %s'''
        cursor.execute(query, [titleName])
        crsr = cursor.fetchall()

        if (len(crsr) <= 0):
            print("\nTitle not found in database.")
            time.sleep(.5)
            break
        else:
            print()
            titleID = crsr[0][0]
            printTitle(titleID)
            print()

            # menu to ask user what they would like to do with the result
            while True:
                print("Would you like to: ")
                print("1) Add this Title to your Future List")
                print("2) Rate this Title")
                print("3) Search for a new Title")
                print("4) Go back to menu")
                stop = True
                try:
                    user_choice = int(input("Enter option here: "))
                except ValueError:
                    print("Please enter a number.\n")
                    time.sleep(.5)

                if user_choice == 1:
                    addToFutureList(userID, titleID)
                elif user_choice == 2:
                    rateTitle(userID, titleID)
                elif user_choice == 3:
                    stop = False
                elif user_choice == 4:
                    pass
                else:
                    print("Please enter a number between 1 and 4.")

                break

        if stop:
            break


# helper function to check if title id is in the db
def titleIDInDB(titleID):
    query = '''Select TitleID from Titles
                    Where TitleID = %d'''
    cursor.execute(query % titleID)
    crsr = cursor.fetchall()

    if len(crsr) == 0:
        return False
    else:
        return True


# allows user to enter actor name to find titles with them in it
def filterByActor(userID):
    run = True
    while run:
        # asking user for input for the actor name
        name = input("Enter Actor Name: ").title()
        actorID = getActorID(name)
        if actorID == -1:
            print("\nNo titles with this actor.")
            time.sleep(.5)
            return
        else:
            query = '''Select TitleID from actors_titles
                       where actorID = %d'''
            cursor.execute(query % actorID)

            crsr = cursor.fetchall()
            i = 1
            j = 10

            if len(crsr) == 0:
                return

            # checking if there are more titles in the search
            while True:
                moreTitles = True
                if len(crsr) <= 0:
                    print("\nNo more titles with this actor.")
                    break
                else:
                    for row in range(i, j):
                        try:
                            print()
                            printTitle(crsr[row][0])
                            print()
                        except:
                            print("\nNo more titles with this actor.")
                            moreTitles = False
                            break
                    i += 10
                    j += 10
                    cont = False
                    if moreTitles:
                        while True:
                            choice = input("Would you like to see more titles(y/n): ").lower()

                            if choice == "y" or choice == "yes":
                                cont = True
                                break
                            elif choice == "n" or choice == "no":
                                break
                            else:
                                print("Please enter 'y' or 'n'")
                if cont:
                    continue

                # second menu for what to do with the titles
                while True:
                    print("Would you like to: ")
                    print("1) Add a Title to your Future List")
                    print("2) Rate a Title")
                    print("3) Search for Another Actor")
                    print("4) Go Back to Menu")
                    stop = True

                    while True:
                        try:
                            user_choice = int(input("Enter option here: "))
                            break
                        except ValueError:
                            print("Please enter a number.\n")

                    if user_choice == 1:
                        cursor.fetchall()
                        while True:
                            titleID = int(input("Enter the ID of the title you would like to add: "))
                            if (titleIDInDB(titleID)):
                                addToFutureList(userID, titleID)
                                stop = True
                                break
                            else:
                                print("ID not in database. Please enter a valid title ID.")
                    elif user_choice == 2:
                        cursor.fetchall()
                        while True:
                            titleID = int(input("Enter the ID of the title you would like to rate: "))
                            if (titleIDInDB(titleID)):
                                rateTitle(userID, titleID)
                                stop = True
                                break
                            else:
                                print("ID not in database. Please enter a valid title ID.")

                    elif user_choice == 3:
                        cursor.fetchall()
                        stop = False
                        break
                    elif user_choice == 4:
                        cursor.fetchall()
                        pass
                    else:
                        print("Please enter a number between 1 and 4.")
                        time.sleep(.5)
                        continue
                    break

                if stop:
                    run = False
                    break
                else:
                    break


# allows user to search by genre
def filterByGenre(userID):
    run = True
    while run:
        # print all countries
        cursor.execute("SELECT * FROM Genres")
        crsr = cursor.fetchall()
        print("\n\t\t\tALL GENRES")
        print("\t---------------------------")
        for row in crsr:
            print("\t\t%d) %s" % (row[0], row[1]))

        while True:

            # get correct int input
            try:
                genreID = int(input("Enter the ID for the genre you would like to choose: "))
                break
            except ValueError:
                print("Please enter a number.\n")

        if genreID <= 0 or genreID >= 43:
            print("\nGenre ID not valid.")
            time.sleep(.5)
            return
        else:
            query = '''SELECT TitleID FROM genres_titles
                            WHERE AttributeID = %d;'''
            cursor.execute(query % genreID)
            crsr = cursor.fetchall()
            i = 1
            j = 10

            # if no titles found, return to menu
            if len(crsr) == 0:
                return

            # checking if there are more titles in the search
            while True:
                moreTitles = True
                if len(crsr) <= 0:
                    print("\nNo more titles in this genre.")
                    break
                else:
                    for row in range(i, j):
                        try:
                            print()
                            printTitle(crsr[row][0])
                            print()
                        except:
                            print("\nNo more titles in this genre.")
                            break
                    i += 10
                    j += 10
                    if moreTitles:
                        while True:
                            cont = False
                            choice = input("Would you like to see more titles(y/n): ").lower()

                            if choice == "y" or choice == "yes":
                                cont = True
                                break
                            elif choice == "n" or choice == "no":
                                break
                            else:
                                print("Please enter 'y' or 'n'")
                if cont:
                    continue

                # second menu for what to do with the titles
                while True:
                    print("Would you like to: ")
                    print("1) Add a Title to your Future List")
                    print("2) Rate a Title")
                    print("3) Search for Another Genre")
                    print("4) Go Back to Menu")
                    stop = True

                    while True:
                        try:
                            user_choice = int(input("Enter option here: "))
                            break
                        except ValueError:
                            print("Please enter a number.\n")

                    if user_choice == 1:
                        cursor.fetchall()
                        while True:
                            titleID = int(input("Enter the ID of the title you would like to add: "))
                            if (titleIDInDB(titleID)):
                                addToFutureList(userID, titleID)
                                stop = True
                                break
                            else:
                                print("ID not in database. Please enter a valid title ID.")
                    elif user_choice == 2:
                        cursor.fetchall()
                        while True:
                            titleID = int(input("Enter the ID of the title you would like to rate: "))
                            if (titleIDInDB(titleID)):
                                rateTitle(userID, titleID)
                                stop = True
                                break
                            else:
                                print("ID not in database. Please enter a valid title ID.")

                    elif user_choice == 3:
                        cursor.fetchall()
                        stop = False
                        break
                    elif user_choice == 4:
                        cursor.fetchall()
                        pass
                    else:
                        print("Please enter a number between 1 and 4.")
                        time.sleep(.5)
                    break

                if stop:
                    run = False
                    break
                else:
                    break


# allows user to search by director name
def filterByDirector(userID):
    run = True
    while run:
        name = input("Enter Director Name: ").title()
        directorID = getDirectorID(name)

        if directorID == -1:
            print("\nNo titles directed by this director.")
            time.sleep(.5)
            return
        else:
            query = '''SELECT TitleID FROM directors_titles
                         WHERE AttributeID = %d'''
            cursor.execute(query % directorID)

            crsr = cursor.fetchall()
            i = 1
            j = 10

            # if no titles found, return to menu
            if len(crsr) == 0:
                return

            # checking if there are more titles in the search
            while True:
                moreTitles = True
                if len(crsr) <= 0:
                    print("\nNo more titles with this director.")
                    break
                else:
                    for row in range(i, j):
                        try:
                            print()
                            printTitle(crsr[row][0])
                            print()
                        except:
                            print("\nNo more titles with this director.")
                            moreTitles = False
                            break
                    i += 10
                    j += 10
                    cont = False
                    if moreTitles:
                        while True:
                            choice = input("Would you like to see more titles(y/n): ").lower()

                            if choice == "y" or choice == "yes":
                                cont = True
                                break
                            elif choice == "n" or choice == "no":
                                break
                            else:
                                print("Please enter 'y' or 'n'")
                if cont:
                    continue

                # second menu for what to do with the titles
                while True:
                    print("Would you like to: ")
                    print("1) Add a Title to your Future List")
                    print("2) Rate a Title")
                    print("3) Search for Another Director")
                    print("4) Go Back to Menu")
                    stop = True

                    while True:
                        try:
                            user_choice = int(input("Enter option here: "))
                            break
                        except ValueError:
                            print("Please enter a number.\n")

                    if user_choice == 1:
                        cursor.fetchall()
                        while True:
                            titleID = int(input("Enter the ID of the title you would like to add: "))
                            if (titleIDInDB(titleID)):
                                addToFutureList(userID, titleID)
                                stop = True
                                break
                            else:
                                print("ID not in database. Please enter a valid title ID.")
                    elif user_choice == 2:
                        cursor.fetchall()
                        while True:
                            titleID = int(input("Enter the ID of the title you would like to rate: "))
                            if (titleIDInDB(titleID)):
                                rateTitle(userID, titleID)
                                stop = True
                                break
                            else:
                                print("ID not in database. Please enter a valid title ID.")

                    elif user_choice == 3:
                        cursor.fetchall()
                        stop = False
                        break
                    elif user_choice == 4:
                        cursor.fetchall()
                        pass
                    else:
                        print("Please enter a number between 1 and 4.")
                        time.sleep(time.sleep(.5))
                    break

                if stop:
                    run = False
                    break
                else:
                    break


# allows user to search for titles by country
def filterByCountry(userID):
    run = True
    while run:
        # print all countries
        cursor.execute("SELECT * FROM Countries")
        crsr = cursor.fetchall()
        print("\n\t\t\tALL COUNTRIES")
        print("\t---------------------------")
        for row in crsr:
            print("\t\t%d) %s" % (row[0], row[1]))

        while True:
            # get correct int input
            try:
                countryID = int(input("Enter the ID for the Country you would like to choose: "))
                break
            except ValueError:
                print("Please enter a number.\n")

        # checking if id is valud
        if countryID <= 0 or countryID >= 118:
            print("\nCountry ID not valid.")
            time.sleep(.5)
            return
        else:
            query = '''SELECT TitleID FROM countries_titles
                        WHERE AttributeID = %d;'''
            cursor.execute(query % countryID)

            crsr = cursor.fetchall()
            i = 1
            j = 10

            # if no titles found, return to menu
            if len(crsr) == 0:
                return

            # checking if there are countries in the search
            while True:
                moreTitles = True
                if len(crsr) <= 0:
                    print("\nNo more titles from this country.")
                    break
                else:
                    for row in range(i, j):
                        try:
                            print()
                            printTitle(crsr[row][0])
                            print()
                        except:
                            print("\nNo more titles from this country.")
                            moreTitles = False
                            break
                    # increment the cursor variables
                    i += 10
                    j += 10

                    cont = False
                    if moreTitles:
                        while True:
                            choice = input("Would you like to see more titles(y/n): ").lower()

                            if choice == "y" or choice == "yes":
                                cont = True
                                break
                            elif choice == "n" or choice == "no":
                                break
                            else:
                                print("Please enter 'y' or 'n'")
                if cont:
                    continue

                # second menu for what to do with the titles
                while True:
                    print("Would you like to: ")
                    print("1) Add a Title to your Future List")
                    print("2) Rate a Title")
                    print("3) Search for Another Country")
                    print("4) Go Back to Menu")
                    stop = True

                    while True:
                        try:
                            user_choice = int(input("Enter option here: "))
                            break
                        except ValueError:
                            print("Please enter a number.\n")

                    if user_choice == 1:
                        cursor.fetchall()
                        while True:
                            titleID = int(input("Enter the ID of the title you would like to add: "))
                            if (titleIDInDB(titleID)):
                                addToFutureList(userID, titleID)
                                stop = True
                                break
                            else:
                                print("ID not in database. Please enter a valid title ID.")
                    elif user_choice == 2:
                        cursor.fetchall()
                        while True:
                            titleID = int(input("Enter the ID of the title you would like to rate: "))
                            if (titleIDInDB(titleID)):
                                rateTitle(userID, titleID)
                                stop = True
                                break
                            else:
                                print("ID not in database. Please enter a valid title ID.")
                    elif user_choice == 3:
                        cursor.fetchall()
                        stop = False
                        break
                    elif user_choice == 4:
                        cursor.fetchall()
                        pass
                    else:
                        print("Please enter a number between 1 and 4.")
                        time.sleep(.5)
                    break

                if stop:
                    run = False
                    break
                else:
                    break


# delete user account and log out
def deleteAccount(userID):
    while True:
        choice = input("Are you sure you would like to delete your account (y/n): ").lower()

        if choice == "y" or choice == "yes":
            cursor.execute("START TRANSACTION")
            query = '''UPDATE Users
                        SET IsDeleted = 1
                        WHERE UserID = %d'''
            cursor.execute(query % userID)
            cursor.execute("COMMIT")
            print("Account Deleted. \nThank you for using Netflix Selector!")
            return 1
        elif choice == "n" or choice == "no":
            return 0
        else:
            print("Please enter 'y' or 'n'")


# allows user to view which titles they have rated
def viewRatings(userID):
    print("\n\t\tRATED TITLES")
    print("----------------------------")
    query = '''SELECT User_Record.TitleID, UserRating FROM User_Record
                INNER JOIN Titles ON User_Record.TitleID = Titles.TitleID
                WHERE UserId = %d
                AND UserRating != 0'''
    cursor.execute(query % userID)
    crsr = cursor.fetchall()

    for row in crsr:
        printTitle(row[0])
        print("Rating:", row[1])
        print("\n")


# lets user view which titles are in their future list and the total watch time it would take
def viewFutureList(userID):
    # printing all the titles in the future list
    print("\n\t\tFUTURE LIST")
    print("----------------------------")
    query = '''SELECT Titles.TitleID
                FROM User_Record
                INNER JOIN Titles ON User_Record.TitleID = Titles.TitleID
                WHERE userID = %d
                AND FutureList = 1'''
    cursor.execute(query % userID)
    crsr = cursor.fetchall()

    for row in crsr:
        printTitle(row[0])
        print()

    # outputting total watch time for movies in future list
    print("\nTotal Movie Watch Time:")
    query = '''SELECT SUM(Duration)
                    FROM User_Record
                    INNER JOIN Titles ON User_Record.TitleID = Titles.TitleID
                    WHERE userID = %d
                    AND FutureList = 1
                    AND type = "Movie"'''
    cursor.execute(query % userID)
    crsr = cursor.fetchall()

    if crsr[0][0] == None:
        print("0 hours")
    else:
        print(round((crsr[0][0]) / 60, 2), "hours")

    # outputting total watch time for tv shows in future list
    print("\nTotal TV Show Watch Time:")
    query = '''SELECT SUM(Duration)
                        FROM User_Record
                        INNER JOIN Titles ON User_Record.TitleID = Titles.TitleID
                        WHERE userID = %d
                        AND FutureList = 1
                        AND type = "TV Show"'''
    cursor.execute(query % userID)
    crsr = cursor.fetchall()

    if crsr[0][0] == None:
        print("0 seasons")
    else:
        print(crsr[0][0], "season(s)")

    time.sleep(.5)


# function to export all movies in future list to a csv file
def exportFutureList(userID):
    file_name = input("Please enter a name for your CSV file: ")

    # cleaning input to add csv if not there
    if file_name[-4:] != ".csv":
        file_name = file_name + ".csv"

    # writing future list to file
    with open(file_name, 'w', newline='') as csv_file:
        header = ["Title", "Type", "Release Year", "Content Rating", "Duration", "Description"]
        write = csv.DictWriter(csv_file, fieldnames=header)
        write.writeheader()
        query = '''SELECT Titles.TitleID, Title, ReleaseYear, Duration, Rating, Type, Description
                    FROM User_Record
                    INNER JOIN Titles ON User_Record.TitleID = Titles.TitleID
                    WHERE userID = %d
                    AND FutureList = 1'''
        cursor.execute(query % userID)
        rows = cursor.fetchall()
        for row in rows:
            write.writerow({'Title': row[1],
                            'Type': row[5],
                            'Release Year': row[2],
                            'Content Rating': row[4],
                            'Duration': row[3],
                            'Description': row[6]})

        print("Successfully Exported Future List to CSV File:", file_name)
        time.sleep(.5)

        db.commit()


# menu of all the options for the user
def menu(userID):
    while True:
        print("\nWhat would you like to do?")
        print("---------MENU---------")
        print("1) Select a Random Movie")
        print("2) Select a Random TV Show")
        print("3) See all Titles")
        print("4) Search by Title")
        print("5) Filter by Actor")
        print("6) Filter by Genre")
        print("7) Filter by Country")
        print("8) Filter by Director")
        print("9) View My Future List")
        print("10) See My Rated Titles")
        print("11) Export Future List")
        print("12) Delete My Account")
        print("13) Log Out and Exit")

        # checking user input is a number
        try:
            user_choice = int(input("Enter option here: "))
        except ValueError:
            print("Please enter a number.\n")
            continue

        if user_choice == 1:
            getRandomMovie(userID)
        elif user_choice == 2:
            getRandomShow(userID)
        elif user_choice == 3:
            printAllTitles(userID)
        elif user_choice == 4:
            searchByTitleName(userID)
        elif user_choice == 5:
            filterByActor(userID)
        elif user_choice == 6:
            filterByGenre(userID)
        elif user_choice == 7:
            filterByCountry(userID)
        elif user_choice == 8:
            filterByDirector(userID)
        elif user_choice == 9:
            viewFutureList(userID)
        elif user_choice == 10:
            viewRatings(userID)
        elif user_choice == 11:
            exportFutureList(userID)
        elif user_choice == 12:
            deleted = deleteAccount(userID)
            if deleted == 1:
                break
        elif user_choice == 13:
            print("\nAll done.")
            break
        else:
            print("\nPlease enter a number between 1 and 13.")
            time.sleep(.5)


# asks user for username and email and logs them in or creates a new account
def login():
    print("Welcome to Netflix Selector!")

    userName = input("Please enter your username or create a new username: ")
    userEmail = input("Please enter your email: ")

    # loading old id if user is in database
    if userInDatabase(userName, userEmail) is True:
        print("\nWelcome back, %s!\n" % userName)
        time.sleep(1)

    # creating new account for new users
    else:
        print("\nNew Account Created.")
        print("Welcome, %s!\n" % userName)
        time.sleep(1)
        cursor.execute("INSERT INTO USERS (Name, Email) VALUES (%s, %s)", [userName, userEmail])

    id = getUserID(userName, userEmail)
    db.commit()
    return id


# calling login and menu to run program
id = login()
menu(id)

# committing and closing database
db.commit()
db.close()