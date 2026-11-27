"""Command-line interface. Talks to Tracker, handles input and output only."""
from __future__ import annotations

import argparse

from .tracker import STATUSES, Tracker


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="jobtracker", description="Track your job applications.")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Add an application")
    add.add_argument("company")
    add.add_argument("role")
    add.add_argument("--notes", default="")

    ls = sub.add_parser("list", help="List applications")
    ls.add_argument("--status", choices=STATUSES)

    upd = sub.add_parser("update", help="Change an application's status")
    upd.add_argument("id", type=int)
    upd.add_argument("status", choices=STATUSES)

    rm = sub.add_parser("remove", help="Delete an application")
    rm.add_argument("id", type=int)

    sub.add_parser("summary", help="Count applications by status")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    tracker = Tracker()

    try:
        if args.command == "add":
            app = tracker.add(args.company, args.role, args.notes)
            print(f"Added #{app.id}: {app.role} at {app.company}")
        elif args.command == "list":
            apps = tracker.list(args.status)
            if not apps:
                print("No applications found.")
            for a in apps:
                print(f"#{a.id:<3} {a.company:<20} {a.role:<28} [{a.status}] {a.date_added}")
        elif args.command == "update":
            app = tracker.update_status(args.id, args.status)
            print(f"#{app.id} is now '{app.status}'")
        elif args.command == "remove":
            tracker.remove(args.id)
            print(f"Removed #{args.id}")
        elif args.command == "summary":
            for status, count in tracker.summary().items():
                print(f"{status:<10} {count}")
    except (KeyError, ValueError) as err:
        print(f"Error: {err}")
