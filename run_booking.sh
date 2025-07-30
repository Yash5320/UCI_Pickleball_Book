#!/bin/bash

# Navigate to the script's directory to ensure all relative paths work
cd /home/pain/Scripts/pickleball_booking_cron || exit 1

# Define the path to the notification script for cleaner code
NOTIFY_SCRIPT="/home/pain/Scripts/cron-notify.sh"
LOG_FILE="/home/pain/Scripts/pickleball_booking_cron/cron.log"
PYTHON_EXEC="/home/pain/Scripts/pickleball_booking_cron/myenv/bin/python"
PYTHON_SCRIPT="court_book.py"

# 1. Send the initial notification to approve Duo
"$NOTIFY_SCRIPT" -t 10000 -i "/home/pain/Pictures/avatar.jpg" \
    "Pickleball Booking" "Starting booking process. Check Duo on your phone."

# 2. Run the Python script and capture its output and exit code.
# The output is saved to the log file for debugging.
"$PYTHON_EXEC" "$PYTHON_SCRIPT" > "$LOG_FILE" 2>&1
EXIT_CODE=$? # Capture the exit code of the Python script

# 3. Check the exit code and send a final notification
if [ $EXIT_CODE -eq 0 ]; then
    # SUCCESS (Exit code 0)
    # Grab the last 4 lines from the log for a quick summary
    SUMMARY=$(tail -n 4 "$LOG_FILE")
    "$NOTIFY_SCRIPT" -i "dialog-ok-apply" "✅ Booking Succeeded" "$SUMMARY"
else
    # FAILURE (Any other exit code)
    # Grab the last 4 lines which likely contain the error message
    ERROR_INFO=$(tail -n 4 "$LOG_FILE")
    "$NOTIFY_SCRIPT" -i "dialog-error" "❌ Booking Failed" "$ERROR_INFO"
fi

exit 0
