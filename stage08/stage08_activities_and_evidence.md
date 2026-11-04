# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: [complete]
Members and UG/PG cohorts: [complete]
Record owner / contribution links for each member: [complete]

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.

- Appointment disappears after cancellation.
Symptom, it describes what the user observes not why is happens

- The data-store removal path is probably being called.
Hypothesis, it's a guess at the cause and the use of the word "probably" shows that the actual cause is unknown.

- The failing test shows store.find_appointment('A1') returns None.
Evidance, it's an observed and repeatable result from running a test.

- The service layer is badly designed.
Opinion, at's a vague judgement with nothing describing why or what is "bad" about it.

- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Evidence, ir shows where the exception was raised giving us evidance of location, however dose not say wha the cause was. In our actual run the LookupError is raised at smartcare/services.py line 141 in AppointmentService.find_appointment(), the faulty value could have been something it tried to call however.


### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason:
Cancelled appointment history scenario.
Expected behaviour: After a SCHEDULED appointment is cancelled its status should change to CANCELLED, and it should still be able to be looked up by its ID, and its still stored in the appointment list.

Observed behaviour: The appointment status does change to CANCELLED, but looking the appointment up afterwards raises "LookupError: Appointment not found".

Minimal reproduction:
    1. Create a new SmartCareDataStore
    2. Register patient P001 and practitioner DR001
    3. Book A001 for P001/DR001 at 2026-11-10 10:00
    4. Call cancel_appointment("A001")
    5. Call find_appointment ("A001")

Initial hypothesis: Canelling the appointment removes it from the store. Or the store stops returning it so then the lookup cant find it.

Evidance to inspect:
    AppointmentService.cancel_appointment() and Appointment.cancel(), for anything that removes or replaces the appointment record.
    SmartCareDataStore.find_appointment(), to see how it searches for the appointments.
    If store.list_appointments() still has A001 after cancelling. This checks if its deleted or just hidden by the look up.

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Test expecting cancelled appointments to be deleted: This is a test defect as FR-07 says cancelled history needs to be retained, so the test goes against the requirements. The test should be changed to check if the cancelled appointment is still able to be found.

Test expecting different practitioner at the same time to conflict: This is also a test defect as it goes against AC-04.2 which says different practitioners at the same time is allowed. A conflict should only apply when its the same practitioner at the same time with another SCHEDULED appointment.

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

The method is too long at 70 lines and taking on too many jobs. It needs to be split up.

Duplicate status strings. Replace duplicate status strings with existing AppointmentStatus enum values so typos cant sneak though.

Direct collection manipulation. The service should go though SmartCareDataStore methods like add_appointment, find_appointment ect. Instead of editiing the stores dictionaries.

Printing inside the service. By removing the prints the service should return values or raise exceptions and leave the output on the console.

Validation mixed in with the method. Use the existing domain and store validation instead of repeating it.

Four nested conditionals. Use raise or return to reduce the number of nested conditionals.

Classifications:

| Change | Type | Why |
| --- | --- | --- |
| Rename appt to appointment | Refactoring | Structure and readability only |
|Extract a repeated conflict | Refactoring | Same logic just moved to one place |
| Add rescheduling | Feature | New behaviour |
| Restore retained cancellation lookup | Repair | Fixes behaviour that breaks FR-07 |
| Replace a magic status sting with the existing enum 
 Refactoring | As long as the compartison give the same result |

Unchanged behaviours:
The same exception types:
    ValueRoor for invalud values, duplicates, conflicts and illegal status changes.
    LookupError for missing records.
Conflicts only for the same practitioner at the same time with a SCHEDULED appointment.
Cancelled appointments are stored not deleted.
Failed operations leaving the store unchanged.

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Using: test_cancel_scheduled_appointment
Exception/assertion: "LookupError: Appointment not found", raised when evaluating "assert".
Expected value: The same Appointment object (A001) with status CANCELLED
Observed value: No object returned, a LookupError was raised instead.
Test line: tests/test_services.py line 211. The two assertions before it were "result is appointment" and "status is AppointmentStatus.CANCELLED", passed so the cancellation worked.
Call path: test line 211 --> AppointmentService.find_appointment() (smartcare/services.py) → SmartCareDataStore.find_appointment() returns None → LookupError raised at smartcare/services.py line 141.
Supporting requirement: FR-07 retain calcelled history and FR-06 cancel appointments.

Ranked plausible causes:
    1. SmartCareDataStore.find_appointment() skips or filters out cancelled appointments.
        Best fit: cancel_appointment() found A001 when it was CHEDULED, but the same lookup fails after it became CNACELLED, so the results seem to depend on the status.
        Check: After cancelling, checking if A001 is still in store.list_appointments(). If it's not there but find_appointment returns None, the lookup is hiding it.
    2. Cancellation removes the appointment from the store.
        Average fit: The store has no public delete method and the test still has the appointment object.
        Check: Compare len(store.list_appointments()) before and after cancelling and look though cancel_appointments() and Appointmend.cancel().
    3. The ID is store or looked up differently
        Weakest fit: The same A001 ID was found successfully by cancel appointment() just before.
        Check: Call find_appointment("A001") before cancelling if it works then the ID handling ins't the cause.

