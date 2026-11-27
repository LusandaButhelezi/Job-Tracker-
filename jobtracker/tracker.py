"""Core logic: data model and storage. No printing or argument parsing here."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

STATUSES = ("saved", "applied", "interview", "offer", "rejected")
DEFAULT_FILE = Path("applications.json")


@dataclass
class Application:
    id: int
    company: str
    role: str
    status: str = "saved"
    date_added: str = field(default_factory=lambda: date.today().isoformat())
    notes: str = ""


class Tracker:
    def __init__(self, path: Path | str = DEFAULT_FILE):
        self.path = Path(path)
        self.applications: list[Application] = self._load()

    # --- storage -------------------------------------------------------
    def _load(self) -> list[Application]:
        if not self.path.exists():
            return []
        with self.path.open() as f:
            return [Application(**item) for item in json.load(f)]

    def _save(self) -> None:
        with self.path.open("w") as f:
            json.dump([asdict(a) for a in self.applications], f, indent=2)

    # --- operations ----------------------------------------------------
    def add(self, company: str, role: str, notes: str = "") -> Application:
        next_id = max((a.id for a in self.applications), default=0) + 1
        app = Application(id=next_id, company=company, role=role, notes=notes)
        self.applications.append(app)
        self._save()
        return app

    def get(self, app_id: int) -> Application:
        for app in self.applications:
            if app.id == app_id:
                return app
        raise KeyError(f"No application with id {app_id}")

    def update_status(self, app_id: int, status: str) -> Application:
        if status not in STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(STATUSES)}")
        app = self.get(app_id)
        app.status = status
        self._save()
        return app

    def remove(self, app_id: int) -> None:
        app = self.get(app_id)
        self.applications.remove(app)
        self._save()

    def list(self, status: str | None = None) -> list[Application]:
        if status is None:
            return list(self.applications)
        return [a for a in self.applications if a.status == status]

    def summary(self) -> dict[str, int]:
        return {s: len(self.list(s)) for s in STATUSES}
