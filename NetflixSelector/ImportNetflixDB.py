import mysql.connector
import csv

db = mysql.connector.connect(
    host="localhost",
    user="root",
    auth_plugin='mysql_native_password',
    passwd="ssSS!5152541",
    database = "Netflix"
)
cursor = db.cursor()

# helper function to get actor id from name
def getActorID(name):
    cursor.execute("select ActorID from Actors where Name = %s", [name])
    crsr = cursor.fetchall()

    if len(crsr) > 0:
        return crsr[0][0]
    else:
        return -1

# helper function to get country id from name
def getCountryID(name):
    cursor.execute("select CountryID from Countries where Name = %s", [name])
    crsr = cursor.fetchall()

    if len(crsr) > 0:
        return crsr[0][0]
    else:
        return -1

# helper function to get genre id from name
def getGenreID(name):
    cursor.execute("select GenreID from Genres where Name = %s", [name])
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

# inputting all the actors, directors, countries, and genres into their respective tables
with open("titleExtras.csv", 'r', newline='') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for line in csv_reader:
        if len(line[0]) != 0:
            cursor.execute("INSERT INTO Directors(Name) VALUES (%s)", [line[0]])
        if len(line[1]) != 0:
            cursor.execute("INSERT INTO Actors(Name) VALUES (%s)", [line[1]])
        if len(line[2]) != 0:
            cursor.execute("INSERT INTO Countries(Name) VALUES (%s)", [line[2]])
        if len(line[3]) != 0:
            cursor.execute("INSERT INTO Genres(Name) VALUES (%s)", [line[3]])
    db.commit()


# inputting all the titles into the db and connecting them to the actors, directors, countries, and genres
with open("netflix.csv", 'r', newline='') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for line in csv_reader:
            TitleID = int(line[0])
            cursor.execute("INSERT INTO Titles(Title,ReleaseYear, Duration, Rating, Type, Description) VALUES (%s,%s,%s,%s,%s,%s)",
                           [line[2], line[79], line[81], line[80], line[1], line[85]])

            for i in range(16,66):
                id = getActorID(line[i])
                # print(type(id))
                # print(id)
                if id != -1:
                    cursor.execute("INSERT INTO Title_Attributes VALUES (%d,%d,%d)" %
                                   (TitleID, id,1))

            for i in range(3,13):
                id = getDirectorID(line[i])
                if id != -1:
                  cursor.execute("INSERT INTO Title_Attributes VALUES (%d,%d,%d)" %
                                 (TitleID, id,2))

            for i in range(66,77):
                id = getCountryID(line[i])
                if id != -1:
                    cursor.execute("INSERT INTO Title_Attributes VALUES (%d,%d,%d)" %
                            (TitleID, id,3))

            for i in range(82,85):

                id = getGenreID(line[i])
                if id != -1:
                    cursor.execute("INSERT INTO Title_Attributes VALUES (%d,%d,%d)" %
                            (TitleID, id,4))
db.commit()
