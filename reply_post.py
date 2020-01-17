#/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
import praw
import re
import os
import time

#while True:

# Create the Reddit instance
reddit = praw.Reddit('bot1')

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

nba_players = []
dict = {}

f = open("names.txt", "r")
for x in f:
    name = [y.strip() for y in x.split(',')]
    first_name = name[1].lower()
    last_name = name[0].lower()
    nba_players.append(first_name + " " + last_name)
f.close()

#OPTIMIZE
# and then dockerize and create some unit tests

subreddit = reddit.subreddit('nba_bot_testing')
for submission in subreddit.new(limit=3):
    if submission.id not in posts_replied_to:
        title = submission.title
        data = title.split()

        first = 0
        second = 1
        for temp in data:
            try:
                for j in range(len(data[second]) + 1):
                    first_name = re.sub("[^a-zA-Z]+", "", data[first]).lower()
                    last_name = re.sub("[^a-zA-Z]+", "", data[second])[:j].lower()
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
                        break
                first += 1
                second += 1
            except IndexError:
                pass       

for submission in subreddit.new(limit=3):
    if submission.id not in posts_replied_to:
        text = submission.selftext
        data = text.split()

        first = 0
        second = 1
        for temp in data:
            try:
                for j in range(len(data[second]) + 1):
                    first_name = re.sub("[^a-zA-Z]+", "", data[first]).lower()
                    last_name = re.sub("[^a-zA-Z]+", "", data[second])[:j].lower()
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
                        break
                first += 1
                second += 1
            except IndexError:
                pass      

first = True
for submission in dict:
    if first:
        submission.reply("Players mentioned in this thread: \n\n" + dict[submission])
        first = False
    else:
        submission.reply(dict[submission])
    posts_replied_to.append(submission.id)

# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")

#    time.sleep(59)