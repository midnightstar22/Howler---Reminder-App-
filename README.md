# 🔥 Weasley Howler Reminder App

Ever wished someone would yell at you to get things done—just like Mrs. Weasley’s infamous Howler to Ron?  
This app is for you! Inspired by the magical world of Harry Potter, the **Weasley Howler Reminder App** is a desktop reminder tool that *literally* shouts your tasks at you using text-to-speech.

## ✨ Features

- **Magical Howler Reminders:** Get spoken reminders for tasks due today, tomorrow, or overdue—just like a real Howler!
- **Persistent Storage:** Reminders are saved in a JSON file so you never lose your tasks.
- **Customizable Voices:** Choose from available system voices for your Howler.
- **Simple Desktop GUI:** Built with [pywebview](https://pywebview.flowrl.com/) for a clean, cross-platform interface.
- **Background Checking:** Reminders are checked every minute in the background—no need to keep clicking refresh.
- **Mark as Complete/Incomplete:** Stay organized and only get yelled at for what you haven’t finished.

## 🧙‍♂️ Why I Built This

As a huge Harry Potter fan, I always loved the scene where Ron gets a Howler from his mom.  
I also tend to forget my tasks, so I thought: *Why not combine magic and productivity?*  
This app is my way of bringing a bit of Hogwarts into daily life—and making sure I never forget my chores again!

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Install dependencies:
  ```sh
  pip install pywebview pyttsx3
  ```

### Running the App

1. Clone this repository:
    ```sh
    git clone https://github.com/yourusername/weasley-howler-reminder.git
    cd weasley-howler-reminder
    ```
2. Make sure `howler_app.html` is present in the folder (see below).
3. Run the app:
    ```sh
    python howler.py
    ```

### Usage

- Add, complete, or delete reminders from the GUI.
- The app will check your reminders every minute and *yell* at you if something is due soon or overdue.
- Customize the voice and speed in the settings.

## 📝 How It Works

- Uses `pyttsx3` for cross-platform text-to-speech.
- Reminders are stored in `reminders.json`.
- The GUI is powered by `pywebview`.
- A background thread checks reminders and triggers Howlers as needed.

## 🧩 Possible Challenges

- Managing background threads without blocking the GUI.
- Handling text-to-speech on different operating systems.
- Ensuring reminders are not missed or duplicated.
- Making the app fun and magical, but also genuinely useful!

## 📸 Screenshots

*(Add screenshots of your app here!)*

## ⚡️ Inspired By

- [Harry Potter and the Chamber of Secrets](https://harrypotter.fandom.com/wiki/Howler)
- My own need for magical motivation!

## 📜 License

MIT License

---

*“Ronald Weasley! How dare you steal that car!”*  
Now, let your computer do the yelling—so you never forget a task again!
