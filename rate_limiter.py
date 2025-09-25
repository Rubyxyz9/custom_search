# rate_limiter.py
import json
import os
import time

USAGE_FILE = ".api_usage.json"
DAILY_LIMIT = 100
SECONDS_IN_DAY = 24 * 60 * 60

def get_usage_data():
    """Reads usage data, creating a new file if one doesn't exist."""
    if not os.path.exists(USAGE_FILE):
        return {"last_reset_timestamp": time.time(), "requests_made": 0}
    try:
        with open(USAGE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"last_reset_timestamp": time.time(), "requests_made": 0}

def save_usage_data(data):
    """Saves the current usage data to its file."""
    with open(USAGE_FILE, "w") as f:
        json.dump(data, f)

def check_and_update_limit():
    """Checks if the API limit has been reached and resets the counter if 24 hours have passed."""
    data = get_usage_data()
    current_time = time.time()

    if current_time - data["last_reset_timestamp"] > SECONDS_IN_DAY:
        print("ℹ️  24-hour period has passed. Resetting API request limit.")
        data["last_reset_timestamp"] = current_time
        data["requests_made"] = 0
        save_usage_data(data)

    if data["requests_made"] >= DAILY_LIMIT:
        remaining_time = SECONDS_IN_DAY - (current_time - data["last_reset_timestamp"])
        hours, rem = divmod(remaining_time, 3600)
        minutes, _ = divmod(rem, 60)
        print(f"❌ API Limit Reached ({data['requests_made']}/{DAILY_LIMIT}). Resets in {int(hours)}h {int(minutes)}m.")
        return False
    return True

def increment_usage():
    """Increments the request counter."""
    data = get_usage_data()
    data["requests_made"] += 1
    save_usage_data(data)
    print(f"   (API Usage: {data['requests_made']}/{DAILY_LIMIT})")

def get_remaining_requests():
    """Returns the number of requests left in the current 24-hour window."""
    data = get_usage_data()
    if time.time() - data["last_reset_timestamp"] > SECONDS_IN_DAY:
        return DAILY_LIMIT
    return DAILY_LIMIT - data["requests_made"]
