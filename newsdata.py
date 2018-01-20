#! /usr/bin/python3

import psycopg2
# Name of the DB to connect to is news. Followed by Querys executed on the DB.
DBNAME = "news"

Question1 = "\n1. What are the most popular three articles of all time?\n"
Question2 = "\n2. Who are the most popular article authors of all time?\n"
Question3 = "\n3. On which days did more than 1% of requests lead to errors?\n"

# ArticleLog View creation query
''' create view artice_log_view as select count(*) as views, articles.title,
articles.author from log,articles where log.path like concat('%',articles.slug)
and status like '%200%' group by articles.title, articles.author order by
views desc;'''

Query1 = "select title, views from artice_log_view limit 3"
Query2 = """select authors.name, sum(artice_log_view.views) as popular_author_views
from authors,artice_log_view where authors.id = artice_log_view.author group by
authors.name order by popular_author_views desc"""

# ErrorPercentage Log view creation query
'''create view ErrorPercentage_log_view as select date(time) as day,round
(100.00 * sum(case when log.status = '200 OK' then 0 else 1 end)/
count(log.status),2) as Error Percentage from log group by day order by
ErrorPercentage desc;'''

Query3 = """select to_char(day, 'DD Mon, YYYY'), errorpercentage from
ErrorPercentage_log_view where errorpercentage > 1"""


def exec_results(query):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result


def display_results_for_views(result):
    i = 0
    for r in result:
        print('\t'+str(result[i][0]) + ' ---> '+str(result[i][1])+' views')
        i = i + 1


def display_results_for_errors(result):
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
