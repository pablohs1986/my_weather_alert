import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

account_sid = 'AC69a60632b6e657b914a85a34a8c9df34'
api_key = os.environ.get("OWM_API_KEY")
auth_token = os.environ.get("AUTH_TOKEN")
OWM_48h_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
WEATHER_PARAMS = {
    "lat": 42.610990445272456,
    "lon": -5.586699521269457,
    "exclude": "current,minutely,hourly",
    "lang": "es",
    "units": "metric",
    "cnt": 4,
    "appid": api_key
}

response = requests.get(OWM_48h_ENDPOINT, WEATHER_PARAMS)
response.raise_for_status()
weather_data = response.json()


def generate_sms_text():
    today_weather = weather_data["daily"][:2][0]
    tomorrow_weather = weather_data["daily"][:2][1]
    today_description = today_weather["weather"][0]["description"]
    today_temp_max = today_weather["temp"]["max"]
    today_temp_min = today_weather["temp"]["min"]
    tomorrow_description = today_weather["weather"][0]["description"]
    tomorrow_temp_max = tomorrow_weather["temp"]["max"]
    tomorrow_temp_min = tomorrow_weather["temp"]["min"]

    return f'MWA LEÓN: Hoy {today_description}, Max. {today_temp_max}° Min. {today_temp_min}°. ' \
           f'Mañana {tomorrow_description}, Max. {tomorrow_temp_max}° Min. {tomorrow_temp_min}°. '


sms = generate_sms_text()


def send_sms():
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body=sms,
        from_='+18456825239',
        to='+34627107436'
    )
    print(message.status)


send_sms()
