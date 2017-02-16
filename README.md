# PacktDailyBookTweet
Creates a Tweet for the Packt Daily Free Technical eBook.

Uses the lxml library to scrape the Packt Daily Free Technical eBook page, then uses the twitter library to post a tweet with the link and title to the book. Sends an email via the smtplib library to confirm success.

Designed to be scheduled/run daily via crontab.
