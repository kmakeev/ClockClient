import requests
import json
import calendar
import time
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import (StringProperty, BooleanProperty, ListProperty)
from kivy.uix.floatlayout import FloatLayout

from tubesClock import TubesClock


__author__ = 'Makeev K.P.'

Builder.load_string("""

<ClockApp>
    id: myApp

<TBPanel>:
    id: tbp
    do_default_tab: False
    #tab_height: 70
    #tab_width: 200
    TabbedPanelItem:
        id: 'General'
        text: 'General'
        MyFloatLayout:
            id: _myFl
            size_hint: (1, 1)
            pos_hint: {'x': 0, 'y': 0}
            Label:
                # color: (1,0,0,1)
                text: 'Show'
                size_hint: (0.1, 0.08)
                pos_hint: {'x': 0.1, 'y': 0.91}
                font_size: '40dp'
            Button:
                id: btn
                text: '-----'
                on_release: _dropdown.open(self)
                # size_hint_y: None
                size_hint: (0.94, 0.07)
                pos_hint: {'x': 0.03, 'y': 0.82}
                height: '48dp'
            DropDown:
                id: _dropdown
                on_parent: self.dismiss()
                # on_select: app.change_mode(args[1])
                Button:
                    text: 'Time'
                    size_hint_y: None
                    height: '48dp'
                    on_release: _dropdown.select(self.text)
                Button:
                    text: 'Date'
                    size_hint_y: None
                    height: '48dp'
                    on_release: _dropdown.select(self.text)
                Button:
                    text: 'Alarm'
                    size_hint_y: None
                    height: '48dp'
                    on_release: _dropdown.select(self.text)
                Button:
                    text: 'Temperature'
                    size_hint_y: None
                    height: '48dp'
                    on_release: _dropdown.select(self.text)
                Button:
                    text: 'Auto'
                    size_hint_y: None
                    height: '48dp'
                    on_release: _dropdown.select(self.text)
            GridLayout:
                cols: 4
                size_hint: (1, 0.3)
                spacing: 1
                pos_hint: {'x': 0, 'y': 0.53}
                Label:
                    text: 'Tubes'
                    font_size: '22dp'
                Label:
                    text: ''
                Label:
                    text: ''
                Switch:
                    id: _sw1
                    # active: True
                    # on_active: app.changeSW1(_sw1.active)

                Label:
                    text: 'Leds'
                    font_size: '22dp'
                Label:
                    text: ''
                Label:
                    text: ''
                Switch:
                    id: _sw2
                    # on_active: app.changeSW2(_sw2.active)
                Label:
                    text: 'Alarm'
                    font_size: '22dp'
                Label:
                    text: ''
                Label:
                    text: ''
                Switch:
                    id: _sw3
                    # on_active: app.changeSW3(_sw3.active)

            Label:
                #color: (1,0,0,1)
                text: 'Set'
                size_hint: (0.1, 0.1)
                pos_hint: {'x': 0.08, 'y': 0.44}
                font_size: '40dp'

            GridLayout:
                cols: 4
                size_hint: (1, 0.3)
                pos_hint: {'x': 0, 'y': 0.16}
                spacing: 1
                Label:
                    text: 'Time'
                    font_size: '22dp'
                Label:
                    text: ''
                Label:
                    text: ''
                Label:
                    text: _myFl._time
                    markup: True
                    font_size: '20dp'
                    color: _myFl.color_text
                    on_ref_press: app.press_time(self.text)

                Label:
                    text: 'Date'
                    font_size: '22dp'
                Label:
                    text: ''
                Label:
                    text: ''
                Label:
                    text: _myFl._date
                    markup: True
                    font_size: '20dp'
                    color: _myFl.color_text
                    on_ref_press: app.press_date(self.text)

                Label:
                    text: 'Alarm'
                    font_size: '22dp'
                Label:
                    text: ''
                Label:
                    text: ''
                Label:
                    text: _myFl._alarm
                    markup: True
                    font_size: '20dp'
                    color: _myFl.color_text
                    on_ref_press: app.press_alarm(self.text)

            GridLayout:
                cols: 2
                size_hint: (1, 0.1)
                spacing: 4
                pos_hint: {'x': 0, 'y': 0.03}
                Button:
                    id: _bt1
                    text: 'BT1'
                    background_color: (1,0,0,1)
                    size_hint: (1, 1)
                    # pos_hint: {'x': 0.0, 'y': 0.0}
                    font_size: 40
                    on_press: app.button1Pressed()
                Button:
                    id: _bt2
                    text: 'BT2'
                    background_color: (1,0,0,1)
                    size_hint: (1, 1)
                    #pos_hint: {'x': 1, 'y': 1}
                    font_size: 40
                    on_press: app.button2Pressed()
            Label:
                text: _myFl.status
                size_hint: (0.2, 0.02)
                font_size: '10dp'
                pos_hint: {'x': 0.03, 'y': 0.007}



    TabbedPanelItem:
        id: 'Advanced'
        text: 'Advanced'

    Popup:
        id: popupSetTime
        title: "Set time"
        content: _PopupSetTime
        size_hint: (1, 0.6)
        pos_hint: {'x': 0, 'y': 0.15}
        ContentPopupSetTime:
            id: _PopupSetTime
            size_hint: (0.5, 0.5)
            pos_hint: popupSetTime.pos_hint
            Spinner:
                id: _time_hours
                size_hint: (0.2, 0.4)
                pos_hint: {'x': 0.19, 'y': 0.5}
                text: '00'
                values: ('00', '01', '02', '03', '04', '05', '06', '07', '08','09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20','21', '22', '23')
                height: '24dp'
                # on_text: app.changeSp1(_sp1.text)
            Spinner:
                id:_time_minutes
                size_hint: (0.2, 0.4)
                pos_hint: {'x': 0.4, 'y': 0.5}
                text: '00'
                values: ('00', '05', '10', '15', '20', '25', '30', '35', '40','45', '50', '55')
                height: '24dp'
                # on_text: app.changeSp1(_sp2.text)
            Spinner:
                id:_time_seconds
                size_hint: (0.2, 0.4)
                pos_hint: {'x': 0.61, 'y': 0.5}
                text: '00'
                values: ('00', '05', '10', '15', '20', '25', '30', '35', '40','45', '50', '55')
                height: '24dp'
                # on_text: app.changeSp1(_sp2.text)

            Button:
                size_hint: (0.4, 0.4)
                pos_hint: {'x': 0.1, 'y': -0.17}
                text: 'Save'
                on_release: app.saveTime()
            Button:
                size_hint: (0.4, 0.4)
                pos_hint: {'x': 0.502, 'y': -0.17}
                text: 'Cancel'
                on_release: popupSetTime.dismiss()

    Popup:
        id: popupSetDate
        title: "Set date"
        content: _PopupSetDate
        size_hint: (1, 0.6)
        pos_hint: {'x': 0, 'y': 0.15}
        ContentPopupSetDate:
            id: _PopupSetDate
            size_hint: (0.5, 0.5)
            pos_hint: popupSetDate.pos_hint
            Spinner:
                id: _date_day
                size_hint: (0.2, 0.4)
                pos_hint: {'x': 0.19, 'y': 0.5}
                text: '01'
                values: ('00')
                height: '24dp'
                # on_text: app.changeSp1(_sp1.text)

            Spinner:
                id:_date_month
                size_hint: (0.2, 0.4)
                pos_hint: {'x': 0.4, 'y': 0.5}
                text: '01'
                values: ('00', '01', '02', '03', '04', '05', '06', '07', '08','09', '10', '11', '12')
                height: '24dp'
                on_text: app.changeSp(_date_month.text)

            Spinner:
                id:_date_year
                size_hint: (0.2, 0.4)
                pos_hint: {'x': 0.61, 'y': 0.5}
                text: '16'
                values: ('16')
                height: '24dp'
                on_text: app.changeSp(_date_year.text)

            Button:
                size_hint: (0.4, 0.4)
                pos_hint: {'x': 0.1, 'y': -0.17}
                text: 'Save'
                on_release: app.saveDate()
            Button:
                size_hint: (0.4, 0.4)
                pos_hint: {'x': 0.502, 'y': -0.17}
                text: 'Cancel'
                on_release: popupSetDate.dismiss()
    Popup:
        id: popupSetAlarm
        title: "Set alarm"
        content: _PopupSetAlarm
        size_hint: (1, 0.6)
        pos_hint: {'x': 0, 'y': 0.15}
        ContentPopupSetAlarm:
            id: _PopupSetAlarm
            size_hint: (1, 0.6)
            pos_hint: popupSetAlarm.pos_hint
            Spinner:
                id: _time_hours_alarm
                size_hint: (0.2, 0.4)
                pos_hint: {'x': 0.29, 'y': 0.5}
                text: '00'
                values: ('00', '01', '02', '03', '04', '05', '06', '07', '08','09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20','21', '22', '23')
                height: '24dp'
                # on_text: app.changeSp1(_sp1.text)
            Spinner:
                id:_time_minutes_alarm
                size_hint: (0.2, 0.4)
                pos_hint: {'x': 0.5, 'y': 0.5}
                text: '00'
                values: ('00', '05', '10', '15', '20', '25', '30', '35', '40','45', '50', '55')
                height: '24dp'
                # on_text: app.changeSp1(_sp2.text)

            Button:
                size_hint: (0.4, 0.4)
                pos_hint: {'x': 0.1, 'y': -0.17}
                text: 'Save'
                on_release: app.saveAlarm()
            Button:
                size_hint: (0.4, 0.4)
                pos_hint: {'x': 0.502, 'y': -0.17}
                text: 'Cancel'
                on_release: popupSetAlarm.dismiss()




""")


