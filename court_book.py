#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import argparse
import sys

# --- ARGUMENT PARSING ---
parser = argparse.ArgumentParser(description="Book a UCI court for a specific day.")
parser.add_argument(
    'day_to_book',
    type=str,
    nargs='?',
    default='day-after',
    choices=['today', 'tomorrow', 'day-after'],
    help="Specify booking day: 'today', 'tomorrow', or 'day-after'. Defaults to 'day-after'."
)
parser.add_argument(
    '-n', '--num-bookings',
    type=int,
    default=2,
    choices=[1, 2],
    help='Number of slots to book (default: 2).'
)
args = parser.parse_args()

load_dotenv()
uci_id = os.getenv("UCI_ID")
uci_password = os.getenv("UCI_PASSWORD")

# --- Browser Setup ---
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://my.campusrec.uci.edu/booking")
wait = WebDriverWait(driver, 20)

# --- Login and Duo Steps ---
print(">>> Starting Login Process...")
try:
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "container-image-link-item"))).click()
    uci_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-sso-shibboleth")))
    uci_button.click()
    print("🔐 Please complete UCI login and approve Duo request on your phone...")
    wait.until(EC.presence_of_element_located((By.ID, "j_username"))).send_keys(uci_id)
    wait.until(EC.presence_of_element_located((By.ID, "j_password"))).send_keys(uci_password)
    wait.until(EC.element_to_be_clickable((By.NAME, "submit_form"))).click()
    print("🔐 Submitted UCInetID and password.")
    print("📲 Waiting for Duo push approval...")
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.ID, "trust-browser-button"))).click()
    print("🔒 Clicked 'Yes, this is my device'")
    print("✅ Duo approved and dashboard loaded")
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "container-image-link-item"))).click()
    time.sleep(1)
except Exception as e:
    print(f"❌ An error occurred during login: {e}")
    driver.quit()
    sys.exit(1)

# --- Date Selection ---
today = datetime.now()
days_to_add = {'today': 0, 'tomorrow': 1, 'day-after': 2}[args.day_to_book]
target_date = today + timedelta(days=days_to_add)
target_day = target_date.day
print(f"\n>>> Selecting Date: {args.day_to_book.upper()} ({target_date.strftime('%A, %b %d')})")

try:
    target_button_selector = f"div.d-none.d-lg-block button.single-date-select-button[data-day='{target_day}']"
    print(f"🔍 Waiting for the DESKTOP button for day '{target_day}' to become clickable...")
    target_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, target_button_selector)))
    target_button.click()
    print(f"✅ Clicked button for day '{target_day}'.")
    time.sleep(2)
except TimeoutException:
    print(f"❌ Timed out waiting for the date button for the {target_day}th. It may not be available for booking.")
    driver.quit()
    sys.exit(1)

# --- MULTI-BOOKING STRATEGY ---
preferred_times = [
    "6 - 7 PM", "7 - 8 PM", "8 - 8:55 PM", "7 - 8 AM", "11 AM - 12 PM",
    "12 - 1 PM", "9 - 10 AM", "10 - 11 AM"
]

booked_slots_list = []
wait_for_booking = WebDriverWait(driver, 10) 

print("\n>>> PRIORITY PASS: Checking for top 2 preferences for immediate booking...")
top_2_prefs = preferred_times[:2]
facility_buttons = driver.find_elements(By.CSS_SELECTOR, "#tabBookingFacilities button")

for facility_button in facility_buttons:
    if len(booked_slots_list) >= args.num_bookings:
        print("--- Desired number of bookings reached during priority pass.")
        break
    try:
        driver.execute_script("arguments[0].click();", facility_button)
        facility_name = facility_button.text.strip()
        print(f"--- Scanning facility for priority slots: {facility_name}...")
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "booking-slot-item")))
        for pref_time in top_2_prefs:
            if len(booked_slots_list) >= args.num_bookings: break
            if pref_time in booked_slots_list: continue
            try:
                xpath_for_button = f"//div[contains(@class, 'booking-slot-item') and .//strong[normalize-space()='{pref_time}']]//button[normalize-space()='Book Now']"
                button_to_click = WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, xpath_for_button)))
                print(f"🎯 Priority slot found! Attempting to book '{pref_time}' on '{facility_name}'.")
                button_to_click.click()
                print("   -> Waiting for booking confirmation...")
                wait_for_booking.until(EC.staleness_of(button_to_click))
                print(f"✅ Slot {len(booked_slots_list) + 1}/{args.num_bookings} booked successfully: {pref_time}")
                booked_slots_list.append(pref_time)
            except TimeoutException:
                pass
            except Exception as e:
                print(f"⚠️ An error occurred while trying to book priority slot '{pref_time}': {e}")
    except Exception as e:
        print(f"⚠️ An error occurred while scanning a facility during priority pass: {e}")
        continue

