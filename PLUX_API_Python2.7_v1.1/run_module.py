from Device import MyDevice as dev
from DeviceFunction import GlobalFunction as devFunction

#Declare device with your Device's MAC Address
device = dev("00:07:80:4D:2E:9E") 

#Device Start
devFunction.exampleStart(device)