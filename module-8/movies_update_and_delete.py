# Daniel Graham
# Date: 7/5/25
# Assignment: Module 8 - Movies: Update & Delete

""" import statements """
import mysql.connector
from mysql.connector import errorcode

from dotenv import dotenv_values

# Using our .env file
secrets = dotenv_values(".env")

""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

def show_films(cursor, title):
    """ function to display film records with joined genre and studio """
    query = """
    SELECT film_name AS Name, film_director AS Director, genre_name AS Genre, studio_name AS 'Studio Name'
    FROM film
    INNER JOIN genre ON film.genre_id = genre.genre_id
    INNER JOIN studio ON film.studio_id = studio.studio_id
    """
    cursor.execute(query)
    films = cursor.fetchall()

    print("\n-- {} --".format(title))
    for film in films:
        print("Name: {}\nDirector: {}\nGenre: {}\nStudio: {}\n".format(film[0], film[1], film[2], film[3]))

try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    # Initial display of films
    show_films(cursor, "DISPLAYING FILMS")

    # Insert new film
    cursor.execute("""
    INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
    VALUES ('The Thing', '1982', 109, 'John Carpenter',
        (SELECT studio_id FROM studio WHERE studio_name = 'Universal Pictures'),
        (SELECT genre_id FROM genre WHERE genre_name = 'Horror'))
    """)
    db.commit()

    # Display after insert
    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    # Update Alien to Horror
    cursor.execute("""
    UPDATE film
    SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Horror')
    WHERE film_name = 'Alien'
    """)
    db.commit()

    # Display after update
    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE - Changed Alien to Horror")

    # Delete Gladiator
    cursor.execute("DELETE FROM film WHERE film_name = 'Gladiator'")
    db.commit()

    # Display after delete
    show_films(cursor, "DISPLAYING FILMS AFTER DELETE - Removed Gladiator")

    input("\n\nPress any key to continue...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
    else:
        print(err)

finally:
    db.close()