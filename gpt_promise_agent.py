import requests, datetime, json, uuid

API_URL = "http://127.0.0.1:8000/promises/update"

def create_promise(context, description, owner="GPT-5", partner="Perplexity", relevance="high"):
    new_promise = {
        "id": f"promise_{uuid.uuid4().hex[:6]}",
        "context": context,
        "owner": owner,
        "partner": partner,
        "description": description,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "last_checked": datetime.datetime.utcnow().isoformat() + "Z",
        "deadline": "",
        "condition": "auto_created == True",
        "status": "open",
        "relevance": relevance,
        "notes": "Automatisch durch GPT-5 erstellt.",
        "last_action_by": owner,
        "history": []
    }
    try:
        res = requests.post(API_URL, json=new_promise)
        print(f"✅ Promise erstellt: {context} | Antwort: {res.json()}")
    except Exception as e:
        print(f"⚠️ Promise konnte nicht erstellt werden: {e}")

def update_promise_status(promise_id, status="done"):
    try:
        update_data = {"id": promise_id, "status": status}
        res = requests.post(API_URL, json=update_data)
        print(f"🔁 Promise {promise_id} → {status} | Antwort: {res.json()}")
    except Exception as e:
        print(f"⚠️ Update fehlgeschlagen: {e}")
