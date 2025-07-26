# UCI Court Booking Bot
A Python script that uses Selenium to automate the process of booking pickleball or tennis courts on the UCI Campus Recreation portal. It is designed to be fast, reliable, and run automatically on a schedule.
Overview
This bot automates the entire court booking process:
Logs into the UCI Campus Recreation portal.
Handles the UCInetID, password, and Duo Push authentication steps.
Navigates to the booking page for a specified day (today, tomorrow, or day-after).
Strategically books one or two courts based on a predefined list of preferred time slots.
Can run in a visible browser for testing or in headless mode for automated execution.
Key Features
Automated Login: Securely handles credentials via an environment file and waits for Duo Push approval.
Strategic Multi-Booking: Books up to two slots based on a user-defined preference list (preferred_times).
Priority Pass: For maximum speed, it first performs a rapid scan to book one of the top two preferred time slots if they are available, before conducting a full scan for other options.
Flexible Scheduling: Command-line arguments allow you to easily specify whether to book for 'today', 'tomorrow', or 'day-after'.
Cross-Platform Automation: Detailed instructions for scheduling the bot on Linux (cron), Windows (Task Scheduler), and macOS (launchd).
Robust & Fast: Replaces fixed time.sleep() delays with intelligent WebDriverWait conditions, making the script faster and more resilient to variations in page load times.
📂 Project Structure
Generated code
/pickleball_booking_cron/
├── myenv/                  # Python virtual environment
├── .env                    # Stores your private credentials (DO NOT COMMIT)
├── .env.example            # Example for the .env file
├── court_book_copy.py      # The main Python script
├── requirements.txt        # List of Python dependencies
├── README.md               # This file
├── run_booking.bat         # (For Windows Task Scheduler)
└── log/                    # Folder for log files
    └── daily_run.log       # General log file
Use code with caution.
⚙️ Installation & Setup
1. Create a Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies.
Generated bash
# Navigate to your project directory
cd /path/to/pickleball_booking_cron

# Create a virtual environment named 'myenv'
python3 -m venv myenv

