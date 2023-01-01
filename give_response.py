import random

GetQuestions = """
                SELECT *
                FROM mutable.survey_questions
                WHERE survey_id = %s;
                """

GetSurveyId = """
                SELECT survey_id 
                FROM mutable.survey_invites
                WHERE invitee_id  = %s;
                """
GiveAnswer = """
                INSERT INTO mutable.survey_responses(question_id, respondent_id, value) 
                VALUES (%s, %s, %s);
             """

UpdateInvite = """
                UPDATE mutable.survey_invites
                SET dismissed = TRUE
                WHERE survey_id = %s AND invitee_id = %s;
                """


def respond(conn, user_id, survey_id):
    cursor = conn.cursor()
    cursor.execute(GetQuestions, [survey_id])
    questions = cursor.fetchall()

    for question in questions:
        question_id = question[0]
        answer = random.randint(1, 5)
        cursor.execute(GiveAnswer, [question_id, user_id, answer])

    dismiss_survey_invite(conn, survey_id, user_id)
    conn.commit()
    cursor.close()


def dismiss_survey_invite(conn, survey_id, user_id):
    if survey_id is None:
        return

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE mutable.survey_invites
    SET dismissed = TRUE
    WHERE survey_id = %s AND invitee_id = %s;
    """, (survey_id, user_id))

    cursor.close()


def getSurveyID(conn, user_id):
    cursor = conn.cursor()
    cursor.execute(GetSurveyId, [user_id])
    survey_id = cursor.fetchone()
    conn.commit()
    cursor.close()
    return survey_id
