import time
import traceback
from collections import deque
from datetime import datetime

import psycopg as psycopg
from psycopg import OperationalError, IntegrityError, InternalError

from performance_stats import insert_performance_stats


class DBConnection:
    def __init__(self, admin=False):
        user = "grp5admin" if admin else "test_prog"
        self.conn = psycopg.connect("hostaddr=139.147.9.166 port=5432 dbname=imdb_proj2 user={}".format(user))
        self.read_stats = deque()
        self.write_stats = deque()
        self.start_time = datetime.now()
        self.recent_requests = 0

    def read_times(self):
        return self.read_stats

    def write_times(self):
        return self.write_stats

    def recording_start_time(self):
        return self.start_time

    def reset_recording_time(self):
        self.start_time = datetime.now()

    def cursor(self):
        return DBCursor(self, self.conn.cursor(), self.read_stats, self.write_stats)

    def commit(self):
        self.conn.commit()

    def close(self):
        insert_performance_stats(self)
        self.recent_requests = 0
        self.conn.close()


class DBCursor:
    def __init__(self, conn, cursor, read_stats, write_stats):
        self.conn = conn
        self.cursor = cursor
        self.read_stats = read_stats
        self.write_stats = write_stats

    def execute(self, query, variables=None):
        self.__exec_or_log(lambda: self.cursor.execute(query, variables), is_read(query))

    def executemany(self, query, vars_list):
        self.__exec_or_log(lambda: self.cursor.executemany(query, vars_list), is_read(query))

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchmany(self, size=0):
        return self.cursor.fetchmany(size)

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()

    def __exec_or_log(self, action, read):
        self.conn.recent_requests += 1
        try:
            start = time.perf_counter_ns()
            action()
            elapsed = round((time.perf_counter_ns() - start) / 1e6)  # convert to milliseconds
            if read:
                self.read_stats.append(elapsed)
            else:
                self.write_stats.append(elapsed)
        except (OperationalError, IntegrityError, InternalError) as err:
            self.conn.conn.rollback()
            print(traceback.format_exc())

            # Don't use the execute method of this class to avoid an infinite loop
            self.conn.conn.execute("""
            INSERT INTO mutable.failed_requests (reason) VALUES (%s);
            """, (str(err),))

            self.conn.conn.commit()

        if self.conn.recent_requests >= 50:
            insert_performance_stats(self.conn)
            self.conn.recent_requests = 0


def is_read(query):
    read_cmd = "select"
    return str.lstrip(query)[:len(read_cmd)].lower() == read_cmd
