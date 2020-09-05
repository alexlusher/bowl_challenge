# Get emails of users who opened email

SELECT DISTINCT a.email_address
FROM users a
INNER JOIN campaign_stats b
ON b.user_id = a.user_id
WHERE b.email_opened IS NOT NULL
ORDER BY a.email_address;

# No. of users who opened emails between 1-2 days, 
# 2-5 days and > 5 days after email is sent. 
# Ex : If the email is sent 21st, # of users who 
# opened email between 23rd and 26th including both 23rd and 26th

# ASSUMPTION: Same day responses are excluded below since the problem
SELECT
    tm.campaign_id,
    tm.range,
    COUNT(tm.user_id) AS users
FROM 
    (
        SELECT 
            user_id,
            campaign_id,
            CAST(JULIANDAY(email_opened) - JULIANDAY(email_sent) AS integer) AS days_between,
            CASE
                WHEN JULIANDAY(email_opened) - JULIANDAY(email_sent) < 1 THEN 'same day'
                WHEN JULIANDAY(email_opened) - JULIANDAY(email_sent) BETWEEN 1 AND 2 THEN '1-2 days'
                WHEN JULIANDAY(email_opened) - JULIANDAY(email_sent) BETWEEN 2.01 AND 5 THEN '2-5 days'
                WHEN JULIANDAY(email_opened) - JULIANDAY(email_sent) > 5 THEN 'greater than 5 days'
            END AS range
        FROM
            campaign_stats
        WHERE email_opened IS NOT NULL
    ) tm
WHERE tm.range != 'same day'
GROUP BY tm.campaign_id, tm.range
ORDER BY tm.campaign_id, tm.range

# Identify the campaign which is more successful? 
# ( define what you think success means and write SQL)

# DEFINITION: Campaign success will be defined by the highest UCTR - Unique Click-Through Rate that eliminates noise
# which stems from opening the same link on different devices. 

SELECT
    tm.campaign_id,
    COUNT(tm.email_url_clicked) AS email_clicked_cnt,
      COUNT(tm.email_sent) AS email_sent_cnt,
        ROUND(CAST(COUNT(tm.email_url_clicked)*1.0/COUNT(tm.email_sent) AS FLOAT),2) AS uctr    
FROM
    (SELECT 
        user_id,
        browser,
        campaign_id,
        email_url_clicked,
        email_sent
    FROM campaign_stats
    WHERE email_sent IS NOT NULL
    GROUP BY user_id, browser -- to ensure we count the same user once from any platform
    ) tm
GROUP BY tm.campaign_id