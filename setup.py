import populate_imdb
from connect import DBConnection
import tear_down


def global_setup():
    conn = DBConnection(True)
    tear_down.tear_down(conn)
    create_immutable_tables(conn)
    create_mutable_tables(conn)
    populate_imdb.insert_imdb_data(conn)
    conn.close()


def create_immutable_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE imdb.actors (
        id int NOT NULL default 0,
        first_name varchar(100) default NULL,
        last_name varchar(100) default NULL,
        gender char(1) default NULL,
        PRIMARY KEY (id)
    );
    """)

    cursor.execute("""
    CREATE TABLE imdb.directors (
        id int NOT NULL default 0,
        first_name varchar(100) default NULL,
        last_name varchar(100) default NULL,
        PRIMARY KEY (id)
    );
    """)

    cursor.execute("""
    CREATE TABLE imdb.movies (
        id int NOT NULL default 0,
        name varchar(100) default NULL,
        year int default NULL,
        rank float default NULL,
        PRIMARY KEY (id)
    );
    """)

    cursor.execute("""
    CREATE TABLE imdb.directors_genres (
        director_id int default NULL,
        genre varchar(100) default NULL,
        prob float default NULL,
        FOREIGN KEY (director_id) REFERENCES imdb.directors (id)
    );
    """)

    cursor.execute("""
    CREATE TABLE imdb.movies_directors (
        director_id int default NULL,
        movie_id int default NULL,
        FOREIGN KEY (director_id) REFERENCES imdb.directors (id),
        FOREIGN KEY (movie_id) REFERENCES imdb.movies (id)
    );
    """)

    cursor.execute("""
    CREATE TABLE imdb.movies_genres (
        movie_id int default NULL,
        genre varchar(100) default NULL,
        FOREIGN KEY (movie_id) REFERENCES imdb.movies (id)
    );
    """)

    cursor.execute("""
    CREATE TABLE imdb.roles (
        actor_id int default NULL,
        movie_id int default NULL,
        role varchar(100) default NULL,
        FOREIGN KEY (actor_id) REFERENCES imdb.actors (id),
        FOREIGN KEY (movie_id) REFERENCES imdb.movies (id)
    );
    """)

    conn.commit()


def create_mutable_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE mutable.users (
        user_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        is_critic BOOLEAN NOT NULL,
        is_hired BOOLEAN NOT NULL,
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.reviews (
        movie_id INTEGER NOT NULL,
        creator_id INTEGER NOT NULL,
        review VARCHAR(12500) NOT NULL,
        engagement INTEGER CHECK (engagement BETWEEN 1 AND 5),
        excitement INTEGER CHECK (excitement BETWEEN 1 AND 5),
        prod_quality INTEGER CHECK (prod_quality BETWEEN 1 AND 5),
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(movie_id, creator_id),
        FOREIGN KEY (movie_id) REFERENCES imdb.movies(id),
        FOREIGN KEY (creator_id) REFERENCES mutable.users(user_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.comments (
        comment_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        movie_id INTEGER NOT NULL,
        review_author_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        comment VARCHAR(1000) NOT NULL,
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (movie_id, review_author_id) REFERENCES mutable.reviews(movie_id, creator_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.review_invites (
        movie_id INTEGER,
        creator_id INTEGER,
        invitee_id INTEGER,
        dismissed BOOLEAN DEFAULT FALSE,
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (movie_id, creator_id, invitee_id),
        FOREIGN KEY (movie_id, creator_id) REFERENCES mutable.reviews(movie_id, creator_id),
        FOREIGN KEY (invitee_id) REFERENCES mutable.users(user_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.want_to_see (
        user_id INTEGER,
        movie_id INTEGER,
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, movie_id),
        FOREIGN KEY (user_id) REFERENCES mutable.users(user_id),
        FOREIGN KEY (movie_id) REFERENCES imdb.movies(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.surveys (
        survey_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        creator_id INTEGER NOT NULL,
        movie_id INTEGER NOT NULL,
        survey_name VARCHAR(100) NOT NULL,
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (creator_id) REFERENCES mutable.users(user_id),
        FOREIGN KEY (movie_id) REFERENCES imdb.movies(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.survey_questions (
        question_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        survey_id INTEGER NOT NULL,
        question VARCHAR(200) NOT NULL,
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (survey_id) REFERENCES mutable.surveys(survey_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.survey_invites (
        survey_id INTEGER,
        invitee_id INTEGER,
        dismissed BOOLEAN DEFAULT FALSE,
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (survey_id, invitee_id),
        FOREIGN KEY (survey_id) REFERENCES mutable.surveys(survey_id),
        FOREIGN KEY (invitee_id) REFERENCES mutable.users(user_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.survey_responses (
        question_id INTEGER,
        respondent_id INTEGER,
        value INTEGER CHECK (value BETWEEN 1 AND 5),
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (question_id, respondent_id),
        FOREIGN KEY (question_id) REFERENCES mutable.survey_questions(question_id),
        FOREIGN KEY (respondent_id) REFERENCES mutable.users(user_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.genres (
        genre_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        name VARCHAR(100) UNIQUE NOT NULL,
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.movie_stats (
        movie_id INTEGER PRIMARY KEY,
        direct_views INTEGER CHECK (direct_views >= 0),
        shares INTEGER CHECK (shares >= 0),
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (movie_id) REFERENCES imdb.movies(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.actor_stats (
        actor_id INTEGER PRIMARY KEY,
        direct_views INTEGER CHECK (direct_views >= 0),
        shares INTEGER CHECK (shares >= 0),
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (actor_id) REFERENCES imdb.actors(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.actor_news (
        article_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        actor_id INTEGER NOT NULL,
        title VARCHAR(100) NOT NULL,
        clicks INTEGER CHECK (clicks >= 0),
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (actor_id) REFERENCES imdb.actors(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.director_stats (
        director_id INTEGER PRIMARY KEY,
        direct_views INTEGER CHECK (direct_views >= 0),
        shares INTEGER CHECK (shares >= 0),
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (director_id) REFERENCES imdb.directors(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.director_news (
        article_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        director_id INTEGER NOT NULL,
        title VARCHAR(100) NOT NULL,
        clicks INTEGER CHECK (clicks >= 0),
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (director_id) REFERENCES imdb.directors(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.genre_stats (
        genre_id INTEGER PRIMARY KEY,
        direct_views INTEGER CHECK (direct_views >= 0),
        shares INTEGER CHECK (shares >= 0),
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (genre_id) REFERENCES mutable.genres(genre_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.movie_to_actor_views (
        movie_id INTEGER NOT NULL,
        actor_id INTEGER NOT NULL,
        count INTEGER CHECK (count >= 0),
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (movie_id, actor_id),
        FOREIGN KEY (movie_id) REFERENCES imdb.movies(id),
        FOREIGN KEY (actor_id) REFERENCES imdb.actors(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.actor_to_movie_views (
        actor_id INTEGER NOT NULL,
        movie_id INTEGER NOT NULL,
        count INTEGER CHECK (count >= 0),
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (actor_id, movie_id),
        FOREIGN KEY (actor_id) REFERENCES imdb.actors(id),
        FOREIGN KEY (movie_id) REFERENCES imdb.movies(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.movie_to_director_views (
        movie_id INTEGER NOT NULL,
        director_id INTEGER NOT NULL,
        count INTEGER CHECK (count >= 0),
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (movie_id, director_id),
        FOREIGN KEY (movie_id) REFERENCES imdb.movies(id),
        FOREIGN KEY (director_id) REFERENCES imdb.directors(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.director_to_movie_views (
        director_id INTEGER NOT NULL,
        movie_id INTEGER NOT NULL,
        count INTEGER CHECK (count >= 0),
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (director_id, movie_id),
        FOREIGN KEY (director_id) REFERENCES imdb.directors(id),
        FOREIGN KEY (movie_id) REFERENCES imdb.movies(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.movie_to_genre_views (
        movie_id INTEGER NOT NULL,
        genre_id INTEGER NOT NULL,
        count INTEGER CHECK (count >= 0),
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (movie_id, genre_id),
        FOREIGN KEY (movie_id) REFERENCES imdb.movies(id),
        FOREIGN KEY (genre_id) REFERENCES mutable.genres(genre_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.genre_to_movie_views (
        genre_id INTEGER NOT NULL,
        movie_id INTEGER NOT NULL,
        count INTEGER CHECK (count >= 0),
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (genre_id, movie_id),
        FOREIGN KEY (genre_id) REFERENCES mutable.genres(genre_id),
        FOREIGN KEY (movie_id) REFERENCES imdb.movies(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.director_to_genre_views (
        director_id INTEGER NOT NULL,
        genre_id INTEGER NOT NULL,
        count INTEGER CHECK (count >= 0),
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (director_id, genre_id),
        FOREIGN KEY (director_id) REFERENCES imdb.directors(id),
        FOREIGN KEY (genre_id) REFERENCES mutable.genres(genre_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.genre_to_director_views (
        genre_id INTEGER NOT NULL,
        director_id INTEGER NOT NULL,
        count INTEGER CHECK (count >= 0),
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (genre_id, director_id),
        FOREIGN KEY (genre_id) REFERENCES mutable.genres(genre_id),
        FOREIGN KEY (director_id) REFERENCES imdb.directors(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.constraints (
        constraint_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        description VARCHAR(200) NOT NULL,
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.integrity_violations (
        constraint_id INTEGER NOT NULL,
        reason VARCHAR(100) NOT NULL,
        creation_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (constraint_id) REFERENCES mutable.constraints(constraint_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.performance_stats (
        is_write BOOLEAN NOT NULL,
        min_time FLOAT CHECK (min_time >= 0),
        avg_time FLOAT CHECK (avg_time >= 0),
        max_time FLOAT CHECK (max_time >= 0),
        start_time TIMESTAMP NOT NULL,
        end_time TIMESTAMP NOT NULL,
        num_requests INTEGER CHECK (num_requests >= 0)
    );
    """)

    cursor.execute("""
    CREATE TABLE mutable.failed_requests (
        reason VARCHAR(500) NOT NULL,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
