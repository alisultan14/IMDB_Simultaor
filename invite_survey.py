Invite = """INSERT INTO mutable.survey_invites(survey_id, invitee_id, dismissed)
            VALUES(%s, %s, false) ON CONFLICT (survey_id, invitee_id) DO NOTHING;"""

SelectAllUsers = """ SELECT user_id
                    FROM mutable.users
                    WHERE is_critic IS FALSE
                    ORDER BY RANDOM() LIMIT 1;
                   """

SelectSurvey = """ SELECT survey_id
                    FROM mutable.surveys
                    WHERE creator_id = %s;
                   """


def invite_to_survey(conn, inviter_id):
    cursor = conn.cursor()

    cursor.execute(SelectSurvey, (inviter_id,))
    survey_id = cursor.fetchone()
    if survey_id is None:

        # User has not created any surveys
        return

    cursor.execute(SelectAllUsers)

    user = cursor.fetchone()
    if user is None:
        return True
    user_Id = user[0]

    cursor.execute(Invite, [survey_id[0], user_Id])

    conn.commit()
    cursor.close()
    return True
