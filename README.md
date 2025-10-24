"""
Movie Management System in Python with MySQL Integration
Author: Priyansh Arya
Description:
This project is a console-based Movie Management System developed in Python.
It uses MySQL as the backend database to store all movie-related information.
The system allows users to perform various operations such as adding new movies,
viewing all movies, searching for movies, deleting movies, and exporting movie
data to a text file. The code is written with detailed comments and explanations
for clarity. This expanded version includes pre-filled sample movies, helper
functions for statistics, and detailed in-code documentation for educational
and submission purposes.
"""

# Import the required module to connect Python with MySQL
import mysql.connector  # Used for database connectivity

# -------------------- DATABASE INITIALIZATION -------------------- #
def connect_and_initialize():
    """
    Connects to the MySQL server, creates the database 'MovieDB' if it does not exist,
    and creates the 'movies' table if it does not exist. Also pre-fills the table
    with sample data if it is empty.
    """
    try:
        # Establish connection to MySQL server
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="PRIYANKAMAM",  # Replace with your MySQL password
            auth_plugin="mysql_native_password"  # Authentication plugin
        )
        cursor = connection.cursor()

        # Create database if it does not exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS MovieDB")
        cursor.execute("USE MovieDB")  # Select the database for use

        # Create movies table with necessary columns
        create_table_query = """
        CREATE TABLE IF NOT EXISTS movies (
            movie_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique ID for each movie
            title VARCHAR(255) NOT NULL,            -- Movie title
            genre VARCHAR(100),                     -- Movie genre
            release_year YEAR,                      -- Release year
            rating DECIMAL(3, 1),                   -- Rating (0.0 to 10.0)
            duration INT,                           -- Duration in minutes
            director VARCHAR(255)                   -- Director's name
        )
        """
        cursor.execute(create_table_query)
        connection.commit()  # Commit changes to database

        # Pre-fill sample movies if table is empty
        cursor.execute("SELECT COUNT(*) FROM movies")
        count = cursor.fetchone()[0]
        if count == 0:
            sample_movies = [
                ("Inception", "Sci-Fi", 2010, 9.0, 148, "Christopher Nolan"),
                ("Interstellar", "Sci-Fi", 2014, 8.6, 169, "Christopher Nolan"),
                ("The Matrix", "Sci-Fi", 1999, 8.7, 136, "Wachowski"),
                ("Avengers: Endgame", "Action", 2019, 8.4, 181, "Russo Brothers"),
                ("The Dark Knight", "Action", 2008, 9.0, 152, "Christopher Nolan"),
                ("Parasite", "Thriller", 2019, 8.6, 132, "Bong Joon-ho"),
                ("Titanic", "Romance", 1997, 7.8, 195, "James Cameron"),
                ("Joker", "Drama", 2019, 8.5, 122, "Todd Phillips")
            ]
            # Insert each sample movie into the database
            for movie in sample_movies:
                cursor.execute(
                    "INSERT INTO movies (title, genre, release_year, rating, duration, director) VALUES (%s,%s,%s,%s,%s,%s)",
                    movie
                )
            connection.commit()  # Save the changes

        # Close database connection
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        exit()  # Stop execution if there is a database error

# -------------------- DATABASE CONNECTION -------------------- #
def connect_db():
    """
    Connects to the MovieDB database and returns the connection object.
    Handles exceptions if the connection fails.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="PRIYANKAMAM",
            database="MovieDB",
            auth_plugin="mysql_native_password"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Connection Error: {err}")
        exit()

# -------------------- ADD NEW MOVIE -------------------- #
def add_movie():
    """
    Allows the user to add a new movie record to the database.
    Prompts the user for title, genre, release year, rating, duration, and director.
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Prompt user input
    title = input("Enter movie title: ")
    genre = input("Enter genre: ")
    release_year = input("Enter release year (YYYY): ")
    rating = input("Enter rating (0.0 - 10.0): ")
    duration = input("Enter duration (minutes): ")
    director = input("Enter director's name: ")

    try:
        query = "INSERT INTO movies (title, genre, release_year, rating, duration, director) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (title, genre, release_year, rating, duration, director))
        conn.commit()
        print("✅ Movie added successfully!")
    except Exception as e:
        print(f"Error adding movie: {e}")
    finally:
        cursor.close()
        conn.close()

