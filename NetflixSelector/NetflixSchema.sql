DROP DATABASE IF EXISTS Netflix;
CREATE DATABASE Netflix;
USE Netflix;

-- creating all tables
CREATE TABLE IF NOT EXISTS Titles(
                        TitleID INT NOT NULL AUTO_INCREMENT,
                        Title LONGTEXT NOT NULL,
                        ReleaseYear INT,
                        Duration VARCHAR(32),
                        Rating VARCHAR(20),
                        Type VARCHAR(20) NOT NULL,
                        DescriptiON TEXT,
                        CONSTRAINT PK_Titles PRIMARY KEY (TitleID)
                        );

CREATE TABLE IF NOT EXISTS Users(
                        UserID INT NOT NULL AUTO_INCREMENT,
                        Name VARCHAR(32),
                        Email VARCHAR(50),
                        IsDeleted INTEGER DEFAULT 0,
                        CONSTRAINT PK_Users PRIMARY KEY  (UserID)
                        );

CREATE TABLE IF NOT EXISTS User_Record(
                        RecordID INT NOT NULL AUTO_INCREMENT,
                        TitleID INT NOT NULL,
                        UserID INT NOT NULL DEFAULT 0,
                        UserRating TINYINT DEFAULT 0,
                        FutureList INTEGER DEFAULT 0,
                        UserWatched INTEGER DEFAULT 0,
                        IsDeleted INTEGER DEFAULT 0,
                        CONSTRAINT PK_UserRecord PRIMARY KEY  (RecordID)
                        );

CREATE TABLE IF NOT EXISTS Actors(
                            ActorID INT NOT NULL AUTO_INCREMENT,
                            Name VARCHAR(80) NOT NULL,
                            TypeID TINYINT NOT NULL DEFAULT 1,
                            CONSTRAINT PK_Actors PRIMARY KEY (ActorID)
                            );

CREATE TABLE IF NOT EXISTS Directors(
                            DirectorID INT NOT NULL AUTO_INCREMENT,
                            Name VARCHAR(80) NOT NULL ,
                            TypeID TINYINT NOT NULL DEFAULT 2,
                            CONSTRAINT PK_Directors PRIMARY KEY (DirectorID)
                            );

CREATE TABLE IF NOT EXISTS Countries(
                            CountryID INT NOT NULL AUTO_INCREMENT,
                            Name VARCHAR(70) NOT NULL,
                            TypeID TINYINT NOT NULL DEFAULT 3,
                            CONSTRAINT PK_Countries PRIMARY KEY  (CountryID)
                            );

CREATE TABLE IF NOT EXISTS Genres(
                            GenreID INT NOT NULL AUTO_INCREMENT,
                            Name VARCHAR(70) NOT NULL,
                            TypeID TINYINT NOT NULL DEFAULT 4,
                            CONSTRAINT PK_Genres PRIMARY KEY  (GenreID)
                            );

CREATE TABLE IF NOT EXISTS Title_Attributes(
                            TitleID INTEGER NOT NULL,
                            AttributeID INTEGER NOT NULL,
                            TypeID TINYINT NOT NULL,
                            CONSTRAINT PK_TitleAttributes PRIMARY KEY  (TitleID, AttributeID, TypeID)
                            );

CREATE TABLE IF NOT EXISTS Attribute_Types(
                            TypeID TINYINT NOT NULL AUTO_INCREMENT,
                            TypeName VARCHAR(70) NOT NULL,
                            CONSTRAINT PK_AttributeTypes PRIMARY KEY  (TypeID)
                            );

-- inserting the types of the attributes into table
INSERT INTO Attribute_Types VALUES (1,"Actor");
INSERT INTO Attribute_Types VALUES (2,"Director");
INSERT INTO Attribute_Types VALUES (3,"Country");
INSERT INTO Attribute_Types VALUES (4,"Genre");


-- foreign keys to cONnect the tables
ALTER TABLE User_Record ADD CONSTRAINT FK_RecordTitle
    FOREIGN KEY (TitleID) REFERENCES Titles (TitleID) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE User_Record ADD CONSTRAINT FK_RecordUser
    FOREIGN KEY (UserID) REFERENCES Users (UserID) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Title_Attributes ADD CONSTRAINT FK_TitlesAttType
    FOREIGN KEY (TitleID ) REFERENCES Titles (TitleID) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Actors ADD CONSTRAINT FK_Attributes_Actor
    FOREIGN KEY (TypeID ) REFERENCES Attribute_Types (TypeID) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Directors ADD CONSTRAINT FK_Attributes_Director
    FOREIGN KEY (TypeID ) REFERENCES Attribute_Types (TypeID) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Countries ADD CONSTRAINT FK_Attributes_Country
    FOREIGN KEY (TypeID ) REFERENCES Attribute_Types (TypeID) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Genres ADD CONSTRAINT FK_Attributes_Genre
    FOREIGN KEY (TypeID ) REFERENCES Attribute_Types (TypeID) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Title_Attributes ADD CONSTRAINT FK_AttributeType
    FOREIGN KEY (TypeID ) REFERENCES Attribute_Types (TypeID) ON DELETE CASCADE ON UPDATE CASCADE;

-- indexes to make queries faster
CREATE INDEX titleID_index ON Titles(TitleID);
CREATE INDEX actorID_index ON Actors(ActorID);
CREATE INDEX directorID_index ON Directors(DirectorID);

-- views to access titles AND their attributes
CREATE VIEW actors_titles AS
SELECT TitleID, ActorID, Name FROM Title_Attributes TA
INNER JOIN Attribute_Types AT ON TA.TypeID = AT.TypeID
INNER JOIN Actors A ON TA.TypeID = A.TypeID AND TA.AttributeID = A.ActorID;

Create view directors_titles as
Select TitleID, AttributeID, Name from Title_Attributes TA
INNER JOIN Attribute_Types AT ON TA.TypeID = AT.TypeID
INNER JOIN Directors D ON TA.AttributeID = D.DirectorID AND TA.TypeID = D.TypeID;

Create view countries_titles AS
Select TitleID, AttributeID, Name FROM Title_Attributes TA
INNER JOIN Attribute_Types AT ON TA.TypeID = AT.TypeID
INNER JOIN Countries C ON TA.AttributeID = C.CountryID AND TA.TypeID = C.TypeID;

CREATE VIEW genres_titles AS
SELECT TitleID,AttributeID, Name FROM Title_Attributes TA
INNER JOIN Attribute_Types AT ON TA.TypeID = AT.TypeID
INNER JOIN Genres G ON TA.AttributeID = G.GenreID AND TA.TypeID = G.TypeID;
