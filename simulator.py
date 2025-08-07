import os
import random
import time
import requests

API_URL = os.getenv("KARMA_API_URL", "https://karma-api2-production.up.railway.app")
SIMULATED_USERS = 20
TRIGGER_SPIKE = os.getenv("TRIGGER_SPIKE", "false").lower() == "true"

# Create fake users in memory
users = [f"sim_user_{i+1}" for i in range(SIMULATED_USERS)]

# Generate fake balances (1–42 Karma)
balances = {user: random.randint(1, 42) for user in users}


def send_karma(sender, recipient, amount):
    payload = {
        "from_user": sender,
        "to_user": recipient,
        "amount": amount
    }
    try:
        r = requests.post(f"{API_URL}/send", json=payload)
        if r.status_code == 200:
            print(f"✅ {sender} sent {amount} Karma to {recipient}")
        else:
            print(f"❌ Failed to send Karma: {r.status_code} — {r.text}")
    except Exception as e:
        print(f"⚠️ Error sending Karma: {e}")


def simulate_transaction():
    sender = random.choice(users)
    recipient = random.choice([u for u in users if u != sender])
    max_send = balances[sender]
    if max_send < 1:
        return  # Skip if sender has no Karma
    amount = random.randint(1, max_send)

    send_karma(sender, recipient, amount)
    balances[sender] -= amount
    balances[recipient] += amount


def simulate_spike():
    print("\n🚀 Triggering Karma activity spike!")
    for _ in range(random.randint(10, 20)):
        simulate_transaction()


def run_forever():
    print(f"\n🌀 Karma Simulation Started with {SIMULATED_USERS} users")
    while True:
        # Decide whether to spike or do a normal transaction
        if TRIGGER_SPIKE:
            simulate_spike()
        else:
            simulate_transaction()

        # Sleep a bit (simulate few tx/hr)
        time.sleep(random.randint(60, 300))  # 1–5 minutes


if __name__ == "__main__":
    run_forever()
