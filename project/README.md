# SmartCare v1.0 — Clinic Management System

## Overview
SmartCare is a Python-based clinic management application developed for Software Technology 1 Assignment 3. It follows the 2026 Revision 2 requirements and covers the UG scope.
## Features
- Patient and practitioner registration and lookup.
- Appointment booking and practitioner conflict prevention.
- Appointment cancellation and retained history.
- Appointment lookup, filtering and sorting.
- Interactive console with error handling.

## Setup and Testing
Tested using Python 3.14.4 and pytest 8.3.5.

From the `project/` directory:

```powershell
python -m pip install -r requirements-dev.txt
python main.py
python main.py --interactive
python -m pytest -q
```

**Regression result:** 51 passed in 0.06s.

**Tested SHA:** `289029c6e2d5bcdd981f15a6121b1611df01f7a5`

## Architecture
- `domain.py` — Entities, validation and appointment status.
- `data_store.py` — Shared in-memory records.
- `services.py` — Registration, booking, cancellation and lookup.
- `queries.py` — Pure filtering and sorting functions.
- `console.py` — User interaction and error recovery.
- `tests/` — Automated tests.

## AI Use
GitHub Copilot assisted with development and testing. Suggestions were reviewed against requirements and verified through human checks and automated tests.

## Limitations
SmartCare is a course project using synthetic data only. Records are lost when the application closes. It does not provide authentication, permanent storage, notifications, billing, clinical decision support or production security guarantees. Appointment times use local naive datetimes at minute precision. Production accessibility, scalability, monitoring and timezone handling have not been established.

## Release Status
**SmartCare v1.0 — Stage 12 verification in progress.**

Final approval, independent reproducibility verification and release SHA are pending.