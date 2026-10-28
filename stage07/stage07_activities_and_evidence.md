# Stage 7 Testing and Verification Record

Group/tutorial: [complete]  Members/cohorts: [complete]
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test | Negative test | Key assertion |
|---|---|---|---|
| FR-01 Register patient | Register a new patient with valid, unique required fields (ID and Name) using PatientService. | Attempt to register a new patient with an existing ID or blank white space. | assert data_store.patient('P001') is patient (This verifies if value error is raised with the negative test).  |
| FR-05 Prevent practitioner conflict | Book two different practitioners as the same time or the same practitioner at  different times. | Attempt to book scheduled appointments for the same practitioner at the same date and time. | pytest.raises(ValueError) when the same practitioner is scheduled at same date and time. |
| FR-06 Cancel appointment | Cancel a valid, currently scheduled appointment using ID. | Attempt to repeatedly cancel an already cancelled appointment or use an unknown ID| assert appointment_status == AppointmentStatus.cancelled (If an Unknown ID is entered or a appointment is canceled a ValueError or LookupError should be raised). |
| FR-07 Retain cancelled history | Look up or query and appointment after it has been successfully cancelled. | Verify that a non-existent ID does not return historical data.  | assert data_store.find_patient('A001') is appointment while ensuring the appointment has been cancelled and not deleted completely.|

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: Weak/unclear  Why: This statement evaluates if true is true (which it always is), this can create issues in the system and doesn't test the application at all. 

`assert appointment is not None`
Judgement: Weak/unclear  Why: This statement checks whether the appointment variable contains an object and isn't empty, this means it tells you nothing about the object that was returned, so if it returned a blank or wrong appointment object it will pass creating issues with the system. 

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: Strong for stated behaviour  Why: It verifies if the status attribute of the Appointment object has successfully transitioned to CANCELLED and if it fails it remains Scheduled which ensures that the business logic actually works. 

`assert len(results) > 0`
Judgement: Weak/unclear  Why: This checks that the list named results has at least one item in it, but it fails to check whether or not the list contains the right data. 

`assert data_store.find_appointment('A1') is appointment`
Judgement: Strong for stated behaviour  Why: This checks whether the object returned by search the data store for 'A1' is the exact same in memory as your local appointment which proves that both the appointment is correct stored and that the correct records is being retrieved and stored. 

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract: 

1 Blank identifiers 
Input/State: Passing an empty string None as the ID when registering a patient/practitioner or booking an appointment.
Expected result: Raises a value error and leaves the data store unchanged
Supporting contract: 

2 Whitespace-only names
Input/State: Passes a string containing only spaces for a required name or specialty field. 
Expected result: Raises a value error
Supporting contract: 

3 Same-time practitioner bookings
Input/State: Attempting to book an appointment at the exact same time an appointment has been scheduled.
Expected result: Raises a value error due to a appointment conflict. 
Supporting contract: 

4 Cancelled appointments
Input/State: Looking up appointment ID after status has changed from Scheduled to Cancelled. 
Expected Result: The cancelled appointment remains retrievable and maintains its cancelled status. 
Supporting contract: 

5 Invalid Status transition
Input/State: Attempting to call cancel_appointment() to an already cancelled appointment.
Expected Result: Raises a value error and leaves the appointment state entirely unchanged. 
Supporting contract: 


### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate | What is wrong | Rewritten test intention |
|---|---|---|
| 1 | Weak assertion: Only asserts that an object is not None which fails to verify if the object contains correct data.  | Assert specific observable properties and attributes of the returned object to ensure it matches the expecteed registration data.|
| 2 | [Weak assertion: Only checks object if it is not none without validating state or buisness logic. | Assert precises state and attributes such as verify appointments intial status is SCHEDULED |
| 3 | Trivial assertion: Asserts TRUE which tests no application code or functionality and will always pass blindly. | Replace with meaningul tests that checks the codes functionality and logic. |
| 4 | Invented requirement: Assumes SMS notifcations exists, testing a feature that is out of scope. | Focus the test on strictly the outlined SmartCare requirements. |
| 5 | Invented requirement: Relies on checking an external/implemented notification service rather than public domain outcomes. | Align the intention with an actual acceptance criterion. |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
This is because code coverage shows which lines of code were executed instead of determing the correctness and quality of the reuqirement assertions. In other words you can execute 100% of your code with weak assertion meaning bugs go completely undetected.

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
|FR-01|AC-01.1|Test-FR01-01| Positive service test |project/tests/test_services.py::test_register_valid_patient| Valid patient data with unique ID is saved in data store. |Passed| Student Authored |
|FR-01|AC-01.2|Test-FRO1-02|Negative boundary test|project/tests/test_services.py::test_register_duplicate_patient_id|Attempting to register with an existing ID raises a ValueError|Passed|Student Authored|

|FR-05|AC-04.1|Test-FR05-01|Negative conflict test|project/tests/test_services.py::test_book_appointment_practitioner_conflict|Booking the same practitioner at the exact same datetime raises a ValueError|Passed|Student Authored|
|FR-05|AC-04.2|Test-FR05-02|Positive boundary test|project/tests/test_services.py::test_book_different_practitioner_same_time_allowed|Booking two different practitioners at the exact same time is permitted.|Passed|Student Authored|

|FR-06|AC-05.1|Test-FR06-01|Postive state change|project/tests/test_services.py::test_cancel_scheduled_appointment|Calling cancel on a SCHEDULED appointment updates its status to CANCELLED.|Passed|Student Authored|
|FR-06|AC-05.3|Test-FR06-02|Negative State test|project/tests/test_services.py::test_cancel_appointment_twice|Attempting to cancel an already cancelled appointment raises ValueError.|Passed|Student Authored|

|FR-07|AC-05.2|Test-FR07-01|Positive history test|project/tests/test_services.py::test_cancel_scheduled_appointment|Cancelled appointments remain retrievable via lookup and listed in store history.|Passed|Student Authored|

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|

| Test-DOM-01 | Domain Model (Patient) | AC-DOM-01 | Positive and Boundary | Verify valid patient construction and ID whitespace trimming. | Patient object successfully stores trimmed ID and correct name attributes. | Student Authored. |

| Test-DOM-02 | Domain Model (Patient) | AC-DOM-02 | Negative | Blank patient ID rejected (Reference intention). | Raises ValueError upon construction with empty or whitespace-only IDs. | Preserved reference intention |

| Test-DOM-03 | Domain Model (Practitioner) | AC-DOM-03 | Positive | Verify valid practitioner construction with required fields. | Practitioner object correctly retains ID, name, and specialty. | Student Authored |

| Test-DOM-04 | Domain Model (Practitioner)| AC-DOM-04 | Negative | Blank Practitioner ID rejected. | Raises ValueError when initialized with a blank ID. | Student Authored |

| Test-DOM-05 | Domain Model (Appointment)| AC-DOM-05 | Positive | A new appointment starts SCHEDULED (Reference intention) | Newly instantiated appointment defaults its status to AppointmentStatus.SCHEDULED. | Preserved reference intention|

| Test-DOM-06 | Domain Model (Appointment) | AC-DOM-06 | Positive | Cancellation changes status (reference intention) | Calling .cancel() successfully updates the appointment status to AppointmentStatus.CANCELLED | Presevered reference intention |

| Test-DOM-07 | Domain Model (Appointment) | AC-DOM-07 | Negative | Repeated cancellation is rejected (reference intention) | Raises ValueError when attempting to cancel an already cancelled appointment. | Preserved reference intention |

|Test-DOM-08 | Domain Model (Appointment) | AC-DOM-08] | Negative | Guarded cancellation on completed appointments | Raises ValueError when trying to cancel an appointment initialized with COMPLETED status. | Student authored |


## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| TEST-SRV-01 | Initialise a fresh SmartCareDataStore and AppointmentService. Capture the baseline appointment count (initial_count = len(store.list_appointments())). | Attempt to call appointment_service.book_appointment("A001", "NON_EXISTENT", "DR001", appointment_time) with an unregistered patient ID. | Catch the expected exception using with pytest.raises(LookupError): and verify that len(store.list_appointments()) == initial_count | Proves that failed service operations leave the data store in a secure, immutable state without creating partial or ghost records. |

| TEST-SRV-02 |Register two patients (P001, P002) and one practitioner (DR001). Book a valid initial appointment (A001) at a specific datetime.|Attempt to book a second appointment (A002) for P002 with the exact same practitioner at the exact same datetime.|Use with pytest.raises(ValueError): to verify the duplication attempt is rejected.|Proves that the service strictly enforces practitioner availability constraints and prevents double-booking.|

| TEST-SRV-03 |Register valid participants and successfully book a scheduled appointment (A001).|Invoke appointment_service.cancel_appointment("A001").|Assert that status updates to CANCELLED and that the appointment is still retained in session listings.|Proves that the cancellation workflow properly transitions operational states while preserving historical audit records.|


## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|

| Test-DOM-01 | Patient construction and trimming | project/tests/test_domain.py::test_patient_valid_construction_and_trimming | Passed

| Test-DOM-02 | Patient Blank ID rejection | project/tests/test_domain.py::test_patient_blank_id_rejected | Passed |

| Test-DOM-03 | Practitioner construction | project/tests/test_domain.py::test_practitioner_valid_construction | Passed |

| Test-DOM-04 | Practitioner rejection | project/tests/test_domain.py::test_practitioner_blank_id_rejected | Passed] |

