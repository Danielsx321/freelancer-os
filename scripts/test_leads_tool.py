"""Tests for leads_tool.py: slug, sent, review and state on a temporary leads folder.

Run from the repo root:
    python3 -m unittest scripts/test_leads_tool.py
No network, no real lead files. The lead below is invented.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parent / "leads_tool.py"

LEAD = """# Northwind Bakery Oct 2026

State:           Drafted
Touches sent:    0 of 5
Opened:          pending
Last sent:       none
Next action:     on send
Channel:         Email; sam@example.com
Contact type:    Named personal (budget 5)
Second channel:  None registered
Subject line:    Online orders failing at the delivery step

## Contact

Person / Role:   Sam Carter; Owner
Company:         Northwind Bakery, Leeds UK

## Log

| # | Date | Channel | Carried | Outcome |
|---|---|---|---|---|
| 1 | pending | Email | Opening; delivery-step diagnosis | |

## Messages

### Touch 1
Hi Sam, ...

## Notes

"""


class LeadsToolTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        (self.dir / "lead-northwind-bakery-2026-10.md").write_text(LEAD)
        self.env = {**os.environ, "LEADS_DIR": str(self.dir)}

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_tool(self, *args: str) -> str:
        r = subprocess.run([sys.executable, str(TOOL), *args], env=self.env, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    def lead(self) -> str:
        return (self.dir / "lead-northwind-bakery-2026-10.md").read_text()

    def test_slug(self) -> None:
        self.assertEqual(self.run_tool("slug", "Northwind Bakery Oct 2026").strip(), "northwind-bakery-2026-10")

    def test_sent_stamps_date_and_next_action(self) -> None:
        out = self.run_tool("sent", "northwind-bakery-2026-10", "--date", "2026-10-01")
        self.assertIn("marked sent 2026-10-01", out)
        text = self.lead()
        self.assertIn("Touches sent:    1 of 5", text)
        self.assertIn("State:           Awaiting reply", text)
        self.assertIn("Next action:     2026-10-03", text)  # touch 2 is 2 days after touch 1
        self.assertIn("| 1 | 2026-10-01 |", text)

    def test_review_lists_due_lead(self) -> None:
        self.run_tool("sent", "northwind-bakery-2026-10", "--date", "2026-10-01")
        out = self.run_tool("review", "--today", "2026-10-03")
        self.assertIn("Northwind Bakery", out)
        self.assertIn("Due now", out)

    def test_state_dead_clears_next_action(self) -> None:
        self.run_tool("state", "northwind-bakery-2026-10", "Dead: bounced")
        text = self.lead()
        self.assertIn("State:           Dead: bounced", text)
        self.assertIn("Next action:     None", text)

    def test_check_finds_company(self) -> None:
        out = self.run_tool("check", "Northwind", "nothing-else")
        self.assertIn("outreach lead", out)
        self.assertIn("northwind", out)


if __name__ == "__main__":
    unittest.main()
