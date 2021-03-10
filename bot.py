import json
import praw


def main():
    with open('quotes.json') as quotes_file:
        quotes_list = json.load(quotes_file)
    with open('login-details.json') as login_details_file:
        login_details = json.load(login_details_file)


if __name__ == '__main__':
    main()