| Test-DOM-05 | Appointment intial status | project/tests/test_domain.py::test_appointment_initial_status_scheduled | Passed] |

| Test-DOM-06 | Appointment cancellation state change | project/tests/test_domain.py::test_appointment_cancellation_changes_status | Passed|

| Test-DOM-07 | Appointment repeated cancellation guard | project/tests/test_domain.py::test_appointment_repeated_cancellation_rejected] | Passed |

| Test-DOM-08 | Appointment completed cancellation guard | project/tests/test_domain.py::test_appointment_completed_cancellation_guar | Passedd |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| TEST-SRV-01 | Patient registration, ID lookup, whitespace trimming, case-sensitivity, and invalid ID rejections. | Patient Service & Input Validation | project/tests/test_services.py (test_register_*, test_find_patient_*) | Passed |

| TEST-SRV-02 | Practitioner registration, ID lookup, whitespace trimming, case-sensitivity, and invalid ID rejections | Practitioner Service & Input Validation| project/tests/test_services.py (test_find_practitioner_*)| Passed |

| TEST-SRV-03 | Valid appointment booking, practitioner time conflict prevention, and valid alternative slot allowance. | Booking and conflict rules | project/tests/test_services.py (test_book_appointment_practitoner_conflict, test_book_different_practitoner_same_time_allowed) | Passed |

| TEST-SRV-04 | Failed service operations with unknown participants raise LookupError and leave data store state completely unchanged. | State immutability on failure | project/tests/test_services.py (test_unknown_participants_leave_state_unchanged) | Passed |

| TEST-SRV-05 | Cancelling scheduled appointments updates status to CANCELLED and retains history for session lookup.| Cancellation and history workflow | project/tests/test_services.py (test_cancel_scheduled_appointment | Passed] |

| TEST-SRV-06 | Cancellation guards reject repeated cancellations, completed appointments, unknown IDs, and invalid inputs. | Cancellation guards and error boundaries | project/tests/test_services.py (test_cancel_appointment_twice, test_cannot_cancel_completed_appointment, etc.) | Passed |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|

| Strict ID & Lookup Boundaries | Whitespace padding (" P001 "), case mismatch ("p001"), and invalid types (None, 123, "").| Whitespace is successfully trimmed to match valid records; case mismatches and invalid types raise ValueError or LookupError. | Prevents data from being lost during entity retrieval. |

| Duplicate Entries | Attempting to register an existing patient ID ("P001") with new data. | Raises ValueError; original record remains completely untouched and is not overwritten.| Prevents accidental data loss or silent overwriting of existing user profiles in the data store. |

| Practitioner Time Conflict | Booking two appointments with the exact same practitioner ("DR001") at the identical datetime(2026, 11, 15, 10, 0). | Raises ValueError; second booking is rejected and omitted from the data store. | Prevents double-booking medical professionals, which would cause clinical scheduling collisions and patient safety hazards.|

| Cancellation Status Guards & Illegal Transitions | Attempting to cancel an appointment twice, cancel a COMPLETED appointment, or use invalid/unknown IDs. | Raises ValueError or LookupError; appointment status remains locked in its current state (CANCELLED or COMPLETED). | Prevents illegal state machine transitions, audit history corruption, and repeated cancellation processing errors. |



## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: [complete]
Acceptance criterion: [quote]
Behaviour to test: [complete]
Human-first test idea/categories: [complete]
Prompt and purpose: [complete or link]

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: [complete]
- What it claims to verify: [complete]
- Requirement trace: [complete]
- Assertion quality: [complete]
- Human critique: [complete]
- Decision: [Accept / Modify / Reject]
- Reason: [complete]
- Final test reference if accepted/modified: [link or not retained]
- Actual verification result: [complete; do not claim an unrun test passed]

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? [response]
Why was it weak? [response]
How did you strengthen it? [response]
Accepted / modified / rejected test decisions and evidence: [link actual decisions in H]

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

Individual test runs and changed-order independence evidence: [commands, results, links]
Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: [concise links where applicable]

## K What the Suite Still Does Not Prove

What does your test suite still not prove? [response]
Coverage if used: [result or not used]
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? [response]
Optional fixtures/parametrisation used and why, if any: [response or not used]

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| [complete] | [complete] | [complete] |

## N Formative Questions

1. What question does verification answer?
[response]

2. What question does validation answer?
[response]

3. What is a unit test?
[response]

4. What is a pytest fixture?
[response]

5. What is parametrisation in pytest?
[response]

6. What is regression testing?
[response]

7. What does code coverage tell us, and what does it not prove?
[response]

8. What makes an assertion weak?
[response]

9. What is the appropriate role of GitHub Copilot as a test assistant?
[response]

10. What is the Stage 7 engineering rule?
[response]

## O Stage Completion

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
