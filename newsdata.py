#! /usr/bin/python3

"""Newsdata module -Log Analysis with PostgreSQL.

The query's are listed in the form of Query1, Query2, Query3 for
Question1, Question2, Question3 respectively & executed.
"""

import psycopg2  # import for postgresql
# Name of the DB to connect to is news. Followed by Querys executed on the DB.
DBNAME = "news"

Question1 = "\n1. What are the most popular three articles of all time?\n"
Question2 = "\n2. Who are the most popular article authors of all time?\n"
Question3 = "\n3. On which days did more than 1% of requests lead to errors?\n"

# ArticleLog View creation query
view1 = """CREATE VIEW artice_log_view AS SELECT count(*) AS views, articles.title,
articles.author FROM log,articles WHERE log.path LIKE concat('%',articles.slug)
AND status LIKE '%200%' GROUP BY articles.title, articles.author ORDER BY
views DESC;"""

Query1 = "SELECT title, views FROM artice_log_view LIMIT 3"
Query2 = """SELECT authors.name, SUM(artice_log_view.views) AS popular_author_views
        FROM authors,artice_log_view WHERE authors.id = artice_log_view.author
        GROUP BY authors.name ORDER BY popular_author_views DESC"""

# ErrorPercentage Log view creation query
view2 = """CREATE VIEW ErrorPercentage_log_view AS SELECT date(time) AS day,round
(100.00 * sum(CASE WHEN log.status = '200 OK' THEN 0 ELSE 1 END)/
count(log.status),2) AS Error Percentage FROM log GROUP BY day ORDER BY
ErrorPercentage DESC;"""

Query3 = """SELECT to_char(day, 'DD Mon, YYYY'), errorpercentage FROM
        ErrorPercentage_log_view WHERE errorpercentage > 1"""


def exec_results(query):
    """Connect to the DB, execute the query & return the results.

    Keyword arguement:
    query -> String with PostgreSQL
    returns a list.
    """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result


def display_results_for_views(result):
    """Parse & print the records in the result for Query1 & Query2.

    Keyword arguement:
    result -> Rows of List with nested lists.
    print the desired result
    """
    i = 0
    for r in result:
        print('\t'+str(result[i][0]) + ' ---> '+str(result[i][1])+' views')
        i = i + 1


def display_results_for_errors(result):
    """Parse & print the records in the result for Query3.

    Keyword arguement:
    result -> Rows of List with nested lists.
    print the desired result
    """
    i = 0
    for r in result:
        print('\t'+str(result[i][0])+' ---> '+str(result[i][1])+' %\n')
        i = i + 1


print(Question1)
print("\nView created for Question 1 & 2 is: %s\n" % view1)
result1 = exec_results(Query1)
display_results_for_views(result1)

print(Question2)
result2 = exec_results(Query2)
display_results_for_views(result2)

print(Question3)
print("\nView created for Question 3 is: %s\n" % view2)
result3 = exec_results(Query3)
display_results_for_errors(result3)