# -------------------- VIEW ALL MOVIES -------------------- #
def view_movies():
    """
    Retrieves all movie records from the database and prints them in a
    formatted table for easy reading.
    """
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM movies"
    cursor.execute(query)
    results = cursor.fetchall()

    if results:
        print("\n=== Movies in Database ===")
        print(f"{'ID':<5} {'Title':<25} {'Genre':<15} {'Year':<6} {'Rating':<7} {'Duration':<10} {'Director'}")
        print("-" * 90)
        for row in results:
            print(f"{row[0]:<5} {row[1]:<25} {row[2]:<15} {row[3]:<6} {row[4]:<7} {row[5]:<10} {row[6]}")
    else:
        print("No movies found in the database.")
    cursor.close()
    conn.close()

# -------------------- SEARCH MOVIE -------------------- #
def search_movie():
    """
    Allows the user to search for movies by title or director name.
    Uses SQL LIKE operator for partial matches.
    """
    conn = connect_db()
    cursor = conn.cursor()

    search_term = input("Enter movie title or director name to search: ")
    query = "SELECT * FROM movies WHERE title LIKE %s OR director LIKE %s"
    cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))
    results = cursor.fetchall()

    if results:
        print("\n=== Search Results ===")
        print(f"{'ID':<5} {'Title':<25} {'Genre':<15} {'Year':<6} {'Rating':<7} {'Duration':<10} {'Director'}")
        print("-" * 90)
        for row in results:
            print(f"{row[0]:<5} {row[1]:<25} {row[2]:<15} {row[3]:<6} {row[4]:<7} {row[5]:<10} {row[6]}")
    else:
        print("No matching movies found.")
    cursor.close()
    conn.close()

# -------------------- DELETE MOVIE -------------------- #
def delete_movie():
    """
    Deletes a movie record based on the movie ID provided by the user.
    """
    conn = connect_db()
    cursor = conn.cursor()

    movie_id = input("Enter the Movie ID to delete: ")
    query = "DELETE FROM movies WHERE movie_id = %s"

    try:
        cursor.execute(query, (movie_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print("✅ Movie deleted successfully.")
        else:
            print("Movie ID not found.")
    except Exception as e:
        print(f"Error deleting movie: {e}")
    finally:
        cursor.close()
        conn.close()

# -------------------- EXPORT MOVIES TO FILE -------------------- #
def export_movies():
    """
    Exports all movies to a text file named 'movies_export.txt'.
    """
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM movies"
    cursor.execute(query)
    results = cursor.fetchall()

    if results:
        with open("movies_export.txt", "w") as file:
            file.write(f"{'ID':<5} {'Title':<25} {'Genre':<15} {'Year':<6} {'Rating':<7} {'Duration':<10} {'Director'}\n")
            file.write("-" * 90 + "\n")
            for row in results:
                file.write(f"{row[0]:<5} {row[1]:<25} {row[2]:<15} {row[3]:<6} {row[4]:<7} {row[5]:<10} {row[6]}\n")
        print("✅ Movies exported to 'movies_export.txt'")
    else:
        print("No movies to export.")
    cursor.close()
    conn.close()

# -------------------- MAIN MENU -------------------- #
def main_menu():
    """
    Displays the main menu of the Movie Management System and
    handles user input to perform different operations.
    """
    while True:
        print("\n===== Movie Management System =====")
        print("1. Add Movie")
        print("2. View Movies")
        print("3. Search Movies")
        print("4. Delete Movie")
        print("5. Export Movies to Text File")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            add_movie()
        elif choice == "2":
            view_movies()
        elif choice == "3":
            search_movie()
        elif choice == "4":
            delete_movie()
        elif choice == "5":
            export_movies()
        elif choice == "6":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 6.")

# -------------------- RUN PROGRAM -------------------- #
if __name__ == "__main__":
    connect_and_initialize()  # Initialize database, table, and pre-fill data
    main_menu()  # Start the main menu loop
