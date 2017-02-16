#!/usr/bin/env python
###############################################################################
# packt-twitter.py
# Creates a Tweet for the Packt Daily Free Technical eBook.
# Uses the lxml library to scrape the Packt Daily Free Technical eBook page, 
# then uses the twitter library to post a tweet with the link and title to the 
# book. Sends an email via the smtplib library to confirm success.
#
# Designed to be scheduled/run daily via crontab.
###############################################################################
# Created: 2017.02.07 by David M. Jones
# Updated: 2017.02.08 by David M. Jones
#          Added script header comments and comments throughout the code.
#
###############################################################################
# To Do List:
# 1. Add option to include image of book cover?
# 2. Improve error handling.
# 3. Improve SMTP security.
# 4. Improve Twitter OAUTH security.
###############################################################################

# Import HTML-related libraries
from lxml import html
import requests

# Import Email-related libraries
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# Import Twitter-realted libraries
import twitter
###############################################################################
# Configuration Variables
###############################################################################
# HTML-related Variables
# The URL to the Packt Free Daily eBook page.
weburl = 'https://www.packtpub.com/packt/offers/free-learning'
# The HTML XPath to the eBook Title.
titleXPath = '//*[@id="deal-of-the-day"]/div/div/div[2]/div[2]/h2/text()'
# The HTML XPath to the Book Cover IMG tag, src attribute.
imgXPath = '//*[@id="deal-of-the-day"]/div/div/div[1]/a/img/@src'
# User-Agent is required, otherwise the Packt website returns HTTP 403.
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

###############################################################################
# Email-related Variables
EMAIL_TO = '[EMAIL_TO]'
EMAIL_FROM = '[EMAIL_FROM]'

###############################################################################
# Twitter-related variables
# https://dev.twitter.com/oauth/overview/application-owner-access-tokens to get these values.
TWITTER_CONSUMER_KEY = '[TWITTER_CONSUMER_KEY]'
TWITTER_CONSUMER_SECRET = '[TWITTER_CONSUMER_SECRET]'
TWITTER_ACCESS_TOKEN_KEY = '[TWITTER_ACCESS_TOKEN_KEY]'
TWITTER_ACCESS_TOKEN_SECRET = '[TWITTER_ACCESS_TOKEN_SECRET]'

###############################################################################
# Function Definitions
###############################################################################
# Define the Function to send an email.
def send_email(fromAddress, toAddress, subject, message):
    # Create the email message object.
    msg = MIMEMultipart()
    # Configure the message with basic from, to, subject, and body type.
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server via TLS.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # Login to the SMTP server.
    server.login(fromAddress, "[PASSWORD]")
    # Create the email message on the SMTP server.
    text = msg.as_string()
    # Send the email message via the SMTP server.
    server.sendmail(fromAddress, toAddress, text)
    # End the login session with the SMTP server.
    server.quit()

###############################################################################
# Define the Function to send a Tweet.
def send_tweet(tweet):
        # Connect to the Twitter API with the OAUTH credentials.
        api = twitter.Api(
                consumer_key = TWITTER_CONSUMER_KEY,
                consumer_secret = TWITTER_CONSUMER_SECRET,
                access_token_key = TWITTER_ACCESS_TOKEN_KEY,
                access_token_secret = TWITTER_ACCESS_TOKEN_SECRET)
        # Post the tweet.
        status = api.PostUpdate(tweet)

###############################################################################
# Define the main function for the script
def main():
        # Request the page.
        page = requests.get(weburl, headers=headers)
        # Parse the HTML.
        tree = html.fromstring(page.content)
        # Grab the Title of the eBook fromthe HTML.
        ebook_title = tree.xpath(titleXPath)[0].strip()
        # Grab the eBook Cover image source attribute.
		# DOES NOT CURRENTLY WORK!
#       imgurl = tree.xpath(imgXPath)
#       print imgurl

        # Compose the tweet.
        tweet = "Today's Packt Free eBook: %s. %s" % (ebook_title, weburl)
        # Get the length of the proposed tweet.
        tweetLength = len (tweet)
#       print tweetLength
        # Check that the tweet is less than 140 characters.
        if tweetLength < 140:
                # The tweet is less than 140 characters, so send it.
#               print tweet
                # Set the email subject and body.
                email_subject = "Daily Tweet Successful!"
                email_body = "The daily tweet was sent successfully!\n\n%s" % tweet
                # Send the tweet.
                send_tweet(tweet)
        else:
                # The tweet was longer than 140 characters, so it's not going to work.
                # Set the email subject and body.
                email_subject = "Daily Tweet Failed"
                email_body = "The daily tweet was too long today!"
                # DON'T send the tweet.

        # Send the status email.
        send_email(EMAIL_FROM, EMAIL_TO, email_subject, email_body)

###############################################################################
# Run the main function for the script
###############################################################################
if __name__ == '__main__':
    main()
