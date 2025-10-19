from fastapi import FastAPI, Body
import json, os

app = FastAPI(title="Unified Promise Registry (UPR)", version="1.1")
DB_PATH = os.path.join(os.path.dirname(__file__), "open_promises.json")


@app.get("/")
def root():
    return {
        "message": "Unified Promise Registry (UPR) läuft ✅",
        "endpoints": ["/promises", "/promises/update"],
        "info": "Rufe /promises auf, um alle Einträge anzuzeigen."
    }


@app.get("/promises")
def get_promises():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@app.post("/promises/update")
def update_promise(p: dict = Body(...)):
    with open(DB_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    for i, entry in enumerate(data):
        if entry["id"] == p["id"]:
            data[i].update(p)
            data[i]["last_action_by"] = "System"
            break
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return {"status": "ok", "updated_id": p["id"]}
