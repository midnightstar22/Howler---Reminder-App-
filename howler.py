import webview
import json
import threading
import time
import pyttsx3
from datetime import datetime, timedelta
import os

class HowlerAPI:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.reminder_file = "reminders.json"
        self.setup_tts_engine()

    def setup_tts_engine(self):
        try:
            voices = self.engine.getProperty('voices')
            if voices:
                self.engine.setProperty('voice', voices[0].id)
            self.engine.setProperty('rate', 170)
            self.engine.setProperty('volume', 1.0)
        except Exception as e:
            print(f"Error setting up TTS engine: {e}")

    def send_howler(self, message, speed=170, volume=1.0, voice_index=0):
        try:
            self.engine.setProperty('rate', int(speed))
            self.engine.setProperty('volume', float(volume))
            voices = self.engine.getProperty('voices')
            if voices and int(voice_index) < len(voices):
                self.engine.setProperty('voice', voices[int(voice_index)].id)
            self.engine.say(message)
            self.engine.runAndWait()
            return {"status": "success", "message": "Howler sent!"}
        except Exception as e:
            print(f"Error sending howler: {e}")
            return {"status": "error", "message": str(e)}

    def load_reminders(self):
        try:
            if os.path.exists(self.reminder_file):
                with open(self.reminder_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading reminders: {e}")
            return []

    def save_reminders(self, reminders):
        try:
            with open(self.reminder_file, 'w') as f:
                json.dump(reminders, f, indent=2)
            return {"status": "success"}
        except Exception as e:
            print(f"Error saving reminders: {e}")
            return {"status": "error", "message": str(e)}

    def add_reminder(self, title, date):
        try:
            reminders = self.load_reminders()
            reminder = {
                "id": int(time.time() * 1000),
                "title": title,
                "date": date,
                "completed": False,
                "completedAt": None,
                "last_howl_time": None,
                "last_today_howl": None,
                "last_overdue_howl": None
            }
            reminders.append(reminder)
            result = self.save_reminders(reminders)
            if result["status"] == "success":
                return {"status": "success", "reminder": reminder}
            return result
        except Exception as e:
            print(f"Error adding reminder: {e}")
            return {"status": "error", "message": str(e)}

    def complete_reminder(self, reminder_id):
        try:
            reminders = self.load_reminders()
            for reminder in reminders:
                if reminder.get('id') == reminder_id:
                    reminder["completed"] = True
                    reminder["completedAt"] = datetime.now().isoformat()
                    break
            return self.save_reminders(reminders)
        except Exception as e:
            print(f"Error completing reminder: {e}")
            return {"status": "error", "message": str(e)}

    def uncomplete_reminder(self, reminder_id):
        try:
            reminders = self.load_reminders()
            for reminder in reminders:
                if reminder.get('id') == reminder_id:
                    reminder["completed"] = False
                    reminder["completedAt"] = None
                    break
            return self.save_reminders(reminders)
        except Exception as e:
            print(f"Error uncompleting reminder: {e}")
            return {"status": "error", "message": str(e)}

    def clear_completed_reminders(self):
        try:
            reminders = self.load_reminders()
            active_reminders = [r for r in reminders if not r.get("completed", False)]
            return self.save_reminders(active_reminders)
        except Exception as e:
            print(f"Error clearing completed reminders: {e}")
            return {"status": "error", "message": str(e)}

    def get_reminders(self):
        return self.load_reminders()

    def delete_reminder(self, reminder_id):
        try:
            reminders = self.load_reminders()
            original_count = len(reminders)
            reminders = [r for r in reminders if r.get('id') != reminder_id]
            if len(reminders) < original_count:
                result = self.save_reminders(reminders)
                if result["status"] == "success":
                    return {"status": "success", "message": "Reminder deleted"}
                return result
            else:
                return {"status": "error", "message": "Reminder not found"}
        except Exception as e:
            print(f"Error deleting reminder: {e}")
            return {"status": "error", "message": str(e)}

    def check_due_reminders(self):
        try:
            reminders = self.load_reminders()
            today = datetime.now().date()
            tomorrow = today + timedelta(days=1)
            current_time = datetime.now()
            print(f"🔍 Checking reminders at {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"📅 Today: {today}, Tomorrow: {tomorrow}")
            print(f"📊 Total reminders to check: {len(reminders)}")
            reminders_to_update = []
            for i, reminder in enumerate(reminders):
                print(f"\n--- Processing reminder {i + 1}/{len(reminders)} ---")
                print(f"📋 Reminder: '{reminder['title']}' (ID: {reminder.get('id', 'No ID')})")
                print(f"📅 Due date: {reminder['date']}")
                print(f"✅ Completed: {reminder.get('completed', False)}")
                if reminder.get("completed", False):
                    print("⏭️ Skipping completed reminder")
                    continue
                try:
                    due_date = datetime.strptime(reminder["date"], "%Y-%m-%d").date()
                    print(f"🎯 Parsed due date: {due_date}")
                    if due_date == tomorrow:
                        print("⏰ This is a TOMORROW reminder")
                        last_howl_time = reminder.get("last_howl_time")
                        print(f"🕐 Last howl time: {last_howl_time}")
                        should_howl = False
                        if 8 <= current_time.hour <= 22:
                            print(f"🕒 Current hour {current_time.hour} is within active hours (8-22)")
                            if not last_howl_time:
                                should_howl = True
                                print(f"🆕 First tomorrow alert for: {reminder['title']}")
                            else:
                                try:
                                    last_howl = datetime.fromisoformat(last_howl_time)
                                    time_diff = (current_time - last_howl).total_seconds() / 60
                                    print(f"⏱️ Time since last howl: {time_diff:.1f} minutes")
                                    if time_diff >= 30:
                                        should_howl = True
                                        print(f"✅ 30min interval passed for: {reminder['title']}")
                                    else:
                                        print(f"⏳ Too soon for: {reminder['title']} (need {30 - time_diff:.1f} more minutes)")
                                except ValueError as e:
                                    print(f"❌ Error parsing last_howl_time: {e}")
                                    should_howl = True
                        else:
                            print(f"🌙 Current hour {current_time.hour} is outside active hours (8-22)")
                        if should_howl:
                            message = f"REMINDER! {reminder['title']} is due TOMORROW!"
                            print(f"🔊 SENDING tomorrow howler: {message}")
                            try:
                                howler_result = self.send_howler(message)
                                print(f"📢 Howler result: {howler_result}")
                                reminder["last_howl_time"] = current_time.isoformat()
                                reminders_to_update.append(i)
                                print(f"✅ Tomorrow reminder sent successfully: {reminder['title']}")
                            except Exception as howler_error:
                                print(f"❌ Error sending howler for {reminder['title']}: {howler_error}")
                        else:
                            print(f"⏸️ Not sending howler for: {reminder['title']}")
                    elif due_date == today:
                        print("🚨 This is a TODAY reminder")
                        last_today_howl = reminder.get("last_today_howl")
                        print(f"🕐 Last today howl: {last_today_howl}")
                        should_howl_today = False
                        if 7 <= current_time.hour <= 23:
                            print(f"🕒 Current hour {current_time.hour} is within active hours (7-23)")
                            if not last_today_howl:
                                should_howl_today = True
                                print(f"🆕 First today alert for: {reminder['title']}")
                            else:
                                try:
                                    last_howl = datetime.fromisoformat(last_today_howl)
                                    time_diff = (current_time - last_howl).total_seconds() / 60
                                    print(f"⏱️ Time since last today howl: {time_diff:.1f} minutes")
                                    if time_diff >= 15:
                                        should_howl_today = True
                                        print(f"✅ 15min interval passed for: {reminder['title']}")
                                    else:
                                        print(f"⏳ Too soon for: {reminder['title']} (need {15 - time_diff:.1f} more minutes)")
                                except ValueError as e:
                                    print(f"❌ Error parsing last_today_howl: {e}")
                                    should_howl_today = True
                        else:
                            print(f"🌙 Current hour {current_time.hour} is outside active hours (7-23)")
                        if should_howl_today:
                            message = f"URGENT! {reminder['title']} is due TODAY!"
                            print(f"🔊 SENDING today howler: {message}")
                            try:
                                howler_result = self.send_howler(message)
                                print(f"📢 Howler result: {howler_result}")
                                reminder["last_today_howl"] = current_time.isoformat()
                                reminders_to_update.append(i)
                                print(f"✅ Today reminder sent successfully: {reminder['title']}")
                            except Exception as howler_error:
                                print(f"❌ Error sending howler for {reminder['title']}: {howler_error}")
                        else:
                            print(f"⏸️ Not sending today howler for: {reminder['title']}")
                    elif due_date < today:
                        print("⚠️ This is an OVERDUE reminder")
                        last_overdue_howl = reminder.get("last_overdue_howl")
                        print(f"🕐 Last overdue howl: {last_overdue_howl}")
                        should_howl_overdue = False
                        if 8 <= current_time.hour <= 20:
                            print(f"🕒 Current hour {current_time.hour} is within active hours (8-20)")
                            if not last_overdue_howl:
                                should_howl_overdue = True
                                print(f"🆕 First overdue alert for: {reminder['title']}")
                            else:
                                try:
                                    last_howl = datetime.fromisoformat(last_overdue_howl)
                                    time_diff = (current_time - last_howl).total_seconds() / 60
                                    print(f"⏱️ Time since last overdue howl: {time_diff:.1f} minutes")
                                    if time_diff >= 60:
                                        should_howl_overdue = True
                                        print(f"✅ 60min interval passed for: {reminder['title']}")
                                    else:
                                        print(f"⏳ Too soon for: {reminder['title']} (need {60 - time_diff:.1f} more minutes)")
                                except ValueError as e:
                                    print(f"❌ Error parsing last_overdue_howl: {e}")
                                    should_howl_overdue = True
                        else:
                            print(f"🌙 Current hour {current_time.hour} is outside active hours (8-20)")
                        if should_howl_overdue:
                            days_overdue = (today - due_date).days
                            message = f"OVERDUE! {reminder['title']} was due {days_overdue} day{'s' if days_overdue > 1 else ''} ago!"
                            print(f"🔊 SENDING overdue howler: {message}")
                            try:
                                howler_result = self.send_howler(message)
                                print(f"📢 Howler result: {howler_result}")
                                reminder["last_overdue_howl"] = current_time.isoformat()
                                reminders_to_update.append(i)
                                print(f"✅ Overdue reminder sent successfully: {reminder['title']}")
                            except Exception as howler_error:
                                print(f"❌ Error sending howler for {reminder['title']}: {howler_error}")
                        else:
                            print(f"⏸️ Not sending overdue howler for: {reminder['title']}")
                    else:
                        print(f"📅 Reminder is for future date: {due_date}")
                except Exception as e:
                    print(f"❌ Error processing reminder {reminder.get('title', 'Unknown')}: {e}")
                    print(f"📄 Reminder data: {reminder}")
                    continue
            if reminders_to_update:
                print(f"\n💾 Saving updated reminders... ({len(reminders_to_update)} updated)")
                save_result = self.save_reminders(reminders)
                print(f"💾 Save result: {save_result}")
            else:
                print("\nℹ️ No reminders sent this check")
        except Exception as e:
            print(f"❌ Critical error in check_due_reminders: {e}")
            import traceback
            traceback.print_exc()

    def get_available_voices(self):
        try:
            voices = self.engine.getProperty('voices')
            voice_list = []
            for i, voice in enumerate(voices):
                voice_info = {
                    "index": i,
                    "name": voice.name if hasattr(voice, 'name') else f"Voice {i + 1}",
                    "id": voice.id
                }
                voice_list.append(voice_info)
            return voice_list
        except Exception as e:
            print(f"Error getting voices: {e}")
            return [{"index": 0, "name": "Default Voice", "id": "default"}]

def reminder_checker_thread(api):
    while True:
        try:
            api.check_due_reminders()
            time.sleep(60)
        except Exception as e:
            print(f"Error in reminder checker: {e}")
            time.sleep(60)

def create_app():
    api = HowlerAPI()
    checker_thread = threading.Thread(target=reminder_checker_thread, args=(api,), daemon=True)
    checker_thread.start()
    html_file = "howler_app.html"
    if not os.path.exists(html_file):
        print(f"HTML file '{html_file}' not found!")
        print("Please save the HTML content to 'howler_app.html' file")
        return None
    try:
        window = webview.create_window(
            title="🔥 Weasley Howler Reminder App 🔥",
            url=html_file,
            js_api=api,
            width=640,
            height=800,
            min_size=(500, 600),
            resizable=True
        )
        return window
    except Exception as e:
        print(f"Error creating webview window: {e}")
        return None

def main():
    try:
        window = create_app()
        if window:
            webview.start(debug=False)
        else:
            print("Failed to create application window")
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Error running application: {e}")

if __name__ == "__main__":
    try:
        import webview
        import pyttsx3
        print("Starting Howler Reminder App...")
        main()
    except ImportError as e:
        print(f"Missing required module: {e}")
        print("Please install required packages:")
        print("pip install pywebview pyttsx3")