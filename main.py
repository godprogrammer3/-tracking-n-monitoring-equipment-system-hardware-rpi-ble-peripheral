from bluez_peripheral.gatt.service import Service
from bluez_peripheral.gatt.characteristic import characteristic, CharacteristicFlags as CharFlags
from bluez_peripheral.gatt.descriptor import descriptor, DescriptorFlags as DescFlags
class ToolloLockerService(Service):
   def __init__(self):
      self._some_value = None
      super().__init__("BEEF", True)

   @characteristic("BEF0", CharFlags.READ)
   def my_readonly_characteristic(self, options):
      print('my_readonly_characteristic trigged')
      return bytes("Hello World!", "utf-8")

   @characteristic("BEF1", CharFlags.WRITE).setter
   def my_writeonly_characteristic(self, value, options):
      print('my_writeonly_characteristic trigged')
      self._some_value = value

from bluez_peripheral.util import *
from bluez_peripheral.advert import Advertisement
from bluez_peripheral.agent import NoIoAgent
import asyncio

async def main():
    bus = await get_message_bus()

    service = ToolloLockerService()
    await service.register(bus)

    # An agent is required to handle pairing 
    agent = NoIoAgent()
    # This script needs superuser for this to work.
    await agent.register(bus)

    adapter = await Adapter.get_first(bus)

    my_service_ids = ["BEEF"] # The services that we're advertising.
    my_appearance = 0 # The appearance of my service.
    # See https://specificationrefs.bluetooth.com/assigned-values/Appearance%20Values.pdf
    my_timeout = 60 # Advert should last 60 seconds before ending (assuming other local
    # services aren't being advertised).
    # Start an advert that will last for 60 seconds.
    advert = Advertisement("toollo-locker", my_service_ids, my_appearance, my_timeout)
    await advert.register(bus, adapter)

    # Handle any dbus requests.
    await bus.wait_for_disconnect()

if __name__ == "__main__":
    asyncio.run(main())