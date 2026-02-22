import json
import threading
import time
import uuid
from pathlib import Path
from typing import List, Optional, Dict

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"
DATA_FILE = CONFIG_DIR / "tokens.json"
LEGACY_DATA_FILE = DATA_DIR / "tokens.json"

class TokenManager:
    def __init__(self):
        self._lock = threading.Lock()
        self.tokens: List[Dict] = []
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self.load()

    def load(self):
        with self._lock:
            source = DATA_FILE if DATA_FILE.exists() else LEGACY_DATA_FILE
            if source.exists():
                try:
                    self.tokens = json.loads(source.read_text(encoding="utf-8"))
                    if source == LEGACY_DATA_FILE and not DATA_FILE.exists():
                        DATA_FILE.write_text(json.dumps(self.tokens, indent=2), encoding="utf-8")
                except Exception:
                    self.tokens = []

    def save(self):
        DATA_FILE.write_text(json.dumps(self.tokens, indent=2), encoding="utf-8")

    def add(self, value: str):
        with self._lock:
            value = value.strip()
            if value.startswith("Bearer "):
                value = value[7:].strip()
                
            for t in self.tokens:
                if t["value"] == value:
                    return t
            
            new_token = {
                "id": uuid.uuid4().hex[:8],
                "value": value,
                "status": "active",
                "fails": 0,
                "added_at": time.time()
            }
            self.tokens.append(new_token)
            self.save()
            return new_token

    def remove(self, tid: str):
        with self._lock:
            self.tokens = [t for t in self.tokens if t["id"] != tid]
            self.save()

    def set_status(self, tid: str, status: str):
        with self._lock:
            for t in self.tokens:
                if t["id"] == tid:
                    t["status"] = status
                    t["fails"] = 0 if status == "active" else t["fails"]
            self.save()

    def get_available(self) -> Optional[str]:
        with self._lock:
            active = [t for t in self.tokens if t["status"] == "active"]
            if active:
                active.sort(key=lambda x: x["fails"])
                return active[0]["value"]

            # Auto-revive one recoverable token to avoid permanent 503
            # caused by transient upstream failures.
            recoverable = [t for t in self.tokens if t["status"] == "error"]
            if not recoverable:
                return None
            recoverable.sort(key=lambda x: x["fails"])
            chosen = recoverable[0]
            chosen["status"] = "active"
            chosen["fails"] = max(0, int(chosen.get("fails", 0)) - 1)
            self.save()
            return chosen["value"]

    def report_exhausted(self, value: str):
        with self._lock:
            for t in self.tokens:
                if t["value"] == value:
                    t["status"] = "exhausted"
            self.save()

    def report_error(self, value: str):
        with self._lock:
            for t in self.tokens:
                if t["value"] == value:
                    t["fails"] += 1
                    if t["fails"] >= 8:
                        t["status"] = "error"
            self.save()

    def report_success(self, value: str):
        with self._lock:
            for t in self.tokens:
                if t["value"] == value:
                    t["fails"] = max(0, int(t.get("fails", 0)) - 1)
                    if t["status"] == "error":
                        t["status"] = "active"
            self.save()

    def list_all(self):
        with self._lock:
            res = []
            for t in self.tokens:
                # mask value
                val = t["value"]
                masked = val[:15] + "..." + val[-10:] if len(val) > 30 else "***"
                res.append({
                    "id": t["id"],
                    "value": masked,
                    "status": t["status"],
                    "fails": t["fails"],
                    "added_at": t["added_at"]
                })
            return res

token_manager = TokenManager()
