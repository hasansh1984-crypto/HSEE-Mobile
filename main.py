
import os
import sqlite3
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


KV = """
ScreenManager:
    Dashboard:
    Activities:
    Resolutions:

<Dashboard>:
    name: "home"

    BoxLayout:
        orientation: "vertical"
        padding: 18
        spacing: 14

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
            color: 0.9, 0.92, 1, 1
            size_hint_y: None
            height: 75

        Label:
            text: "شرکت شهرک‌های صنعتی لرستان"
            font_size: "17sp"
            size_hint_y: None
            height: 45

        Button:
            text: "کارتابل فعالیت‌ها"
            size_hint_y: None
            height: 65
            on_release: app.root.current = "activities"

        Button:
            text: "مصوبات جلسات"
            size_hint_y: None
            height: 65
            on_release: app.root.current = "resolutions"

        Button:
            text: "ثبت فعالیت جدید"
            size_hint_y: None
            height: 65
            on_release: app.new_activity()

        Button:
            text: "آمار سامانه"
            size_hint_y: None
            height: 65
            on_release: app.statistics()

        Widget:

        Label:
            text: "نسخه مستقل آفلاین HSEE"
            size_hint_y: None
            height: 40


<Activities>:
    name: "activities"

    BoxLayout:
        orientation: "vertical"
        padding: 12
        spacing: 10

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
            text: "ثبت فعالیت جدید"
            size_hint_y: None
            height: 55
            on_release: app.new_activity()

        Button:
            text: "بازگشت"
            size_hint_y: None
            height: 50
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
            size_hint_y: None
            height: 55

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
            height: 55
            on_release: app.new_resolution()

        Button:
            text: "بازگشت"
            size_hint_y: None
            height: 50
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
        self.title = "HSEE Mobile"
        Window.clearcolor = (0.035, 0.07, 0.14, 1)

        # محل امن ذخیره اطلاعات در اندروید
        self.db_path = os.path.join(
            self.user_data_dir,
            "hsee.db"
        )

        self.init_db()

        root = Builder.load_string(KV)

        self.load_activities()
        self.load_resolutions()

        return root

    def connect_db(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.connect_db() as db:

            db.execute("""
                CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT,
                    created TEXT
                )
            """)

            db.execute("""
                CREATE TABLE IF NOT EXISTS resolutions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    created TEXT
                )
            """)

    def show_message(self, title, message):
        Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.85, 0.35)
        ).open()

    def new_activity(self):

        box = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=10
        )

        title = TextInput(
            hint_text="موضوع فعالیت",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        description = TextInput(
            hint_text="شرح فعالیت",
            multiline=True
        )

        save = Button(
            text="ذخیره فعالیت",
            size_hint_y=None,
            height=50
        )

        box.add_widget(title)
        box.add_widget(description)
        box.add_widget(save)

        popup = Popup(
            title="ثبت فعالیت جدید",
            content=box,
            size_hint=(0.92, 0.7)
        )

        def save_item(instance):

            if not title.text.strip():
                self.show_message(
                    "خطا",
                    "موضوع فعالیت را وارد کنید."
                )
                return

            with self.connect_db() as db:
                db.execute(
                    """
                    INSERT INTO activities
                    (title, description, status, created)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        title.text.strip(),
                        description.text.strip(),
                        "جدید",
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M"
                        )
                    )
                )

            popup.dismiss()
            self.load_activities()
            self.show_message(
                "ثبت موفق",
                "فعالیت ذخیره شد."
            )

        save.bind(on_release=save_item)
        popup.open()

    def load_activities(self):

        if not self.root:
            return

        layout = self.root.get_screen(
            "activities"
        ).ids.activity_list

        layout.clear_widgets()

        with self.connect_db() as db:
            rows = db.execute(
                """
                SELECT id, title, description,
                       status, created
                FROM activities
                ORDER BY id DESC
                """
            ).fetchall()

        for row in rows:

            item = Button(
                text=(
                    f"{row[0]} - {row[1]}\n"
                    f"{row[2]}\n"
                    f"وضعیت: {row[3]}\n"
                    f"تاریخ: {row[4]}"
                ),
                size_hint_y=None,
                height=115
            )

            layout.add_widget(item)

    def new_resolution(self):

        box = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=10
        )

        title = TextInput(
            hint_text="عنوان مصوبه",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        description = TextInput(
            hint_text="شرح مصوبه"
        )

        save = Button(
            text="ذخیره مصوبه",
            size_hint_y=None,
            height=50
        )

        box.add_widget(title)
        box.add_widget(description)
        box.add_widget(save)

        popup = Popup(
            title="ثبت مصوبه جدید",
            content=box,
            size_hint=(0.92, 0.7)
        )

        def save_item(instance):

            if not title.text.strip():
                self.show_message(
                    "خطا",
                    "عنوان مصوبه را وارد کنید."
                )
                return

            with self.connect_db() as db:
                db.execute(
                    """
                    INSERT INTO resolutions
                    (title, description, created)
                    VALUES (?, ?, ?)
                    """,
                    (
                        title.text.strip(),
                        description.text.strip(),
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M"
                        )
                    )
                )

            popup.dismiss()
            self.load_resolutions()
            self.show_message(
                "ثبت موفق",
                "مصوبه ذخیره شد."
            )

        save.bind(on_release=save_item)
        popup.open()

    def load_resolutions(self):

        if not self.root:
            return

        layout = self.root.get_screen(
            "resolutions"
        ).ids.resolution_list

        layout.clear_widgets()

        with self.connect_db() as db:
            rows = db.execute(
                """
                SELECT id, title, description, created
                FROM resolutions
                ORDER BY id DESC
                """
            ).fetchall()

        for row in rows:

            item = Button(
                text=(
                    f"{row[0]} - {row[1]}\n"
                    f"{row[2]}\n"
                    f"تاریخ: {row[3]}"
                ),
                size_hint_y=None,
                height=100
            )

            layout.add_widget(item)

    def statistics(self):

        with self.connect_db() as db:

            activities = db.execute(
                "SELECT COUNT(*) FROM activities"
            ).fetchone()[0]

            resolutions = db.execute(
                "SELECT COUNT(*) FROM resolutions"
            ).fetchone()[0]

        self.show_message(
            "آمار سامانه",
            f"تعداد فعالیت‌ها: {activities}\n"
            f"تعداد مصوبات: {resolutions}"
        )


if __name__ == "__main__":
    HSEEApp().run()
