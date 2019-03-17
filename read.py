from bluepy import btle
from bluepy.btle import Scanner, DefaultDelegate, ScanEntry, Peripheral
import struct 

"""Delegate for receiving BTLE events"""
class BTEventHandler(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.device_macs = []

    def handleDiscovery(self, dev, isNewDev, isNewData):
        """ Adv data """
        if isNewDev:
            print "Found new device:", dev.addr, dev.getScanData()
            self.device_macs.append(dev.addr)

        """ Scan response """
        if isNewData:
            print "Received more data:", dev.addr, dev.getScanData()

    def handleNotification(self, cHandle, data):
        """ Print value only if handle is 40, battery characteristic """
        if cHandle == 40:
            print struct.unpack('B', data)

handler = BTEventHandler()

""" Create a scanner with the handler as delegate """
scanner = Scanner().withDelegate(handler)

""" Start scanning for (argument) seconds. While scanning, handleDiscovery will be called whenever a new device or new data is found"""
devs = scanner.scan(30)

""" After end of scan, print all device addresses heard """
for mac in handler.device_macs:
    print mac

""" Get Hexiwear address """
hexi_addr = [dev for dev in devs if dev.getValueText(0x8) == 'HEXIWEAR'][0].addr 

""" Create peripheral object with the delegate """
hexi = Peripheral().withDelegate(handler)

""" Connect to hexiwear """
hexi.connect(hexi_addr)

""" Get battery service """
battery = hexi.getCharacteristics(uuid="2a19")[0]

""" Get client configuration descriptor and write 1 to it to enable notification"""
battery_desc = battery.getDescriptors(forUUID=0x2902)[0]
battery_desc.write(b"\x01", True)

""" Infinite loop to receive notifications """
print "Entering notification receiving loop"
while True:
    hexi.waitForNotifications(1.0)

