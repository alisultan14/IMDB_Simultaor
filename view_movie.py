from choose import choose_action
import view_actor
import view_director
import view_genre


def choose_random_movie(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM imdb.movies ORDER BY RANDOM() LIMIT 1;")
    (movie_id, ) = cursor.fetchone()
    cursor.close()

    return movie_id


def view_movie_directly(conn, user_id, movie_id):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO mutable.movie_stats(movie_id, direct_views, shares) 
    VALUES (%s, 1, 0)
    ON CONFLICT (movie_id) DO UPDATE 
        SET direct_views = movie_stats.direct_views + 1, last_updated = CURRENT_TIMESTAMP;
    """, (movie_id,))

    conn.commit()
    cursor.close()

    view_movie(conn, user_id, movie_id)
    return True


def view_movie_from_actor(conn, user_id, movie_id, actor_id):
    if movie_id is None:
        return True

    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO mutable.actor_to_movie_views(actor_id, movie_id, count) 
    VALUES (%s, %s, 1)
    ON CONFLICT (actor_id, movie_id) DO UPDATE 
        SET count = actor_to_movie_views.count + 1, last_updated = CURRENT_TIMESTAMP;
    """, (actor_id, movie_id))

    conn.commit()
    cursor.close()

    view_movie(conn, user_id, movie_id)
    return True


def view_movie_from_director(conn, user_id, movie_id, director_id):
    if movie_id is None:
        return True

    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO mutable.director_to_movie_views(director_id, movie_id, count) 
    VALUES (%s, %s, 1)
    ON CONFLICT (director_id, movie_id) DO UPDATE 
        SET count = director_to_movie_views.count + 1, last_updated = CURRENT_TIMESTAMP;
    """, (director_id, movie_id))

    conn.commit()
    cursor.close()

    view_movie(conn, user_id, movie_id)
    return True


def view_movie_from_genre(conn, user_id, movie_id, genre_id):
    if movie_id is None:
        return True

    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO mutable.genre_to_movie_views(genre_id, movie_id, count) 
    VALUES (%s, %s, 1)
    ON CONFLICT (genre_id, movie_id) DO UPDATE 
        SET count = genre_to_movie_views.count + 1, last_updated = CURRENT_TIMESTAMP;
    """, (genre_id, movie_id))

    conn.commit()
    cursor.close()

    view_movie(conn, user_id, movie_id)
    return True


def view_movie(conn, user_id, movie_id):
    get_comments(conn, movie_id)

    weights = [40, 12, 12, 12, 12, 12]
    actions = [
        lambda: False,
        lambda: view_actor.view_actor_from_movie(conn, user_id, get_random_related_actor(conn, movie_id), movie_id),
        lambda: view_director.view_director_from_movie(conn, user_id, get_random_related_director(conn, movie_id),
                                                       movie_id),
        lambda: view_genre.view_genre_from_movie(conn, user_id, get_random_related_genre(conn, movie_id), movie_id),
        lambda: share(conn, movie_id),
        lambda: want_to_see(conn, user_id, movie_id)
    ]

    while choose_action(weights, actions):
        pass


def get_comments(conn, movie_id):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * 
    FROM mutable.comments
    WHERE movie_id = %s;
    """, (movie_id,))
    comments = cursor.fetchall()

    cursor.close()


def want_to_see(conn, user_id, movie_id):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT user_id, movie_id 
    FROM mutable.want_to_see 
    WHERE user_id = %s AND movie_id = %s;
    """, (user_id, movie_id))

    already_want_to_see = cursor.fetchone() is not None

    if already_want_to_see:
        cursor.execute("""
        DELETE FROM mutable.want_to_see
        WHERE user_id = %s AND movie_id = %s;
        """, (user_id, movie_id))
    else:
        cursor.execute("""
        INSERT INTO mutable.want_to_see(user_id, movie_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING;
        """, (user_id, movie_id))

    conn.commit()
    cursor.close()

    return True


def share(conn, movie_id):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO mutable.movie_stats(movie_id, direct_views, shares) 
    VALUES (%s, 0, 1)
    ON CONFLICT (movie_id) DO UPDATE 
        SET shares = movie_stats.shares + 1, last_updated = CURRENT_TIMESTAMP;
    """, (movie_id,))

    conn.commit()
    cursor.close()
    return True


def get_random_related_actor(conn, movie_id):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT actor_id, movie_id 
    FROM imdb.roles 
    WHERE movie_id = %s 
    ORDER BY RANDOM() 
    LIMIT 1;
    """, (movie_id,))

    result = cursor.fetchone()

    if result is None:
        return None

    (actor_id, result_movie_id) = result

    return actor_id


def get_random_related_director(conn, movie_id):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT director_id, movie_id 
    FROM imdb.movies_directors 
    WHERE movie_id = %s 
    ORDER BY RANDOM() 
    LIMIT 1;
    """, (movie_id,))

    result = cursor.fetchone()

    if result is None:
        return None

    (director_id, result_movie_id) = result

    return director_id


def get_random_related_genre(conn, movie_id):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT genre_id, movie_id 
    FROM imdb.movies_genres 
    JOIN mutable.genres 
    ON movies_genres.genre = genres.name
    WHERE movie_id = %s 
    ORDER BY RANDOM() 
    LIMIT 1;
    """, (movie_id,))

    result = cursor.fetchone()

    if result is None:
        return None

    (genre_id, result_movie_id) = result

    return genre_id
