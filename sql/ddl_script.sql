# This table contains all users

CREATE TABLE users (
user_id TEXT NOT NULL,
email_address TEXT NOT NULL,
email_unsubscribed INTEGER NULL);


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
browser TEXT NULL,
email_sent DATE NULL,
email_delivered DATE NULL,
email_bounced INTEGER NULL,
email_unsubscribed INTEGER NULL,
email_opened DATE NULL,
email_url_clicked DATE NULL,
user_subscribed DATE NULL);