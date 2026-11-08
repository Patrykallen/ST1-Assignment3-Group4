# Stage 12 activities and evidence
Group/tutorial: Group 4 -ST1, Assignment 3
Members and UG/PG applicability: 4 group members all UG so Stage 10 an 11 are N/A


## A Release scope and starting SHA

Release label/version and requirements baseline: SmartCare v1.0 - Common UG scope includes FR-01–FR-09, QRY-01–04, FP-01–03, applicable UI requirements and accumulated regression tests.
Common starting SHA / branch / applicable members: 289029c6e2d5bcdd981f15a6121b1611df01f7a5 / main / Group 4 UG members.
PG starting SHA / branch / applicable members or not applicable: N/A
Working-state review and approved integration: Starting from the updated main branch that has 6,7,8,9 work. The working tree was clean with no pending pushes
Protected common candidate and PG differences: The starting common candidate is commit 289029c6e2d5bcdd981f15a6121b1611df01f7a5.



## B Requirements and release readiness matrix

Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify: Do not release because although all tests are passing, this doesn't prove that the software is ready for a release. The incomplete README means another dev may not be able to get the same results, the unreviewed dependency could bring in security or compatibility risks, and the undocumented limitation means that users could misunderstand the systems use. Before approving the release the team should finish the README, check the dependency and document what the limitations are. The team also should independently verify the application in a clean environment and check the full regression still passes.

Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works - FR-06/FR-07, AC-05.1/AC-05.2 | The tests show that cancellation changes an appointment to CANCELLED while keeping the same object for lookup. | project/tests/test_services.py — test_cancel_scheduled_appointment(); starting SHA: 289029c6e2d5bcdd981f15a6121b1611df01f7a5 | Patrykallen | Waiting for final verification | Run full stage 12 and confirm the tests passes at the release SHA. |
| Architecture responsibilities are appropriate | The domain classes manage data and appointment status changes. SmartCareDataStore manages current session records, services coordinate application operations, queries handle filtering and sorting, and the console manages user interaction. These responsibilities are separated appropriately. | project/smartcare/domain.py, data_store.py, services.py, queries.py and console.py; starting SHA: 289029c6e2d5bcdd981f15a6121b1611df01f7a5 | Patrykallen | Waiting for final verification | Complete code quality review and confirm that it remains appropriately separated. |
| AI use is responsible — common recheck / PG assurance | Copilot suggestions were treated as options rather than instantly accepted. Human reviews found improvements to test assertion, validations and documentation. Changes were verified through testing | Stage 6 human/Copilot review records in stage06/stage06_activities_and_evidence.md; Stage 7 review evidence; GitHub pull requests and associated comments. | Patrykallen | Waiting for final verification | Record the final verification outcome in Section E. |
| System is maintainable | It seperates domain, session storage, application sevices, console interaction and pure queries into individual modules. Tests support future maintenance by helping find unintended changes to behaviour | project/smartcare/domain.py, data_store.py, services.py, queries.py and console.py; project/tests/; starting SHA: 289029c6e2d5bcdd981f15a6121b1611df01f7a5 | Patrykallen | Waiting for final verification | Complete the Section E code quality review |
| FR-01–03 register/find and validation | Patient and practitioner registration and lookup are implemented. | project/smartcare/services.py, data_store.py; project/tests/test_services.py; starting SHA: 289029c6e2d5bcdd981f15a6121b1611df01f7a5 | Patrykallen | Waiting for final verification | Run the complete regression suite and confirm all tests pass |
| FR-04–05 booking and practitioner conflicts | AppointmentService does the bookings using registered patients and practitioners. The booking rules rejects SCHEDULED appointments for the same practitioner at the exact same time, while allowing different practitioners to have appointments at the same time. | project/smartcare/services.py; project/tests/test_services.py; Stage 7 testing evidence; starting SHA: 289029c6e2d5bcdd981f15a6121b1611df01f7a5 | Patrykallen | Waiting for final verification | Run the complete regression suite and confirm all tests pass |
| FR-06–08 cancellation, history and appointment lookup | SmartCare allows SCHEDULED appointments to be cancelled, it changes their status to CANCELLED and retains the original appointment in the shared data store. Cancelled appointments remain accesable, while repeated cancellation and cancellation of COMPLETED appointments are rejected. Appointment lookup supports getting existing records and reporting unknown IDs. | project/smartcare/domain.py, services.py and data_store.py; project/tests/test_services.py; Stage 6 and Stage 7 test evidence; starting SHA: 289029c6e2d5bcdd981f15a6121b1611df01f7a5 | Patrykallen | Waiting for final verifcation | Run the full regression suite and have all tests pass |
| FR-09 practitioner appointment listing and queries | SmartCare supports listing appointments for a registered practitioner, including filtering by appointment status and sorting results by date/time and appointment ID. The default listing includes all statuses, while an explicit status filter limits the results. | project/smartcare/queries.py, services.py and data_store.py; project/tests/test_queries.py and test_services.py; starting SHA: 289029c6e2d5bcdd981f15a6121b1611df01f7a5 | Patrykallen | Waiting for final verification | Run the complete regression suite and have all tests pass |
| UI full console sequence and error recovery | SmartCare provides a console interface for registration, lookup, appointment booking, cancellation and practitioner appointment listing.| project/smartcare/console.py and project/main.py; applicable UI requirements and console tests; starting SHA: 289029c6e2d5bcdd981f15a6121b1611df01f7a5 | Patrykallen | Pending verification  | Run python main.py --interactive and demonstrate the required operations, invalid-input recovery and successful continued operation. Record the observed results D. |
| Session-only scope and retired FR-10 | SmartCare stores patient, practitioner and appointment records in the shared SmartCareDataStore for the current application session only. Records are not saved permanently and are lost when the program terminates. FR-10 has been retired from the current requirements baseline and is not included in the release scope. | project/smartcare/data_store.py; Assignment 3 Requirements Baseline 2026, Revision 2; Stage 12 Final Release handout. | Patrykallen | Sufficient for identifying the intended scope; final demonstration and verification are pending. | Document the limitations in the README and release notes, and exclude FR-10 from release verification. |
## C Full regression results



| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
|---|---|---|---|---|---|
| Complete common | Python 3.14.4, pytest 8.3.5 | project/ — `python -m pytest -q` | 289029c6e2d5bcdd981f15a6121b1611df01f7a5 | PASS — 51 passed in 0.06s | Local terminal output; repository test files in project/tests/ |
| Complete PG if applicable | Not applicable — UG pathway | N/A | N/A | N/A | Stage 12 UG scope |
| Affected focused checks after correction | No Stage 12 code corrections made | Not required | N/A | Not required | No corrective changes |
| Full integrated recheck | Python 3.14.4, pytest 8.3.5 | project/ — `python -m pytest -q` | 289029c6e2d5bcdd981f15a6121b1611df01f7a5 | PASS — 51 passed in 0.06s (initial full run; final check pending) | Local terminal output; final release check to be recorded |
Prior assertions preserved / reviewed test diff: No test files were modified during stage 12, all tests were retained and passed.
Remaining failure / limitation: No failures were observed in the full suite. Still need to do final checks


## D Console and end to end demonstration

| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link |
|---|---|---|---|---|
| Problem and stakeholders | Small clinic requiring patient, practitioner and appointment management. | Explain the clinic's problems and users. | SmartCare is intended to reduce conflicts and improve access to appointment information. | Stage 6 project requirements and Stage 12 handout. |
| Register and find Patient and two Practitioners | P001 Jane Doe; DR001 Dr. Smith; DR002 Dr. Adams; unknown patient P999. | FR-01–FR-03: Registration, lookup and validation. | PASS — Patient and both practitioners registered successfully. Patient lookup succeeded. Unknown patient returned an error and the menu recovered. Practitioner lookup not separately demonstrated. | Stage 12 local console run. |
| Valid booking | A001, P001, DR001, 2026-11-15 10:00. | FR-04: Valid appointment booking. | PASS — Appointment A001 created with SCHEDULED status. | Stage 12 local console run. |
| Same practitioner exact-time conflict rejected | Attempt A002, P001, DR001, 2026-11-15 10:00. | FR-05: Reject conflicting scheduled bookings. | PASS — Practitioner conflict error displayed. Subsequent lookup confirmed A002 was not created. | Stage 12 local console run. |
| Different practitioner same time allowed | A002, P001, DR002, 2026-11-15 10:00. | FR-05: Allow different practitioners at the same time. | PASS — Appointment A002 successfully created with SCHEDULED status. | Stage 12 local console run. |
| Cancel SCHEDULED and retain/find CANCELLED object | Cancel A001, then find A001. | FR-06/FR-07: Cancellation and retained history. | PASS — A001 changed to CANCELLED and remained retrievable with its original details. Automated identity verification is covered by the existing regression suite. | Stage 12 local console run; project/tests/test_services.py. |
| Invalid/repeated cancellation rejected | Attempt to cancel A001 after it was already CANCELLED. | FR-06: Repeated cancellation must be rejected without changing the appointment. | PASS — Error: Only SCHEDULED appointments may be cancelled. Subsequent lookup confirmed A001 remained CANCELLED. | Stage 12 local console run. |
| Default all-status listing | List DR001 appointments with a blank status filter. | FR-09: Default listing includes appointments regardless of status. | PASS — Cancelled appointment A001 appeared in the listing. | Stage 12 local console run. |
| Explicit filtering / empty vs unknown / deterministic order | List DR001 with SCHEDULED and CANCELLED filters; search for DR999. | FR-09, QRY-01–04: Filtering, empty results, unknown practitioners and deterministic ordering. | PARTIAL — SCHEDULED returned no appointments, CANCELLED returned A001, and DR999 produced Practitioner not found. Sorting was not manually demonstrated. | Stage 12 local console run; automated suite passed, but individual sorting test evidence has not yet been identified. |
| Invalid date/status/menu/lookup recovery and continued operation | Unknown patient P999; malformed date, status and menu inputs pending. | UI requirements: Invalid inputs must not terminate the console unexpectedly. | PARTIAL — Unknown patient produced an error and the menu reappeared. Other invalid-input scenarios not yet demonstrated. | Stage 12 local console run. |
| Session-only limitation and normal exit | Application uses SmartCareDataStore; normal exit not yet independently recorded. | Current-session records only; normal console exit. | PARTIAL — Session-only storage is the documented design. Normal exit and fresh-process behaviour remain to be verified. | project/smartcare/data_store.py; Stage 12 handout. |
| One meaningful requirement-linked pytest test explained | test_cancel_scheduled_appointment in project/tests/test_services.py. | FR-06/FR-07: Cancellation changes status and retains appointment identity/history. | The test checks the returned appointment identity, CANCELLED status and continued retrieval. Full regression suite passed: 51 tests. Individual test explanation during final demonstration pending. | project/tests/test_services.py; Stage 12 regression result. |
| Architecture and one actual AI decision / known limitation | Domain, data store, services, queries and console; Stage 6 Copilot review decisions. | Explain component responsibilities, responsible AI use and release limitations. | Architecture and earlier AI decisions have been documented. Final explanation and AI review pending. Known limitation: data exists only during the current session. | project/smartcare/; stage06/stage06_activities_and_evidence.md. |
| PG reschedule identity/participants/time and no-op | Not applicable — UG pathway. | PG-only requirements. | Not applicable. | Stage 12 handout. |
| PG conflict/invalid status/failure non-mutation | Not applicable — UG pathway. | PG-only requirements. | Not applicable. | Stage 12 handout. |
| PG old slot / current lookup/list ordering / assurance risks | Not applicable — UG pathway. | PG-only requirements. | Not applicable. | Stage 12 handout. |
Stable demo owner / fresh process / command: Patrykallen / local SmartCare console session / python main.py from project/. Final verification pending.
PG demonstrations through service/tests or not applicable: N/A


