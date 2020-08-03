import plux
import datetime

class GlobalFunction():
    
    def exampleFindDevices():
        devices = plux.BaseDev.findDevices()
        print("Found devices: ", devices)
    
    def exampleStart(dev):
        try:   # MAC address of device
            props = dev.getProperties()
            print('Properties:', props)
            dev.start(1000, 0xFF, 16)   # 1000 Hz, ports 1-8, 16 bits
            dev.loop()  # returns after receiving 10000 frames (onRawFrame() returns True)
            dev.stop()
            dev.close()
        except Exception as e:
            print(e)
            if (dev):
                dev.close()
    
    def exampleStartSources(dev):
        srcx = plux.Source()
        srcx.port = 1
        # nBits defaults to 16
        # freqDivisor defaults to 1
        # chMask defaults to 1
        
        srcy = plux.Source()
        srcy.port = 2
        srcy.nBits = 8
        srcy.freqDivisor = 3  # divide base frequency by 3 for this source
        
        srcz = plux.Source()
        srcz.port = 3
        srcz.freqDivisor = 2  # divide base frequency by 2 for this source
        
        dev.start(1000, (srcx, srcy, srcz)) # base freq: 1000 Hz, ports 1-3 as defined by sources
        dev.loop()   # returns after receiving 10000 frames (onRawFrame() returns True)
        dev.stop()
        dev.close()
    
    def exampleAddSchedule(dev):
        srcx = plux.Source()
        srcx.port = 1
        
        srcy = plux.Source()
        srcy.port = 2
        
        srcz = plux.Source()
        srcz.port = 3
        
        dev.setTime()   # adjust device RTC
        
        sch = plux.Schedule()
        sch.baseFreq = 1000 # in Hz
        sch.startTime = datetime.datetime.now() + datetime.timedelta(0,10)  # start an internal acquisition 10 seconds from now 
        #sch.startTime = 1  # decomment this line to start an internal acquisition with external trigger
        sch.duration = 30   # maximum duration of 30 seconds
        sch.sources = (srcx, srcy, srcz)
    
        dev.addSchedule(sch)
        dev.close()
        
    def exampleReplaySessions(dev):
        sessions = dev.getSessions()
        for s in sessions:
            dev.replaySession(s.startTime)  # replay all sessions on device
        dev.close
