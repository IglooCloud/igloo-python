from igloo import Client, User, Thing, FloatVariable
import asyncio
from random import randint


def read_temp():
    return randint(5, 25)


async def monitor_temperature(client):
    temperature = FloatVariable(client, "e1b1e97b-1f64-4d92-a563-c2ff60bb3870")
    while True:
        measured = read_temp()
        print("Temperature now: %d" % measured)
        temperature.value = measured
        client.mutation_root.createFloatSeriesNode(
            "b2bfaaab-8803-41dc-be28-c4009dabf1cf", measured)
        await asyncio.sleep(60)


async def main():
    client = Client(token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ0aGluZ0lkIjoiZWEyZmQwNjAtZjk4Mi00MWI2LTg4YmMtNmIwYzkwODEwNDFkIiwidG9rZW5UeXBlIjoiVEhJTkdfQUNDRVNTIn0.3_XlSkryEh-N3h0Nl-S-MbUrFwbFlLJ4nJUKTARDD4Vp-zrmapHrIo9Y0nW_BNdOjoK4og2_I_H4QSiYyYGcXQ")
    thing = Thing(client, "ea2fd060-f982-41b6-88bc-6b0c9081041d")
    await asyncio.gather(monitor_temperature(client), thing.keepOnline())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
