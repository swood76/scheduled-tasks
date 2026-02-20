import requests
import datetime as dt
import smtplib
import time
from zoneinfo import ZoneInfo
import os
MY_LAT =  os.environ.get(MY_LAT)
MY_LONG = os.environ.get(MY_LONG)
ET = ZoneInfo("America/New_York")

remaining = 60



#print(f"iss lat {iss_lat}")
#print(f"iss long {iss_long}")
time_date = dt.datetime.now(dt.timezone.utc)
#time_date = dt.datetime.now()
now_utc = dt.datetime.now(ET)
print(f"Time using Time Zone {now_utc}")
parameters = {

    "lat": MY_LAT,
     "lng": MY_LONG,
     "formatted": 0,
     "cnt": 4,

}
sun_response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)

sun_response.raise_for_status()
sun_data = sun_response.json()
#print(data)

sunrise_list = sun_data["results"]["sunrise"].split("T")[1].split(":")[0]
sunset_list = sun_data["results"]["sunset"].split("T")[1].split(":")[0]
sunrise = sunrise_list
sunset = sunset_list
sunrise_str = sun_data["results"]["sunrise"]
sunset_str = sun_data["results"]["sunset"]
sunrise_utc = dt.datetime.fromisoformat(sunrise_str.replace("Z", "+00:00"))
sunset_utc  = dt.datetime.fromisoformat(sunset_str.replace("Z", "+00:00"))

sunrise_et = sunrise_utc.astimezone(ET)
sunset_et  = sunset_utc.astimezone(ET)
print(f"sunrise UTC {sunrise} \n\r sunrise ET {sunrise_et}")
print(f"sunset UTC  {sunset} \n\r sunset ET {sunset_et} ")
#time_date_list = time_date
current_hour = time_date.time().hour
print(f"current hour {current_hour}")
night = False
day = False

def is_night():

    if current_hour > int(sunset) or current_hour < int(sunrise):
        print("It is Nightime")
        return True
    else:
        print("It is Daytime")
        return False
my_email = os.environ.get("MY_EMAIL")
is_night()

recipients = [e.strip() for e in os.environ["RECEPIENT_EMAIL"].split(",")]

password= os.environ.get("MY_PASSWORD")
def is_overhead(my_lat, my_lng, tot_deg):
    
   # return abs(my_lat - iss_lat) <= tot_deg and abs(my_lng - iss_long) <= tot_deg
   #return true if iss_lat and long is +/-5 within my lat and long
    return MY_LAT-tot_deg <= iss_lat <= MY_LAT+tot_deg and MY_LONG-tot_deg <= iss_long <= MY_LONG+tot_deg 
def check_iss():
    #global iss_match
    global iss_lat, iss_long
    try:
        iss_response = requests.get(url="http://api.open-notify.org/iss-now.json", timeout=10)
        iss_response.raise_for_status()
        iss_data = iss_response.json()
        iss_lat = float(iss_data["iss_position"]["latitude"])
        iss_long = float(iss_data["iss_position"]["longitude"])
        print(f"iss pos {iss_lat} {iss_long}")
    except requests.exceptions.ConnectTimeout as error:
        print(f"HTTPConnection Error {error}")
        return
    except requests.exceptions.Timeout:
         print("Timed out...attempting to connect again")
    

   
    if is_overhead(MY_LAT, MY_LONG,2):
        print("Look up!")
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=recipients,
                msg=f"Subject: ISS Alert \n\n Look up the ISS is overhead! \n At {iss_lat} {iss_long} at {time_date.time()}"

                
            ) 
           # iss_match = True
#while True:

def get_iss_data():
    global iss_lat, iss_long
    try:
        iss_response = requests.get(url="http://api.open-notify.org/iss-now.json", timeout=10)
        iss_response.raise_for_status()
        iss_data = iss_response.json()
    except requests.exceptions.ConnectTimeout as error:
        print(f"HTTPConnection Error {error}")
        return
    except requests.exceptions.Timeout:
         print("Timed out...attempting to connect again")
    

    iss_lat = iss_data["iss_position"]["latitude"]
    iss_long = iss_data["iss_position"]["longitude"]
    print(f"iss pos {iss_lat} {iss_long}")

def min_tick():
    global remaining
    global  iss_long
    if remaining > 0:
        remaining-=1
        get_iss_data()
        print(f"remaining {remaining} {iss_lat} {iss_long}")
        time.sleep(1)
    else:
        print(f"remaining {remaining}")
        check_iss()
        remaining = 60
    #min_tick()
    
    #print(f"remaining {remaining}")
while True:
    #min_tick()
    check_iss()
    time.sleep(60)
