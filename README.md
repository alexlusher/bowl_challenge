<b>PROBLEM DESCRIPTION</b>:

The JSON data set represents the email activity of customers during a campaign.
PS: Please make necessary assumptions where necessary 

<b>DELIVERABLES</b>:
<b>TASK 1. Script to load the data</b>
<b>TASK 2. Table(s) design </b>

<b>DIRECTORY STRUCTURE</b>:

- /config - This directory contains project configuration settings and, if needed, connectivity setting to any RDBMS
- /data - This directory contains SQLite DB
- /data - This directory contains log file. In production, timestamp would be added to each log file name.
- /sql - This directory contains all SQL scripts, including DDL and queries to answer Question 4.


<b>TASK 3. Describe assumptions</b>

<b>ASSUMPTIONS MADE</b>:
1) This solution is designed for batch processing of JSON files with email campaign data, and therefore does not use streaming
2) Each JSON file contains responses for a single campaign. In case of additional files with responses for the same campaign, they will be appended into the database
3) This solution uses SQLiteDB for portability purposes. In production, it would be replaced with a full-scale RDBMS.
4) Due to the use of SQLiteDB, each table has only column "updated", vs typically used "created" and "updated" and does not use UPSERT operator that is not available for this version of SQLite 3.6. In production, the code would include both "created" and "updated" and the new records would be upserted to update, for instance, users who decided to get unsibscribed.
5) The DB design contains 3 tables - fact table "campaign_stats" and two dimension tables "users" and "campaigns". The first dimension table is needed to tag users who unsubscribed from receiving future emails and to avoid overcounting. The other dimension table "campaigns" might help to get additional campaign insights. In production, there would be more dimension tables to capture geolocation and time, etc.
6) The used SQL was tailored to be used with SQLiteDB and would look different for production RDBMS. It is also possible to use python library like "SQL Alchemy" to avoid rewriting SQL every time when it is necessary to switch DB.

<b>TASK 4:</b>
Write SQL to answer the following questions (Use the tables designed above) 
   - Get emails of users who opened email
   - Number of users who opened emails between 1-2 days, 2-5 days and > 5 days after email is sent. Example: If the email is sent 21st, # of users who opened email between 23rd and 26th including both 23rd and 26th
   - Identify the campaign which is more successful? (Define what you think success means and write SQL) 


<i><b>NOTE:</b> Used Navicat in order to create and debug the above SQL queries for SQLiteDB</i>
  
  
   <b>RESPONSE:</b>
   Please see queries from the sub-directory /sql
   
<b>TASK 5: Dockerize the solution</b>
<b>TASK 6: Any test cases you can think of?</b>

<b>RESPONSE: The following parameters can be subject to A/B testing:</b>

-	Subject line (Length, Topic, Personalization)
-	Pre-header (Inclusion, Content)
-	Day or time (Day of week, time)
-	Call to action (Copy, color)
-	Content (positive, specific or generic)

<b>TASK 7: How would you design it if it was streaming data?</b>

<b>RESPONSE: If latency is an issue, then Kafka or Spark streaming would more appropriate than sequential Python batch processing of JSON files.</b>

The Spark-based solution for data stream would be a microservice with REST API where JSON data are processed by Spark and the processed data would be stored in datastore.
The Python code would be adapted for PySpark.

<b>TASK 8: Any other insights you can derive from the data? </b>

<b>RESPONSE: The following metrics can be captured to measure email campaign funnel:</b>
- Number of emails delivered
- Number of emails opened
- Click-through rate
- Click-to-open rate
- Unsubscribe rate
- Bounce rate
- Spam complaints 




