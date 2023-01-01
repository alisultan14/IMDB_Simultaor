from copy import deepcopy

import choose_user
import cleanup
import create_users
import log
import parallel
import setup
from check_integrity import check_violations
from connect import DBConnection
from create_news import insert_news_continuously


def run_test(seconds, num_users, overwrite=False):
    conn = DBConnection()

    # Do cleanup of old data first in case we want to look at it after a test
    cleanup.cleanup(conn)

    create_users.insert_users(conn, num_users)

    actions = [lambda stop_evt: insert_news_continuously(conn, stop_evt)]
    arguments = [()]
    users = choose_user.get_all_users(conn)
    for user in users:
        actions.append(lambda connection, usr, stop_evt: choose_user.pick(connection, usr, stop_evt))
        arguments.append((DBConnection(), deepcopy(user)))

    parallel.run_in_parallel(seconds, actions, arguments)
    check_violations(conn)

    log.generate_report(conn, "report.txt", overwrite)

    conn.close()


def create_tables():
    setup.global_setup()


run_test(30, 50, overwrite=True)

