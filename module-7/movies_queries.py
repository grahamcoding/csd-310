# Daniel Graham
# Date 6/21/25

""" import statements """
import mysql.connector # to connect
from mysql.connector import errorcode

import dotenv # to use .env file
from dotenv import load_dotenv
from dotenv import dotenv_values

#using our .env file
secrets = dotenv_values(".env")

""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}

try:
    """ Try/catch block for handling potential MySQL database errors """
    db = mysql.connector.connect(**config)  # connect to the database

    cursor = db.cursor()

    # Query 1: Select all fields from the studio table
    print("\n-- DISPLAYING Studio RECORDS --")
    cursor.execute("SELECT * FROM studio;")
    studios = cursor.fetchall()
    for studio in studios:
        print("Studio ID: {}\nStudio Name: {}\n".format(studio[0], studio[1]))

    # Query 2: Select all fields from the genre table
    print("\n-- DISPLAYING Genre RECORDS --")
    cursor.execute("SELECT * FROM genre;")
    genres = cursor.fetchall()
    for genre in genres:
        print("Genre ID: {}\nGenre Name: {}\n".format(genre[0], genre[1]))

    # Query 3: Select movie names with runtime less than 120 minutes
    print("\n-- DISPLAYING Short Film RECORDS (runtime < 120 min) --")
    cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120;")
    short_films = cursor.fetchall()
    for film in short_films:
        print("Film Name: {}\nRuntime: {} minutes\n".format(film[0], film[1]))

    # Query 4: Group film names and directors by director
    print("\n-- DISPLAYING Director RECORDS in Grouped Order --")
    cursor.execute("SELECT film_director, film_name FROM film ORDER BY film_director;")
    directors = cursor.fetchall()
    for director in directors:
        print("Director: {}\nFilm Name: {}\n".format(director[0], director[1]))

    input("\n\n  Press any key to continue...")


except mysql.connector.Error as err:
    """ on error code """

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:
    """ close the connection to MySQL """

    db.close()