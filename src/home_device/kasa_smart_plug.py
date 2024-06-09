import asyncio

from kasa import SmartPlug

ipaddress = "192.168.0.179"

plug = SmartPlug(ipaddress)


async def turn_on(smart_plug: SmartPlug):
    await plug.update()  ## necessary
    await plug.turn_on()
    print(plug.state_information)
    return


asyncio.run(turn_on(plug))
