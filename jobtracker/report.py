"""Executive summary report: KPIs, risks, recommended actions and commentary.

Structured like a management dashboard: overall status first, then the
breakdown, then risks, then what to do next. Pure functions, no printing,
so the same data can feed the terminal view and the HTML export.
"""
from __future__ import annotations

from datetime import date
from html import escape

from .tracker import STATUSES, Application

STALE_AFTER_DAYS = 14
ACTIVE_STATUSES = ("applied", "interview")
SUBMITTED_STATUSES = ("applied", "interview", "offer", "rejected")


def _pct(part: int, whole: int) -> float:
    return round(100 * part / whole, 1) if whole else 0.0


def _days_since(iso_date: str, today: date) -> int:
    return (today - date.fromisoformat(iso_date)).days


def compute_metrics(apps: list[Application], today: date | None = None) -> dict:
    """Turn raw applications into the KPIs a manager would ask for."""
    today = today or date.today()
    counts = {s: sum(1 for a in apps if a.status == s) for s in STATUSES}
    submitted = sum(counts[s] for s in SUBMITTED_STATUSES)
    responded = counts["interview"] + counts["offer"] + counts["rejected"]

    stale = [
        a for a in apps
        if a.status == "applied" and _days_since(a.last_activity, today) >= STALE_AFTER_DAYS
    ]
    return {
        "total": len(apps),
        "counts": counts,
        "submitted": submitted,
        "response_rate": _pct(responded, submitted),
        "interview_rate": _pct(counts["interview"] + counts["offer"], submitted),
        "active": sum(counts[s] for s in ACTIVE_STATUSES),
        "stale": stale,
    }


def generate_commentary(m: dict) -> list[str]:
    """Automated management commentary: plain-English reading of the numbers."""
    if m["total"] == 0:
        return ["No applications tracked yet. Add your first one to start building a pipeline."]

    lines = [
        f"{m['total']} applications tracked, {m['submitted']} submitted and {m['active']} currently active."
    ]
    if m["submitted"] == 0:
        lines.append("Nothing has been submitted yet; the pipeline is still in preparation.")
    elif m["response_rate"] >= 30:
        lines.append(f"Response rate is healthy at {m['response_rate']}%.")
    else:
        lines.append(
            f"Response rate is low at {m['response_rate']}%; consider tailoring CVs and cover letters more closely."
        )
    if m["counts"]["offer"]:
        lines.append(f"{m['counts']['offer']} offer(s) received. Decision needed.")
    return lines


def recommended_actions(m: dict, today: date | None = None) -> list[str]:
    today = today or date.today()
    actions = []
    for a in m["stale"]:
        days = _days_since(a.last_activity, today)
        actions.append(f"Follow up on #{a.id} {a.company} ({days} days without an update).")
    if m["counts"]["saved"]:
        actions.append(f"Submit or discard the {m['counts']['saved']} saved application(s).")
    if m["counts"]["interview"]:
        actions.append(f"Prepare for {m['counts']['interview']} interview(s).")
    return actions or ["No urgent actions. Keep the pipeline moving."]


def render_text(apps: list[Application], today: date | None = None) -> str:
    today = today or date.today()
    m = compute_metrics(apps, today)
    out = [f"APPLICATION PIPELINE: EXECUTIVE SUMMARY ({today.isoformat()})", ""]

    out.append("OVERALL STATUS")
    out += [f"  {line}" for line in generate_commentary(m)]

    out += ["", "KEY METRICS"]
    out.append(f"  Response rate:  {m['response_rate']}%")
    out.append(f"  Interview rate: {m['interview_rate']}%")

    out += ["", "PIPELINE"]
    top = max(m["counts"].values()) or 1
    for status, n in m["counts"].items():
        bar = "█" * round(20 * n / top)
        out.append(f"  {status:<10} {bar} {n}")

    out += ["", f"RISKS (applied, no update for {STALE_AFTER_DAYS}+ days)"]
    out += [f"  #{a.id} {a.company}: {a.role}" for a in m["stale"]] or ["  None"]

    out += ["", "RECOMMENDED ACTIONS"]
    out += [f"  - {a}" for a in recommended_actions(m, today)]
    return "\n".join(out)


def render_html(apps: list[Application], today: date | None = None) -> str:
    """Single-file HTML dashboard: KPI cards, bar chart, risks, actions."""
    today = today or date.today()
    m = compute_metrics(apps, today)
    top = max(m["counts"].values()) or 1

    bars = "".join(
        f'<div class="row"><span>{s}</span>'
        f'<div class="bar" style="width:{100 * n / top:.0f}%"></div><b>{n}</b></div>'
        for s, n in m["counts"].items()
    )
    li = lambda items: "".join(f"<li>{escape(i)}</li>" for i in items)
    risks = li(f"#{a.id} {a.company}: {a.role}" for a in m["stale"]) or "<li>None</li>"

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Application Pipeline</title>
<style>
body{{font-family:system-ui,sans-serif;max-width:720px;margin:2rem auto;padding:0 1rem;color:#1a1a1a}}
.cards{{display:flex;gap:1rem;margin:1rem 0}}
.card{{flex:1;background:#f3f5f9;border-radius:8px;padding:1rem;text-align:center}}
.card h2{{margin:0;font-size:2rem}} .card p{{margin:.2rem 0 0;color:#555}}
.row{{display:flex;align-items:center;gap:.75rem;margin:.3rem 0}}
.row span{{width:5.5rem}} .bar{{height:1rem;background:#2f6fed;border-radius:4px;min-width:2px}}
</style></head><body>
<h1>Application Pipeline</h1><p>Executive summary, {today.isoformat()}</p>
<div class="cards">
<div class="card"><h2>{m['total']}</h2><p>Tracked</p></div>
<div class="card"><h2>{m['active']}</h2><p>Active</p></div>
<div class="card"><h2>{m['response_rate']}%</h2><p>Response rate</p></div>
<div class="card"><h2>{m['interview_rate']}%</h2><p>Interview rate</p></div>
</div>
<h3>Commentary</h3><ul>{li(generate_commentary(m))}</ul>
<h3>Pipeline</h3>{bars}
<h3>Risks</h3><ul>{risks}</ul>
<h3>Recommended actions</h3><ul>{li(recommended_actions(m, today))}</ul>
</body></html>"""
