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

*************Setting up the database and Creating Views***
1. Load the data in local database using the command,
  psql -d news -f newsdata.sql
2. The database includes three tables,

  * The authors table includes information about the authors of articles.
  * The articles table includes the articles themselves.
  * The log table includes one entry for each time a user has accessed the site.
3. Use psql -d news to connect to database.

***************Views created for running the queries below******
1. create view artice_log_view as 
    select count(*) as views, articles.title, articles.author 
    from log,articles 
    where log.path like concat('%',articles.slug) and status like '%200%' 
    group by articles.title, articles.author order by views desc;
    
 2.  create view ErrorPercentage_log_view as 
      select date(time) as day,round(100.00 * sum(case when log.status = '200 OK' then 0 else 1 end)/count(log.status),2) as Error
      Percentage 
      from log 
      group by day 
      order by ErrorPercentage desc; 
      
********************To Run the Python program*******************
1. Once the Virtual machine is up, navigate to newsdata directory.
2. Place the newsdata.py folder.
3. Run the newsdata.py folder with the below command,
$ python newsdata.py
