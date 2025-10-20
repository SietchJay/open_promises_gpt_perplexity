import os, re, time, json, datetime, requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# === KONFIGURATION ===
CACHE_PATH = r"C:\Users\clej_\AppData\Local\Packages\OpenAI.ChatGPT-Desktop_2p2nqsd0c76g0\LocalCache\Roaming\ChatGPT"
PROMISE_API = "http://127.0.0.1:8000/promises/update"
SCAN_EXT = [".json", ".log", ".txt"]  # welche Dateien überwacht werden

def utc_now():
    return datetime.datetime.utcnow().isoformat() + "Z"


def send_promise_to_server(text):
    payload = {
        "id": f"promise_{datetime.datetime.now().strftime('%H%M%S')}",
        "context": "ChatGPT_Desktop",
        "owner": "GPT-5",
        "partner": "User",
        "description": text,
        "created_at": utc_now(),
        "status": "open",
        "relevance": "high",
        "notes": "Automatisch erkannt aus ChatGPT Cache-Datei"
    }
    try:
        r = requests.post(PROMISE_API, json=payload, timeout=5)
        if r.status_code == 200:
            print(f"✅ Promise erkannt & übertragen: {text[:80]}...")
        else:
            print(f"⚠️ Server-Antwort: {r.status_code}")
    except Exception as e:
        print(f"⚠️ Promise konnte nicht gesendet werden: {e}")

def scan_file(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except Exception:
        return
    pattern = re.compile(r"\b(ich\s+werde|ich\s+mache|ich\s+erstelle|ich\s+schreibe|ich\s+baue|ich\s+analysiere)\b", re.IGNORECASE)
    matches = pattern.findall(text)
    if matches:
        send_promise_to_server(text)

class CacheHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if any(event.src_path.endswith(ext) for ext in SCAN_EXT):
            print(f"📡 Änderung erkannt → {os.path.basename(event.src_path)}")
            scan_file(event.src_path)

if __name__ == "__main__":
    print("🧩 Starte ChatGPT-Cache-Watcher...")
    event_handler = CacheHandler()
    observer = Observer()
    observer.schedule(event_handler, CACHE_PATH, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
