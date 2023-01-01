def calculate_movie_stats(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT  
        movie_id,
        
        (SELECT name from imdb.movies WHERE movies.id = movie_stats.movie_id) AS title,
        
        (SELECT COUNT(*) 
        FROM mutable.want_to_see 
        WHERE movie_id = movie_stats.movie_id) AS want_to_see,
        
        shares, direct_views,
        
        (SELECT SUM(count) 
        FROM mutable.actor_to_movie_views 
        WHERE movie_id = movie_stats.movie_id) AS actor_views,
        
        (SELECT SUM(count) FROM mutable.genre_to_movie_views WHERE movie_id = movie_stats.movie_id) AS genre_views,
        
        (SELECT SUM(count) FROM mutable.director_to_movie_views WHERE movie_id = movie_stats.movie_id) 
        AS director_views,
        
        (SELECT AVG(engagement) FROM mutable.reviews WHERE movie_id = movie_stats.movie_id) AS engagement,
        
        (SELECT AVG(excitement) FROM mutable.reviews WHERE movie_id = movie_stats.movie_id) AS excitement,
        
        (SELECT AVG(prod_quality) FROM mutable.reviews WHERE movie_id = movie_stats.movie_id) AS prod_quality
    FROM mutable.movie_stats
    ORDER BY shares DESC;
    """)

    stats = []
    result = cursor.fetchall()

    for (movie_id, title, want_to_see, shares, direct_views, actor_views, genre_views, director_views, engagement,
         excitement, prod_quality) in result:
        stats.append({
            "movie_id": movie_id,
            "title": title,
            "want_to_see": want_to_see or 0,
            "shares": shares or 0,
            "direct_views": direct_views or 0,
            "actor_views": actor_views or 0,
            "genre_views": genre_views or 0,
            "director_views": director_views or 0,
            "engagement": engagement,
            "excitement": excitement,
            "prod_quality": prod_quality
        })

    cursor.close()
    return stats


def calculate_actor_stats(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        actor_id, 
        
        (SELECT CONCAT(last_name, ', ', first_name) 
        FROM imdb.actors WHERE actors.id = actor_stats.actor_id) AS name,
        
        shares, direct_views,

        (SELECT SUM(count) 
        FROM mutable.movie_to_actor_views 
        WHERE actor_id = actor_stats.actor_id) AS movie_views
    FROM mutable.actor_stats
    ORDER BY shares DESC;
    """)

    stats = []
    result = cursor.fetchall()

    for (actor_id, name, shares, direct_views, movie_views) in result:
        stats.append({
            "actor_id": actor_id,
            "name": name,
            "shares": shares or 0,
            "direct_views": direct_views or 0,
            "movie_views": movie_views or 0
        })

    cursor.close()
    return stats


def get_popular_actor_articles(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT actor_id, title, clicks
    FROM mutable.actor_news
    ORDER BY clicks DESC
    LIMIT 10;
    """)

    articles = []
    result = cursor.fetchall()

    for (actor_id, title, clicks) in result:
        articles.append({
            "actor_id": actor_id,
            "title": title,
            "clicks": clicks or 0
        })

    return articles


def calculate_genre_stats(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        genre_id, 
        
        (SELECT NAME FROM mutable.genres WHERE genres.genre_id = genre_stats.genre_id) AS name,
        
        shares, direct_views,
        
        (SELECT SUM(count) 
        FROM mutable.movie_to_genre_views 
        WHERE genre_id = genre_stats.genre_id) AS movie_views,
        
        (SELECT SUM(count) 
        FROM mutable.director_to_genre_views 
        WHERE genre_id = genre_stats.genre_id) AS director_views
    FROM mutable.genre_stats
    ORDER BY shares DESC;
    """)

    stats = []
    result = cursor.fetchall()

    for (genre_id, name, shares, direct_views, movie_views, director_views) in result:
        stats.append({
            "genre_id": genre_id,
            "name": name,
            "shares": shares or 0,
            "direct_views": direct_views or 0,
            "movie_views": movie_views or 0,
            "director_views": director_views or 0
        })

    cursor.close()
    return stats


def calculate_director_stats(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        director_id, 
        
        (SELECT CONCAT(last_name, ', ', first_name) 
        FROM imdb.directors WHERE directors.id = director_stats.director_id) AS name,
        
        shares, direct_views,
        
        (SELECT SUM(count) 
        FROM mutable.movie_to_director_views 
        WHERE director_id = director_stats.director_id) AS movie_views,
        
        (SELECT SUM(count) 
        FROM mutable.genre_to_director_views
        WHERE director_id = director_stats.director_id) AS genre_views
    FROM mutable.director_stats
    ORDER BY shares DESC;
    """)

    stats = []
    result = cursor.fetchall()

    for (director_id, name, shares, direct_views, movie_views, genre_views) in result:
        stats.append({
            "director_id": director_id,
            "name": name,
            "shares": shares or 0,
            "direct_views": direct_views or 0,
            "movie_views": movie_views or 0,
            "genre_views": genre_views or 0
        })

    cursor.close()
    return stats


def get_popular_director_articles(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT director_id, title, clicks
    FROM mutable.director_news
    ORDER BY clicks DESC
    LIMIT 10;
    """)

    articles = []
    result = cursor.fetchall()

    for (director_id, title, clicks) in result:
        articles.append({
            "director_id": director_id,
            "title": title,
            "clicks": clicks or 0
        })

    return articles


