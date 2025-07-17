import os
from urllib.request import Request, urlopen
import json
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt

mapper = [
    {"topic": "/devices/weather",
     "meta": {"driver": "yandex-weather", "title": {"en": "Yandex Weather"}}
     },
    {"topic": "/devices/weather/meta/driver",
     "value": "yandex-weather"
     },
    {"topic": "/devices/weather/meta/name",
     "value": "Yandex Weather"
     },
    {"path": ["fact", "icon"],
     "topic": "/devices/weather/controls/fact_icon",
     "meta": {"order": 1, "readonly": True, "type": "text"}
     },
    {"path": ["fact", "condition"],
     "topic": "/devices/weather/controls/fact_condition",
     "meta": {"order": 2, "readonly": True, "type": "text"}
     },
    {"path": ["fact", "cloudness"],
     "topic": "/devices/weather/controls/fact_cloudness",
     "meta": {"order": 3, "readonly": True, "type": "value"}
     },
    {"path": ["fact", "temp"],
     "topic": "/devices/weather/controls/fact_temperature",
     "meta": {"order": 4, "readonly": True, "type": "value"}
     },
    {"path": ["fact", "humidity"],
     "topic": "/devices/weather/controls/fact_humidity",
     "meta": {"order": 5, "readonly": True, "type": "value"}
     },
    {"path": ["forecasts", 0, "parts", "day", "icon"],
     "topic": "/devices/weather/controls/forecast_today_day_icon",
     "meta": {"order": 6, "readonly": True, "type": "text"}
     },
    {"path": ["forecasts", 0, "parts", "day", "condition"],
     "topic": "/devices/weather/controls/forecast_today_day_condition",
     "meta": {"order": 7, "readonly": True, "type": "text"}
     },
    {"path": ["forecasts", 0, "parts", "day", "cloudness"],
     "topic": "/devices/weather/controls/forecast_today_day_cloudness",
     "meta": {"order": 8, "readonly": True, "type": "value"}
     },
    {"path": ["forecasts", 0, "parts", "day", "temp_avg"],
     "topic": "/devices/weather/controls/forecast_today_day_temperature",
     "meta": {"order": 9, "readonly": True, "type": "value"}
     },
    {"path": ["forecasts", 0, "parts", "day", "humidity"],
     "topic": "/devices/weather/controls/forecast_today_day_humidity",
     "meta": {"order": 10, "readonly": True, "type": "value"}
     },

    {"path": ["forecasts", 0, "parts", "night", "icon"],
     "topic": "/devices/weather/controls/forecast_today_night_icon",
     "meta": {"order": 11, "readonly": True, "type": "text"}
     },
    {"path": ["forecasts", 0, "parts", "night", "condition"],
     "topic": "/devices/weather/controls/forecast_today_night_condition",
     "meta": {"order": 12, "readonly": True, "type": "text"}
     },
    {"path": ["forecasts", 0, "parts", "night", "cloudness"],
     "topic": "/devices/weather/controls/forecast_today_night_cloudness",
     "meta": {"order": 13, "readonly": True, "type": "value"}
     },
    {"path": ["forecasts", 0, "parts", "night", "temp_avg"],
     "topic": "/devices/weather/controls/forecast_today_night_temperature",
     "meta": {"order": 14, "readonly": True, "type": "value"}
     },
    {"path": ["forecasts", 0, "parts", "night", "humidity"],
     "topic": "/devices/weather/controls/forecast_today_night_humidity",
     "meta": {"order": 15, "readonly": True, "type": "value"}
     },
    {"path": ["forecasts", 1, "parts", "day", "icon"],
     "topic": "/devices/weather/controls/forecast_tomorrow_day_icon",
     "meta": {"order": 16, "readonly": True, "type": "text"}
     },
    {"path": ["forecasts", 1, "parts", "day", "condition"],
     "topic": "/devices/weather/controls/forecast_tomorrow_day_condition",
     "meta": {"order": 17, "readonly": True, "type": "text"}
     },
    {"path": ["forecasts", 1, "parts", "day", "cloudness"],
     "topic": "/devices/weather/controls/forecast_tomorrow_day_cloudness",
     "meta": {"order": 18, "readonly": True, "type": "value"}
     },
    {"path": ["forecasts", 1, "parts", "day", "temp_avg"],
     "topic": "/devices/weather/controls/forecast_tomorrow_day_temperature",
     "meta": {"order": 19, "readonly": True, "type": "value"}
     },
    {"path": ["forecasts", 1, "parts", "day", "humidity"],
     "topic": "/devices/weather/controls/forecast_tomorrow_day_humidity",
     "meta": {"order": 20, "readonly": True, "type": "value"}
     },

    {"path": ["forecasts", 1, "parts", "night", "icon"],
     "topic": "/devices/weather/controls/forecast_tomorrow_night_icon",
     "meta": {"order": 21, "readonly": True, "type": "text"}
     },
    {"path": ["forecasts", 1, "parts", "night", "condition"],
     "topic": "/devices/weather/controls/forecast_tomorrow_night_condition",
     "meta": {"order": 22, "readonly": True, "type": "text"}
     },
    {"path": ["forecasts", 1, "parts", "night", "cloudness"],
     "topic": "/devices/weather/controls/forecast_tomorrow_night_cloudness",
     "meta": {"order": 23, "readonly": True, "type": "value"}
     },
    {"path": ["forecasts", 1, "parts", "night", "temp_avg"],
     "topic": "/devices/weather/controls/forecast_tomorrow_night_temperature",
     "meta": {"order": 24, "readonly": True, "type": "value"}
     },
    {"path": ["forecasts", 1, "parts", "night", "humidity"],
     "topic": "/devices/weather/controls/forecast_tomorrow_night_humidity",
     "meta": {"order": 25, "readonly": True, "type": "value"}
     }

]


def read_value(path, data):
    path = path.copy()
    while len(path) > 0:
        data = data[path.pop(0)]
    return data


def load_weather():
    if os.path.isfile("weather.json"):
        with open("weather.json", "r") as f:
            try:
                content = json.load(f)
                if content["ts"] > datetime.now().timestamp():
                    return content["weather"]
            except json.decoder.JSONDecodeError as e:
                print(e)
    req = Request(f"https://api.weather.yandex.ru/v2/forecast?lat={os.environ['YANDEX_WEATHER_LAT']}&lon={os.environ['YANDEX_WEATHER_LON']}&format=json")
    req.add_header('X-Yandex-Weather-Key', os.environ['YANDEX_WEATHER_KEY'])
    try:
        weather = json.loads(urlopen(req).read())
        with open("weather.json", "w") as f:
            json.dump({
                "ts": (datetime.now() + timedelta(hours=1)).timestamp(),
                "weather": weather
            }, f)
        return weather
    except Exception as e:
        print(e)
        return {}


weather = load_weather()

count = 0

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    global count
    for value in mapper:
        if value.get("meta"):
            client.publish(value["topic"] + "/meta", json.dumps(value["meta"]), retain=True)
            count += 1
            for key, data in value["meta"].items():
                client.publish(value["topic"] + "/meta/" + key, str(data), retain=True)
                count += 1
        if value.get("path"):
            client.publish(value["topic"], str(read_value(value["path"], weather)), retain=True)
            count += 1
        if value.get("value"):
            client.publish(value["topic"], str(value["value"]), retain=True)
            count += 1


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed")


def on_publish(client, userdata, mid, reason, properties):
    global count
    count -= 1
    if count == 0:
        client.disconnect()


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_publish = on_publish

mqttc.connect("127.0.0.1", 1883, 60)

mqttc.loop_forever()
