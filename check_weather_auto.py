import requests
import datetime as dt
import os
from twilio.rest import Client
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")



client = Client(account_sid, auth_token)


time_data = dt.datetime.now()

API_KEY = os.environ.get("OWM_API_KEY")

MY_LAT =  float(os.environ.get("MY_LAT"))
MY_LONG = float(os.environ.get("MY_LONG"))

VIRTUAL_WHATSAPP = os.environ.get("VIRTUAL_WHATSAPP")
MY_PHONE = os.environ.get("MY_PHONE")
weather_parameters = {

    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": API_KEY,
    "cnt": 4,

}
OWE_URL = "https://api.openweathermap.org/data/2.5/forecast"
response = requests.get(url=OWE_URL, params=weather_parameters)
OWE_data = response.json()

from_whats_app = os.environ.get("VIRTUAL_WHATSAPP")
will_it_rain = False
will_it_snow = False
rain_times = []
rain_amounts = []
#4 gives next 12 hours since every 3 hours 
rain_hour_list = []
other_weather_hour_list = []
rain_amounts = []
other_weather_time_counter = 0
rain_time_counter = 0
snow_hour_list =[]
snow_time_counter = 0
#loop through each 3 hour forecast in OWE Response 
for hours in OWE_data["list"]:
    
   #tap into first entry of weather list (list of weather objects), get Rain String Element with main key
    condition = hours["weather"][0]["main"]
    if condition == "Rain": 
        #print("It will rain in the next 12 hours")
        will_it_rain = True
        #print(f"hours {hours["dt_txt"]}")
       
        rain_amounts.append(hours["rain"]["3h"])
        rain_hour_list.append(hours["dt_txt"])
        rain_time_OWE = OWE_data["city"]["timezone"]
        print(f"rain time owe using city and timezone {rain_time_OWE}")
        rain_utc_dt = dt.datetime.strptime(rain_hour_list[rain_time_counter], "%Y-%m-%d %H:%M:%S").replace(tzinfo=dt.timezone.utc)
        OWE_UTC_SECS = OWE_data["city"]["timezone"]
        rain_local_tz = dt.timezone(dt.timedelta(seconds=OWE_UTC_SECS))
        rain_local_dt = rain_utc_dt.astimezone(rain_local_tz)
        print(f"{will_it_rain} it will {hours["weather"][0]["main"]} {hours["rain"]["3h"]}mm at {rain_local_dt.strftime("%Y-%m-%d %I:%M:%S %p")}  ")
        client = Client(account_sid, auth_token)
     


        message = client.messages.create(
        from_=VIRTUAL_WHATSAPP,
        body=f"Bring an ☔️! It will {hours["weather"][0]["main"]} " \
        f"({hours["rain"]["3h"]}mm) at {rain_local_dt.strftime("%Y-%m-%d %I:%M:%S %p")} 🌧️",                                            
                                 
        to=MY_PHONE
        )
        rain_time_counter +=1
       # hour_list.append()
    elif condition == "Snow":
     
        will_it_snow = True
        snow_hour_list.append(hours["dt_txt"])
        utc_dt = dt.datetime.strptime(snow_hour_list[snow_time_counter], "%Y-%m-%d %H:%M:%S").replace(tzinfo=dt.timezone.utc)
        OWE_UTC_SECS = OWE_data["city"]["timezone"]
        local_tz = dt.timezone(dt.timedelta(seconds=OWE_UTC_SECS))
        snow_local_dt = utc_dt.astimezone(local_tz)
     
        message = client.messages.create(
        from_=VIRTUAL_WHATSAPP,
        body=f"❄️ Be careful! It will {hours["weather"][0]["main"]} " \
        f"({hours["snow"]["3h"]}mm) at {snow_local_dt.strftime("%Y-%m-%d %I:%M:%S %p")} ❄️",
        to=MY_PHONE
        )
        
       # print(f" time owe using city and timezone {rain_time_OWE}")
        snow_time_counter+=1
    elif hours["weather"][0]["main"] != "Snow" and hours["weather"][0]["main"] != "Rain":
        
        other_weather_hour_list.append(hours["dt_txt"])
        utc_dt = dt.datetime.strptime(other_weather_hour_list[other_weather_time_counter], "%Y-%m-%d %H:%M:%S").replace(tzinfo=dt.timezone.utc)
        OWE_UTC_SECS = OWE_data["city"]["timezone"]
        local_tz = dt.timezone(dt.timedelta(seconds=OWE_UTC_SECS))
        local_dt = utc_dt.astimezone(local_tz)
       # print("OWE dt_txt (UTC):", utc_dt)
       # print("Local time:", local_dt.strftime("%Y-%m-%d %I:%M:%S"))
        print(f"{will_it_rain} it will {hours["weather"][0]["main"]} at {local_dt.strftime("%Y-%m-%d %I:%M:%S %p")} ")
        
       # print(f" time owe using city and timezone {rain_time_OWE}")
        other_weather_time_counter+=1
       # print("It wont rain in the next 12 hours")
        
print(f"Will it rain in the next 12 hours {will_it_rain}")
#give me the first list entry 

print("\n\r\n\r\n\r")
#print(f"Open Weather Data over Next 24 Hours {OWE_data}")
print(f"List of rain time {rain_hour_list}")
print(f"Rain Amounts {rain_amounts} ")
