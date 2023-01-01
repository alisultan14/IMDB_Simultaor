from hired_critic import *
from general_user import *
from user_critic import *

# This program will retrieve all the users from the database at the start of a test and randomly determine an order
# of all the users. For each user, it will start the associated program for that user's type (hired critic,
# user critic, or general user) to run concurrently for a given amount of time.
SelectAllUsers = """SELECT user_id, is_critic, is_hired
                    FROM mutable.users
                    ORDER BY RANDOM();
                """


def get_all_users(conn):
    cursor = conn.cursor()
    cursor.execute(SelectAllUsers)
    users = cursor.fetchall()
    cursor.close()
    return users


def pick(conn, user, stop_evt):
    user_id = user[0]
    is_critic = user[1]
    is_hired = user[2]

    if is_hired:
        hired_critic(conn, user_id, stop_evt)
    elif is_critic:
        user_critic(conn, user_id, stop_evt)
    else:
        general_user(conn, user_id, stop_evt)

    conn.close()
