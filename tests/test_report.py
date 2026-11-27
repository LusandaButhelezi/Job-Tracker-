from datetime import date

from jobtracker.report import (
    compute_metrics,
    generate_commentary,
    recommended_actions,
    render_html,
    render_text,
)
from jobtracker.tracker import Application

TODAY = date(2026, 11, 27)


def make(id, status, added="2026-11-20"):
    return Application(id=id, company=f"Co{id}", role="Dev", status=status, date_added=added)


def test_rates_are_calculated_from_submitted_applications():
    apps = [make(1, "saved"), make(2, "applied"), make(3, "interview"), make(4, "rejected")]
    m = compute_metrics(apps, TODAY)
    assert m["submitted"] == 3
    assert m["response_rate"] == 66.7  # 2 of 3 submitted got a response


def test_empty_tracker_does_not_divide_by_zero():
    m = compute_metrics([], TODAY)
    assert m["response_rate"] == 0.0
    assert "No applications" in generate_commentary(m)[0]


def test_stale_applications_flagged_for_follow_up():
    apps = [make(1, "applied", added="2026-11-01"), make(2, "applied", added="2026-11-25")]
    m = compute_metrics(apps, TODAY)
    assert [a.id for a in m["stale"]] == [1]
    assert any("Follow up on #1" in a for a in recommended_actions(m, TODAY))


def test_text_and_html_reports_render():
    apps = [make(1, "applied"), make(2, "offer")]
    assert "EXECUTIVE SUMMARY" in render_text(apps, TODAY)
    assert "<html" in render_html(apps, TODAY)
