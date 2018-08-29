import praw
import urllib.request
import datetime
from twilio.rest import Client
# in order to receive a text message alert every time you get new wallpapers,
# sign up for twillio at www.twilio.com and enter your account id and token id
account = "xxxxxxx"
token = "yyyyyyy"
client = Client(account, token)
# get the current time
now = datetime.datetime.now()
# enter your client id, client secret, reddit user name and reddit password, you don't need to change the user agent
reddit = praw.Reddit(client_id="xxxxxxx", client_secret="xxxxxxY",
                     username="xxxxx", password="xxxx", user_agent="my_reddit_api")
# call the subbreddit that you want to download your images
subreddit = reddit.subreddit("wallpapers")
# set the time filter on the images to download and how many images you want to download
top_wallpapers = subreddit.top(time_filter="week", limit=10)
# set the path that you want the files to download to
file_path = 'C:\\xx\\xx\\xx\\xx'
counter = 1
link_errors = []
# iterate through each post/submission object
for submissions in top_wallpapers:
    # get the URL for each submission
    url = submissions.url
    try:
        # download the image and store it in the desired path
        urllib.request.urlretrieve(
            url, file_path + "\\" + "image" + str(counter) + ".jpg")
        counter += 1
    except Exception as e:
        # sometimes the links don't allow urlib requests, if so, store the failed link
        link_errors.append(url)
# if there were no errors with the links
if link_errors == []:
    # "to" is the number(which must be verified by twilio) that you want to receive the text message on, "from" is your twilio number
    message = client.messages.create(to="xxxyyyzzzz", from_="xxxyyyzzzz",
                                     body="New wallpapers downloaded, time that the wallpapers were downloaded: "+ now.strftime("%Y-%m-%d %H:%M"))
# if there are errors in one or more links
else:
    message = client.messages.create(to="xxxyyyzzzz", from_="xxxyyyzzzz",
                                     body=("New wallpapers downloaded, however there were error with links: " + " ".join([str(link) for link in link_errors]) + ". Time that the wallpapers were downloaded: " + now.strftime("%Y-%m-%d %H:%M")))
