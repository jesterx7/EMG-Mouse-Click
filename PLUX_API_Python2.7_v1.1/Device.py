# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 14:16:20 2020

@author: See
"""

import plux
import keyboard
import joblib
import matplotlib.pyplot as plt
from pynput.mouse import Button, Controller
from FeatureExtraction import FeatureExtract as fe

class MyDevice(plux.MemoryDev):
    # callbacks override
    secs = 0
    scaler = joblib.load('scaler.pkl')
    mouse = Controller()
    model = joblib.load('knn_model.pkl')
    record = False
    record_frame = 0
    record_data = []
    y_data = []
    x_data = []
        
    def onRawFrame(self, nSeq, data):
        self.y_data.append(data)
        self.x_data.append(nSeq)
        if (data[0] < 28586 or data[0] > 36586) and self.record == False:
            self.record = True
            print('Record Start')
            
        if self.record:
            self.record_data.append(data[0])
            self.record_frame += 1
            
        if self.record_frame == 1500:
            data_point = [fe.getAllData(fe, self.record_data)]
            data_point = self.scaler.transform(data_point)
            y = self.model.predict(data_point)
            print(y)
            if y[0] == 1:
                self.mouse.click(Button.left, 1)
                print('Mouse Left Click')
                save_file = open('mouse.txt', 'w')
                save_file.write('left')
                save_file.close()
            elif y[0] == 2:
                self.mouse.click(Button.right, 1)
                print('Mouse Right Click')
                save_file = open('mouse.txt', 'w')
                save_file.write('right')
                save_file.close()
            print('Record End')
            self.record_data = []
            self.record_frame = 0
            self.record = False
            
        if keyboard.is_pressed('q'):
            self.x_data = [(x / 1000) for x in self.x_data]
            plt.plot(self.x_data, self.y_data)
            plt.ylabel('Amplitude')
            plt.xlabel('Time (s)')
            plt.savefig('emg_signal.png')
            return True
        #if data[0] > 52000:
        #    self.mouse.click(Button.left, 1)
        #if nSeq >= 10000: return True  # Stop after receiving 10000 frames
        return False

    def onEvent(self, event):
        if type(event) == plux.Event.DigInUpdate:
            print('Digital input event - Clock source:', event.timestamp.source, \
                  ' Clock value:', event.timestamp.value, ' New input state:', event.state)
        elif type(event) == plux.Event.SchedChange:
            print('Schedule change event - Action:', event.action, \
                  ' Schedule start time:', event.schedStartTime)
        elif type(event) == plux.Event.Sync:
            print('Sync event:')
            for tstamp in event.timestamps:
                print(' Clock source:', tstamp.source, ' Clock value:', tstamp.value)
        elif type(event) == plux.Event.Disconnect:
            print('Disconnect event - Reason:', event.reason)
            return True
        return False
        
    def onInterrupt(self, param):
        print('Interrupt:', param)
        return False

    def onTimeout(self):
        print('Timeout')
        return False

    def onSessionRawFrame(self, nSeq, data):
        if nSeq % 1000 == 0:
            print('Session:', nSeq, data)
        return False

    def onSessionEvent(self, event):
        if type(event) == plux.Event.DigInUpdate:
            print('Session digital input event - Clock source:', event.timestamp.source, \
                  ' Clock value:', event.timestamp.value, ' New input state:', event.state)
        elif type(event) == plux.Event.Sync:
            print('Session sync event:')
            for tstamp in event.timestamps:
                print(' Clock source:', tstamp.source, ' Clock value:', tstamp.value)
        return False
    
    def setModel(self, method):
        if method.lower() == 'knn':
            self.model = joblib.load('knn_3_model.pkl')
        else:
            self.model = joblib.load('svm_rbf_model.pkl')

