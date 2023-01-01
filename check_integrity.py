# List integrity constraints.
GetConstraintsQ = """SELECT constraint_id, description FROM mutable.constraints;"""
# List frequencies of integrity violations grouped by the constraint.
GetFrequencyofIntegrityViolationsQ = """SELECT COUNT(*)
                                        FROM mutable.integrity_violations
                                        GROUP BY constraint_id;
                                        """
# Retrieve system performance statistics.
GetPerformanceStatsQ = """SELECT * 
                         FROM mutable.performance_stats; """

# List failed requests and their frequently grouped by the failure reason.
CountFailedRequestsQ = """SELECT COUNT(*)
                        FROM mutable.failed_requests
                        GROUP BY reason;
                     """
# Check if there are any users who are hired but not critics.
GetHiredUsersQ = """SELECT user_id 
                FROM mutable.users 
                WHERE is_hired IS TRUE 
                AND is_critic IS FALSE;"""

# Check if any general users wrote a review.
CheckforReviewsQ = """SELECT creator_id 
                    FROM mutable.reviews 
                    WHERE creator_id IN (
                        SELECT user_id FROM mutable.users 
                        WHERE is_hired IS FALSE 
                        AND is_critic IS FALSE);"""

# Check if any hired critics or general users were invited to comment on a review.
CheckReviewInviteQ = """SELECT invitee_id FROM mutable.review_invites WHERE invitee_id IN (SELECT user_id FROM 
mutable.users WHERE is_hired IS TRUE OR is_critic IS FALSE); """

# Check if any user commented on a review, but their invitation was not dismissed.
CheckInviteDismssedQ = """SELECT movie_id, review_author_id, user_id FROM mutable.comments WHERE user_id IN (SELECT 
invitee_id FROM mutable.review_invites WHERE movie_id = comments.movie_id AND review_author_id = 
comments.review_author_id AND dismissed IS FALSE); """

# Check if any general users created a survey.
CheckSurveyUserQ = """SELECT creator_id FROM mutable.surveys WHERE creator_id IN (SELECT user_id FROM mutable.users 
WHERE is_hired IS FALSE AND is_critic IS FALSE); """

# Check if any surveys have no questions.
CheckNoQuestionQ = """SELECT survey_id FROM mutable.surveys WHERE NOT EXISTS (SELECT question_id FROM 
mutable.survey_questions WHERE survey_id = surveys.survey_id); """

# Check if any critics were invited to respond to a survey.
CheckCriticSurveyQ = """SELECT invitee_id FROM mutable.survey_invites WHERE invitee_id IN (SELECT user_id FROM 
mutable.users WHERE is_critic IS TRUE); """

# Check whether users who were not invited responded to a survey.
CheckRespondnotInvitedQ = """SELECT DISTINCT survey_id, respondent_id FROM mutable.survey_responses JOIN 
mutable.survey_questions ON survey_responses.question_id = survey_questions.question_id WHERE respondent_id NOT IN (
SELECT invitee_id FROM mutable.survey_invites WHERE survey_id = survey_invites.survey_id); """

# Check if any user responded to a survey, but their invitation was not dismissed.
CheckSurveyInvitenotDismissedQ = """SELECT DISTINCT survey_id, respondent_id FROM mutable.survey_responses JOIN 
mutable.survey_questions ON survey_responses.question_id = survey_questions.question_id WHERE respondent_id IN (SELECT 
invitee_id FROM mutable.survey_invites WHERE survey_id = survey_questions.survey_id AND dismissed IS FALSE); """

# Check if any movie's views came from an actor that was not in the movie.
CheckMovieActorQ = """SELECT * FROM mutable.actor_to_movie_views WHERE NOT EXISTS (SELECT * FROM imdb.roles WHERE 
actor_id = actor_to_movie_views.actor_id AND movie_id = actor_to_movie_views.movie_id); """

# Check if any movie's views came from a director who did not direct the movie.
CheckMovieDirectorQ = """SELECT * FROM mutable.director_to_movie_views WHERE NOT EXISTS (SELECT * FROM 
imdb.movies_directors WHERE director_id = director_to_movie_views.director_id AND movie_id = 
director_to_movie_views.movie_id); """

