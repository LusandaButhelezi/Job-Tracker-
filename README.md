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
python -m jobtracker remove 1
```

Statuses: `saved`, `applied`, `interview`, `offer`, `rejected`.

## Project structure

```
jobtracker/
  tracker.py   # data model + JSON storage (core logic)
  cli.py       # argument parsing and printing
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
- [ ] v0.2: Search, sort, and filter by company; follow-up reminders
- [ ] v0.3: Swap JSON for SQLite
- [ ] v0.4: Export to CSV, weekly summary report
- [ ] v0.5: REST API with FastAPI
- [ ] v0.6: Simple web dashboard, deployment