if len(booked_slots_list) < args.num_bookings:
    print(f"\n>>> Priority pass complete. Booked {len(booked_slots_list)} slot(s).")
    print(f">>> Proceeding to standard scan to fulfill remaining {args.num_bookings - len(booked_slots_list)} booking(s).")
    print("\n>>> PASS 1: Gathering all remaining available slots from all facilities...")
    available_slots_info = {}
    facility_buttons = driver.find_elements(By.CSS_SELECTOR, "#tabBookingFacilities button")

    for facility_button in facility_buttons:
        try:
            driver.execute_script("arguments[0].click();", facility_button)
            facility_name = facility_button.text.strip()
            print(f"--- Scanning facility: {facility_name}...")
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "booking-slot-item")))
            slots_on_page = driver.find_elements(By.CLASS_NAME, "booking-slot-item")
            for slot in slots_on_page:
                book_button = slot.find_element(By.CSS_SELECTOR, "button")
                if book_button.text.strip().upper() == 'BOOK NOW':
                    time_label = slot.find_element(By.CSS_SELECTOR, "p > strong").text.strip()
                    if time_label not in booked_slots_list and time_label not in available_slots_info:
                        available_slots_info[time_label] = facility_name
                        print(f"    -> Found available slot: '{time_label}' on '{facility_name}'")
        except Exception as e:
            print(f"⚠️ An error occurred while scanning a facility: {e}")
            continue

    print(f"\n>>> PASS 2: Analyzing remaining slots to book up to {args.num_bookings} total slot(s)...")
    while len(booked_slots_list) < args.num_bookings:
        best_slot_to_book = None
        for pref_time in preferred_times:
            if pref_time in available_slots_info:
                best_slot_to_book = pref_time
                break
        if not best_slot_to_book:
            print("--- No more available slots match your preferences.")
            break
        target_facility_name = available_slots_info[best_slot_to_book]
        print(f"🎯 Top preference found! Attempting to book '{best_slot_to_book}' on '{target_facility_name}'.")
        try:
            all_facility_tabs = driver.find_elements(By.CSS_SELECTOR, "#tabBookingFacilities button")
            for tab in all_facility_tabs:
                if tab.text.strip() == target_facility_name:
                    driver.execute_script("arguments[0].click();", tab)
                    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "booking-slot-item")))
                    break
            xpath_for_button = f"//div[contains(@class, 'booking-slot-item') and .//strong[normalize-space()='{best_slot_to_book}']]//button[normalize-space()='Book Now']"
            button_to_click = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_for_button)))
            button_to_click.click()
            print("   -> Waiting for booking confirmation...")
            wait_for_booking.until(EC.staleness_of(button_to_click))
            print(f"✅ Slot {len(booked_slots_list) + 1}/{args.num_bookings} booked successfully: {best_slot_to_book}")
            booked_slots_list.append(best_slot_to_book)
            del available_slots_info[best_slot_to_book]
        except Exception as e:
            print(f"❌ Failed to book the slot for '{best_slot_to_book}'. Error: {e}")
            del available_slots_info[best_slot_to_book]
            continue
else:
    print("\n>>> All desired bookings were fulfilled during the priority pass.")

print("\n--------------------")
print("Booking Summary:")
if booked_slots_list:
    print(f"✅ Successfully booked {len(booked_slots_list)} slot(s):")
    for t in booked_slots_list:
        print(f"  - {t}")
else:
    print("❌ No slots matching your preferences were found available.")
print("--------------------")

print("Script finished. Closing browser.")
driver.quit()
if booked_slots_list:
    sys.exit(0)
else:
    sys.exit(1)
