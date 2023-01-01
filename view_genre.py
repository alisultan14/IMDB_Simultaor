from choose import choose_action
import view_director
import view_movie


def choose_random_genre(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT genre_id FROM mutable.genres ORDER BY RANDOM() LIMIT 1;")
    (genre_id, ) = cursor.fetchone()
    cursor.close()

    return genre_id


def view_genre_directly(conn, user_id, genre_id):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO mutable.genre_stats(genre_id, direct_views, shares) 
    VALUES (%s, 1, 0)
    ON CONFLICT (genre_id) DO UPDATE 
        SET direct_views = genre_stats.direct_views + 1, last_updated = CURRENT_TIMESTAMP;
    """, (genre_id,))

    conn.commit()
    cursor.close()

    view_genre(conn, user_id, genre_id)
    return True


def view_genre_from_movie(conn, user_id, genre_id, movie_id):
    if genre_id is None:
        return True

    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO mutable.movie_to_genre_views(movie_id, genre_id, count) 
    VALUES (%s, %s, 1)
    ON CONFLICT (movie_id, genre_id) DO UPDATE 
        SET count = movie_to_genre_views.count + 1, last_updated = CURRENT_TIMESTAMP;
    """, (movie_id, genre_id))

    conn.commit()
    cursor.close()

    view_genre(conn, user_id, genre_id)
    return True


def view_genre_from_director(conn, user_id, genre_id, director_id):
    if genre_id is None:
        return True

    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO mutable.director_to_genre_views(director_id, genre_id, count) 
    VALUES (%s, %s, 1)
    ON CONFLICT (director_id, genre_id) DO UPDATE 
        SET count = director_to_genre_views.count + 1, last_updated = CURRENT_TIMESTAMP;
    """, (director_id, genre_id))

    conn.commit()
    cursor.close()

    view_genre(conn, user_id, genre_id)
    return True


def view_genre(conn, user_id, genre_id):
    weights = [40, 20, 20, 20]
    actions = [
        lambda: False,
        lambda: view_movie.view_movie_from_genre(conn, user_id, get_random_related_movie(conn, genre_id), genre_id),
        lambda: view_director.view_director_from_genre(conn, user_id, get_random_related_director(conn, genre_id),
                                                       genre_id),
        lambda: share(conn, genre_id)
    ]

    while choose_action(weights, actions):
        pass


def share(conn, genre_id):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO mutable.genre_stats(genre_id, direct_views, shares) 
    VALUES (%s, 0, 1)
    ON CONFLICT (genre_id) DO UPDATE 
        SET shares = genre_stats.shares + 1, last_updated = CURRENT_TIMESTAMP;
    """, (genre_id,))

    conn.commit()
    cursor.close()
    return True


def get_random_related_movie(conn, genre_id):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT movie_id, genre_id
    FROM imdb.movies_genres
    JOIN mutable.genres
    ON genres.name = movies_genres.genre
    WHERE genre_id = %s 
    ORDER BY RANDOM() 
    LIMIT 1;
    """, (genre_id,))

    result = cursor.fetchone()

    if result is None:
        return None

    (movie_id, result_genre_id) = result

    return movie_id


def get_random_related_director(conn, genre_id):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT director_id, genre_id
    FROM imdb.directors_genres 
    JOIN mutable.genres
    ON genres.name = directors_genres.genre
    WHERE genre_id = %s 
    ORDER BY RANDOM() 
    LIMIT 1;
    """, (genre_id,))

    result = cursor.fetchone()

    if result is None:
        return None

    (director_id, result_genre_id) = result

    return director_id
