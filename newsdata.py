import psycopg2
DBNAME = "news"

Question1 = "\n1. What are the most popular three articles of all time?\n"
Question2 = "\n2. Who are the most popular article authors of all time?\n"
Question3 = "\n3. On which days did more than 1% of requests lead to errors?\n"

Query1 = "select title, views from artice_log_view limit 3"
Query2 = "select authors.name, sum(artice_log_view.views) as popular_author_views from authors,artice_log_view where authors.id = artice_log_view.author group by authors.name order by popular_author_views desc"
Query3 = "select to_char(day, 'DD Mon, YYYY'), errorpercentage from ErrorPercentage_log_view where errorpercentage > 1"

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
		print ('\t' + str(result[i][0]) + ' ---> ' + str(result[i][1]) + ' views')
		i = i + 1

def display_results_for_errors(result):
	i = 0
	for r in result:
		print ('\t' + str(result[i][0]) + ' ---> ' + str(result[i][1]) + ' %\n')
		i = i + 1

print (Question1)
result1 = exec_results(Query1)
display_results_for_views(result1)

print (Question2)
result2 = exec_results(Query2)
display_results_for_views(result2)

print (Question3)
result3 = exec_results(Query3)
display_results_for_errors(result3)
