from fastapi import FastAPI, Body
import json

app = FastAPI()
DB_PATH = "open_promises.json"

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
            break
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return {"status": "ok"}
