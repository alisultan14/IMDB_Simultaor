from choose import choose_action
import view_genre
import view_movie
import create_news


def choose_random_director(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM imdb.directors ORDER BY RANDOM() LIMIT 1;")
    (director_id, ) = cursor.fetchone()
    cursor.close()

    return director_id


def view_director_directly(conn, user_id, director_id):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO mutable.director_stats(director_id, direct_views, shares) 
    VALUES (%s, 1, 0)
    ON CONFLICT (director_id) DO UPDATE 
        SET direct_views = director_stats.direct_views + 1, last_updated = CURRENT_TIMESTAMP;
    """, (director_id,))

    conn.commit()
    cursor.close()

    view_director(conn, user_id, director_id)
    return True


def view_director_from_movie(conn, user_id, director_id, movie_id):
    if director_id is None:
        return True

    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO mutable.movie_to_director_views(movie_id, director_id, count) 
    VALUES (%s, %s, 1)
    ON CONFLICT (movie_id, director_id) DO UPDATE 
        SET count = movie_to_director_views.count + 1, last_updated = CURRENT_TIMESTAMP;
    """, (movie_id, director_id))

    conn.commit()
    cursor.close()

    view_director(conn, user_id, director_id)
    return True


def view_director_from_genre(conn, user_id, director_id, genre_id):
    if director_id is None:
        return True

    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO mutable.genre_to_director_views(genre_id, director_id, count) 
    VALUES (%s, %s, 1)
    ON CONFLICT (genre_id, director_id) DO UPDATE 
        SET count = genre_to_director_views.count + 1, last_updated = CURRENT_TIMESTAMP;
    """, (genre_id, director_id))

    conn.commit()
    cursor.close()

    view_director(conn, user_id, director_id)
    return True


def view_director(conn, user_id, director_id):
    weights = [40, 15, 15, 15, 15]
    actions = [
        lambda: False,
        lambda: view_movie.view_movie_from_director(conn, user_id, get_random_related_movie(conn, director_id),
                                                    director_id),
        lambda: view_genre.view_genre_from_director(conn, user_id, get_random_related_genre(conn, director_id),
                                                    director_id),
        lambda: share(conn, director_id),
        lambda: create_news.increase_clicks_director(conn, create_news.get_director_article(conn, director_id))
    ]

    while choose_action(weights, actions):
        pass


def share(conn, director_id):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO mutable.director_stats(director_id, direct_views, shares) 
    VALUES (%s, 0, 1)
    ON CONFLICT (director_id) DO UPDATE 
        SET shares = director_stats.shares + 1, last_updated = CURRENT_TIMESTAMP;
    """, (director_id,))

    conn.commit()
    cursor.close()
    return True


def get_random_related_movie(conn, director_id):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT movie_id, director_id
    FROM imdb.movies_directors 
    WHERE director_id = %s 
    ORDER BY RANDOM() 
    LIMIT 1;
    """, (director_id,))

    result = cursor.fetchone()

    if result is None:
        return None

    (movie_id, result_director_id) = result

    return movie_id


def get_random_related_genre(conn, director_id):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT genre_id, director_id
    FROM imdb.directors_genres 
    JOIN mutable.genres
    ON genres.name = directors_genres.genre
    WHERE director_id = %s 
    ORDER BY RANDOM() 
    LIMIT 1;
    """, (director_id,))

    result = cursor.fetchone()

    if result is None:
        return None

    (genre_id, result_director_id) = result

    return genre_id