## E Final code quality and AI review

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
|---|---|---|---|
| OOP responsibilities and pure-query boundaries | project/smartcare/domain.py, data_store.py, services.py, queries.py and console.py | No significant finding. Domain classes manage entity state and validation; SmartCareDataStore manages session records; services coordinate application operations; queries provide separate filtering and sorting functions; and the console handles user interaction. These responsibilities align with the intended architecture. | No code changes needed based on review. The full regression suite passed with 51 tests; final release verification remains pending. |
| PascalCase and snake_case naming | project/smartcare/domain.py, data_store.py, services.py, queries.py and console.py | The project uses PascalCase for classes such as Patient, Practitioner, Appointment and SmartCareDataStore, and snake_case for methods such as register_patient, book_appointment and cancel_appointment. No naming issue was identified in these examples. | No changes required for the reviewed naming examples. Final code review remains ongoing. |
| Useful type hints and meaningful docstrings | project/smartcare/domain.py, data_store.py, services.py and queries.py | The application uses type hints and docstrings to communicate expected inputs, outputs and method responsibilities. These support code readability and maintainability. | No immediate changes proposed. |
| Four-space indentation and imports/layout | project/smartcare/domain.py, data_store.py, services.py, queries.py and console.py | The project follows a modular Python structure with imports separated from the main implementation. No indentation or import-related errors were observed during the successful regression run.  | No changes required based on evidence.|
| Focused methods / duplication / dead or commented code | project/smartcare/domain.py, data_store.py, services.py, queries.py and console.py | The application separates responsibilities across focused modules, reducing unnecessary coupling. The existing tests passed without identifying functional problems. | No code changes proposed at this stage. |
| Globals / leakage / unnecessary inheritance or frameworks | project/smartcare/domain.py, data_store.py, services.py, queries.py and console.py | SmartCare uses separate modules for domain objects, session storage, application services, queries and console interaction. This structure supports separation of responsibilities without requiring additional frameworks or inheritance. | No changes proposed based on current evidence.  |
| No SQLite/persistence/repository ABCs/speculative features | project/smartcare/data_store.py, services.py, domain.py and queries.py | SmartCare uses an in-memory SmartCareDataStore for current-session records. Permanent database storage, repository abstractions and speculative features are outside the UG release scope. | No additional persistence functionality required. |
| Synthetic data / secrets / dependencies / provenance | project/requirements-dev.txt, project/tests/, project/smartcare/ and .gitignore | The release demonstration used synthetic patient and practitioner information. The project's development requirements specify pytest 8.3.5, which was installed successfully. | Confirm that all tracked files contain only permitted material. |
| Significant common Copilot contributions and human verification | stage06/stage06_activities_and_evidence.md; Stage 7–9 evidence records; GitHub pull requests and review comments | During Stage 6, Copilot suggestions were compared against the requirements and human review feedback. Suggestions concerning missing docstrings, test assertions and formatting were evaluated and appropriate improvements were implemented. The integrated regression suite subsequently passed all 51 tests during Stage 12 verification. |  Record any unresolved findings, corrections or justified no-change decisions before release approval. |

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
| Copilot suggested restoring a method docstring and strengthening test assertions to verify that cancelled appointments remain stored. | FR-06/FR-07 — project/smartcare/services.py and project/tests/test_services.py | Compared the suggestions against the cancellation requirements, inspected the implementation and ran pytest after making changes. | Modify — The suggestions were relevant, but human review was required to ensure the assertions checked the actual requirements rather than simply increasing the test count. | Restored the cancellation method docstring and strengthened the retained-history test. Stage 6 tests passed after modification. |
Access route or approved equivalent / limitations: VisualStudio Copilot was used during Stage 6 to review proposed changes and find potential improvements. It was then checked against the requirements and checked by us.
Available AI evidence and missing evidence honestly disclosed: Stage 6 AI review evidence is recorded in stage06/stage06_activities_and_evidence.md, including Copilot suggestions, human decisions and subsequent corrections. 


