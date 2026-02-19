import smtplib
import datetime as dt
import os
import random
quote_list = []
#open quote.txt file as quotefile
with open("quotes.txt", "r", encoding="utf-8") as f:
    quotes = [q.strip() for q in f if q.strip()]

today = dt.date.today()
weekday_name = today.strftime("%A")           # e.g. "Thursday"
day_of_year = today.timetuple().tm_yday       # 1..366

# Deterministic "daily" quote (changes every day)
quote = quotes[(day_of_year - 1) % len(quotes)]
#print(quotes_.strip("\n"))
quote_stripped = []



#set up email connection, login, sender, and receipient 
#using smtplib module open server using SMTP as connection object

my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("MY_PASSWORD")

recipients = [e.strip() for e in os.environ["RECEPIENT_EMAIL"].split(",")]


now = dt.datetime.now() #use now method from datatime class/package to get current time, date...
print(f"What are we getting with now {now}")
day = now.weekday() #get weekday
year = now.year
print(f"Day of week {day}")
print(f"Current year {year}")

with smtplib.SMTP("smtp.gmail.com", 587) as connection:

    connection.starttls() #enable transport layer security
    connection.login(user=my_email, password=password)
    #if day == 3:
    connection.sendmail(
        from_addr=my_email,
        to_addrs=recipients,
        msg=f"Subject: {weekday_name} Motivational Quote\n\n {quote}".encode("utf-8")
        )
        