# Check if any movie's views came from a genre that the movie is not part of.
CheckMovieGenreQ = """SELECT * FROM mutable.genre_to_movie_views JOIN mutable.genres ON genre_to_movie_views.genre_id = 
genres.genre_id WHERE NOT EXISTS (SELECT * FROM imdb.movies_genres WHERE genre = genres.name AND movie_id = 
genre_to_movie_views.movie_id); """

# Check if any actor's views came from a movie they were not in.
CheckActorMovieQ = """SELECT * FROM mutable.movie_to_actor_views WHERE NOT EXISTS (SELECT * FROM imdb.roles WHERE 
actor_id = movie_to_actor_views.actor_id AND movie_id = movie_to_actor_views.movie_id); """

# Check if any director's views came from a movie they did not direct.
CheckDirectorMovieQ = """SELECT * FROM mutable.movie_to_director_views WHERE NOT EXISTS (SELECT * FROM 
imdb.movies_directors WHERE director_id = movie_to_director_views.director_id AND movie_id = 
movie_to_director_views.movie_id); """

# Check if any director's views came from a genre they are not associated with.
CheckDirectorGenreQ = """SELECT * FROM mutable.genre_to_director_views JOIN mutable.genres ON genre_to_director_views.genre_id = 
genres.genre_id WHERE NOT EXISTS (SELECT * FROM imdb.directors_genres WHERE genre = genres.name AND director_id = 
genre_to_director_views.director_id); """

# Check if any genre's views came from a movie it is not associated with.
CheckGenreMovieQ = """SELECT * FROM mutable.movie_to_genre_views JOIN mutable.genres ON movie_to_genre_views.genre_id = 
genres.genre_id WHERE NOT EXISTS (SELECT * FROM imdb.movies_genres WHERE genre = genres.name AND movie_id = 
movie_to_genre_views.movie_id); """

# Check if any genre's views came from a director it is not associated with.
CheckGenreDirectorQ = """SELECT * FROM mutable.director_to_genre_views JOIN mutable.genres ON director_to_genre_views.genre_id = 
genres.genre_id WHERE NOT EXISTS (SELECT * FROM imdb.directors_genres WHERE genre = genres.name AND director_id = 
director_to_genre_views.director_id); """


# functions to check for the invdividual integrity violations

# Returns the constraints
# in the constraints table
def GetConstraints(conn):
    cursor = conn.cursor()
    cursor.execute(GetConstraintsQ)
    result = cursor.fetchall()
    cursor.close()

    db_constraints = []
    for (constraint_id, description) in result:
        db_constraints.append({
            "constraint_id": constraint_id,
            "description": description
        })
    return db_constraints


