import pytest

from jobtracker.tracker import Tracker


@pytest.fixture
def tracker(tmp_path):
    return Tracker(tmp_path / "apps.json")


def test_add_assigns_incrementing_ids(tracker):
    first = tracker.add("Acme", "Junior Developer")
    second = tracker.add("Globex", "Business Analyst")
    assert (first.id, second.id) == (1, 2)


def test_data_persists_between_instances(tmp_path):
    path = tmp_path / "apps.json"
    Tracker(path).add("Acme", "Junior Developer")
    assert len(Tracker(path).list()) == 1


def test_update_status(tracker):
    app = tracker.add("Acme", "Dev")
    tracker.update_status(app.id, "interview")
    assert tracker.get(app.id).status == "interview"


def test_invalid_status_rejected(tracker):
    app = tracker.add("Acme", "Dev")
    with pytest.raises(ValueError):
        tracker.update_status(app.id, "ghosted")


def test_remove(tracker):
    app = tracker.add("Acme", "Dev")
    tracker.remove(app.id)
    assert tracker.list() == []


def test_summary_counts(tracker):
    a = tracker.add("Acme", "Dev")
    tracker.add("Globex", "BA")
    tracker.update_status(a.id, "applied")
    assert tracker.summary()["applied"] == 1
    assert tracker.summary()["saved"] == 1
