def cleanup(conn):
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM mutable.comments;
    DELETE FROM mutable.review_invites;
    DELETE FROM mutable.want_to_see;
    DELETE FROM mutable.survey_invites;
    DELETE FROM mutable.survey_responses;
    DELETE FROM mutable.survey_questions;
    DELETE FROM mutable.movie_stats;
    DELETE FROM mutable.actor_stats;
    DELETE FROM mutable.director_stats;
    DELETE FROM mutable.genre_stats;
    DELETE FROM mutable.movie_to_actor_views;
    DELETE FROM mutable.actor_to_movie_views;
    DELETE FROM mutable.movie_to_director_views;
    DELETE FROM mutable.director_to_movie_views;
    DELETE FROM mutable.movie_to_genre_views;
    DELETE FROM mutable.genre_to_movie_views;
    DELETE FROM mutable.director_to_genre_views;
    DELETE FROM mutable.genre_to_director_views;
    DELETE FROM mutable.actor_news;
    DELETE FROM mutable.director_news;
    DELETE FROM mutable.integrity_violations;
    DELETE FROM mutable.constraints;
    DELETE FROM mutable.performance_stats;
    DELETE FROM mutable.failed_requests;
    DELETE FROM mutable.reviews;
    DELETE FROM mutable.surveys;
    DELETE FROM mutable.users;
    """)

    conn.commit()