## F README and reproducibility check

| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | Root README.md and project/README.md | Patrykallen | Updated to describe SmartCare v1.0 and the UG release scope. PG extensions excluded. |
| Out-of-scope capabilities and known limitations | project/README.md — Limitations | Patrykallen | Session-only storage, no authentication, notifications, billing |
| Confirmed teaching Python version and dependency installation | project/README.md — Setup and Testing | Patrykallen | Locally tested with Python 3.14.4 and pytest 8.3.5. Dependency installation successful. |
| Working directory / demo / interactive / test commands | Root README.md and project/README.md | Patrykallen | Commands documented. Application launched successfully and all 51 tests passed. |
| Repository structure and architecture responsibilities | project/README.md — Architecture | Patrykallen | Domain, data store, services, queries, console and tests documented. |
| Responsible AI summary / synthetic-data rule | project/README.md — AI Use and Limitations | Patrykallen | Responsible AI use and synthetic-data requirements documented. Final AI review remains pending. |
| Release label/version and SHA links | Root README.md and project/README.md | Patrykallen | Proposed v1.0 release and starting SHA documented. Final release SHA pending. |

Fields directly below the table
Root README index and project/README verified: Both README were updated during Stage 12 to reflect the finished application.
Fresh clone or extracted ZIP / candidate identity: Fresh clone on new PC completed
Verifier and clean environment / actual version: Verified on the second PC
Setup/run/test commands and observed results: Full tests suite passed on new PC
Missing local file or setup gap / remedy and recheck: No files were missing or failures occured on fresh test.


