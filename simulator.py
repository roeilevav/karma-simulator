# karma_simulator.py

import os
import random
import string
import time
import threading
import requests

API_URL = os.getenv("KARMA_API_URL", "https://karma-api2-production.up.railway.app")
SIM_USER_COUNT = int(os.getenv("SIM_USER_COUNT", 20))
TRIGGER_SPIKE = os.getenv("TRIGGER_SPIKE", "false").lower() == "true"

users = []

def register_user(user_id, username):
    payload = {
        "user_id": str(user_id),
        "username": username
    }
    try:
        response = requests.post(f"{API_URL}/register", json=payload)
        if response.status_code == 200:
            print(f"✅ Registered {username} (ID {user_id})")
            return True
        else:
            print(f"⚠️ Failed to register {username}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception during registration of {username}: {e}")
        return False


def register_users():
    global users
    print(f"🌀 Karma Simulation Started with {SIM_USER_COUNT} users")
    for i in range(SIM_USER_COUNT):
        user_id = f"sim_user_{i+1}"
        username = f"Sim User {i+1}"
        if register_user(user_id, username):
            users.append(user_id)

def send_random_transaction():
    if len(users) < 2:
        print("⛔ Not enough users to send Karma.")
        return

    sender = random.choice(users)
    receiver = random.choice([u for u in users if u != sender])
    amount = round(random.uniform(1, 5), 2)

    response = requests.post(f"{API_URL}/send", json={
        "sender_id": sender,
        "receiver_id": receiver,
        "amount": amount
    })

    if response.status_code == 200:
        print(f"📤 {sender} sent {amount} Karma to {receiver}")
    else:
        print(f"❌ Failed to send Karma: {response.status_code} — {response.text}")

def run_normal_activity():
    while True:
        send_random_transaction()
        time.sleep(random.randint(60, 300))  # 1–5 minutes

def run_spike():
    print("🔥 Spike mode active: sending burst of transactions")
    for _ in range(30):
        send_random_transaction()
        time.sleep(random.uniform(0.2, 1.0))  # rapid-fire
    print("✅ Spike complete")

if __name__ == "__main__":
    register_users()

    if TRIGGER_SPIKE:
        run_spike()
    else:
        # Run in background thread so Railway doesn't kill it for inactivity
        t = threading.Thread(target=run_normal_activity)
        t.start()
        while True:
            time.sleep(3600)  # keep main thread alive
