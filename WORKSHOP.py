import mysql.connector

# Function to connect to MySQL and create the database and table
def connect_and_initialize():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Your MySQL username
            password="PRIYANKAMAM",  # Your MySQL password
            auth_plugin="mysql_native_password"
        )
        cursor = connection.cursor()

        # Create database if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS MovieDB")
        cursor.execute("USE MovieDB")

        # Create movies table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS movies (
            movie_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            genre VARCHAR(100),
            release_year YEAR,
            rating DECIMAL(3, 1),
            duration INT,
            director VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()

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
                ("Parasite", "Thriller", 2019, 8.6, 132, "Bong Joon-ho")
            ]
            for m in sample_movies:
                cursor.execute(
                    "INSERT INTO movies (title, genre, release_year, rating, duration, director) VALUES (%s,%s,%s,%s,%s,%s)",
                    m
                )
            connection.commit()

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit()

# Function to connect to MovieDB
def connect_db():
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
        print(f"Error: {err}")
        exit()

# Function to add a movie
def add_movie():
    conn = connect_db()
    cursor = conn.cursor()
    title = input("Enter movie title: ")
    genre = input("Enter genre: ")
    release_year = input("Enter release year: ")
    rating = input("Enter rating (0.0 - 10.0): ")
    duration = input("Enter duration (in minutes): ")
    director = input("Enter director's name: ")
    
    try:
        query = "INSERT INTO movies (title, genre, release_year, rating, duration, director) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (title, genre, release_year, rating, duration, director))
        conn.commit()
        print("Movie added successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to view all movies
def view_movies():
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM movies"
    cursor.execute(query)
    results = cursor.fetchall()
    if results:
        print("\n=== Movies ===")
        print(f"{'ID':<5} {'Title':<25} {'Genre':<15} {'Year':<6} {'Rating':<7} {'Duration':<10} {'Director'}")
        print("-" * 80)
        for row in results:
            print(f"{row[0]:<5} {row[1]:<25} {row[2]:<15} {row[3]:<6} {row[4]:<7} {row[5]:<10} {row[6]}")
    else:
        print("No movies found!")
    cursor.close()
    conn.close()

# Function to search for a movie
def search_movie():
    conn = connect_db()
    cursor = conn.cursor()
    search_term = input("Enter movie title or director name: ")
    query = "SELECT * FROM movies WHERE title LIKE %s OR director LIKE %s"
    cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))
    results = cursor.fetchall()
    if results:
        print("\n=== Search Results ===")
        print(f"{'ID':<5} {'Title':<25} {'Genre':<15} {'Year':<6} {'Rating':<7} {'Duration':<10} {'Director'}")
        print("-" * 80)
        for row in results:
            print(f"{row[0]:<5} {row[1]:<25} {row[2]:<15} {row[3]:<6} {row[4]:<7} {row[5]:<10} {row[6]}")
    else:
        print("No movies found!")
    cursor.close()
    conn.close()

# Function to delete a movie
def delete_movie():
    conn = connect_db()
    cursor = conn.cursor()
    movie_id = input("Enter movie ID to delete: ")
    query = "DELETE FROM movies WHERE movie_id = %s"
    try:
        cursor.execute(query, (movie_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print("Movie deleted successfully!")
        else:
            print("Movie not found!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to export movies to a text file
def export_movies():
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM movies"
    cursor.execute(query)
    results = cursor.fetchall()
    if results:
        with open("movies_export.txt", "w") as file:
            file.write(f"{'ID':<5} {'Title':<25} {'Genre':<15} {'Year':<6} {'Rating':<7} {'Duration':<10} {'Director'}\n")
            file.write("-" * 80 + "\n")
            for row in results:
                file.write(f"{row[0]:<5} {row[1]:<25} {row[2]:<15} {row[3]:<6} {row[4]:<7} {row[5]:<10} {row[6]}\n")
        print("Movies exported to 'movies_export.txt'")
    else:
        print("No movies to export!")
    cursor.close()
    conn.close()

# ===== AI-style Recommendation Feature (Case-Insensitive) =====
def recommend_movie():
    conn = connect_db()
    cursor = conn.cursor()
    movie_title = input("Enter a movie you like for recommendation: ")
    
    # Get the genre of the selected movie (case-insensitive)
    cursor.execute("SELECT genre FROM movies WHERE LOWER(title)=LOWER(%s)", (movie_title,))
    result = cursor.fetchone()
    if not result:
        print("Movie not found!")
        cursor.close()
        conn.close()
        return
    
    genre = result[0]
    # Recommend other movies of same genre with high rating (case-insensitive)
    cursor.execute(
        "SELECT title, rating FROM movies WHERE genre=%s AND LOWER(title)!=LOWER(%s) ORDER BY rating DESC LIMIT 5",
        (genre, movie_title)
    )
    recommendations = cursor.fetchall()
    
    if recommendations:
        print(f"\nBecause you liked '{movie_title}' ({genre}), you may also like:")
        for r in recommendations:
            print(f"{r[0]} - Rating: {r[1]}")
    else:
        print("No recommendations found!")
    
    cursor.close()
    conn.close()
# ============================================

# Main menu
def main_menu():
    while True:
        print("\n===== Movie Management System =====")
        print("1. Add Movie")
        print("2. View Movies")
        print("3. Search Movies")
        print("4. Delete Movie")
        print("5. Export Movies to Text File")
        print("6. Recommend Movies")
        print("7. Exit")
        choice = input("Enter your choice: ")
        
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
            recommend_movie()
        elif choice == "7":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

# Run the program
if __name__ == "__main__":
    connect_and_initialize()  # Initialize database, table, and pre-fill sample movies
    main_menu()
