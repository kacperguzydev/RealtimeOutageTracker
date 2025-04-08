import praw
from datetime import datetime, timedelta

class RedditMonitor:
    def __init__(self, client_id, client_secret, user_agent):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    def search_outage_mentions(self, keyword, time_window_minutes=60):
        """Searches Reddit for posts mentioning outages within the specified time window."""
        subreddit = self.reddit.subreddit('all')
        time_threshold = datetime.utcnow() - timedelta(minutes=time_window_minutes)
        matches = []
        for submission in subreddit.search(keyword, sort='new', time_filter='hour'):
            created = datetime.utcfromtimestamp(submission.created_utc)
            if created >= time_threshold:
                matches.append({
                    'title': submission.title,
                    'created_utc': submission.created_utc,
                    'url': submission.url
                })
        return matches
