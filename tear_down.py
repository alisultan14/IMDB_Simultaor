def tear_down(conn):
    cursor = conn.cursor()

    cursor.execute("""
    DROP TABLE IF EXISTS mutable.comments;
    DROP TABLE IF EXISTS mutable.review_invites;
    DROP TABLE IF EXISTS mutable.want_to_see;
    DROP TABLE IF EXISTS mutable.survey_invites;
    DROP TABLE IF EXISTS mutable.survey_responses;
    DROP TABLE IF EXISTS mutable.survey_questions;
    DROP TABLE IF EXISTS mutable.movie_stats;
    DROP TABLE IF EXISTS mutable.actor_stats;
    DROP TABLE IF EXISTS mutable.director_stats;
    DROP TABLE IF EXISTS mutable.genre_stats;
    DROP TABLE IF EXISTS mutable.movie_to_actor_views;
    DROP TABLE IF EXISTS mutable.actor_to_movie_views;
    DROP TABLE IF EXISTS mutable.movie_to_director_views;
    DROP TABLE IF EXISTS mutable.director_to_movie_views;
    DROP TABLE IF EXISTS mutable.movie_to_genre_views;
    DROP TABLE IF EXISTS mutable.genre_to_movie_views;
    DROP TABLE IF EXISTS mutable.director_to_genre_views;
    DROP TABLE IF EXISTS mutable.genre_to_director_views;
    DROP TABLE IF EXISTS mutable.actor_news;
    DROP TABLE IF EXISTS mutable.director_news;
    DROP TABLE IF EXISTS mutable.integrity_violations;
    DROP TABLE IF EXISTS mutable.constraints;
    DROP TABLE IF EXISTS mutable.performance_stats;
    DROP TABLE IF EXISTS mutable.failed_requests;
    DROP TABLE IF EXISTS mutable.reviews;
    DROP TABLE IF EXISTS mutable.genres;
    DROP TABLE IF EXISTS mutable.surveys;
    DROP TABLE IF EXISTS mutable.users;
    DROP TABLE IF EXISTS imdb.directors_genres;
    DROP TABLE IF EXISTS imdb.movies_directors;
    DROP TABLE IF EXISTS imdb.movies_genres;
    DROP TABLE IF EXISTS imdb.roles;
    DROP TABLE IF EXISTS imdb.actors;
    DROP TABLE IF EXISTS imdb.directors;
    DROP TABLE IF EXISTS imdb.movies;
    """)

    conn.commit()