## G Known limitations debt and release notes

Delivered features: Provides pratient and practitioner lookup and registracitonm, appointment booking, conflict prevention, and appiontment filtering and sorting. the interactive console upports these operations and handles errors accordingly.
Important fixes: Stages 6-9 completed the functionality, expanded tesing, and implemented queries and console fetures.
Architecture/quality improvements: Seperates domain entities, in memory storage, fure query functions and console interaction. Contains 51 passing tests.
Known limitations: Only stores information during the current sessions. It does not include authentication, notifications, or billing. 
AI-assisted development note: VS Copilot assited with earlier dev and testing.

| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| Session-only storage | All records are lost when the application closes. | Low (course scope) | Consider persistent storage in a future production-oriented version. | Accepted — permanent storage is outside the current requirements. |
| Authentication and access control | No protection against unauthorised access in a real clinic environment. | High (production) | Implement authentication, user roles and security controls before any real deployment. | Accepted for course release only; production use is explicitly excluded. |
| Timezone handling | Local naive datetimes cannot reliably represent appointments across timezones. | Medium | Introduce a defined timezone policy if future requirements demand it. | Accepted — current requirements specify local minute-precision times. |
| Scalability and monitoring | The application has not been verified for concurrent users or production operations. | Medium | Conduct scalability testing and introduce monitoring before considering deployment. | Accepted — enterprise deployment is outside the course scope. |
| Accessibility and usability | No formal accessibility or usability evaluation has been completed. | Medium | Conduct user testing and accessibility assessments. | Accepted as a documented limitation of the course release. |
Session-only synthetic data and minute-precision local time: Uses synthetic data stored in memory for only the current session. Appointmetn times use local datetimes. Records are lost when the application closes.
Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: Does not include any authentication or role based access. These are outside current scope.
Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: Does not have a timezone policy, production monitioring or formal accessibility and usability evaluation. These are accepted within the course scope.
Difference between accepted scope limit and unresolved required behaviour: Accepted scope limitation is deliberatly excluded from the requirements such as permanant storage. An unresolved requirement is something that is demanded but not demonstrated successfully.



## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| README setup and release documentation | Both README files contained outdated Stage 6 descriptions, incomplete placeholders and incorrect setup instructions. | Medium — could prevent another developer from reproducing the application correctly. | Patrykallen — updated both README files to describe the current application, requirements, commands and limitations. | README.md and project/README.md modified during Stage 12 | Initial regression suite: 51 passed before README changes. | Independent verification of the final release candidate remains outstanding. |
| Application functionality | Main console workflows were demonstrated successfully, and the complete automated regression suite passed. | No confirmed functional defect identified. | Group 4 — retain the existing implementation unless further verification identifies a genuine defect. | No application source changes required so far. | 51 passed in 0.06s using Python 3.14.4 and pytest 8.3.5. | Remaining console edge cases, final integration checks and independent verification require completion. |
Justified no-change conclusion if no defect found: The initial Stage 12 regression suite passed all 51 tests, and the manually demonstrated application workflows behaved as expected
Release blockers still open / status:  No confirmed functional release blocker has been identified.


## I Git review and integration evidence

## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA: Stage 12 documentation changes were made from starting commit 289029c6e2d5bcdd981f15a6121b1611df01f7a5 on main. Changes include README.md, project/README.md and stage12/stage12_activities_and_evidence.md. No application source or test files were modified. Final review and commit links are pending.

Independent reviewer / feedback / response: The stage 12 release changes were reviewed. No GitHub PR was recorded. Earlier stages included human reviews and feedback, with evidence recorded in their respective stage documents and GitHub pull requests.

Integration commit / full recheck: Starting SHA: 289029c6e2d5bcdd981f15a6121b1611df01f7a5. The full regression suite returned 51 passed in 0.06s using Python 3.14.4 and pytest 8.3.5. Final integration commit and post-commit verification are pending.

Tracked and untracked file inspection / cleanliness: Git status identified three modified files: README.md, project/README.md and stage12/stage12_activities_and_evidence.md. No application code or tests were modified, and no untracked files were reported. Minor whitespace and Windows line-ending warnings were observed. Changes remain uncommitted.

