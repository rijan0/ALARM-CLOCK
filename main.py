from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.audio import SoundLoader  
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from datetime import datetime, timedelta

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        layout = FloatLayout()

     
        image = Image(source='person_waking_up.png', size_hint=(None, None), size=(350, 350), pos_hint={'x': 0.12, 'y': 0.3})
        image.center = layout.center  
        layout.add_widget(image)

        logo = Image(source='LOGO.png', size_hint=(None, None), size=(350, 350), pos_hint={'x': 0.1, 'y': 0.65})
        layout.add_widget(logo)

       
        start_button = Button(
            text="GET STARTED",
            size_hint=(None, None),
            size=(300, 60),
            pos_hint={'x': 0.16, 'y': 0.05},  
            background_normal='',  
            background_color=(0, 0, 0, 0),  
            color=(1, 1, 1, 1), 
            font_size='24sp'  
        )

       
        with start_button.canvas.before:
            Color(0.3, 0.3, 0.3, 1)  
            self.border = RoundedRectangle(
                size=start_button.size,
                pos=start_button.pos,
                radius=[25]  
            )

        
        start_button.bind(pos=self.update_border, size=self.update_border)

        
        start_button.bind(on_press=self.change_screen)

        layout.add_widget(start_button)

       
        with layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  
            self.rect = Rectangle(size=layout.size, pos=layout.pos)

       
        layout.bind(size=self._update_rect, pos=self._update_rect)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
      
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_border(self, instance, value):
        
        self.border.pos = instance.pos
        self.border.size = instance.size

    def change_screen(self, instance):
        
        self.manager.current = 'next_screen'

class NextScreen(Screen):
    def __init__(self, **kwargs):
        super(NextScreen, self).__init__(**kwargs)

        layout = FloatLayout()

        
        scroll_view = ScrollView(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})

        scroll_layout = FloatLayout(size_hint=(None, None), size=(Window.width, 1000))  

        
        label = Label(text="SET ALARM TIME", size_hint=(None, None), size=(300, 60), pos_hint={'x': 0.1, 'y': 0.85},
                      color=(1, 1, 1, 1), font_size='30sp')
        scroll_layout.add_widget(label)
        l2 = Label(text="SET ALARM SOUND FIRST", size_hint=(None, None), size=(150, 30), pos_hint={'x': 0.2, 'y': 0.80},
                      color=(1, 1, 1, 1), font_size='15sp')
        scroll_layout.add_widget(l2)

        # Add Hour Spinner
        self.hour_spinner = Spinner(
            text='Hour',
            values=[str(i).zfill(2) for i in range(1, 13)], 
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'x': 0.07, 'y': 0.7}
        )
        scroll_layout.add_widget(self.hour_spinner)

        
        self.minute_spinner = Spinner(
            text='Minute',
            values=[str(i).zfill(2) for i in range(0, 60, 1)],  
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'x': 0.22, 'y': 0.7}
        )
        scroll_layout.add_widget(self.minute_spinner)

       
        self.am_pm_spinner = Spinner(
            text='AM',
            values=['AM', 'PM'],
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'x': 0.37, 'y': 0.7}
        )
        scroll_layout.add_widget(self.am_pm_spinner)

        
        set_alarm_button = Button(
            text="Set Alarm",
            size_hint=(None, None),
            size=(300, 60),
            pos_hint={'x': 0.1, 'y': 0.3},  
            background_normal='',  
            background_color=(0, 0, 0, 0),  
            color=(1, 1, 1, 1),  
            font_size='24sp'  
        )

        with set_alarm_button.canvas.before:
            Color(0.3, 0.3, 0.3, 1)  
            self.set_alarm_border = RoundedRectangle(
                size=set_alarm_button.size,
                pos=set_alarm_button.pos,
                radius=[25]  
            )

        
        set_alarm_button.bind(pos=self.update_set_alarm_border, size=self.update_set_alarm_border)
       
        self.button_click_sound = SoundLoader.load('button_click.mp3')  #

        if not self.button_click_sound:
            print("Error: Sound file 'button_click.mp3' not found or failed to load.")
        else:
            print("Sound loaded successfully.")

        set_alarm_button.bind(on_press=self.set_alarm)

        scroll_layout.add_widget(set_alarm_button)

        set_alarm_sound_button = Button(
            text="Set Alarm Sound",
            size_hint=(None, None),
            size=(300, 60),
            pos_hint={'x': 0.1, 'y': 0.2}, 
            background_normal='',  
            background_color=(0, 0, 0, 0), 
            color=(1, 1, 1, 1),  
            font_size='24sp'
        )

        

        
        set_alarm_sound_button.bind(on_press=self.set_alarm_sound)

        scroll_layout.add_widget(set_alarm_sound_button)

       
        scroll_view.add_widget(scroll_layout)

        layout.add_widget(scroll_view)

        self.add_widget(layout)

        
        self.alarm_time = None

        Clock.schedule_interval(self.check_alarm, 60)

    def update_set_alarm_border(self, instance, value):
       
        self.set_alarm_border.pos = instance.pos
        self.set_alarm_border.size = instance.size

    def set_alarm(self, instance):
        hour = int(self.hour_spinner.text)
        minute = int(self.minute_spinner.text)
        am_pm = self.am_pm_spinner.text

        if am_pm == "PM" and hour != 12:
            hour += 12 
        elif am_pm == "AM" and hour == 12:
            hour = 0 

       
        now = datetime.now()
        self.alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        print(f"Alarm set for: {self.alarm_time.strftime('%H:%M:%S')}")

    def set_alarm_sound(self, instance):
        
        filechooser = FileChooserIconView()

       
        select_button = Button(text="Select", size_hint=(None, None), size=(150, 50), pos_hint={'x': 0.10, 'y': 0.0})
        select_button.bind(on_press=lambda x: self.set_selected_alarm_sound(filechooser.selection))

       
        close_button = Button(text="Close", size_hint=(None, None), size=(150, 50), pos_hint={'x': 0.5, 'y': 0.0})
        close_button.bind(on_press=self.close_popup)

       
        self.popup = Popup(title="Select Alarm Sound", content=filechooser,
                           size_hint=(0.9, 0.9), auto_dismiss=False)

        filechooser.add_widget(select_button)
        filechooser.add_widget(close_button)

      
        self.popup.open()

    def close_popup(self, instance=None):
       
        if self.popup:
            self.popup.dismiss()

    def set_selected_alarm_sound(self, selected_file):
       
        if selected_file:
            sound_path = selected_file[0]  
            self.button_click_sound = SoundLoader.load(sound_path) 

            if self.button_click_sound:
                print(f"Selected alarm sound: {sound_path}")
            else:
                print(f"Error: Unable to load selected sound file: {sound_path}")

    def check_alarm(self, dt):
      
        if self.alarm_time and datetime.now() >= self.alarm_time:
            print("Alarm ringing...")
            if self.button_click_sound:
                self.button_click_sound.play()  
            self.alarm_time = None  
    

class AlarmApp(App):
    def build(self):
     
        Window.clearcolor = (0.2, 0.4, 0.6, 1)  
        Window.size = (450, 900)  

        screen_manager = ScreenManager()

        screen_manager.add_widget(MainScreen(name='main_screen'))
        screen_manager.add_widget(NextScreen(name='next_screen'))

        return screen_manager


if __name__ == "__main__":
    AlarmApp().run()
