#/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
import argparse
import os
import praw
import re
import sys

nba_players = []
dict = {}
reddit = praw.Reddit('bot1')

def main(argv=sys.argv[1:]):
    
    limit_count = 3
    subreddit_name = "nba_bot_testing"
    print(argv)

    if len(argv) is 1:
        if not isinstance(argv[0],str):
            sys.exit("Given subreddit is not a string")
        else:
            subreddit_name = argv[0]
    elif len(argv) is 2:
        if not isinstance(argv[0],str) or not isinstance(argv[1],str):
            if not isinstance(argv[1],str):
                sys.exit("Given subreddit is not a string")
            else:
                sys.exit("Given limit is not a int")
        else:
            subreddit_name = argv[0]
            limit_count = int(argv[1])
    elif len(argv) >= 3:
        sys.exit("Too many arguments")

    posts_replied_to = repeat_comments()
    load_nba_players()

    title_parse(subreddit_name, limit_count,posts_replied_to)
    text_parse(subreddit_name, limit_count,posts_replied_to)
    post_comments(posts_replied_to)
    write_to_file(posts_replied_to)


def repeat_comments():
    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []
    else:
        # Read the file into a list and remove any empty values
        with open("posts_replied_to.txt", "r") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = list(filter(None, posts_replied_to))
    return posts_replied_to


def load_nba_players():
    f = open("names.txt", "r")
    for x in f:
        name = [y.strip() for y in x.split(',')]
        first_name = name[1].lower()
        last_name = name[0].lower()
        nba_players.append(first_name + " " + last_name)
    f.close()

def title_parse(subreddit_name, limit,posts_replied_to):
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.new(limit=3):
        if submission.id not in posts_replied_to:
            title = submission.title
            data = title.split()

            first = 0
            second = 1
            for temp in data:
                try:
                    first_name = re.sub("[^a-zA-Z]+", "", data[first]).lower()
                    last_name = re.sub("[^a-zA-Z]+", "", data[second]).lower()
                    potential_name = first_name + " " + last_name
                    potential_name = potential_name.lower()
                    print(potential_name)
                    if potential_name in nba_players:
                        potential_name = first_name.capitalize() + " " + last_name.capitalize()
                        comment = "[" + potential_name + "]" + "(" + "https://www.basketball-reference.com/players/" + last_name[:1] + "/" + last_name[:5] + first_name[:2] + "01.html" + ")" + "\n\n" 
                        if (dict.get(submission) is None):
                            dict[submission] = comment
                        else:
                            comment += dict[submission]
                            dict[submission] = comment
                    first += 1
                    second += 1
                except IndexError:
                    pass   
    
def text_parse(subreddit_name,limit_count,posts_replied_to): 
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.new(limit=limit_count):
        if submission.id not in posts_replied_to:
            text = submission.selftext
            data = text.split()

            first = 0
            second = 1
            for temp in data:
                try:
                    first_name = re.sub("[^a-zA-Z]+", "", data[first]).lower()
                    last_name = re.sub("[^a-zA-Z]+", "", data[second]).lower()
                    potential_name = first_name + " " + last_name
                    potential_name = potential_name.lower()
                    print(potential_name)
                    if potential_name in nba_players:
                        potential_name = first_name.capitalize() + " " + last_name.capitalize()
                        comment = "[" + potential_name + "]" + "(" + "https://www.basketball-reference.com/players/" + last_name[:1] + "/" + last_name[:5] + first_name[:2] + "01.html" + ")" + "\n\n" 
                        if (dict.get(submission) is None):
                            dict[submission] = comment
                        else:
                            comment += dict[submission]
                            dict[submission] = comment
                    first += 1
                    second += 1
                except IndexError:
                    pass      

def post_comments(posts_replied_to):
    first = True
    for submission in dict:
        if first:
            submission.reply("Players mentioned in this thread: \n\n" + dict[submission])
            first = False
        else:
            submission.reply(dict[submission])
        posts_replied_to.append(submission.id)

def write_to_file(posts_replied_to):
    with open("posts_replied_to.txt", "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")