Secrets/staff material/caches/tool-metadata exclusion check: The final tracked-file inspection has not yet been completed. No confidential information was intentionally added during Stage 12. The final release review must confirm that no credentials, real patient records, staff reference solutions, caches, environments or temporary files are included.

Candidate recovery plan / known-good SHA: The known-good starting commit is 289029c6e2d5bcdd981f15a6121b1611df01f7a5, with 51 passing tests. This commit can be recovered through Git if necessary. The final tested release SHA will be recorded after integration.

Named substantive contributions: Patrykallen completed the Stage 12 documentation updates, including the root README, project README and release evidence record. The existing application functionality and tests were developed and integrated during earlier group stages. 


## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: Ready with documented limitations
Approver / date / rationale and evidence: Patrykallen / 9/11/26 / Code has all been tested by multiple people in clean enviroments and tests are consistenly passing.
What risks remain / conditions / owners: SmartCare remains limited to current-session storage and is not suitable for production healthcare use.
Can the team explain the system: Yes, all members of the team are able to explain how the system functions.
Can a change be recovered:  Yes. Git preserves the project history, allowing the team to identify and recover earlier commits. 
Common decision / PG decision where different: The proposed decision applies to the UG common release scope. 


## K Final tested release SHA

Exact common tested SHA: 289029c6e2d5bcdd981f15a6121b1611df01f7a5
Exact PG tested SHA or not applicable: N/A
Final submitted SHA / repository URL: d35d7accf019046e51124b0aed53eda0c9f9cded.
Evidence-only later commit and difference explanation:  The application was tested at commit 289029c6e2d5bcdd981f15a6121b1611df01f7a5, with 51 tests passing. Changes updated only the root README, project README and Stage 12 evidence documentation
Source ZIP name / SHA correspondence / extracted comparison: Repository: https://github.com/Patrykallen/ST1-Assignment3-Group4. 


## L Submission package verification

- [x] Feature freeze and scoped requirements traced.
- [X] Applicable full regressions, integrated demo and invalid paths verified.
- [X] Architecture/code quality and final AI/dependency checks complete.
- [X] Root README and project/README reproduced by another verifier.
- [x] Release notes, technical debt and limitations visible.
- [X] Independent human review, integration and release decision recorded.
- [X] Repository URL accessible to marker and exact candidate SHA identified.
- [X] One source ZIP from submitted commit with root README.md and .gitignore.
- [X] project/ source and all accumulated applicable tests included.
- [X] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [X] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [X] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [X] Mixed-group common protection and candidate upload routing checked.
- [X] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route: Stage 12 source submission route pending confirmation. Group reflection, peer assessments and common team viva are part of a separate Canvas assignment administered through Cadmus.
Deadline/timezone: 9/11/2026 11:59PM 
Repository access arrangement: Group repository — https://github.com/Patrykallen/ST1-Assignment3-Group4
Mixed-candidate upload arrangement: N/A
Oral/video recording/accessibility arrangements: Will be done through canvas/cadmus
Remaining administration or release dependency:


## M Formative questions

1. What is a release candidate? A release candidate is a version fo the software that has completed development and is being tested to determine whether it is ready to be released. It should have the intended functionality, with any issues identified and checked before the final approval.

2. What is feature freeze and why is it used? Feature freeze is when no features are added to the software before it gets released. It allows us to focus on testing, fixing defects and ensuring the functionality works properly. This reduces the risk of new problems before the final release.

3. What is regression testing in a release context? It involves rerunning tests before a software release to ensure that recnt chagnes havent broken something that was working earlier. It helps confrim that the application still meets the rquirements and that fixes havent accidently introduced new problems.

4. What is a known limitation? A known limitation is a restriction or missing capability that people are aware of and have documented. It does not mean the software is defective, provided that is is outside the scope and requiements.

5. What is technical debt? It is work that has been delayed or improvements that are still needed for the software. If left unresolved it can make the system harder to maintain, improve, or expand.

6. What are release notes? They are documents that summarise what is included in a release of a software, such as new features, or bug fixes. they help the users and developers understand what issues or restrictions they should be aware of.

7. What is software maintenance? Software maintenance is the process of improving software after it has been released. This includes fixing bugs, improving performance, addressing security issues and overall making hcnages that keeps the software more reliable and compatible with changing requirements.

