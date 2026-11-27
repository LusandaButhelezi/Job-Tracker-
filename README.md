# Job Tracker

A command-line tool for tracking job applications, built in Python as I learn the language properly. It starts small and grows in stages (see the roadmap below).

## Usage

Requires Python 3.9+. No dependencies.

```bash
python -m jobtracker add "Acme Corp" "Junior Developer" --notes "Graduate programme"
python -m jobtracker list
python -m jobtracker list --status applied
python -m jobtracker update 1 interview
python -m jobtracker summary
python -m jobtracker report
python -m jobtracker report --html dashboard.html
python -m jobtracker remove 1
```

Statuses: `saved`, `applied`, `interview`, `offer`, `rejected`.

## Executive report

`report` turns the raw list into a management-style summary, ordered the way a decision-maker reads it: overall status, key metrics (response and interview rates), pipeline breakdown, risks (applications with no update for 14+ days) and recommended actions, plus automatically generated commentary. `--html` saves the same view as a single-file dashboard.

## Project structure

```
jobtracker/
  tracker.py   # data model + JSON storage (core logic)
  cli.py       # argument parsing and printing
  report.py    # KPIs, commentary and text/HTML dashboards
tests/         # pytest tests
```

Logic and interface are kept separate so the storage or interface can be swapped later without rewriting everything.

## Run the tests

```bash
pip install pytest
pytest
```

## Roadmap

- [x] v0.1: CLI with JSON storage, tests
- [x] v0.2: Executive report: KPIs, risks, recommended actions, HTML dashboard
- [ ] v0.3: Search, sort, and filter by company
- [ ] v0.4: Swap JSON for SQLite
- [ ] v0.5: Export to CSV, charts over time (trends)
- [ ] v0.6: REST API with FastAPI
- [ ] v0.7: Interactive web dashboard, deployment
