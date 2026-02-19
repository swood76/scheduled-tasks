import smtplib
import datetime as dt
import os
quote_list = []
#open quote.txt file as quotefile
with open("quotes.txt", "r", encoding="utf-8") as quotefile:
    #create list of each line of txt file
    quote_list = quotefile.readlines()

#print(quotes_.strip("\n"))
quote_stripped = []

#loop through each quote in quote_list and strip "\n" character
for quotes in quote_list:

    quote_stripped.append(quotes.strip("\n"))
quote_counter = 5
print(quote_stripped)

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
    if day == 3:
        connection.sendmail(
            from_addr=my_email,
            to_addrs=recipients,
            msg=f"Subject: Thursday Motivational Quote\n\n {quote_list[quote_counter]}".encode("utf-8")
            )
        quote_counter += 1




