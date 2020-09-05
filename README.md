<b>PROBLEM DESCRIPTION</b>:

The JSON data set represents the email activity of customers during a campaign.
PS: Please make necessary assumptions where necessary 

<b>DELIVERABLES</b>:
1) Script to load the data
2) Table(s) design 
3) Assumptions
4) Write SQL to answer the following questions (Use the tables designed above) 
   - Get emails of users who opened email
   - Number of users who opened emails between 1-2 days, 2-5 days and > 5 days after email is sent. Example: If the email is sent 21st, # of users who opened email between 23rd and 26th including both 23rd and 26th
   - Identify the campaign which is more successful? (Define what you think success means and write SQL) 
5) Dockerize the solution
6) Any test cases you can think of?

<b>RESPONSE: The following parameters can be subject to A/B testing:</b>

-	Subject line (Length, Topic, Personalization)
-	Pre-header (Inclusion, Content)
-	Day or time (Day of week, time)
-	Call to action (Copy, color)
-	Content (positive, specific or generic)


7) How would you design it if it was streaming data?
8) Any other insights you can derive from the data 

<b>RESPONSE: The following metrics can be captured to measure email campaign funnel</b>
- #1: Number of emails delivered
- #2: Number of emails opened
- #3: Click-through rate
- #4: Click-to-open rate
- #5: Unsubscribe rate
- #6: Bounce rate
- #7: Spam complaints 


<b>ASSUMPTIONS</b>:

For the purpose of this exercise, SQLiteDB will be used as a backend

<b>DIRECTORY STRUCTURE</b>:

- config
- sql
- unittests


