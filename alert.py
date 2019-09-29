from igloo import Client, User, FloatVariable
import asyncio


async def main():
    client = Client(asyncio=True, token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VySWQiOiJmODFhODQ3Zi1mZDAyLTQzMDgtOWY3Zi02MTNkZjQ2OTUyNzMiLCJ0b2tlbklkIjoiZjdiZDA1NzMtZTYzMC00ZGIxLTllMTItODE2MDA5NTgyODU4IiwiYWNjZXNzTGV2ZWwiOiJERVZJQ0UiLCJ0b2tlblR5cGUiOiJQRVJNQU5FTlQifQ.VuPRvdMayBg7GxixT4QBjXd3jYO_3Q24Fctx508_p5iRxY96zv0z9-UXQsYGJiJjsI3E7ei2gtgEF84gsm8bnA")

    async for node in client.subscription_root.floatSeriesNodeCreated(seriesId="15dcf4e4-e7de-4c0e-a944-a1e63fbebb3d"):
        print(node.value)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
