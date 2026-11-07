# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: <!-- complete -->
Members and responsibilities: <!-- complete -->
Stage 8 integrated SHA, command, working directory and actual result: <!-- complete -->

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason |
|---|---|---|
| Patient identity | Transient / session state | Stored in-memory in `SmartCareDataStore` during execution, wiped on exit. |
| Appointment history | Transient / session state | Retained in-memory across bookings and cancellations within the active session. |
| Temporary menu choice | Transient state | Local variable captured during each loop iteration of the CLI console. |
| Practitioner specialty | Domain / reference configuration | Seeded reference data associated with practitioner records in memory. |
| Debug print output | Transient execution log | Printed to stdout during runtime verification, not stored. |
| Appointment status | Transient domain object attribute | Tracks lifecycle (`SCHEDULED`, `CANCELLED`, `COMPLETED`) in memory. |

What is intentionally lost on exit? All runtime registrations, bookings, cancellations, and state modifications, data persistence and database storage are not part of Stage 9.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design, no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| appointment_sort_key | `appointment: Appointment` | `tuple` (`datetime`, `str`) | Extracts sorting criteria with tie-breaking by appointment ID. | Domain model date and ID attributes. |
| select_appointments | `appointments: list[Appointment]`, `practitioner_id: str`, `status: Optional[str] = None` | `list[Appointment]` | Pure query filtering by practitioner and optional status, returning sorted results. | Service query specifications (QRY-01–04). |
| Service listing | `practitioner_id: str`, `status: Optional[str] = None` | `list[Appointment]` | Coordinates store access and invokes pure query functions. | `AppointmentService` coordination layer. |
| Console | CLI `sys.stdin` / `sys.stdout` | `None` (side effects via I/O) | Manages interactive menu loop, user prompts, and exception handling (`ValueError`, `LookupError`). | `console.py` terminal interface (UI-01–02). |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: Entities are linked via identifiers stored in memory within domain objects, satisfying entity relationships without external databases.

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input | Violates separation of concerns by coupling domain logic to I/O devices. | Console handles `input()`, while service/domain methods update state without prompting the user. |
| Service prints/reads the menu | Violates service layer boundaries, services should handle business logic and coordination, not CLI UI. | Console manages terminal display and user prompts, services return data or raise domain exceptions. |
| Query sorts its source in place | Violates pure function principles by mutating input collections destructively. | Queries use `sorted()` or return new lists without mutating original collections in place. |
| Store prints Appointment saved | Violates single responsibility principle by mixing data storage with terminal presentation. | Data store manages collections silently, the console/UI prints confirmation messages. |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: 
`.sort()` mutates the original list in place and returns `None`, whereas `sorted()` creates and returns a new list object, leaving the source list entirely unmodified.

Score-example prediction and explanation of passing the named key: Passing a key function extracts comparison criteria (tuple of date_time and appointment_id) so Python compares structured tuples rather than raw domain objects directly, ensuring deterministic ordering even when timestamps match.

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion:
Cancellation changes an appointment's status (`SCHEDULED` -> `CANCELLED`) while maintaining the object in memory for audit history, where deletion would remove it completely. Same-session lookup verifies objects in the active data store. All-status listing includes scheduled, cancelled, and completed appointments based on filtering, while `SCHEDULED`-only exclusion ensures historical or cancelled slots do not block new bookings.

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: Designed pure query functions (`select_appointments`, `appointment_sort_key`) in `queries.py` to keep filtering logic side-effect-free, and structured `AppointmentService` and `console.py` to cleanly separate business logic from CLI I/O and exception handling.

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| QRY-01 | Practitioner ID, optional status | `select_appointments()` in `queries.py` | Returns filtered list of appointments matching criteria | `test_queries.py` |
| UI-01 | Menu option inputs (1–8) | `console.py` `run_menu()` | Executes corresponding service action successfully | `test_workflows.py` |
| FR-05 | Appointment ID | `AppointmentService.cancel_appointment()` | Updates status to `CANCELLED`, preserves history | `test_services.py` |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: 
Empty inputs return empty collections or trigger validation messages, unknown IDs raise `LookupError`, invalid formats raise `ValueError`. Enum conversion maps string inputs to strict enumeration values. Error handling catches domain exceptions cleanly in the console without crashing, ensuring application state remains unchanged upon rejection.

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| QRY-01 / test_select_appointments | `queries.py` | Practitioner isolation: filtering returns only appointments matching `practitioner_id` | Passed (100% green) | `project/tests/test_queries.py` |
| QRY-02 / test_status_filter | `queries.py` | Enum status filter (SCHEDULED, CANCELLED, COMPLETED) & default ALL when status is omitted | Passed (100% green) | `project/tests/test_queries.py` |
| QRY-03 / test_sorting | `queries.py` | Sorted chronologically by `date_time`, with ID tie-breaking for equal timestamps | Passed (100% green) | `project/tests/test_queries.py` |
| QRY-04 / test_immutability | `queries.py` | Input list remains unmutated; fresh list returned with preserved object references | Passed (100% green) | `project/tests/test_queries.py` |
| QRY-05 / test_query_edge_cases | `queries.py` | Edge cases: unknown practitioner returns empty list, invalid status raises ValueError | Passed (100% green) | `project/tests/test_queries.py` |
| FR-05 / test_cancel_history | `services.py` | Cancelled appointment status updated to CANCELLED while object remains retrievable in history | Passed (100% green) | `project/tests/test_services.py` |
| QRY-01-S / test_service_listing | `services.py` | Service delegation to query layer returns expected practitioner appointments | Passed (100% green) | `project/tests/test_services.py` |


