import json
import random
import datetime

# Active and history file paths
ACTIVE_FILE = "active_code.json"
HISTORY_FILE = "codes_history.json"

def generate_code():
    return str(random.randint(100000, 999999))  # 6-digit random code

def save_code(code):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save as active code
    with open(ACTIVE_FILE, "w") as f:
        json.dump({"code": code, "time": timestamp}, f)

    # Append to history
    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    history.append({"code": code, "time": timestamp})
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

if __name__ == "__main__":
    code = generate_code()
    save_code(code)
    print(f"✅ Attendance code for this hour: {code}")
