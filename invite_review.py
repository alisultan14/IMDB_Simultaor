Invite = """INSERT INTO mutable.review_invites(movie_id, creator_id, invitee_id, dismissed)
            VALUES(%s, %s, %s, false) ON CONFLICT (movie_id, creator_id, invitee_id) DO NOTHING;"""

SelectAllUsers = """ SELECT user_id
                    FROM mutable.users
                    WHERE is_critic IS TRUE AND is_hired IS FALSE
                    ORDER BY RANDOM() LIMIT 1;
                   """

SelectReview = """ SELECT movie_id
                    FROM mutable.reviews
                    WHERE creator_id = %s;
                   """


def invite_to_review(conn, inviter_id):
    cursor = conn.cursor()

    cursor.execute(SelectReview, (inviter_id,))
    movie_id = cursor.fetchone()
    if movie_id is None:

        # User has not created any reviews
        return

    cursor.execute(SelectAllUsers)

    user = cursor.fetchone()
    if user is None:
        return True
    user_Id = user[0]

    cursor.execute(Invite, [movie_id[0], inviter_id, user_Id])

    conn.commit()
    cursor.close()
    return True
