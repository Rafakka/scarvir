
import json, os
from datetime import datetime

LOG_PATH = os.path.join("logs", "app.log")
os.makedirs("logs", exist_ok=True)

def log_event(action: str, id_curto: str = None, origem: str = None, success: bool = True, extra: dict = None, err: str = None):
    rec = {
        "ts": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "action": action,
        "id_curto": id_curto,
        "origem": origem,
        "success": success,
        "err": err,
        "extra": extra or {}
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
