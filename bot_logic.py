

import csv
from datetime import datetime


clients = {
    "client1": {
        "subscription_end": "2026-12-31",
        "status": "active"
    }
}


def check_subscription(client_id):
    client = clients.get(client_id)

    if not client:
        return False

    if client["status"] != "active":
        return False

    today = datetime.now().date()
    expiry = datetime.strptime(client["subscription_end"], "%Y-%m-%d").date()

    return today <= expiry


def save_lead(client_id, phone, name, student_class):
    filename = f"leads_{client_id}.csv"

    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now(),
            phone,
            name,
            student_class
        ])



sessions = {}

def handle_message(client_id, phone, message):

    if not check_subscription(client_id):
        return "Your subscription has expired. Please renew to continue service."

    if phone not in sessions:
        sessions[phone] = {"step": "ask_class", "data": {}}
        return "Welcome! Which class are you interested in?"

    step = sessions[phone]["step"]

    if step == "ask_class":
        sessions[phone]["data"]["class"] = message
        sessions[phone]["step"] = "ask_name"
        return "Please share your name."

    elif step == "ask_name":
        sessions[phone]["data"]["name"] = message
        
        name = message
        student_class = sessions[phone]["data"]["class"]
        
        save_lead(client_id, phone, name, student_class)

        sessions[phone]["step"] = "complete"
        return f"Thanks {message}! Our team will contact you shortly."


    return "Done."