def get_review_statistics(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        COUNT(DISTINCT (reviews.movie_id, reviews.creator_id)) as num_reviews, 
        
        AVG(engagement), AVG(excitement), AVG(prod_quality),
                
        COUNT(comments.comment_id) / NULLIF(CAST((SELECT COUNT(*) FROM imdb.movies) AS FLOAT), 0) AS avg_comments, 
        
        (SELECT COUNT(*) FROM imdb.movies) - COUNT(DISTINCT reviews.movie_id) as movies_no_reviews
    FROM mutable.reviews
    LEFT JOIN mutable.comments 
    ON reviews.movie_id = comments.movie_id AND reviews.creator_id = comments.review_author_id;
    """)

    (num_reviews, avg_engagement, avg_excitement, avg_prod_quality, avg_comments,
     movies_no_reviews) = cursor.fetchone()

    return [{
        "num_reviews": num_reviews or 0,
        "avg_engagement": avg_engagement,
        "avg_excitement": avg_excitement,
        "avg_prod_quality": avg_prod_quality,
        "avg_comments": avg_comments,
        "movies_no_reviews": movies_no_reviews or 0
    }]


def get_most_active_hired_critics_by_reviews(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        user_id, CONCAT(last_name, ', ', first_name) AS name,
        (SELECT COUNT(*) FROM mutable.reviews WHERE creator_id = users.user_id) AS reviews_written
    FROM mutable.users
    WHERE is_hired IS TRUE
    ORDER BY reviews_written DESC;
    """)

    stats = []
    result = cursor.fetchall()

    for (user_id, name, reviews_written) in result:
        stats.append({
            "user_id": user_id,
            "name": name,
            "reviews_written": reviews_written or 0
        })

    return stats


def get_top_user_critics_by_comments_produced(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT users.user_id, CONCAT(users.last_name, ', ', users.first_name) AS name, 
    COUNT(comments.comment_id) AS replies
    FROM mutable.users
    LEFT JOIN mutable.comments
    ON users.user_id = comments.review_author_id
    WHERE is_critic IS TRUE
    GROUP BY users.user_id
    ORDER BY replies DESC
    LIMIT 10;
    """)

    stats = []
    result = cursor.fetchall()

    for (user_id, name, replies) in result:
        stats.append({
            "user_id": user_id,
            "name": name,
            "replies": replies or 0
        })

    return stats


def get_review_comment_time(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        AVG(comments.creation_TS - reviews.creation_TS) as reply_time
    FROM mutable.reviews 
    JOIN mutable.comments ON reviews.movie_id = comments.movie_id AND reviews.creator_id = comments.review_author_id;
    """)

    ((avg_reply_time), ) = cursor.fetchone()
    return [{"avg_reply_time": avg_reply_time}]


def get_survey_stats(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        COUNT(DISTINCT surveys.survey_id) as num_surveys, 
        
        COUNT(DISTINCT survey_questions.question_id) / NULLIF(CAST(COUNT(DISTINCT surveys.survey_id) AS FLOAT), 0) 
        AS avg_questions, 
        
        AVG(value) 
    FROM mutable.surveys 
    LEFT JOIN mutable.survey_questions ON surveys.survey_id = survey_questions.survey_id 
    LEFT JOIN mutable.survey_responses ON survey_questions.question_id = survey_responses.question_id;
    """)

    (num_surveys, avg_questions, avg_value) = cursor.fetchone()

    return [{
        "num_surveys": num_surveys or 0,
        "avg_questions": avg_questions,
        "avg_value": avg_value
    }]


def get_most_active_hired_critics_by_surveys(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        user_id, CONCAT(last_name, ', ', first_name) AS name,
         
        (SELECT COUNT(*) FROM mutable.surveys WHERE creator_id = users.user_id) AS surveys_written
    FROM mutable.users
    WHERE is_hired IS TRUE
    ORDER BY surveys_written DESC;
    """)

    stats = []
    result = cursor.fetchall()

    for (user_id, name, surveys_written) in result:
        stats.append({
            "user_id": user_id,
            "name": name,
            "surveys_written": surveys_written or 0
        })

    return stats


def get_survey_response_rates(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        survey_id, survey_name, respondents, invites, CAST(respondents AS FLOAT) / NULLIF(invites, 0) AS response_rate 
        FROM (SELECT
            survey_id, survey_name,
        
            (SELECT COUNT(*) FROM mutable.survey_invites WHERE survey_id = surveys.survey_id) AS invites,
            
            (SELECT COUNT(DISTINCT respondent_id) FROM 
            mutable.survey_responses 
            JOIN mutable.survey_questions 
            ON survey_responses.question_id = survey_questions.question_id WHERE survey_id = surveys.survey_id) 
            AS respondents
        FROM mutable.surveys) AS stats
    ORDER BY response_rate DESC;
    """)

    stats = []
    result = cursor.fetchall()

    for (survey_id, survey_name, survey_responses, invites, response_rate) in result:
        stats.append({
            "survey_id": survey_id,
            "survey_name": survey_name,
            "invites": invites or 0,
            "survey_responses": survey_responses or 0,
            "response_rate": response_rate
        })

    return stats


def get_survey_response_time(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
    AVG(survey_responses.creation_TS - survey_invites.creation_TS)
    FROM mutable.survey_invites 
    JOIN mutable.survey_responses 
    ON survey_invites.invitee_id = survey_responses.respondent_id WHERE survey_responses.question_id in 
        (SELECT question_id FROM mutable.survey_questions WHERE survey_id = survey_invites.survey_id);
    """)

    ((avg_reply_time), ) = cursor.fetchone()
    return [{"avg_reply_time": avg_reply_time}]
