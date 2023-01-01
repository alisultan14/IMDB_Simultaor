from datetime import datetime

import calculate_statistics
import check_integrity
import failed_requests
import performance_stats


def generate_report(conn, file_name, overwrite=False):
    file = open_file(file_name, overwrite)
    write_report_header(file)

    write_section_name(file, "Page Statistics")
    write_table(file, "Movies", ["movie_id", "title", "want_to_see", "shares", "direct_views", "actor_views",
                                 "genre_views", "director_views", "engagement", "excitement", "prod_quality"],
                calculate_statistics.calculate_movie_stats(conn))
    write_table(file, "Actors", ["actor_id", "name", "shares", "direct_views", "movie_views"],
                calculate_statistics.calculate_actor_stats(conn))
    write_table(file, "Genres", ["genre_id", "name", "shares", "direct_views", "movie_views", "director_views"],
                calculate_statistics.calculate_genre_stats(conn))
    write_table(file, "Directors", ["director_id", "name", "shares", "direct_views", "movie_views", "genre_views"],
                calculate_statistics.calculate_director_stats(conn))

    write_section_name(file, "News Articles")
    write_table(file, "Popular Actor Articles", ["actor_id", "title", "clicks"],
                calculate_statistics.get_popular_actor_articles(conn))
    write_table(file, "Popular Director Articles", ["director_id", "title", "clicks"],
                calculate_statistics.get_popular_director_articles(conn))

    write_section_name(file, "Active Users")
    write_table(file, "Most Active Hired Critics by Reviews", ["user_id", "name", "reviews_written"],
                calculate_statistics.get_most_active_hired_critics_by_reviews(conn))
    write_table(file, "Most Active Hired Critics by Surveys", ["user_id", "name", "surveys_written"],
                calculate_statistics.get_most_active_hired_critics_by_surveys(conn))
    write_table(file, "Top User Critics by Comments Produced", ["user_id", "name", "replies"],
                calculate_statistics.get_top_user_critics_by_comments_produced(conn))

    write_section_name(file, "Reviews and Surveys")
    write_table(file, "Reviews", ["num_reviews", "avg_engagement", "avg_excitement", "avg_prod_quality", "avg_comments",
                                  "movies_no_reviews"],
                calculate_statistics.get_review_statistics(conn))
    write_table(file, "Average Review Reply Time (s)", ["avg_reply_time"],
                calculate_statistics.get_review_comment_time(conn))
    write_table(file, "Surveys", ["num_surveys", "avg_questions", "avg_value"],
                calculate_statistics.get_survey_stats(conn))
    write_table(file, "Survey Response Rates", ["survey_id", "survey_name", "invites", "survey_responses",
                                                "response_rate"],
                calculate_statistics.get_survey_response_rates(conn))
    write_table(file, "Survey Response Time", ["avg_reply_time"],
                calculate_statistics.get_survey_response_time(conn))

    write_section_name(file, "Integrity Violations")
    write_table(file, "Constraints", ["constraint_id", "description"], check_integrity.GetConstraints(conn))
    write_table(file, "Violations", ["constraint_id", "reason", "time"], check_integrity.GetIntegrityViolations(conn))

    write_section_name(file, "System Performance")
    write_table(file, "Read/Write Times (ms)", ["type", "min", "avg", "max", "start_time", "end_time", "num_req"],
                performance_stats.get_performance_stats(conn))

    write_section_name(file, "Failed Requests")
    write_table(file, "Failures", ["time", "reason"], failed_requests.get_failed_requests(conn))

    file.close()


def open_file(file_name, overwrite=False):
    return open(file_name, "w" if overwrite else "a")


def write_report_header(file):
    file.write("""\n+--------------------------------------------------+\
    \n REPORT GENERATED {}\
    \n+--------------------------------------------------+\n""".format(datetime.now()))


def write_section_name(file, section_name):
    separator = "\n" + ("=" * len(section_name))

    file.write(separator + "\n")
    file.write("{}".format(section_name))
    file.write(separator)


def write_table(file, title, headings, entries):
    content = """\n{}\n""".format(title)

    heading_lengths = {}

    for heading in headings:
        heading_lengths[heading] = len(heading)
        for stats in entries:
            value_length = len(str(stats[heading]))
            heading_lengths[heading] = max(value_length, heading_lengths[heading])

        heading_lengths[heading] += 5

        content += ("{{:_<{}}}".format(heading_lengths[heading])).format(heading)

    for stats in entries:
        content += "\n"
        for heading in headings:
            content += ("{{:<{}}}".format(heading_lengths[heading])).format(str(stats[heading]))

    content += "\n"

    file.write(content)
