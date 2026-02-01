from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# 🔹 MongoDB Connection
MONGO_URI = "mongodb+srv://balajisamala679_db_user:Mongo123@cluster0.kbkwms9.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["github_webhooks"]
collection = db["events"]

# 🔹 Home page (UI)
@app.route("/")
def home():
    return render_template("index.html")

# 🔹 Webhook receiver
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    event_type = request.headers.get("X-GitHub-Event")

    if event_type == "push":
        event = {
            "type": "push",
            "author": data["pusher"]["name"],
            "to_branch": data["ref"].split("/")[-1],
            "timestamp": datetime.utcnow()
        }
        collection.insert_one(event)

    return jsonify({"status": "ok"}), 200

# 🔹 API for UI (polls every 15s)
@app.route("/events")
def get_events():
    events = list(
        collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(10)
    )

    for e in events:
        e["timestamp"] = e["timestamp"].strftime("%d %b %Y %I:%M %p UTC")

    return jsonify(events)

if __name__ == "__main__":
    app.run(debug=True)
