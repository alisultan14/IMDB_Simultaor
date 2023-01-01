import random

from view_movie import choose_random_movie

# SQL Statement for the insertion of the Reviews
InsertReviews = """
INSERT INTO mutable.reviews(movie_id, creator_id, review, engagement, excitement, prod_quality)
VALUES(%s, %s, %s, %s, %s, %s) 
ON CONFLICT (movie_id, creator_id) 
DO UPDATE SET review = EXCLUDED.review, last_updated = CURRENT_TIMESTAMP; """
# names that are used to name an article - 296 in total
Reviews = ["The best movie of the year hands down",
           "Good cinematography but lacks storyline",
           "Overall a disaster",
           "Waste of your money and time",
           "A masterpiece",
           "Should be nominated for the Oscars",
           "This could have been done much better",
           "Good screenplay and plot but lacks big names",
           "Too long to keep someone interester",
           "Could be improved in many areas",
           "Simple movie that delivers at every stage",
           "Good movie overall",
           "Could have been done way better",
           "One of the best movie",
           "Only appeals to certain audiences"]


def insertReview(conn, user_id):
    cursor = conn.cursor()
    engagement = random.randint(1, 5)
    excitement = random.randint(1, 5)
    prod_quality = random.randint(1, 5)
    review = random.choice(Reviews)
    cursor.execute(InsertReviews, [choose_random_movie(conn), user_id, review, engagement, excitement, prod_quality])
    conn.commit()
    cursor.close()
    return True