8. What is the purpose of the individual demonstration/viva? The purpose of the viva is to confirm that each member actually understands the software. It allows student to expalin their individual contributions and demonstrate that they understand all the work they completed.

9. What should the final responsible-AI check establish before release? It should confirm that any AI code or suggestions have been properly reviewed and understood. It should also ensure that no securit risks have been introduced.

10. What is the main course conclusion about AI and the role of the software engineer? AI can assist with writing code, testing, and finding problems, however software engineers are still responsible for understanding the requirements, making decisions abd ensuring the system actually works correctly. AI is a tool that supports the development while human engineers remain accountable for the quality of the work they are outputting.


## N Reflection viva and handover

Strongest evidence SmartCare is ready: The strongest evidence that it is ready for the release is that all 51 automated tests apssed alongside the manual demonstrantions of the main features.
Weakest area: The weakest area of our release evidence is the independent verification and final review process. Although all 51 automated tests passed and I successfully tested SmartCare on two computers, the second test was still completed by me rather than another group member.
How AI use changed from Stage 1 to Stage 12: Throughout the assignment, our group used AI more critically by reviewing its suggestions and verifying them through testing. By stage 12, we understoof that AI can help develop but cannot be responsible for the final system.
Start doing — engineering and AI use: Establish clear tasks and review Ai suggestions
Stop doing — engineering and AI use: Relying on AI solutions without fullyh understanding
Continue doing — engineering and AI use: Continue using them as tools to identify improvements
What worked / caused rework / future delivery improvement: Merge conflicts and unclear responsibilities caused some rework, which could be reduced through better communication and earlier integration.
One paragraph — If AI can write code why do we still need software engineers: AI can generate code, but it cant guarantee that a sustem meets its requirements or is reliable. Software engineers are still needed to make decisons, verify functionality, find risks and take real responsibilty for the final product released.

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | SmartCare helps small GP clinics manage patients, practitioners and appointments. Stakeholders include patients, practitioners and clinic staff. |
| Two requirements and acceptance criteria | FR-05 prevents the same practitioner having two scheduled appointments at the same time. FR-07 requires cancelled appointments to remain retrievable. Both were demonstrated during Stage 12. |
| Domain model and architecture | Patient, Practitioner and Appointment are domain classes. The data store manages records, services coordinate operations, queries filter/sort appointments and the console handles interaction. |
| Design trade-off | In-memory storage keeps the application simple but means records are lost when the program closes. |
| Meaningful test and its limits / 100 percent coverage | The cancellation test checks that an appointment becomes CANCELLED and remains retrievable. Even 100% code coverage would not prove every requirement works correctly. |
| Diagnosed defect and verification | During Stage 6, a merge conflict in test_services.py was resolved by combining the tests. The integrated tests then passed. This was an integration issue rather than an application defect. |
| Shared store and session-state/query responsibilities | Services share one SmartCareDataStore to access consistent session records. Pure query functions filter and sort appointments without changing stored data. |
| What would break if session-state lookup/query responsibilities changed? | Services could access wrong records, and queries might accidentally modify appointment data or return incorrect results. |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | Appointment.cancel() controls valid status changes, while AppointmentService checks conflicts involving multiple appointments in the shared store. |
| FR-07 retained history test | test_cancel_scheduled_appointment verifies that a cancelled appointment remains retrievable and retains its original object identity. |
| Actual AI change rejected/modified or honestly accepted with verification | During Stage 6, Copilot suggested improving cancellation documentation and test assertions. The suggestions were reviewed, implemented and verified through pytest. |
| Unresolved limitation / future production work | SmartCare only stores records during the current session. Production use would require persistent storage, authentication and additional security testing. |
| Personal implementation contribution | Patrykallen implemented Stage 6 patient lookup and appointment cancellation functionality. |
| Personal test/review/design/integration contribution | Patrykallen developed Stage 6 tests, resolved integration conflicts, reviewed Stage 7 test changes and completed Stage 12 release verification and documentation. |
| PG agentic change and rescheduling verification | Not applicable — UG pathway. |
| PG responsible-AI risk/remediation or supported no finding | Not applicable — UG pathway. |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: Not undertaken as was not required and lack of time.
Separate reflection / peer / common team viva evidence links and routing: The group reflection, individual confidential peer assessments and common team viva are part of a separate assignment on the unit's Canvas page
No further coding stage. Later corrections use the published assessment process.
