import give_response
import leave_comment
from choose import choose_action


def view_activity_list(conn, user_id):
    weights = [1, 1, 2, 2]
    actions = [
        lambda: dismiss_review_invite_no_response(conn, *get_random_active_review_invite(conn, user_id), user_id),
        lambda: dismiss_survey_invite_no_response(conn, get_random_active_survey_invite(conn, user_id), user_id),
        lambda: open_review(conn, *get_random_active_review_invite(conn, user_id), user_id),
        lambda: open_survey(conn, get_random_active_survey_invite(conn, user_id), user_id)
    ]

    choose_action(weights, actions)
    return True


def get_random_active_review_invite(conn, user_id):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT movie_id, creator_id, invitee_id, dismissed
    FROM mutable.review_invites
    WHERE invitee_id = %s AND dismissed IS FALSE
    ORDER BY RANDOM()
    LIMIT 1;
    """, (user_id, ))

    result = cursor.fetchone()
    if result is None:
        return None, None

    (movie_id, creator_id, invitee_id, dismissed) = result

    cursor.close()

    return movie_id, creator_id


def get_random_active_survey_invite(conn, user_id):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT survey_id, invitee_id, dismissed
    FROM mutable.survey_invites
    WHERE invitee_id = %s AND dismissed IS FALSE
    ORDER BY RANDOM()
    LIMIT 1;
    """, (user_id,))

    result = cursor.fetchone()
    if result is None:
        return None

    (survey_id, invitee_id, dismissed) = result

    cursor.close()

    return survey_id


def dismiss_review_invite_no_response(conn, movie_id, creator_id, user_id):
    leave_comment.dismiss_review_invite(conn, movie_id, creator_id, user_id)
    conn.commit()


def dismiss_survey_invite_no_response(conn, survey_id, user_id):
    give_response.dismiss_survey_invite(conn, survey_id, user_id)
    conn.commit()


def open_review(conn, movie_id, creator_id, user_id):
    if movie_id is not None and creator_id is not None:
        leave_comment.insert_comment(conn, movie_id, creator_id, user_id)


def open_survey(conn, survey_id, user_id):
    if survey_id is not None:
        give_response.respond(conn, user_id, survey_id)
