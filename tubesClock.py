import requests
import json
from kivy.event import EventDispatcher
from kivy.properties import (StringProperty, BooleanProperty, NumericProperty)


# For clock management class
class TubesClock(EventDispatcher):

    _timeHH = StringProperty('--')
    _timeMM = StringProperty('--')
    _timeSS = StringProperty('--')
    _dateDD = StringProperty('--')
    _dateMM = StringProperty('--')
    _dateYY = StringProperty('--')
    _alarmHH = StringProperty('--')
    _alarmMM = StringProperty('--')
    isConnected = BooleanProperty(False)

    isLedsOn = BooleanProperty(False)
    isTubesOn = BooleanProperty(False)
    isAlarmOn = BooleanProperty(False)
    mode = StringProperty('Auto')

    btn1Press = BooleanProperty(False)
    btn2Press = BooleanProperty(False)

    modes_string = ['Time', 'Date', 'Alarm', 'Temperature', 'Auto']
    _timeout = NumericProperty(3)
    content = ''
    parsed_string = {}
    set_string = {"led": 255, "mode": 0, "isAl": "false", "m_a": "true", "tset": 0, "btn1": 1, "btn2": 0}
    # set_string_button = {"btn1": 0, "btn2": 0}
    url = ''

    def __init__(self, _url):
        self.url = _url
        self.get_arduino()
        if self.isConnected:
            self.parsing_content()
        self.bind(isTubesOn=self.on_isTubesOn)
        self.bind(isLedsOn=self.on_isLedsOn)
        self.bind(isAlarmOn=self.on_isAlarmOn)
        self.bind(mode=self.on_change_mode)
        self.bind(btn1Press=self.on_btn1Press)
        self.bind(btn2Press=self.on_btn2Press)
        self.bind(_alarmMM=self.on_alarmMM)
        self.bind(_timeSS=self.on_timeSS)
        self.bind(_dateYY=self.on_dateYY)


# Get json-string from arduino
    def get_arduino(self):
        try:
            x = requests.get(self.url, timeout=self._timeout)
            self.content = x.content
            print(self.content)
            self.isConnected = True
        except:
            print('Error, not connection to Clock')
            self.isConnected = False

    def parsing_content(self):
        content = self.content
        set_string = self.set_string
        if content:
            patched_content = content.decode('utf-8')
            print(patched_content)
            if patched_content[-1] != '}':
                print(patched_content[-4::])
                if patched_content[-4::] == 'fals':
                    patched_content += 'e}'
                elif patched_content[-5::] == 'false':
                    patched_content += '}'
            try:
                self.parsed_string = json.loads(patched_content)
                set_string["led"] = self.parsed_string["led"]
                # set_string["mode"] = self.parsed_string["mode"]
                set_string["isAl"] = self.parsed_string["isAl"]
                set_string["m_a"] = self.parsed_string["m_a"]
                self.mode = self.modes_string[self.parsed_string["mode"]]
                if set_string["led"] > 0:
                    self.isLedsOn = True
                else:
                    self.isLedsOn = False
                if self.set_string["mode"] != 5:
                    self.isTubesOn = True
                else:
                    self.isTubesOn = False
                if set_string["isAl"]:
                    self.isAlarmOn = True
                    self._alarmHH = self.nonZeroStr(self.parsed_string["alHour"])
                    self._alarmMM = self.nonZeroStr(self.parsed_string["alMin"])
                else:
                    self.isAlarmOn = False
                self._timeHH = self.nonZeroStr(self.parsed_string["hh"])
                self._timeMM = self.nonZeroStr(self.parsed_string["min"])
                self._timeSS = self.nonZeroStr(self.parsed_string["sec"])
                self._dateDD = self.nonZeroStr(self.parsed_string["dd"])
                self._dateMM = self.nonZeroStr(self.parsed_string["mm"])
                self._dateYY = self.nonZeroStr(self.parsed_string["yy"])
            except:
                print("Not parse Json-string -", patched_content)
                pass

    def set_arduino(self, str_):

        print(json.dumps(str_).encode('utf-8'))
        try:
            y = requests.put(self.url, timeout=5, data=json.dumps(str_).encode('utf-8'))
        except:
            print("Sets in arduino erros -")
            pass

    def nonZeroStr(self, aa):
        a1 = aa // 10
        a2 = aa % 10
        return str(a1)+str(a2)

    def on_isLedsOn(self, instance, value):
        print('Leds Change')
        if self.isConnected:
            if not value:                       # previos state
                self.set_string["led"] = 1
            else:
                self.set_string["led"] = 0
            self.set_arduino(self.set_string)

    def on_isTubesOn(self, instance, value):
        print('Tubes Change')
        if self.isConnected:
            if not value:
                self.set_string["mode"] = 0
            else:
                self.set_string["mode"] = 5
            self.set_arduino(self.set_string)

    def on_isAlarmOn(self, instance, value):
        print('Alarm Change')
        if self.isConnected:
            if value:
                self.set_string["isAl"] = "true"
                self.set_string["tset"] = 0
                self.set_string["alSet"] = 1
                self.set_string["mode"] = 2
                self.set_string["alHour"] = self._alarmHH
                self.set_string["alMin"] = self._alarmMM
            else:
                self.set_string["isAl"] = "false"
            self.set_arduino(self.set_string)

    def on_change_mode(self, instance, value):
        print('Mode Change to - ', value)
        if self.isConnected:
            if value == self.modes_string[4]:
                self.set_string["m_a"] = "true"
                self.set_string["mode"] = 0
            else:
                self.set_string["m_a"] = "false"
                self.set_string["mode"] = self.modes_string.index(value)
            self.set_string["tset"] = 0
            self.set_string["alSet"] = 0
            self.set_arduino(self.set_string)

    def on_btn1Press(self, instance, value):
        print("Button 1 pressed")
        if self.isConnected:
            self.set_string["btn1"] = 0
            self.set_arduino(self.set_string)
            self.set_string["btn1"] = 1


    def on_btn2Press(self, instance, value):
        print("Button 2 pressed")
        if self.isConnected:
            self.set_string["btn2"] = 1
            self.set_arduino(self.set_string)
            self.set_string["btn1"] = 0

    def on_alarmMM(self, instance, value):
        print("Save alarm in clock")
        self.set_string["alHour"] = self._alarmHH
        self.set_string["alMin"] = self._alarmMM

    def on_timeSS(self, instance, value):
        print('Save new time')

    def on_dateYY(self, instance, value):
        print('Save new date')

