import csv
from array import array


def insert_imdb_data(conn):
    cursor = conn.cursor()

    # Insert data into movies table
    with open('imdb_movies.csv', 'r') as insert_Movies:
        for row in make_csv_reader(insert_Movies):
            cursor.execute(
                "INSERT INTO imdb.movies (id, name, year, rank) VALUES(%s,%s,%s,%s);",
                get_values_from_row(row))

    print("Finished movies")

    # Insert data into actors table
    with open('imdb_actors.csv', 'r') as insert_Actors:
        for row in make_csv_reader(insert_Actors):
            cursor.execute(
                "INSERT INTO imdb.actors (id, first_name, last_name, gender) VALUES(%s,%s,%s,%s);",
                get_values_from_row(row))

        conn.commit()

    print("Finished actors")

    # Insert data into directors table
    with open('imdb_directors.csv', 'r') as insert_Directors:
        for row in make_csv_reader(insert_Directors):
            cursor.execute(
                "INSERT INTO imdb.directors (id, first_name, last_name) VALUES(%s,%s,%s);",
                get_values_from_row(row))
        conn.commit()

    print("Finished directors")

    # Insert data into directors_genres table
    with open('imdb_directors_genres.csv', 'r') as insert_Directors_Genres:
        director_ids = get_random_director_ids(conn)
        director_index = 0

        for row in make_csv_reader(insert_Directors_Genres):
            (director_id, genre, prob) = get_values_from_row(row)
            if not is_director_id(conn, director_id):
                director_id = director_ids[director_index]
                director_index = (director_index + 1) % len(director_ids)
            cursor.execute(
                "INSERT INTO imdb.directors_genres (director_id, genre, prob) VALUES(%s,%s,%s);",
                (director_id, genre, prob))
        conn.commit()

    print("Finished directors_genres")

    # Insert data into Professor_courses table
    with open('imdb_roles.csv', 'r') as insert_Roles:
        for row in make_csv_reader(insert_Roles):
            cursor.execute(
                "INSERT INTO imdb.roles (actor_id, movie_id, role) VALUES(%s,%s,%s);",
                get_values_from_row(row))
        conn.commit()

    print("Finished roles")

    # Insert data into movies_directors table
    with open('imdb_movies_directors.csv', 'r') as insert_Movies_Directors:
        movie_ids = get_random_movie_ids(conn)
        movie_index = 0

        director_ids = get_random_director_ids(conn)
        director_index = 0

        for row in make_csv_reader(insert_Movies_Directors):
            (movie_id, director_id) = get_values_from_row(row)
            if not is_movie_id(conn, movie_id):
                movie_id = movie_ids[movie_index]
                movie_index = (movie_index + 1) % len(movie_ids)
            if not is_director_id(conn, director_id):
                director_id = director_ids[director_index]
                director_index = (director_index + 1) % len(director_ids)

            cursor.execute(
                "INSERT INTO imdb.movies_directors (movie_id, director_id) VALUES(%s,%s);",
                (movie_id, director_id))
        conn.commit()

    print("Finished movies_directors")

    # Insert data into movies_genres table
    with open('imdb_movies_genres.csv', 'r') as insert_Movies_Genres:
        movie_ids = get_random_movie_ids(conn)
        movie_index = 0

        for row in make_csv_reader(insert_Movies_Genres):
            (movie_id, genre) = get_values_from_row(row)
            if not is_movie_id(conn, movie_id):
                movie_id = movie_ids[movie_index]
                movie_index = (movie_index + 1) % len(movie_ids)
            cursor.execute(
                "INSERT INTO imdb.movies_genres (movie_id, genre) VALUES(%s,%s);",
                (movie_id, genre))
        conn.commit()

    print("Finished movies_genres")

    cursor.execute("""
    INSERT INTO mutable.genres (name) 
    SELECT DISTINCT genre FROM imdb.movies_genres UNION SELECT DISTINCT genre FROM imdb.directors_genres;""")
    conn.commit()
    print("Finished inserting all genres")

    # ending session
    cursor.close()


def is_director_id(conn, director_id):
    cursor = conn.cursor()
    cursor.execute("SELECT id from imdb.directors WHERE id = %s LIMIT 1;", (director_id, ))
    is_valid = cursor.fetchone() is not None
    cursor.close()
    return is_valid


def is_movie_id(conn, movie_id):
    cursor = conn.cursor()
    cursor.execute("SELECT id from imdb.movies WHERE id = %s LIMIT 1;", (movie_id, ))
    is_valid = cursor.fetchone() is not None
    cursor.close()
    return is_valid


def get_random_director_ids(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id from imdb.directors ORDER BY RANDOM();")

    director_ids = array('i')

    for (director_id, ) in cursor.fetchall():
        director_ids.append(director_id)

    return director_ids


def get_random_movie_ids(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id from imdb.movies ORDER BY RANDOM();")

    movie_ids = array('i')

    for (movie_id,) in cursor.fetchall():
        movie_ids.append(movie_id)

    return movie_ids


def make_csv_reader(file):
    return csv.reader(file, delimiter=',', quotechar='\'', escapechar='\\')


def get_values_from_row(row):
    return trim(row)


def trim(strings):
    return [remove_quotes(string.strip()) for string in strings]


def remove_quotes(string):
    result = string
    if result.startswith("'"):
        result = result[1:]
    if result.endswith("'"):
        result = result[:-1]
    if result == "NULL":
        return None
    return result
