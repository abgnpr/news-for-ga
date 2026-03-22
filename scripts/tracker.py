#!/usr/bin/env python3
"""
Daily newspaper reading tracker TUI.
Navigate days with arrow keys, toggle completion, and add remarks.
Data stored in data/tracker.csv.
"""

import csv
import curses
import os
from datetime import date, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CSV_PATH = DATA_DIR / "tracker.csv"

PAPERS = ["The Hindu", "The Hindu Business Line"]
FIELDS = ["date", "the_hindu", "business_line", "remark"]


def load_data() -> dict[str, dict]:
    """Load tracker CSV into a dict keyed by date string."""
    records = {}
    if CSV_PATH.exists():
        with open(CSV_PATH, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records[row["date"]] = {
                    "the_hindu": row.get("the_hindu", "") == "yes",
                    "business_line": row.get("business_line", "") == "yes",
                    "remark": row.get("remark", ""),
                }
    return records


def save_data(records: dict[str, dict]):
    """Write all records back to CSV, sorted by date."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for d in sorted(records):
            r = records[d]
            writer.writerow({
                "date": d,
                "the_hindu": "yes" if r["the_hindu"] else "no",
                "business_line": "yes" if r["business_line"] else "no",
                "remark": r.get("remark", ""),
            })


def get_record(records, d: date) -> dict:
    key = d.isoformat()
    if key not in records:
        records[key] = {"the_hindu": False, "business_line": False, "remark": ""}
    return records[key]


def streak(records) -> int:
    """Count consecutive days (ending yesterday or today) where both papers are done."""
    d = date.today()
    count = 0
    while True:
        key = d.isoformat()
        r = records.get(key)
        if r and r["the_hindu"] and r["business_line"]:
            count += 1
            d -= timedelta(days=1)
        else:
            break
    return count


def month_calendar(year: int, month: int) -> list[list[int | None]]:
    """Return weeks (Mon=0) for given month. None for empty cells."""
    from calendar import monthcalendar
    return [[d or None for d in week] for week in monthcalendar(year, month)]


def draw(stdscr, current: date, records: dict, cursor: int, editing_remark: bool, remark_buf: str):
    stdscr.erase()
    h, w = stdscr.getmaxyx()
    rec = get_record(records, current)

    # Colors
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)   # done
    curses.init_pair(2, curses.COLOR_RED, -1)      # not done
    curses.init_pair(3, curses.COLOR_CYAN, -1)     # header
    curses.init_pair(4, curses.COLOR_YELLOW, -1)   # highlight
    curses.init_pair(5, curses.COLOR_WHITE, -1)    # dimmed

    GREEN = curses.color_pair(1) | curses.A_BOLD
    RED = curses.color_pair(2)
    CYAN = curses.color_pair(3) | curses.A_BOLD
    YELLOW = curses.color_pair(4) | curses.A_BOLD
    DIM = curses.color_pair(5)

    def safe_addstr(r, c, text, attr=0):
        """Write text only if it fits on screen."""
        if r < 0 or r >= h - 1 or c >= w:
            return
        text = text[:w - c - 1]
        if text:
            try:
                stdscr.addstr(r, c, text, attr)
            except curses.error:
                pass

    row = 1

    # Title
    title = "  News Tracker  "
    safe_addstr(row, max(0, (w - len(title)) // 2), title, CYAN)
    row += 2

    # Date display with nav hint
    day_name = current.strftime("%A")
    date_str = current.strftime("%d %B %Y")
    nav = f"<  {day_name}, {date_str}  >"
    safe_addstr(row, max(0, (w - len(nav)) // 2), nav, YELLOW)
    row += 1

    today = date.today()
    if current == today:
        label = "(today)"
    elif current == today - timedelta(days=1):
        label = "(yesterday)"
    elif current == today + timedelta(days=1):
        label = "(tomorrow)"
    else:
        delta = (today - current).days
        if delta > 0:
            label = f"({delta} days ago)"
        else:
            label = f"(in {-delta} days)"
    safe_addstr(row, max(0, (w - len(label)) // 2), label, DIM)
    row += 2

    # Paper status
    items = [
        ("The Hindu", rec["the_hindu"]),
        ("Business Line", rec["business_line"]),
    ]

    for i, (name, done) in enumerate(items):
        marker = ">" if cursor == i and not editing_remark else " "
        check = "[x]" if done else "[ ]"
        attr = GREEN if done else RED
        line = f" {marker} {check} {name}"
        safe_addstr(row, 4, line, attr)
        row += 1

    row += 1

    # Remark
    marker = ">" if cursor == 2 and not editing_remark else " "
    remark_display = remark_buf if editing_remark else (rec["remark"] or "-")
    remark_label = f" {marker} Remark: "
    safe_addstr(row, 4, remark_label, DIM)
    if editing_remark:
        safe_addstr(row, 4 + len(remark_label), remark_display + "_", YELLOW)
    else:
        safe_addstr(row, 4 + len(remark_label), remark_display, DIM)
    row += 2

    # Status summary
    both = rec["the_hindu"] and rec["business_line"]
    if both:
        safe_addstr(row, 4, "  Done for the day!", GREEN)
    elif rec["the_hindu"] or rec["business_line"]:
        safe_addstr(row, 4, "  Partially done", YELLOW)
    else:
        safe_addstr(row, 4, "  Not started", RED)
    row += 2

    # Streak
    s = streak(records)
    if s > 0:
        safe_addstr(row, 4, f"  Current streak: {s} day{'s' if s != 1 else ''}", GREEN)
    row += 2

    # Mini calendar
    cal = month_calendar(current.year, current.month)
    month_label = current.strftime("%B %Y")
    safe_addstr(row, 4, f"  {month_label}", CYAN)
    row += 1
    safe_addstr(row, 4, "  Mo Tu We Th Fr Sa Su", DIM)
    row += 1
    for week in cal:
        if row >= h - 1:
            break
        col = 6
        for day_num in week:
            if day_num is None:
                col += 3
                continue
            d = date(current.year, current.month, day_num)
            key = d.isoformat()
            r = records.get(key)
            display = f"{day_num:2d}"
            if d == current:
                safe_addstr(row, col, f"[{display}]", YELLOW)
                col += 3
            elif r and r["the_hindu"] and r["business_line"]:
                safe_addstr(row, col, f" {display}", GREEN)
                col += 3
            elif r and (r["the_hindu"] or r["business_line"]):
                safe_addstr(row, col, f" {display}", YELLOW)
                col += 3
            else:
                safe_addstr(row, col, f" {display}", DIM)
                col += 3
        row += 1

    row += 1

    # Help
    help_lines = [
        "left/right: prev/next day   up/down: select field",
        "space/enter: toggle   r: edit remark",
        "q/ctrl+c: quit            autosaves on every change",
    ]
    for line in help_lines:
        safe_addstr(row, 4, f"  {line}", DIM)
        row += 1

    stdscr.noutrefresh()
    curses.doupdate()


def main(stdscr):
    curses.curs_set(0)
    stdscr.timeout(-1)
    curses.raw()  # disable Ctrl+S/Ctrl+Q flow control

    records = load_data()
    current = date.today()
    cursor = 0  # 0=Hindu, 1=BL, 2=remark
    editing_remark = False
    remark_buf = ""

    while True:
        draw(stdscr, current, records, cursor, editing_remark, remark_buf)
        key = stdscr.getch()

        if editing_remark:
            if key in (curses.KEY_ENTER, 10, 13):  # confirm
                rec = get_record(records, current)
                rec["remark"] = remark_buf
                save_data(records)
                editing_remark = False
            elif key == 27:  # Escape — cancel
                editing_remark = False
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                remark_buf = remark_buf[:-1]
            elif 32 <= key <= 126:
                remark_buf += chr(key)
            continue

        if key in (ord("q"), 3):  # q or Ctrl+C
            break
        elif key == curses.KEY_LEFT:
            current -= timedelta(days=1)
        elif key == curses.KEY_RIGHT:
            current += timedelta(days=1)
        elif key == curses.KEY_UP:
            cursor = max(0, cursor - 1)
        elif key == curses.KEY_DOWN:
            cursor = min(2, cursor + 1)
        elif key in (ord(" "), curses.KEY_ENTER, 10, 13):
            rec = get_record(records, current)
            if cursor == 0:
                rec["the_hindu"] = not rec["the_hindu"]
                save_data(records)
            elif cursor == 1:
                rec["business_line"] = not rec["business_line"]
                save_data(records)
            elif cursor == 2:
                editing_remark = True
                remark_buf = rec.get("remark", "")
        elif key == ord("r"):
            rec = get_record(records, current)
            editing_remark = True
            remark_buf = rec.get("remark", "")
            cursor = 2


if __name__ == "__main__":
    curses.wrapper(main)
