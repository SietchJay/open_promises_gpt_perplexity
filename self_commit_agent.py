import requests, datetime, re, json, time, uuid, os

API_URL = "http://127.0.0.1:8000/promises/update"
CHAT_LOG = "chat_transcript.txt"
PENDING_FILE = "pending_promises.json"

# Hilfsfunktion für aktuelle Zeit in UTC
def utc_now():
    return datetime.datetime.now(datetime.UTC).isoformat() + "Z"

# Promise-Erstellung
def create_promise(context, description):
    promise = {
        "id": f"promise_{uuid.uuid4().hex[:6]}",
        "context": context,
        "owner": "GPT-5",
        "partner": "Perplexity",
        "description": description,
        "created_at": utc_now(),
        "last_checked": utc_now(),
        "deadline": "",
        "condition": "auto_created == True",
        "status": "open",
        "relevance": "high",
        "notes": "Automatisch durch GPT-5 erstellt.",
        "last_action_by": "GPT-5",
        "history": []
    }

    try:
        res = requests.post(API_URL, json=promise, timeout=3)
        res.raise_for_status()
        print(f"🟢 Neues Promise erstellt: {context} → Antwort: {res.json()}")
    except Exception as e:
        print(f"⚠️ Server offline – Promise lokal gespeichert: {context}")
        store_pending_promise(promise)

# Lokale Speicherung, falls Server offline
def store_pending_promise(promise):
    if not os.path.exists(PENDING_FILE):
        with open(PENDING_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(PENDING_FILE, "r+", encoding="utf-8") as f:
        data = json.load(f)
        data.append(promise)
        f.seek(0)
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Promise offline zwischengespeichert: {promise['context']}")

# Späterer Upload, wenn Server wieder online
def sync_pending_promises():
    if not os.path.exists(PENDING_FILE):
        return
    try:
        with open(PENDING_FILE, "r", encoding="utf-8") as f:
            pending = json.load(f)
        if not pending:
            return
        print(f"🔄 Versuche, {len(pending)} gespeicherte Promises zu synchronisieren...")
        uploaded = []
        for p in pending:
            res = requests.post(API_URL, json=p, timeout=3)
            if res.status_code == 200:
                uploaded.append(p)
                print(f"✅ Promise synchronisiert: {p['context']}")
        if uploaded:
            # Entferne hochgeladene Einträge
            remaining = [p for p in pending if p not in uploaded]
            with open(PENDING_FILE, "w", encoding="utf-8") as f:
                json.dump(remaining, f, indent=2, ensure_ascii=False)
    except Exception:
        pass  # Wenn immer noch offline → beim nächsten Durchlauf erneut versuchen

# Erkennung von Verpflichtungen
def detect_promises(line):
    if re.search(r"\b(ich\s+werde|ich\s+mache|ich\s+erstelle|ich\s+schreibe|ich\s+baue)\b", line, re.IGNORECASE):
        context = "AutoPromise_" + datetime.datetime.now().strftime("%H%M%S")
        create_promise(context, line.strip())
        return True
    return False

# Erkennung von Abschlüssen
def detect_completion(line):
    if re.search(r"\b(fertig|abgeschlossen|erledigt|vollendet|hier\s+ist\s+das\s+ergebnis)\b", line, re.IGNORECASE):
        print(f"🔔 Fertigstellung erkannt: {line.strip()}")
        return True
    return False

def monitor_chat():
    print("🧠 Selbstverpflichtungs-Agent aktiv – überwacht Chat-Datei...")
    seen = 0
    while True:
        sync_pending_promises()  # versucht bei jedem Durchlauf zu senden
        if not os.path.exists(CHAT_LOG):
            time.sleep(5)
            continue

        with open(CHAT_LOG, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines[seen:]:
            detect_promises(line)
            detect_completion(line)

        seen = len(lines)
        time.sleep(5)

if __name__ == "__main__":
    monitor_chat()
