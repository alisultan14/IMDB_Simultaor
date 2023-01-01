from activity_list import view_activity_list
from choose import choose_action
from create_reviews import insertReview
from create_surveys import make_surveys
from invite_survey import invite_to_survey
from view_actor import view_actor_directly, choose_random_actor
from view_director import view_director_directly, choose_random_director
from view_genre import view_genre_directly, choose_random_genre
from view_movie import view_movie_directly, choose_random_movie


def user_critic(conn, user_id, stop_evt):
    weights = [1, 1, 1, 1, 2, 2, 2, 2]
    actions = [
        lambda: view_movie_directly(conn, user_id, choose_random_movie(conn)),
        lambda: view_actor_directly(conn, user_id, choose_random_actor(conn)),
        lambda: view_director_directly(conn, user_id, choose_random_director(conn)),
        lambda: view_genre_directly(conn, user_id, choose_random_genre(conn)),
        lambda: make_surveys(conn, user_id),
        lambda: invite_to_survey(conn, user_id),
        lambda: insertReview(conn, user_id),
        lambda: view_activity_list(conn, user_id)
    ]

    while not stop_evt.is_set() and choose_action(weights, actions):
        pass
