import json
import time
import random

import praw


MIN_INTERVAL_HOURS = 2
MAX_INTERVAL_HOURS = 5
SUBREDDIT = 'CryptoCurrency'


def get_daily_discussion_post(subreddit_instance: praw.models.Subreddit):
    for sticky_num in range(1, 2):
        discussion_post = subreddit_instance.sticky(number=sticky_num)
        if 'daily discussion' in discussion_post.title.lower():
            print(f'Got daily discussion post, title {discussion_post.title}')
            return discussion_post

    print("Couldn't find daily discussion post!")
    return None


def send_quote(submission: praw.models.Submission, quotes_list: list, last_quote: str = ''):
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
    print('Starting..')
    with open('quotes.json') as quotes_file:
        quotes_list = json.load(quotes_file)
    with open('login-details.json') as login_details_file:
        login_details = json.load(login_details_file)

    reddit = praw.Reddit(
        client_id=login_details['client_id'],
        client_secret=login_details['client_secret'],
        user_agent=login_details['user_agent'],
        username=login_details['username'],
        password=login_details['password']
    )
    print('Logged into reddit')
    subreddit_instance = reddit.subreddit(SUBREDDIT)

    last_quote = ''
    keep_running = True
    while keep_running:
        discussion_post = get_daily_discussion_post(subreddit_instance)
        last_quote = send_quote(discussion_post, quotes_list, last_quote)

        sleep_time_hours = random.randint(MIN_INTERVAL_HOURS, MAX_INTERVAL_HOURS)
        sleep_time_seconds = sleep_time_hours * (60**2)
        print(f'Waiting for {sleep_time_hours} hours')
        time.sleep(sleep_time_seconds)


if __name__ == '__main__':
    main()
