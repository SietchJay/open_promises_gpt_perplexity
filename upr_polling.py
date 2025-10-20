import requests, time, datetime, webbrowser

API_URL = "http://127.0.0.1:8000/promises"

# Öffnet den Browser beim Start automatisch
webbrowser.open(API_URL)

def check_promises():
    try:
        promises = requests.get(API_URL).json()
        print(f"\n[{datetime.datetime.now()}] Überprüfung gestartet...")
        for p in promises:
            if p["status"] in ("open", "in_progress"):
                print(f"🔍 {p['context']} → Status: {p['status']}")
                # Beispielhafte Logik
                if "Strategiepapier" in p["context"]:
                    p["status"] = "done"
                    p["last_action_by"] = "GPT-5"
                    requests.post(f"{API_URL}/update", json=p)
                    print(f"✅ {p['context']} wurde als 'done' markiert.")
        print(f"[{datetime.datetime.now()}] Überprüfung abgeschlossen.")
    except Exception as e:
        print(f"⚠️ Fehler bei der Überprüfung: {e}")

# Prüfungsschleife (alle 60 Sekunden)
while True:
    check_promises()
    time.sleep(60)
from gpt_promise_agent import create_promise
