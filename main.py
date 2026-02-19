import smtplib
import datetime as dt
import pandas
import os

#datetime
PLACEHOLDER = "[NAME]"
now = dt.datetime.now()
day = now.day
print(f"current data and time {now}")
print(f"What day is it {day}")
# 1. Update the birthdays.csv
#birthday_file = open("")
birthday_csv = pandas.read_csv("birthdays.csv")
birthday_dict = {row["names"]:row["day"] for (index, row) in birthday_csv.iterrows()}
print(f"birthday dict {birthday_dict}")
birthday_list = []
with open("birthdays.csv", "r") as birthday_file:

    birthday_list = birthday_file.readlines()

print(f"birthday list {birthday_list}")
# 2. Check if today matches a birthday in the birthdays.csv
bday_list = []
name_list = []
month_list = []
day_counter = 0
bday_today = False
for names, bday in birthday_dict.items():
    bday_list.append(bday)
    name_list.append(names)
    if bday == day:
        bday_today = True
        print("Happy Birthday!")
    else:
        print("Its not your birthday")

print(f"day {bday_list}")
print(f"name {name_list}")
# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
with open("letter_templates/letter_1.txt") as letterfile:

    letter_content = letterfile.read()

    for name in name_list:

        bday_letter = letter_content.replace(PLACEHOLDER, name)

print(f"content of letter {bday_letter}")
# 4. Send the letter generated in step 3 to that person's email address.


my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("PASSWORD")

recepient_email = os.environ.get("RECEPIENT_EMAIL")

#separate user row by col so email can be index
split_bday_list = birthday_list[1].split(",")
print(birthday_list[1].split(","))
email_bday_from_list = split_bday_list[2]
print(email_bday_from_list)
name_from_list = split_bday_list[1]
if bday_today == True:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=recepient_email,     #email_bday_from_list,
            msg=f"Subject: Happy Birthday! {name_from_list}\n\n {bday_letter}"

        )
