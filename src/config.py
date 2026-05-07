import datetime

# ── test mode ─────────────────────────────────────────────────────────────────
# When True, fixes "today" to TEST_DATE so queries work against the synthetic
# dataset regardless of the real calendar date.
# TEST_DATE is ~20% into the Fall 2026 semester (Sep 8 – Dec 17):
#   past:    Lab 1 (Sep 14), HPS RR1 (Sep 22), FIN405 Case Study 1 (Sep 25)
#   today:   CS350 Lab 2 due (Sep 28)
#   upcoming: Sprint 1 demo (Oct 5), HPS RR2 (Oct 6), CAPM PS1 (Oct 9), ...
TEST_MODE = True
TEST_DATE = datetime.date(2026, 9, 28)


def today() -> datetime.date:
    return TEST_DATE if TEST_MODE else datetime.date.today()
