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

# CREATE VIEW Query- View with slug column derived from path for log table.
logview = """CREATE VIEW log_with_slug
AS
SELECT split_part(path, '/',3) AS log_slug, path, id
FROM log;"""

Query1 = """SELECT articles.title, count(*) AS articleview
FROM articles, log_with_slug
WHERE articles.slug = log_with_slug.log_slug
GROUP BY articles.title
ORDER BY articleview DESC
LIMIT 3;"""

Query2 = """SELECT authors.name , count(*) AS authorsview
FROM authors, log_with_slug, articles
WHERE authors.id = articles.author AND articles.slug = log_with_slug.log_slug
GROUP BY authors.name
ORDER BY authorsview DESC;"""

# CREATE VIEW Query- Total Log successful hits on a day from Log Table.
loghitsview = """CREATE VIEW log_hits
AS
SELECT count(*) AS hits, date_trunc('day', time) as hits_date
FROM log
GROUP BY date_trunc('day', time);"""

# CREATE VIEW Query- Total Log 404 errors on a day from Log Table.
logerrorview = """CREATE VIEW log_errors
AS
SELECT count(*) AS errors, date_trunc('day', time) as errors_date
FROM log
WHERE status like '%404%'
GROUP BY date_trunc('day', time);"""

Query3 = """SELECT to_char(day, 'DD Mon, YYYY') AS Date,
round(error_percent, 2) AS error_percent
FROM (SELECT (cast(log_errors.errors as decimal)/log_hits.hits )*100
AS error_percent, log_errors.errors_date AS day
FROM log_errors, log_hits
WHERE log_errors.errors_date = log_hits.hits_date) AS Temp
WHERE Temp.error_percent > 1;"""


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
result1 = exec_results(Query1)
display_results_for_views(result1)

print(Question2)
result2 = exec_results(Query2)
display_results_for_views(result2)

print(Question3)
result3 = exec_results(Query3)
display_results_for_errors(result3)

print("\nView created for Question 1 & 2 below,")
print("\n%s" % logview)
print("\nViews created for Question 3 below,")
print("\n%s" % loghitsview)
print("\n%s" % logerrorview)