Why is a traceback alone not enough?
It shows where the exception was raised, in this case line 141 but not why it was raised. The LoopupError is the correct behaviour for a missing appointment. The actual issue is whatever made the store return None, and that could have been in another function or file entirely.

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

The failure only shows the symptoms of the problem not the cause. Changing the code straight away is just guessing. You might acidentaly patch where the error appeared instead of where the fault is. "fix" a test that was actually correct or a product that was correct but the test was wrong. Break other behaviour that you want or hie the problem and it could come back later.
You should first try reproduce the issue so you can narrow down what is causing it. Compare the results to the requirements and use mutiple tests to see which part is acutally broken. Before rerunning the tests to see if you were correct.


Classification responses (1–5, each with reason):
The classification responses can be found in A.1.

Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect:
Totorial debugging record can be found in A.2.

Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks:
Traceback can be found in A.5.

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline:
SHA: b50010ba093eb3d2e5210509ebbdc902ac3ccdfe (“Stage 07 complete”, main)
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.

- Baseline test command / working directory / observed result / evidence:
python -m pytest from project/ at b50010b – 45 passed, 0 failed.

- Clean preparation SHA if a record-only commit followed Stage 7:
SHA: 1a454aa30f70c0913a25d0e1b9df103ea5321105 (“update .gitignore”).
Omly .gitignore changed no code or tests changed, so the code is the same as the Stage 7 SHA.

- Branch and preparer / how teammates obtained this branch:
Branch debug/stage08 was prepared by Muthuraman and pushed to origin. Myself (Gerbich) got it with git fetch origin then git switch debug/stage08.

- Downloaded tool version, source SHA256 and --check outcome:
=====================================================
Muthuraman to complete as I dont have access to this.
=====================================================

- --apply and --verify output summaries / artefact references:
=====================================================
Muthuraman to complete as I dont have access to this.
=====================================================

- Bounded diff inspected and recovery location (not committed):
git diff b50010b e356c85, shows changes to:
project/smartcare/data_store.py 
SmartCareDataStore.find_appointment() 
SmartCareDataStore.has_practitioner_conflict()

=====================================================
Muthuraman to complete recovery location as I dont have access to this.
=====================================================

- Prepared faulty-state commit SHA:
e356c85350a8db8b37714c8ad9ac433ed27de7d9 (“prepare debugg stage08”) on debug/stage08.

- Preparation or recovery issues and resolution, if any: 
=====================================================
Muthuraman to complete as I dont have access to this.
=====================================================

- Initial prepared full-suite command / result / key failures:
python -m pytest from project/ at e356c85 – 4 failed, 41 passed:
    1.  tests/test_services.py::test_book_different_practitoner_same_time_allowed: 
        ValueError (practitioner conflict raised for a different practitioner)
    2.  tests/test_starter.py::test_conflict_rule_and_different_practitioner: 
        Failed: DID NOT RAISE ValueError (same practitioner at the same time was not rejected)
    3.  tests/test_services.py::test_cancel_scheduled_appointment: 
        LookupError: Appointment not found after cancelling
    4. tests/test_services.py::test_cancel_appointment_twice: 
        LookupError instead of ValueError on the second cancel

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: 
After a SCHEDULED appointment is cancelled its status becomes CANCELLED which is correct. However the appointment is no longer able to be found by its ID. Lookup raises LoopupError: Appointment not found. Trying to cancel the same appointment a second time also raises LookupError instead of being rejected as an illegal transition.

- Expected behaviour and requirement: 
The same appointment object stays in the store with the CANCELLED status and is still able to be returned by lookup, and cancelling it again raises ValueError. This comes from the requirements:
FR-06-08, BR-06-7, AC-5.1-5.3 and AC-06.1

- Minimal synthetic reproduction steps: 
1. Create a new SmartCareDataStore with the 3 services
2. Register patient P001 "test patient" and practitioner DR001 "test doctor", "general practice".
3. Book A001 for P001/D001 at 2026-11-10 10:00
4. Call cancel_appointment("A001").
5. Call find_appointment("A001"), it should raise a LookupError, where the A001 object was expected.
6. Call cancel_appointment("A001"), again and iss if it raises a LookupError where ValueError was expected.

- Meaningful failing test path/name and exact relevant failure: 
1.  tests/test_services.py::test_cancel_scheduled_appointment: line 211, 
    assert appointment_service.find_appointment("A001") is appointment,
    gives LookupError: Appointment not found, 
    raised at smartcare/services.py:141.

2. tests/test_services.py::test_cancel_appointment_twice: line 237, 
    the second cancel_appointment("A001") inside pytest.raises(ValueError), 
    gives LookupError: Appointment not found, 
    raised at smartcare/services.py:154.

- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour:
The practitioner conflict rule is working backwards. Booking a different practitioner at the same time as an existing appointment is rejected with "ValueError: Practitioner already has a SCHEDULED appointment at this time", while booking the same practitioner twice at the same time is accepted.

- Expected behaviour and requirement:
Only another SCHEDULED appointment booking for the same practitioner at exactly the same date and time should be rejected with ValueError. A different practitioner at that same date and time is allowed, this comes from:
FR-05, BR-05 AC-04.1 and AC-04.2

- Minimal synthetic reproduction steps: 
1. Create a new SmartCareDataStore and three services.
2. Register patient P001 and practioners DR001 and DR002.
3. Book A001 for Poo01/DR001 at 2026-11-10 10:00
4. Book A002 for P001/DR002 at the same time, it raises ValueError where a successful booking was expected.
5. Book A003 for P001/DR001 at the same time, it gets booked where ValueError was expected.

- Meaningful failing test path/name and exact relevant failure: 
1.  tests/test_services.py::test_book_different_practitoner_same_time_allowed: line 180, 
    booking A002 with DR002, gives ValueError: Practitioner already has a SCHEDULED appointment at this time, 
    raised at smartcare/services.py:127. This breaks AC-04.2.

2.  tests/test_starter.py::test_conflict_rule_and_different_practitioner: line 127, 
    with pytest.raises(ValueError) around booking A2 with the same practitioner D1 at the same time, 
    gives Failed: DID NOT RAISE ValueError. This breaks AC-04.1.

- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible:
SmartCareDataStore.has_practitioner_conflict(), checks to see if the practitioner already has an appointment, however it looks like the practitioner ID might be flipped around as. It checks if the practitioner ID matches a different practitioner instead of the same one. The rule fails in two ways as the same practitioner is allowed and a different practitioner is rejected. A missing or broken check should only cause one of those issues but one that been flipped around explains both.

Evidence intended to inspect / competing explanation / discriminating check: 
Evidence: has_practitioner_conflict() in smartcare/data_store.py, 
the prepared diff, and the call in AppointmentService.book_appointment().

Competing explanation: book_appointment() gives the wrong ID or datetime to the conflict check.

Discriminating check: After booking A001 with DR001, call store.has_practitioner_conflict('DR001', time) and store.has_practitioner_conflict('DR002', time). 
If they return False and True (flipped) the fault is in the store method.
If they return True and False (The right way around) the fault is in how the service calls it.

Member and saved sequence/time or commit showing this preceded consultation: 
Jack Gerbich, last commit was: 6f25ee3 (“Completed Stage 8 Parts A and B”, 2026-11-04). The next commit will include sections C, D and E as a time stamp before consultation.
Commit after sections C, D and E were completed but before consultation: debug/stage08 975cfa4

### F8-02 human entry
Likely cause and why plausible: 
SmartCareDataStore.find_appointment() is skipping over cancelled appointments. The same A001 lookup works while the appointment is SCHEDULED as cancel_appointment finds it, but fails afterwards once the appointment becomes CANCELLED. So the result depends on the status not the ID as both tests fail looking up the ID after its canceled.

Evidence intended to inspect / competing explanation / discriminating check:
Evidence: 
SmartCareDataStore.find_appointment(), 
the prepared diff git diff b50010b e356c85,
AppointmentService.cancel_appointment(),
Appointment.cancel()

Competinf explanation: Cancellation removes the appointment from the stores dictionary.

Discriminating check: After cancelling check whether A001 is still in store.list_appointments() and if the count had been changed. If it's still listed but find_appointment() returns None the lookup is hiding it. If its done something must be deleting it.

Member and saved sequence/time or commit showing this preceded consultation: 
Jack Gerbich, last commit was: 6f25ee3 (“Completed Stage 8 Parts A and B”, 2026-11-04). The next commit will include sections C, D and E as a time stamp before consultation.
Commit after sections C, D and E were completed but before consultation: debug/stage08 975cfa4

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

### F8-02 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [complete] | [complete] | [complete] |
| F8-01 after repair | [complete] | [complete] | [complete] |
| F8-02 before repair | [complete] | [complete] | [complete] |
| F8-02 after repair | [complete] | [complete] | [complete] |
| Full suite after both repairs, before refactor | [complete] | [complete] | [complete] |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: [complete]
Unrelated failures investigated / resolution: [complete or not applicable with reason]

## H. Refactoring decision and before/after verification

Smell and exact location: [complete]
Small proposed structural change / why justified: [complete before editing]
External behaviour to preserve / relevant tests: [complete]
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: [complete]

2. Where should expected behaviour come from during debugging?

Response: [complete]

3. What is a debugging hypothesis?

Response: [complete]

4. What is a regression test and why is it retained?

Response: [complete]

5. What is meant by root cause?

Response: [complete]

6. What is refactoring?

Response: [complete]

7. What is a swallowed exception?

Response: [complete]

8. What is a code smell?

Response: [complete]

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: [complete]

10. What is the Stage 8 engineering rule?

Response: [complete]

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]