Purity explanation from code inspection, including absence of hidden state and I/O: 
`select_appointments` and `appointment_sort_key` in `queries.py` are pure functions. They compute outputs solely from explicit input arguments, perform no global or hidden state access, execute no I/O operations (`print` or `input`), and use `sorted()` to return a new list container without mutating the original input list.

What the tests do and do not establish: 
The unit tests establish that the filtering and sorting algorithms work correctly without side effects on given lists of in-memory domain objects. They do not establish CLI terminal rendering, user keypress interaction, or permanent database persistence.

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| Automated service workflow | `test_services.py` / `test_workflows.py` | Registration, booking, conflict check, cancellation, and practitioner listing | All 51 unit tests passed successfully; state transitions verified in-memory | `project/tests/test_services.py` |
| FR-01–09 Domain Workflow | Service test suite execution | Full lifecycle from patient/practitioner creation to appointment filtering | Correct domain exceptions (`LookupError`, `ValueError`) raised on invalid operations | `project/tests/test_workflows.py` |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit, duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: <!-- reference -->
Actual prompt/context supplied: <!-- paste or accessible reference -->
Actual response: <!-- accessible reference -->

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| | | | | | |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: <!-- response -->

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? 
The concerns between pure query funcitons (`queres.py`), state coordination services (`servies.py`), and CLI I/O presentation (`console.py`). Making sure that pure queries stayed free of side effects and I/O operations while services managed state mutations was a core challenge rather than a simple detail for filtering.

2. Which Copilot suggestion did you reject as over-engineering, and why? 
The suggestion to make make complex data base caching layers or external persistance libraries, which were not used because Stage 9 mandates volatile, in memory only state without external databases.
3. How did you prove cancelled appointments remain retrievable and listable in the same session? Through unit tests verifiying that calling `.cancel()` updated the status attribute to `CANCELLED` while preserving the object in the data store collection, so it can be retrieved and filtered when listing appointments.

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? 
It is pure because it takes explicit inputs, computes a determined result, and returns a new list without changing inputs or performing I/O. Mutating input lists in place or printing/logging inside the function would make side effects and break purity.

2. Which explicit inputs are needed, and why avoid a global store? 
Explicit inputs (such as the appointment collection, practitioner ID, and optional status) ensure functions are deterministic and easily testable, where global stores create hidden state dependencies, tight coupling, and difficult test isolation.

3. How can a new list reuse Appointment objects safely? 
By creating a new collection container (like a list returned by `sorted()` or comprehension) that holds references to existing `Appointment` objects without modifying their internal data fields or duplicating the domain objects themselves.

4. Why use a named key, and what breaks equal-time ties? 
A named key function extracts structured comparison values (such as a tuple of `date_time` and `appointment_id`), providing deterministic sorting where appointment IDs break ties when two appointments share the exact same timestamp.

5. How do default and explicit status filters differ? 
A default filter (when status is omitted or blank) returns all appointments across every status for that practitioner, whereas an explicit filter restricts the result set to a specific status value (e.g., `SCHEDULED`, `CANCELLED`, or `COMPLETED`).

6. How do empty, unknown practitioner and invalid filter cases differ? 
An empty case returns an empty collection when no matches exist, an unknown practitioner ID triggers a lookup error or empty result set, an invalid filter or malformed date raises a `ValueError`.

7. Which console errors recover, and how is unchanged state checked? 
`ValueError` and `LookupError` are caught within the console menu loop, displaying an error message and re-prompting the user without crashing, leaving existing data state unchanged.

8. What is data integrity for registered participants, conflicts and history? 
Data integrity ensures unique identification of participants, prevents overlapping appointment time conflicts for the same practitioner, and maintains audit history by preserving cancelled and completed records in memory.

9. What is Copilot's review role, and who verifies findings? 
Copilot acts as an AI pair programming assistant offering critique, code suggestions, and alternative patterns. The human developer retains final responsibility to critically evaluate, adapt, and rigorously test every finding.

10. How do pure functions and OOP responsibilities work together? 
Pure functions handle side-effect-free data transformation, querying, and sorting, while object-oriented domain classes encapsulate state, invariants, and business rules, forming a clean, modular architecture.

## H. Review, completion and common handover

Issues and bounded branches: <!-- links -->
PR/diff and another-member human reviewer: <!-- actual links/name -->
Review responses and Copilot comparison: <!-- links -->
Integrated common Stage 9 SHA: <!-- complete -->
Full regression command, working directory, actual count/result and evidence: <!-- complete -->
README run instructions and scope/limitations: <!-- link -->
Unresolved issues and support/action: <!-- complete -->
UG common candidate / PG future branch plan: <!-- complete -->

- [ ] Query contracts, purity, new lists and named-key ordering verified.
- [ ] Service empty/unknown/invalid cases and cancellation history verified.
- [ ] Every console command and invalid-input recovery demonstrated.
- [ ] Query and workflow tests plus all previous tests pass actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [ ] Reflections and ten formative responses completed.
- [ ] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
