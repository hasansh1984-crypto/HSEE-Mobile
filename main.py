
import os
import sqlite3
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label

DB = os.path.join(os.path.dirname(__file__), "hsee.db")

KV = """
ScreenManager:
    Dashboard:
    Activities:
    Resolutions:

<Dashboard>:
    name: "home"
    BoxLayout:
        orientation: "vertical"
        padding: 16
        spacing: 12
        canvas.before:
            Color:
                rgba: 0.035, 0.07, 0.14, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "سامانه مدیریت HSEE"
            font_size: "25sp"
            bold: True
            color: 0.85, 0.88, 1, 1
            size_hint_y: None
            height: 65

        Label:
            text: "شرکت شهرک‌های صنعتی لرستان"
            font_size: "16sp"
            size_hint_y: None
            height: 35

        GridLayout:
            cols: 2
            spacing: 10

            Button:
                text: "کارتابل فعالیت‌ها"
                on_release: app.root.current = "activities"

            Button:
                text: "مصوبات جلسات"
                on_release: app.root.current = "resolutions"

            Button:
                text: "ثبت فعالیت جدید"
                on_release: app.new_activity()

            Button:
                text: "آمار سامانه"
                on_release: app.statistics()

        Widget:

        Label:
            text: "نسخه مستقل آفلاین | HSEE Mobile"
            size_hint_y: None
            height: 35

<Activities>:
    name: "activities"
    BoxLayout:
        orientation: "vertical"
        padding: 12
        spacing: 8

        Label:
            text: "کارتابل فعالیت‌ها"
            font_size: "23sp"
            size_hint_y: None
            height: 55

        ScrollView:
            GridLayout:
                id: activity_list
                cols: 1
                spacing: 8
                size_hint_y: None
                height: self.minimum_height

        Button:
            text: "بازگشت"
            size_hint_y: None
            height: 48
            on_release: app.root.current = "home"

<Resolutions>:
    name: "resolutions"
    BoxLayout:
        orientation: "vertical"
        padding: 12
        spacing: 10

        Label:
            text: "مصوبات جلسات"
            font_size: "23sp"

        ScrollView:
            GridLayout:
                id: resolution_list
                cols: 1
                spacing: 8
                size_hint_y: None
                height: self.minimum_height

        Button:
            text: "ثبت مصوبه جدید"
            size_hint_y: None
            height: 50
            on_release: app.new_resolution()

        Button:
            text: "بازگشت"
            size_hint_y: None
            height: 48
            on_release: app.root.current = "home"
"""

class Dashboard(Screen):
    pass

class Activities(Screen):
    pass

class Resolutions(Screen):
    pass

class HSEEApp(App):

    def build(self):
        self.init_db()
        self.title = "HSEE Mobile"
        Window.clearcolor = (0.035, 0.07, 0.14, 1)
        root = Builder.load_string(KV)
        self.load_activities()
        self.load_resolutions()
        return root

    def init_db(self):
        with sqlite3.connect(DB) as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    description TEXT,
                    status TEXT,
                    created TEXT
                )
            """)
            db.execute("""
                CREATE TABLE IF NOT EXISTS resolutions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    description TEXT,
                    created TEXT
                )
            """)

    def new_activity(self):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.textinput import TextInput

        box = BoxLayout(orientation="vertical", padding=10, spacing=8)
        title = TextInput(hint_text="موضوع فعالیت", multiline=False)
        desc = TextInput(hint_text="شرح فعالیت")
        from kivy.uix.button import Button
        save = Button(text="ذخیره فعالیت", size_hint_y=None, height=45)

        box.add_widget(title)
        box.add_widget(desc)
        box.add_widget(save)

        popup = Popup(title="ثبت فعالیت جدید", content=box,
                      size_hint=(0.9, 0.65))

        def save_item(instance):
            if not title.text.strip():
                return
            with sqlite3.connect(DB) as db:
                db.execute(
                    "INSERT INTO activities VALUES (NULL,?,?,?,?)",
                    (title.text, desc.text, "جدید",
                     datetime.now().strftime("%Y-%m-%d %H:%M"))
                )
            popup.dismiss()
            self.load_activities()

        save.bind(on_release=save_item)
        popup.open()

    def load_activities(self):
        screen = self.root.get_screen("activities")
        layout = screen.ids.activity_list
        layout.clear_widgets()

        with sqlite3.connect(DB) as db:
            rows = db.execute(
                "SELECT id,title,description,status FROM activities ORDER BY id DESC"
            ).fetchall()

        from kivy.uix.button import Button
        for row in rows:
            item = Button(
                text=f"{row[0]} - {row[1]}\\n{row[2]}\\nوضعیت: {row[3]}",
                size_hint_y=None,
                height=95
            )
            layout.add_widget(item)

    def new_resolution(self):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button

        box = BoxLayout(orientation="vertical", padding=10, spacing=8)
        title = TextInput(hint_text="عنوان مصوبه", multiline=False)
        desc = TextInput(hint_text="شرح مصوبه")
        save = Button(text="ذخیره", size_hint_y=None, height=45)
        box.add_widget(title)
        box.add_widget(desc)
        box.add_widget(save)

        popup = Popup(title="ثبت مصوبه", content=box,
                      size_hint=(0.9, 0.65))

        def save_item(instance):
            if not title.text.strip():
                return
            with sqlite3.connect(DB) as db:
                db.execute(
                    "INSERT INTO resolutions VALUES (NULL,?,?,?)",
                    (title.text, desc.text,
                     datetime.now().strftime("%Y-%m-%d %H:%M"))
                )
            popup.dismiss()
            self.load_resolutions()

        save.bind(on_release=save_item)
        popup.open()

    def load_resolutions(self):
        screen = self.root.get_screen("resolutions")
        layout = screen.ids.resolution_list
        layout.clear_widgets()

        with sqlite3.connect(DB) as db:
            rows = db.execute(
                "SELECT id,title,description FROM resolutions ORDER BY id DESC"
            ).fetchall()

        from kivy.uix.button import Button
        for row in rows:
            layout.add_widget(Button(
                text=f"{row[0]} - {row[1]}\\n{row[2]}",
                size_hint_y=None,
                height=85
            ))

    def statistics(self):
        with sqlite3.connect(DB) as db:
            count = db.execute(
                "SELECT COUNT(*) FROM activities"
            ).fetchone()[0]

        Popup(
            title="آمار سامانه",
            content=Label(text=f"تعداد فعالیت‌های ثبت‌شده: {count}"),
            size_hint=(0.8, 0.35)
        ).open()


if __name__ == "__main__":
    HSEEApp().run()
