from igloo import Client, User
import asyncio

client = Client(asyncio=True, token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJleHAiOjE1NTQ0OTcyNjksInVzZXJJZCI6ImU3NjFmZmUyLWUzZDktNDRiNi1iNjJkLTQzZjhlOWMxNGM2MiIsImFjY2Vzc0xldmVsIjoiT1dORVIiLCJ0b2tlblR5cGUiOiJURU1QT1JBUlkifQ.gZFA4bxGLNwiAs5ZoyUlZ4lgItBNUrxOuKhToC5bMR_W5xDym7Hbj1lfUv_RQHe2-IHDUL7n-xHdVkeVdA4PmA")


async def main():
    user = User(client)
    name = user.name
    email = user.email

    print(await name)
    print(await email)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