class TBPanel(TabbedPanel):

    def __init__(self, *args, **kwargs):
        super(TBPanel, self).__init__(*args, **kwargs)


class ContentPopupSetTime(FloatLayout):
    def __init__(self, *args, **kwargs):
        super(ContentPopupSetTime, self).__init__(*args, **kwargs)


class ContentPopupSetDate(FloatLayout):
    def __init__(self, *args, **kwargs):
        super(ContentPopupSetDate, self).__init__(*args, **kwargs)


class ContentPopupSetAlarm(FloatLayout):
    def __init__(self, *args, **kwargs):
        super(ContentPopupSetAlarm, self).__init__(*args, **kwargs)


class MyFloatLayout(FloatLayout):

    def __init__(self, *args, **kwargs):
        super(MyFloatLayout, self).__init__(*args, **kwargs)

    status = StringProperty('')
    color_text = ListProperty([1, 1, 1, 1])
    _time = StringProperty("[ref=time]--:--:--[/ref]")
    _date = StringProperty('[ref=time]--/--/--[/ref]')
    _alarm = StringProperty('[ref=time]--:--[/ref]')



class ClockApp(App):
    _panel = TBPanel()
    content = ''
    parsed_string = {}
    set_string = {"led": 255, "mode": 0, "isAl": "false", "m_a": "true", "tset": 0, "btn1": 1, "btn2": 0}
    url = ''
    #  icon = 'src//icon.png'
    title = 'Application for clock management'
    # use_kivy_settings = False
    isConnected = BooleanProperty(False)


    def build(self):
        _panel = self._panel
        self.url = self.config.get('Clock', 'url')
        self._tubes = TubesClock(self.url)
        if self._tubes.isConnected:
            self._panel.ids["_sw2"].active = self._tubes.isLedsOn
            self._panel.ids["_sw1"].active = self._tubes.isTubesOn
            self._panel.ids["_sw3"].active =self._tubes.isAlarmOn
            self._panel.ids["_time_hours_alarm"].text = self._tubes._alarmHH
            self._panel.ids["_time_minutes_alarm"].text = self._tubes._alarmMM
            _alarm = self._tubes._alarmHH + ':' + self._tubes._alarmMM
            self._panel.ids["_myFl"]._alarm = '[ref=time]' + _alarm + '[/ref]'
            _time = self._tubes._timeHH + ':' + self._tubes._timeMM + ':' + self._tubes._timeSS
            self._panel.ids["_myFl"]._time = '[ref=time]' + _time + '[/ref]'
            _date = self._tubes._dateDD + '/' + self._tubes._dateMM + '/' + self._tubes._dateYY
            self._panel.ids["_myFl"]._date = '[ref=time]' + _date + '[/ref]'
            self._panel.ids["_myFl"].status = 'Connected'
            self._panel.ids["_myFl"].color_text = [1, 1, 1, 1]
        else:
            self._panel.ids["_myFl"].status = 'Not Connected'
            self._panel.ids["_myFl"].color_text = [1, 1, 1, 0.3]
        # self.get_arduino_()

        self._panel.ids["_sw1"].bind(active=self.changeSW1)
        self._panel.ids["_sw2"].bind(active=self.changeSW2)
        self._panel.ids["_sw3"].bind(active=self.changeSW3)
        self._panel.ids["_dropdown"].bind(on_select=self.change_mode)

        return _panel

    def build_config(self, config):
        config.add_section('Clock')
        config.set('Clock', 'url', 'http://192.168.4.1')

    def build_settings(self, settings):
        settings.add_json_panel('Application for clock management', self.config, data='''[
            { "type": "title", "title": "Options" },
            { "type": "string",
              "title": "URL address of clock",
              "section": "Clock",
              "key": "url"}
              ]''')

    def on_config_change(self, config, section, key, value):
        token = (section, key)
        if token == ('Clock', 'url'):
            pass


    def changeSW1(self, instance,value):
        print("SWitch 1 change", value)
        if value:
            self._tubes.isTubesOn = 0
        else:
            self._tubes.isTubesOn = 5

    def changeSW2(self, instance, value):
        print("SWitch 2 change", value)
        if value:
            self._tubes.isLedsOn = True
        else:
            self._tubes.isLedsOn = False

    def changeSW3(self, instance, value):
        print("SWitch 3 change", value)
        if value:
            self._tubes.isAlarmOn = True
            _alarm = self._tubes._alarmHH + ':' + self._tubes._alarmMM
            self._panel.ids["_myFl"]._alarm = '[ref=time]' + _alarm + '[/ref]'
        else:
            self._tubes.isAlarmOn = False
            self._panel.ids["_myFl"]._alarm = '[ref=time]--:--[/ref]'

    def change_mode(self, instance, value):
        print('DropDown change - ', value)
        self._tubes.mode = value
        self._panel.ids["btn"].text = value

    def press_time(self, value):
        print('Time pressed', value)
        self._panel.ids["_time_hours"].text = self._tubes._timeHH
        self._panel.ids["_time_minutes"].text = self._tubes._timeMM
        self._panel.ids["_time_seconds"].text = self._tubes._timeSS
        mm = [self._tubes.nonZeroStr(x) for x in range(00, 60, 1)]
        self._panel.ids["_time_minutes"].values = tuple(mm)
        self._panel.ids["_time_seconds"].values = tuple(mm)
        self._panel.ids["popupSetTime"].open()

    def press_date(self, value):
        print('Date pressed', value)
        self._panel.ids["_date_day"].text = self._tubes._dateDD
        self._panel.ids["_date_month"].text = self._tubes._dateMM
        self._panel.ids["_date_year"].text = self._tubes._dateYY
        year = [str(x) for x in range(16, 50, 1)]
        self._panel.ids["_date_year"].values = tuple(year)
        if self._panel.ids["_date_month"].text == '--':
            mm = 1
        else:
            mm = self._panel.ids["_date_month"].text
        if self._panel.ids["_date_year"].text == '--':
            yy = 16
        else:
            yy = self._panel.ids["_date_year"].text
        day = [self._tubes.nonZeroStr(x) for x in range(1, calendar.monthrange(int(yy), int(mm))[1] + 1, 1)]
        self._panel.ids["_date_day"].values = tuple(day)
        self._panel.ids["popupSetDate"].open()

    def changeSp(self, value):
        print('Select ', value)
        year = [str(x) for x in range(16, 50, 1)]
        self._panel.ids["_date_year"].values = tuple(year)
        if self._panel.ids["_date_month"].text == '--':
            mm = 1
        else:
            mm = self._panel.ids["_date_month"].text
        if self._panel.ids["_date_year"].text == '--':
            yy = 16
        else:
            yy = self._panel.ids["_date_year"].text
        day = [self._tubes.nonZeroStr(x) for x in range(1, calendar.monthrange(int(yy), int(mm))[1] + 1, 1)]
        self._panel.ids["_date_day"].values = tuple(day)
        dd = self._panel.ids["_date_day"].text
        if dd != '--':
            if int(dd) > int(day[-1]):
                self._panel.ids["_date_day"].text = day[-1]

    def press_alarm(self, value):
        print('Alarm pressed', value)
        self._panel.ids["popupSetAlarm"].open()


    def saveTime(self):
        if self.isConnected:
            self._tubes._timeHH = self._panel.ids["_time_hours"].text
            self._tubes._timeMM = self._panel.ids["_time_minutes"].text
            self._tubes._timeSS = self._panel.ids["_time_seconds"].text
            _time = self._tubes._timeHH + ':' + self._tubes._timeMM + ':' + self._tubes._timeSS
            self._panel.ids["_myFl"]._time = '[ref=time]' + _time + '[/ref]'
            print('Save Time - ', self._panel.ids["_myFl"]._time)
        else:
            print('Time not saved')
        self._panel.ids["popupSetTime"].dismiss()

    def saveDate(self):
        if self.isConnected:
            self._tubes._dateDD = self._panel.ids["_date_day"].text
            self._tubes._dateMM = self._panel.ids["_date_month"].text
            self._tubes._dateYY = self._panel.ids["_date_year"].text
            _date = self._tubes._dateDD + '/' + self._tubes._dateMM + '/' + self._tubes._dateYY
            self._panel.ids["_myFl"]._date = '[ref=date]' + _date + '[/ref]'
            print('Save Date - ', self._panel.ids["_myFl"]._date)
        else:
            print('Date not saved')
        self._panel.ids["popupSetDate"].dismiss()

    def saveAlarm(self):
        if self.isConnected:
            print('Save Alarm')
            self._tubes._alarmHH = self._panel.ids["_time_hours_alarm"].text
            self._tubes._alarmMM = self._panel.ids["_time_minutes_alarm"].text
            _alarm = self._tubes._alarmHH + ':' + self._tubes._alarmMM
            self._panel.ids["_myFl"]._alarm = '[ref=alarm]' + _alarm + '[/ref]'
            self._panel.ids["_sw3"].active = True
        else:
            print('Alarm not turned On')
        self._panel.ids["popupSetAlarm"].dismiss()

    def button1Pressed(self):
        self._tubes.btn1Press = not self._tubes.btn1Press

    def button2Pressed(self):
        self._tubes.btn1Press = not self._tubes.btn1Press

    def on_pause(self):

        return True

    def on_resume(self):
        pass

    def on_resize(self, win, width, heigth):
        print(width, heigth, win)


    def on_start(self):
        pass
        # self.root_window.fbind('on_resize', self.on_resize)
        # self.root_window.system_size = [640, 960]
        # self.root_window.heigth = 1920


if __name__ == '__main__':
    ClockApp().run()











