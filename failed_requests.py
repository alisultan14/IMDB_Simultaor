def get_failed_requests(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT reason, time FROM mutable.failed_requests;
    """)

    requests = []

    for (reason, time) in cursor.fetchall():
        requests.append({
            "reason": reason,
            "time": time
        })

    return requests