def GetIntegrityViolations(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT constraint_id, reason, creation_TS FROM mutable.integrity_violations;""")
    result = cursor.fetchall()
    cursor.close()

    violations = []
    for (constraint_id, reason, timestamp) in result:
        violations.append({
            "constraint_id": constraint_id,
            "reason": reason,
            "time": timestamp
        })
    return violations


# function to count the frequencies of integrity violation grouped by constrain
# returns the result as a frequency of integrity violation
def GetFrequencyofIntegrityViolations(conn):
    cursor = conn.cursor()
    cursor.execute(GetFrequencyofIntegrityViolationsQ)
    return cursor.fetchall()


# function to execute and return the performance stats
def GetPerformanceStats(conn):
    cursor = conn.cursor()
    cursor.execute(GetPerformanceStatsQ)
    return cursor.fetchall()


# function to count the failed requests 
def CountFailedRequests(conn):
    cursor = conn.cursor()
    cursor.execute(CountFailedRequestsQ)
    return cursor.fetchall()


# check if there was an error related to hired critics
def GetHiredUsers(conn):
    cursor = conn.cursor()
    cursor.execute(GetHiredUsersQ)
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        return True
    return False


# checking test to see whether a general user wrote a review
def CheckforReviews(conn):
    cursor = conn.cursor()
    cursor.execute(CheckforReviewsQ)
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        return True
    return False


# checking test to make sure that no user had an invite which needs to be dismissed
def CheckReviewInvite(conn):
    cursor = conn.cursor()
    cursor.execute(CheckReviewInviteQ)
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        return True
    return False


# checking if the critic has given review but not dismissed their invite
def CheckInviteDismssed(conn):
    cursor = conn.cursor()
    cursor.execute(CheckInviteDismssedQ)
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        return True
    return False


# checking if the survey invitation was not dismissed
def CheckSurveyUser(conn):
    cursor = conn.cursor()
    cursor.execute(CheckSurveyUserQ)
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        return True
    return False


# Check if it is an empty survey or not
def CheckNoQuestion(conn):
    cursor = conn.cursor()
    cursor.execute(CheckNoQuestionQ)
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        return True
    return False


# Check if a critic, instead of a user was invited to do a survey
def CheckCriticSurvey(conn):
    cursor = conn.cursor()
    cursor.execute(CheckCriticSurveyQ)
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        return True
    return False


# Checking test to see if a user was invited to a survey
def CheckRespondnotInvited(conn):
    cursor = conn.cursor()
    cursor.execute(CheckRespondnotInvitedQ)
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        return True
    return False


# Check if a user was invited to the survey but they did not dismiss it
def CheckSurveyInvitenotDismissed(conn):
    cursor = conn.cursor()
    cursor.execute(CheckSurveyInvitenotDismissedQ)
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        return True
    return False


def CheckMovieActor(conn):
    cursor = conn.cursor()
    cursor.execute(CheckMovieActorQ)
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        return True
    return False


##Check if any director's views came from a genre they are not associated with.
def CheckMovieDirector(conn):
    cursor = conn.cursor()
    cursor.execute(CheckMovieDirectorQ)
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        return True
    return False


##Check if any genre's views came from a movie it is not associated with.
def CheckMovieGenre(conn):
    cursor = conn.cursor()
    cursor.execute(CheckMovieGenreQ)
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        return True
    return False


def CheckActorMovie(conn):
    cursor = conn.cursor()
    cursor.execute(CheckActorMovieQ)
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        return True
    return False


def CheckDirectorMovie(conn):
    cursor = conn.cursor()
    cursor.execute(CheckDirectorMovieQ)
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        return True
    return False


def CheckDirectorGenre(conn):
    cursor = conn.cursor()
    cursor.execute(CheckDirectorGenreQ)
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        return True
    return False


# Check if any movies's views came from a genre it is not associated with.
def CheckGenreMovie(conn):
    cursor = conn.cursor()
    cursor.execute(CheckGenreMovieQ)
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        return True
    return False


# Check if any genre's views came from a director it is not associated with.
def CheckGenreDirector(conn):
    cursor = conn.cursor()
    cursor.execute(CheckGenreDirectorQ)
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        return True
    return False


constraints = {
    "hired but not critics": GetHiredUsers,
    "general user wrote review": CheckforReviews,
    "hired critic or general user was invited to comment on review": CheckReviewInvite,
    "review invite were not dismissed after response": CheckInviteDismssed,
    "general user created a survey": CheckSurveyUser,
    "survey created without a question": CheckNoQuestion,
    "critic was invited to respond to survey": CheckCriticSurvey,
    "survey respondent was not invited": CheckRespondnotInvited,
    "survey invite was not dismissed after response": CheckSurveyInvitenotDismissed,
    "movie views came from unrelated actor": CheckMovieActor,
    "movie views came from unrelated director": CheckMovieDirector,
    "movie views came from unrelated genre": CheckMovieGenre,
    "actor views came from unrelated movie": CheckActorMovie,
    "director views came from unrelated movie": CheckDirectorMovie,
    "director views came from unrelated genre": CheckDirectorGenre,
    "genre views came from unrelated movie": CheckGenreMovie,
    "genre views came from unrelated director": CheckGenreDirector
}


def check_violations(conn):
    cursor = conn.cursor()
    for description, fxn in constraints.items():
        cursor.execute(
            """INSERT INTO mutable.constraints (description) VALUES (%s) RETURNING constraint_id;""",
            (description, )
        )

        (constraint_id, ) = cursor.fetchone()
        if not fxn(conn):
            cursor.execute("""INSERT INTO mutable.integrity_violations (constraint_id, reason) VALUES (%s, %s);""",
                           (constraint_id, description))

    conn.commit()
