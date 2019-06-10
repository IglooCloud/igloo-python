from igloo import Client, User, Thing, FloatValue
import asyncio
from random import randint


def read_temp():
    return randint(5, 25)


def read_humidity():
    return randint(30, 70)


async def monitor_temperature(client):
    temperature = FloatValue(client, "a6ac761c-07c1-4575-8f8b-50b46eea555c")
    temperature.unitOfMeasurement = "°C"
    temperature.precision = 0.1
    while True:
        measured = read_temp()
        print("Temperature now: %d" % measured)
        temperature.value = measured
        client.mutation_root.createFloatSeriesNode(
            "94d4e8fc-ea84-4d82-95d5-24b57781d50e", measured)
        await asyncio.sleep(1)


async def monitor_humidity(client):
    humidity = FloatValue(client, "8cd110ca-d818-41fb-b87b-3ef38020cc7b")
    while True:
        measured = read_humidity()
        print("Humidity now: %d" % measured)
        humidity.value = measured
        await asyncio.sleep(1)


async def main():
    client = Client(token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VySWQiOiJmODFhODQ3Zi1mZDAyLTQzMDgtOWY3Zi02MTNkZjQ2OTUyNzMiLCJ0b2tlbklkIjoiZjdiZDA1NzMtZTYzMC00ZGIxLTllMTItODE2MDA5NTgyODU4IiwiYWNjZXNzTGV2ZWwiOiJERVZJQ0UiLCJ0b2tlblR5cGUiOiJQRVJNQU5FTlQifQ.VuPRvdMayBg7GxixT4QBjXd3jYO_3Q24Fctx508_p5iRxY96zv0z9-UXQsYGJiJjsI3E7ei2gtgEF84gsm8bnA")
    thing = Thing(client, "39fc078e-a94d-4184-8008-3e97750f5e73")
    await asyncio.gather(monitor_humidity(client), monitor_temperature(client), thing.keepOnline())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
