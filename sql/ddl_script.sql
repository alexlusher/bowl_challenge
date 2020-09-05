# This table contains all users

CREATE TABLE users (
user_id TEXT NOT NULL,
email_address TEXT NOT NULL,
ip_address TEXT NULL,
browser TEXT NULL,
os TEXT NULL,
country TEXT NULL,
city TEXT NULL,
telecom_vendor TEXT NULL);


# This table contains a list of all campaigns
CREATE TABLE campaigns (
campaign_id TEXT NOT NULL,
campaign_name TEXT NOT NULL,
campaign_start DATE NOT NULL,
campaign_end DATE NULL,
campaign_active INT NULL);

# This table contains all campaign stats
CREATE TABLE campaign_stats (
campaign_id TEXT NOT NULL,
user_id TEXT NOT NULL,
email_sent DATETIME NULL,
email_opened DATETIME NULL,
email_url_clicked DATETIME NULL,
user_subscribed DATETIME NULL);

# This table contains ip ranges to resolve IP address
CREATE TABLE ip_resolution (
ip_range_start TEXT NOT NULL,
ip_range_end TEXT NOT NULL,
city TEXT NOT NULL,
country TEXT NOT NULL,
telecom TEXT NOT NULL);