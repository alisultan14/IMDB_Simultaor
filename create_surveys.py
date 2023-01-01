import random

import choose_user
from create_survey_questions import insert_survey_questions
from invite_survey import invite_to_survey
from view_movie import choose_random_movie

# this create a survey title
DESC = ["Top", "Bottom", "Worst", "Best"]
NUMBER = ["30", "10", "20", "50", "100"]
SUBJECT = ["Must Watch", "Favourite Netflix", "Returning Favourite"]
FILM = ["Movie", "Tv Show", "Short Film", "Drama", "Action Movie", "Romance Movie", "K-Drama", "Action Drama",
        "Comedy TV Show", "Drama TV Show", "Fantasy TV Show", "Horror TV Show", "Mystery TV Show", "Romance TV Show",
        "Thriller TV Show",
        "Drama Movie", "Fantasy Movie", "Horror Movie", "Mystery Movie", "Romance Movie", "Thriller Movie"]
TIME = ["of The Year", "of The Month", "of The Decade", "of The Month"]

CreateSurvey = """INSERT INTO mutable.surveys(creator_id, movie_id, survey_name)
VALUES(%s, %s, %s) RETURNING survey_id;"""


# Create a new survey in the database made by a certain user. The survey_id is auto-generated.

def make_survey():
    desc = random.choice(DESC)
    number = random.choice(NUMBER)
    subject = random.choice(SUBJECT)
    film = random.choice(FILM)
    time = random.choice(TIME)
    return number, desc, subject, film, time


def make_surveys(conn, user_id):
    cursor = conn.cursor()

    survey = ' '.join(make_survey())

    movie_id = choose_random_movie(conn)
    cursor.execute(CreateSurvey, [user_id, movie_id, survey])
    ((survey_id), ) = cursor.fetchone()

    insert_survey_questions(cursor, survey_id)

    conn.commit()
    cursor.close()

    users = choose_user.get_all_users(conn)

    for index in range(0, min(5, len(users))):
        invite_to_survey(conn, users[index][0])
    return True
