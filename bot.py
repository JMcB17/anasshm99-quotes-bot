#!/usr/bin/env python

"""Bot to send a random quote every so often on the latest discussion post for a subreddit.

Files:
    login-details.json -- reddit login details. See login-details.template.json
    quotes.json -- quotes to choose from. See quotes.template.json
"""

import json
import time
import random

import praw


__version__ = '0.1.0'

MIN_INTERVAL_HOURS = 2
MAX_INTERVAL_HOURS = 5
SUBREDDIT = 'CryptoCurrency'


def get_daily_discussion_post(subreddit_instance: praw.models.Subreddit):
    """Try to get the daily discussions post for a subreddit.

    Args:
        subreddit_instance
    Returns:
        The submission object for the discussion post, or None if it couldn't be found.
    Works by searching the stickied posts of the subreddit for a post with 'daily discussion' in the title.
    """
    for sticky_num in range(1, 2):
        discussion_post = subreddit_instance.sticky(number=sticky_num)
        if 'daily discussion' in discussion_post.title.lower():
            print(f'Got daily discussion post, title {discussion_post.title}')
            return discussion_post

    print("Couldn't find daily discussion post!")
    return None


def send_quote(submission: praw.models.Submission, quotes_list: list, last_quote: str = ''):
    """Generate a random quote from a list, and comment it on a post.

    Args:
        submission -- post to comment on
        quotes_list -- list of quotes to pick from
        last_quote -- if you provide this, the function will try not to send the last quote again
    Returns:
        The string quote that was sent.
    """
    # try not to send the same quote twice in a row
    if last_quote and len(quotes_list) > 1:
        try:
            quotes_list.remove(last_quote)
        except ValueError:
            pass

    quote = random.choice(quotes_list)
    print(f'Chose quote {quote}')
    submission.reply(quote)
    print('Sent quote')

    return quote


def main():
    """Run the bot.

    Loads the quote list and login details from the json files.
    Logs into reddit with the login details.
    Loops to send a quote on the latest discussion post, then sleep for a random amount of time within
    the given intervals.
    """
    print('Starting..')
    with open('quotes.json') as quotes_file:
        quotes_list = json.load(quotes_file)
    with open('login-details.json') as login_details_file:
        login_details = json.load(login_details_file)

    reddit = praw.Reddit(
        client_id=login_details['client_id'],
        client_secret=login_details['client_secret'],
        user_agent=login_details['user_agent'].format(version=__version__),
        username=login_details['username'],
        password=login_details['password']
    )
    print('Logged into reddit')
    subreddit_instance = reddit.subreddit(SUBREDDIT)

    last_quote = ''
    keep_running = True
    while keep_running:
        discussion_post = get_daily_discussion_post(subreddit_instance)
        if discussion_post is not None:
            last_quote = send_quote(discussion_post, quotes_list, last_quote)

        sleep_time_hours = random.randint(MIN_INTERVAL_HOURS, MAX_INTERVAL_HOURS)
        sleep_time_seconds = sleep_time_hours * (60**2)
        print(f'Waiting for {sleep_time_hours} hours')
        time.sleep(sleep_time_seconds)


if __name__ == '__main__':
    main()
