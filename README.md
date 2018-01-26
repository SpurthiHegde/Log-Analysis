# Log-Analysis
Log Analysis project with PostgreSQL

****************PreRequisites *************************
1.  Python3
2.  Vagrant
3.  VirtualBox

****************Setup Project:***************************
1. Install Vagrant and VirtualBox
2. Download or Clone fullstack-nanodegree-vm repository.
3. Download the data from <a target="_blank" href="https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip">here</a>
4. Unzip this file after downloading it. The file inside is called newsdata.sql.
5. Copy the newsdata.sql file and content of this current repository, by downloading.

***************Launching the Virtual Machine*************
1. Launch the Vagrant VM inside Vagrant sub-directory in the downloaded fullstack-nanodegree-vm repository using command,
  $ vagrant up
  
2. Then Log into this using command,
  $ vagrant ssh

3. Change directory to /vagrant and run a ls command to view the sub directories.
4. Navigate to the newsdata.sql folder with dc command.

*************Setting up the database and Creating Views*******
1. Load the data in local database using the command,
  psql -d news -f newsdata.sql
2. The database includes three tables,

  * The authors table includes information about the authors of articles.
  * The articles table includes the articles themselves.
  * The log table includes one entry for each time a user has accessed the site.
3. Use psql -d news to connect to database.

***************Views created for running the queries below*********

1. 
CREATE VIEW log_with_slug
AS
SELECT split_part(path, '/',3) AS log_slug, path, id 
FROM log;
    
 2.  
CREATE VIEW log_hits
AS
SELECT count(*) AS hits, date_trunc('day', time) as hits_date
FROM log
GROUP BY date_trunc('day', time);

3.  
CREATE VIEW log_errors
AS
SELECT count(*) AS errors, date_trunc('day', time) as errors_date
FROM log 
WHERE status like '%404%'
GROUP BY date_trunc('day', time);
      
********************To Run the Python program*******************
1. Once the Virtual machine is up, navigate to newsdata directory.
2. Create views mentioned above.
2. Run the newsdata.py folder with the below command,
$ python newsdata.py
