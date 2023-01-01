from datetime import datetime


def insert_performance_stats(conn):
    read_stats = (False, *calculate_performance_stats(conn, conn.read_times()))
    write_stats = (True, *calculate_performance_stats(conn, conn.write_times()))
    conn.reset_recording_time()

    conn.conn.execute("""
    INSERT INTO mutable.performance_stats (is_write, min_time, avg_time, max_time, start_time, end_time, num_requests)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, read_stats)
    conn.conn.execute("""
    INSERT INTO mutable.performance_stats (is_write, min_time, avg_time, max_time, start_time, end_time, num_requests)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, write_stats)

    conn.conn.commit()


def get_performance_stats(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT is_write, min_time, avg_time, max_time, start_time, end_time, num_requests FROM mutable.performance_stats
    ORDER BY start_time, end_time;
    """)

    stats = []

    for (is_write, min_time, avg_time, max_time, start_time, end_time, num_requests) in cursor.fetchall():
        stats.append({
            "type": "W" if is_write else "R",
            "min": min_time,
            "avg": avg_time,
            "max": max_time,
            "start_time": start_time,
            "end_time": end_time,
            "num_req": num_requests
        })

    return stats


def calculate_performance_stats(conn, stats):
    min_time = 0
    avg_time = 0
    max_time = 0
    start_time = conn.recording_start_time()
    end_time = datetime.now()

    num_requests = len(stats)
    for _ in range(0, num_requests):
        stat = stats.pop()
        min_time = min(stat, min_time)
        avg_time += stat
        max_time = max(stat, max_time)

    if num_requests > 0:
        avg_time /= num_requests

    return min_time, avg_time, max_time, start_time, end_time, num_requests