# Activate the virtual environment
# On Linux/macOS:
source myenv/bin/activate
# On Windows:
myenv\Scripts\activate.bat
Use code with caution.
Bash
2. Install Dependencies
Create a file named requirements.txt with the following content:
Generated code
selenium
webdriver-manager
python-dotenv
Use code with caution.
Then, install these packages using pip:
Generated bash
pip install -r requirements.txt
Use code with caution.
Bash
3. Set Up Environment Variables
This script uses a .env file to securely store your login credentials. Create a file named .env in the project root and add your credentials:
Generated code
UCI_ID="your_ucinet_id"
UCI_PASSWORD="your_password"
Use code with caution.
Security Warning: The .env file contains sensitive information. Never share it or commit it to version control.
🚀 Usage
Make sure your virtual environment is activated before running the script.
Basic Usage
To run the script with all default settings (book 2 slots for the 'day-after-tomorrow'):
Generated bash
python court_book_copy.py
Use code with caution.
Bash
Command-Line Arguments
day_to_book (optional, positional): today, tomorrow, day-after. Default: day-after
-n, --num-bookings (optional, flag): Number of slots to book (1 or 2). Default: 2
Examples
Book 1 slot for tomorrow:
Generated bash
python court_book_copy.py tomorrow -n 1
Use code with caution.
Bash
Book 2 slots for today:
Generated bash
python court_book_copy.py today -n 2
Use code with caution.
Bash
🤖 Automated Daily Execution
To run the script automatically every day, you need to use your operating system's native task scheduler. The core requirements are the same for all systems:
Enable Headless Mode: The script must be configured to run Chrome without a GUI.
Use Absolute Paths: Schedulers run in a minimal environment and don't know your user's PATH.
Set Working Directory: The script needs to run from its project directory to find the .env file.
Enable Logging: Since you won't see any output, redirecting it to a log file is essential.
First, enable headless mode in court_book_copy.py by modifying the "Browser Setup" section:
Generated python
# --- Browser Setup ---
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
Use code with caution.
Python
Next, follow the instructions for your operating system:
A) On Linux (using cron)
B) On Windows (using Task Scheduler)
C) On macOS (using launchd or cron)
A) On Linux (using cron)
Find Absolute Paths: Open a terminal, activate your virtual environment, and run:
Generated bash
which python # Example: /home/your_username/Scripts/pickleball_booking_cron/myenv/bin/python
cd ~/Scripts/pickleball_booking_cron && pwd # Example: /home/your_username/Scripts/pickleball_booking_cron
Use code with caution.
Bash
Create a Log Directory: mkdir -p ~/Scripts/pickleball_booking_cron/log
Edit your Crontab: Open the cron table editor with crontab -e and add the following line, substituting your actual paths:
Generated crontab
# Run the UCI court booker every day at 12:02 AM
02 00 * * * cd /home/your_username/Scripts/pickleball_booking_cron && /home/your_username/Scripts/pickleball_booking_cron/myenv/bin/python court_book_copy.py > /home/your_username/Scripts/pickleball_booking_cron/log/daily_run.log 2>&1
Use code with caution.
Crontab
B) On Windows (using Task Scheduler)
Find Absolute Paths: Open Command Prompt, activate your virtual environment, and run:
Generated cmd
where python :: Example: C:\Users\YourUser\Scripts\pickleball_booking_cron\myenv\Scripts\python.exe
cd C:\Users\YourUser\Scripts\pickleball_booking_cron && echo %cd% :: Example: C:\Users\YourUser\Scripts\pickleball_booking_cron
Use code with caution.
Cmd
Create a Runner Script (run_booking.bat): In your project directory, create this file with your absolute paths:
Generated batch
@echo off
cd "C:\Users\YourUser\Scripts\pickleball_booking_cron"
if not exist "log" mkdir "log"
"C:\Users\YourUser\Scripts\pickleball_booking_cron\myenv\Scripts\python.exe" court_book_copy.py > "log\daily_run.log" 2>&1
Use code with caution.
Batch
Schedule the Task:
Open Task Scheduler.
Click "Create Basic Task..." and follow the wizard:
Name: UCI Court Booker
Trigger: Daily, starting at 12:02:00 AM.
Action: Start a program.
Program/script: Browse to and select your run_booking.bat file.
When you finish, check the box to "Open the Properties dialog...".
In Properties, select "Run whether user is logged on or not" and click OK. You will be prompted for your user password.
C) On macOS (using launchd or cron)
For macOS, launchd is the modern, recommended method as it is more reliable, especially on laptops that may be asleep at the scheduled time.
Recommended Method: launchd
Find Absolute Paths: Open Terminal, activate your virtual environment, and run:
Generated bash
which python # Example: /Users/your_username/Scripts/pickleball_booking_cron/myenv/bin/python
cd ~/Scripts/pickleball_booking_cron && pwd # Example: /Users/your_username/Scripts/pickleball_booking_cron
Use code with caution.
Bash
Create a .plist file: Create the directory mkdir -p ~/Library/LaunchAgents, then create a file at ~/Library/LaunchAgents/com.myname.ucibooker.plist with the following content, substituting your own paths:
Generated xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.myname.ucibooker</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/your_username/Scripts/pickleball_booking_cron/myenv/bin/python</string>
        <string>/Users/your_username/Scripts/pickleball_booking_cron/court_book_copy.py</string>
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
Use code with caution.
Xml
Load the Job: In Terminal, run launchctl load ~/Library/LaunchAgents/com.myname.ucibooker.plist. The job is now scheduled.
Alternative for macOS: cron (Legacy)
Note: This method is not recommended as it will fail to run if your Mac is asleep at the scheduled time.
Find Paths: Follow step 1 from the launchd section.
Edit Crontab: Run crontab -e and add the following line with your paths:
Generated crontab
02 00 * * * cd /Users/your_username/Scripts/pickleball_booking_cron && /Users/your_username/Scripts/pickleball_booking_cron/myenv/bin/python court_book_copy.py > /Users/your_username/Scripts/pickleball_booking_cron/log/daily_run.log 2>&1
Use code with caution.
Crontab
Grant Permissions: You may need to go to System Settings > Privacy & Security > Full Disk Access and grant access to cron (found at /usr/sbin/cron) and your Terminal app.
⚠️ Important Notes
Duo Push: The script waits up to 180 seconds for you to approve the Duo Push notification on your mobile device during the login process.
Website Changes: This script is dependent on the website's structure. If the UCI Campus Rec portal is updated, this script may break and will require maintenance.
Ethical Use: This tool is for personal convenience. Please use it responsibly.
