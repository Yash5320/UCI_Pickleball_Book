# UCI Court Booking Bot
A Python script that uses Selenium to automate the process of booking pickleball or tennis courts on the UCI Campus Recreation portal. It is designed to be fast, reliable, and run automatically on a schedule.
## Overview
This bot automates the entire court booking process:
- Logs into the UCI Campus Recreation portal.
- Handles the UCInetID, password, and Duo Push authentication steps.
- Navigates to the booking page for a specified day (today, tomorrow, or day-after).
- Strategically books one or two courts based on a predefined list of preferred time slots.
- Can run in a visible browser for testing or in headless mode for automated execution.

## Key Features
1. Automated Login: Securely handles credentials via an environment file and waits for Duo Push approval.
2. Strategic Multi-Booking: Books up to two slots based on a user-defined preference list (preferred_times).
3. Priority Pass: For maximum speed, it first performs a rapid scan to book one of the top two preferred time slots if they are available, before conducting a full scan for other options.
4. Flexible Scheduling: Command-line arguments allow you to easily specify whether to book for 'today', 'tomorrow', or 'day-after'.
5. Cross-Platform Automation: Detailed instructions for scheduling the bot on Linux (cron), Windows (Task Scheduler), and macOS (launchd).
6. Robust & Fast: Replaces fixed time.sleep() delays with intelligent WebDriverWait conditions, making the script faster and more resilient to variations in page load times.

## 📂 Project Structure
```
/pickleball_booking_cron/
├── myenv/                  # Python virtual environment
├── .env                    # Example for the .env file
├── court_book.py           # The main Python script
├── requirements.txt        # List of Python dependencies
├── README.md               # This file
├── run_booking.bat         # (For Windows Task Scheduler)
└── log/                    # Folder for log files
    └── daily_run.log       # General log file
```

## ⚙️ Installation & Setup
1. Create a Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies.
2. Navigate to your project directory
```
cd /path/to/pickleball_booking_cron
```
3. Create a virtual environment named 'myenv'
```python3 -m venv myenv```
4. Activate the virtual environment
    * On Linux/macOS:
```source myenv/bin/activate```
    * On Windows:
```myenv\Scripts\activate.bat```

5. Install Dependencies
  - Install the packages in requirements.txt using pip:
```
pip install -r requirements.txt
```

6. Set Up Environment Variables

This script uses a .env file to securely store your login credentials.
Create a file named .env in the project root and add your credentials:
```
UCI_ID="your_ucinet_id"
UCI_PASSWORD="your_password"
```
Security Warning: The .env file contains sensitive information. Never share it or commit it to version control.

## 🚀 Usage
Make sure your virtual environment is activated before running the script.

1. Basic Usage
To run the script with all default settings (book 2 slots for the 'day-after-tomorrow'):
```
python court_book.py
```

2. Command-Line Arguments
    - day_to_book (optional, positional): today, tomorrow, day-after.
        * Default: day-after
    - -n, --num-bookings (optional, flag): Number of slots to book (1 or 2).
        * Default: 2

4. Examples

  - Book 1 slot for tomorrow:
```
python court_book.py tomorrow -n 1
```

  - Book 2 slots for today:
```
python court_book.py today -n 2
```

## 🤖 Automated Daily Execution
To run the script automatically every day, you need to use your operating system's native task scheduler. The core requirements are the same for all systems:
- Enable Headless Mode: The script must be configured to run Chrome without a GUI.
- Use Absolute Paths: Schedulers run in a minimal environment and don't know your user's PATH.
- Set Working Directory: The script needs to run from its project directory to find the .env file.
- Enable Logging: Since you won't see any output, redirecting it to a log file is essential.
First, enable headless mode in court_book.py by modifying the "Browser Setup" section:


### Browser Setup
```
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
```

### a. On Linux (using cron)

  1. Find Absolute Paths: Open a terminal, activate your virtual environment, and run:
```
which python                                # Example: /home/your_username/Scripts/pickleball_booking_cron/myenv/bin/python
cd ~/Scripts/pickleball_booking_cron && pwd # Example: /home/your_username/Scripts/pickleball_booking_cron
```
  2. Create a Log Directory: ```mkdir -p ~/Scripts/pickleball_booking_cron/log```

Edit your Crontab: Open the cron table editor with ```crontab -e``` and add the following line, substituting your actual paths:
```
# Run the UCI court booker every day at 12:02 AM
02 00 * * * cd /home/your_username/Scripts/pickleball_booking_cron && /home/your_username/Scripts/pickleball_booking_cron/myenv/bin/python court_book.py > /home/your_username/Scripts/pickleball_booking_cron/log/daily_run.log 2>&1
```

### b. On Windows (using Task Scheduler)
  
1. Find Absolute Paths: Open Command Prompt, activate your virtual environment, and run:

```
where python                                                      :: Example: C:\Users\YourUser\Scripts\pickleball_booking_cron\myenv\Scripts\python.exe
cd C:\Users\YourUser\Scripts\pickleball_booking_cron && echo %cd% :: Example: C:\Users\YourUser\Scripts\pickleball_booking_cron
```

2. Create a Runner Script (run_booking.bat): In your project directory, create this file with your absolute paths:

```
@echo off
cd "C:\Users\YourUser\Scripts\pickleball_booking_cron"
if not exist "log" mkdir "log"
"C:\Users\YourUser\Scripts\pickleball_booking_cron\myenv\Scripts\python.exe" court_book.py > "log\daily_run.log" 2>&1
```

3. Schedule the Task:
  - Open Task Scheduler.
  - Click "Create Basic Task..." and follow the wizard:

```
Name: UCI Court Booker
Trigger: Daily, starting at 12:02:00 AM.
Action: Start a program.
```

  - Program/script: Browse to and select your run_booking.bat file.
  - When you finish, check the box to "Open the Properties dialog...".
  - In Properties, select "Run whether user is logged on or not" and click OK. You will be prompted for your user password.

### c. On macOS (using launchd)
  - For macOS, launchd is the modern, recommended method as it is more reliable, especially on laptops that may be asleep at the scheduled time.
  - Find Absolute Paths: Open Terminal, activate your virtual environment, and run:

```
which python                                # Example: /Users/your_username/Scripts/pickleball_booking_cron/myenv/bin/python
cd ~/Scripts/pickleball_booking_cron && pwd # Example: /Users/your_username/Scripts/pickleball_booking_cron
```

  - Create a .plist file: Create the directory `mkdir -p ~/Library/LaunchAgents`, then create a file at `~/Library/LaunchAgents/com.myname.ucibooker.plist` with the following content, substituting your own paths:
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.myname.ucibooker</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/your_username/Scripts/pickleball_booking_cron/myenv/bin/python</string>
        <string>/Users/your_username/Scripts/pickleball_booking_cron/court_book.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/your_username/Scripts/pickleball_booking_cron</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>0</integer>
        <key>Minute</key><integer>2</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/your_username/Scripts/pickleball_booking_cron/log/daily_run.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/your_username/Scripts/pickleball_booking_cron/log/daily_run.log</string>
</dict>
</plist>
```
  - Load the Job: In Terminal, run launchctl load `~/Library/LaunchAgents/com.myname.ucibooker.plist`. The job is now scheduled.
## ⚠️ Important Notes
- Duo Push: The script waits up to 180 seconds for you to approve the Duo Push notification on your mobile device during the login process.
- Website Changes: This script is dependent on the website's structure. If the UCI Campus Rec portal is updated, this script may break and will require maintenance.
- Ethical Use: This tool is for personal convenience. Please use it responsibly.
