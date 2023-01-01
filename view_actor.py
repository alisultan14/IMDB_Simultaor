from choose import choose_action
import view_movie
import create_news


def choose_random_actor(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM imdb.actors ORDER BY RANDOM() LIMIT 1;")
    (actor_id,) = cursor.fetchone()
    cursor.close()

    return actor_id


def view_actor_directly(conn, user_id, actor_id):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO mutable.actor_stats(actor_id, direct_views, shares) 
    VALUES (%s, 1, 0)
    ON CONFLICT (actor_id) DO UPDATE 
        SET direct_views = actor_stats.direct_views + 1, last_updated = CURRENT_TIMESTAMP;
    """, (actor_id,))

    conn.commit()
    cursor.close()

    view_actor(conn, user_id, actor_id)
    return True


def view_actor_from_movie(conn, user_id, actor_id, movie_id):
    if actor_id is None:
        return True

    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO mutable.movie_to_actor_views(movie_id, actor_id, count) 
    VALUES (%s, %s, 1)
    ON CONFLICT (movie_id, actor_id) DO UPDATE 
        SET count = movie_to_actor_views.count + 1, last_updated = CURRENT_TIMESTAMP;
    """, (movie_id, actor_id))

    conn.commit()
    cursor.close()

    view_actor(conn, user_id, actor_id)
    return True


def view_actor(conn, user_id, actor_id):
    weights = [40, 20, 20, 20]
    actions = [
        lambda: False,
        lambda: view_movie.view_movie_from_actor(conn, user_id, get_random_related_movie(conn, actor_id), actor_id),
        lambda: share(conn, actor_id),
        lambda: create_news.increase_clicks_actor(conn, create_news.get_actor_article(conn, actor_id))
    ]

    while choose_action(weights, actions):
        pass


def share(conn, actor_id):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO mutable.actor_stats(actor_id, direct_views, shares) 
    VALUES (%s, 0, 1)
    ON CONFLICT (actor_id) DO UPDATE 
        SET shares = actor_stats.shares + 1, last_updated = CURRENT_TIMESTAMP;
    """, (actor_id,))

    conn.commit()
    cursor.close()
    return True


def get_random_related_movie(conn, actor_id):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT movie_id, actor_id
    FROM imdb.roles 
    WHERE actor_id = %s 
    ORDER BY RANDOM() 
    LIMIT 1;
    """, (actor_id,))

    result = cursor.fetchone()

    if result is None:
        return None

    (movie_id, result_actor_id) = result

    return movie_id
