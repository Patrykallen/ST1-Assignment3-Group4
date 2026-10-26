# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Wednesday 2:30 - 4:30
- Members, GitHub usernames and cohorts: Patryk, Muthuraman, Jack
- Repository URL: https://github.com/Patrykallen/ST1-Assignment3-Group4
- Starting SHA: ad4e7caa803758e440dbbe395cd4e3cfd6678ddf

## A Requirement to issue activities

### FR-02 Patient Search

- Title: FR-02 Find an existing patient by ID
- Context: SmartCare needs to retrieve the patients who have already been registerd.
- Requirement: Implement PatientService.find_patient(patient_id) to locate and return the stored patient object
- Acceptance criteria:
    - A valid patient ID returns the same patient object.
    - Whitespace surrounding the ID is ignored
    - Patient ID are case sensitive
    - An unkown but valid ID raises a LookupError.
    - A blank or invalid ID raises a ValueError
- Scope: Implement the existing patient lookup method using the given SmartCareDataStore. Do not add any new search features, storage systems or dependencies.
- Definition of Done: THe method hits all acceptance criteria, relevant tests pass, the original tests remain passing, and other people have reviewed and approved it
- Owner: Patrykallen
- Actual issue link: https://github.com/Patrykallen/ST1-Assignment3-Group4/issues/2

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: FR-06/FR-07 - Cancel appointments while retaining the history
- Context: SmartCare needs to allow the scheduled  appointments to be cancelled while keeping their record available for furture lookups.
- Requirement: Implement AppointmentService.cancel_appointment(appointment_id) using the existing domain cancellation method. Cancelled appointments must remain stored and retrievable at any time.
- Acceptance criteria: 
    - A scheduled appointment can be cancelled and its status becomes CANCELLED
    - The method returns the same Appointment object
    - Cancelled appointments remain accessible from the data store.
    - Cancelling an already cancelled appointment returns a ValueError
    - Cancelling a completed appointment raises a ValueError
    - Unknown appointment ID's return a LookupError
    - Blank appointment ID's raise ValueError
    - Failed cancellation attempts do not change the existing status
- Scope: Implement the cancellation service method using the supplied data store and Appointment.cancel(). DO not modify protected status attributes, delete appointments or introduce any new dependencies.
- Definition of Done: All acceptance criteria are covberd by tests, the original eight tests continue to pass, another member reviews and approves the changes.
- Owner: Patrykallen
- Actual issue link: https://github.com/Patrykallen/ST1-Assignment3-Group4/issues/3

## B Commit quality

| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | Weak | Too vague and doesnt explain what was changed |
| final version | Weak | Doesnt identify what was added or modified |
| Add patient search by ID | Strong | Clearly describes the feature that was implemented |
| fix stuff | Weak | Does not explain what was fixed or why it needed to be fixed |
| Prevent cancellation of completed appointments | Strong | Clearly describes a behaviour that was corrected |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: The PR includes changes unrelated to appointment cancellation, making it too large and difficult to review
- Responsibility and architecture concerns: Renaming patient fields and restructuring unrelated code could affect other parts fo SmartCare system. The new dependency may add more complexity, especially when the domain and service classes already support cancellation.
- Testing and review concerns: The unrelated changes could introduce some errors in existing functionality. Passing tests alone does not mean all changes are correct, so the reviewer must inspect the actual code changes and check for unintended effects.
- Changes to remove or separate, with reasons: Keep only the appointment cancellation implementation and its relevant tests in this PR. Move the unrelated patient field changes and restructuring into separate issues and PRs. Remove the new dependency unless it is genuinely needed and approved.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: Copilot hasnt shown which tests were ran, what the results were, or whether anyh code meets teh acceptance criteria. It also hasnt checked the changes for unrelated modifications or incorrect responsibilities.
- Follow-up review question 1: Which tests were ran, and what evidence shows they passed?
- Follow-up review question 2: Does Patient search return the original store Patient object rather than making a new one?
- Follow-up review question 3: Does appointment cancellation use the existing Appointment.cancel() method instead of modifying the status directly?
- Follow-up review question 4: Are cancelled appointments retained as required by FR-07?
- Follow-up review question 5: Does the PR contain any unrelated changes or new dependencies that arent necessary for the requirement?
- Additional questions if useful: Do the tests verify object identity and unchanged state after a failed cancellation? Are invalid IDs and illegal appointment traintions handled with the correct exceptions?

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | Use Clear names that cover the main goal of your task |
| Commit message convention | Use short, descriptive messages explaining the chances, such as Add Patient lookup by ID |
| PR size | Each pull request should be focused on one requirement or a small related change |
| Another-member review requirement | Every PR must be reviewed by at least one other memeber. Members cannotapprove their own PRs. |
| Merge rule | You can only merge when all relevant tests have pass, review feedback has been resolved, and a member has approved the PR |
| Significant Copilot disclosure rule | Record all meaningful Copilot assistance, including what was suggested, whether it was used, and how it was verified |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| [issue 1] | FR-02 | Patrykallen | https://github.com/Patrykallen/ST1-Assignment3-Group4/issues/2 | Open |
| [issue 2] | FR-06/07 | Patrykallen | https://github.com/Patrykallen/ST1-Assignment3-Group4/issues/3 | Open |
| [issue 3] | FR-03 | Patrykallen | https://github.com/Patrykallen/ST1-Assignment3-Group4/issues/4 | Open |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: https://github.com/Patrykallen/ST1-Assignment3-Group4/pull/5 - FR02: Implement patinet search by ID with tests
- Linked issue and requirement: https://github.com/Patrykallen/ST1-Assignment3-Group4/issues/2 - FR02 Patient Search
- Feature branch: feature/fr02-patient-search
- Changed behaviour: Implemented patient lookup
- Meaningful commits: Docstring correction implementation
- Test command, directory and observed result: python -m pytest from project/ — 16 passed on the feature branch
- Another-member reviewer: Muthuraman
- Human observations recorded before Copilot: https://github.com/Patrykallen/ST1-Assignment3-Group4/pull/5#issuecomment-6416459455
- Requirement, responsibilities, test assertions and unrelated-scope checks: Tests verify object identity, unknown IDs, whitespace, case sensitivity and invalid IDs. No unrelated functionality was intentionally changed.
- Key feedback: Clarify how whitespace and caps are handeled
- Author response/change and verification: Explained that whitespace is trimmed but ID intentially remain case sensitive. Added the docstring after the copilot review and ran tests with 16 passing 
- Reviewer recheck and approval: Given Approval by Muthuraman to merge
- Merge outcome and SHA: 7a260a5c4b36ad5769dfdaf4a46ba8f6cdd04cf3
- Significant Copilot assistance: Copilot reviewed the diff, found no concerns and suggested adding docstring
- Linked issue closure: Open
- Each member updated main: Done
- Integrated verification after merge: python -m pytest from project/ — 16 passed full sha:0df34594b539952faf9c9814ef28bc7278559088.

FR-03
- PR link and title: https://github.com/Patrykallen/ST1-Assignment3-Group4/pull/6 — Implement practitioner lookup by ID with tests
- Linked issue and requirement: https://github.com/Patrykallen/ST1-Assignment3-Group4/issues/4 - FR-03 supporting practitioner lookup
- Feature branch: feature/practitioner-lookup
- Changed behaviour: Implemented Practioner search.
- Meaningful commits: Commited Copilot improvements
- Test command, directory and observed result: python -m pytest from project/ — 16 passed on the original feature branch
- Another-member reviewer: Muthuraman
- Human observations recorded before Copilot: https://github.com/Patrykallen/ST1-Assignment3-Group4/pull/6#issuecomment-6416202668
- Requirement, responsibilities, test assertions and unrelated-scope checks: Uses data store to validate and lookup IDs. Tests verify object identity, trimmed IDs, case sensitive, error handling. No new dependencies were added
- Key feedback: The human reviewer identified no necessary changes.
- Author response/change and verification: Accepted both Copilot suggestions
- Reviewer recheck and approval: Given approval to merge by Muthuraman
- Merge outcome and SHA: f9f8ce3bfae7fd0f2088d8a2c7e17969d9959e34
- Significant Copilot assistance: Reviewed diff, found no concerns, reccomeneded optional changes
- Linked issue closure: Open
- Each member updated main: Done
- Integrated verification after merge: python -m pytest from project/  - Final sha:0df34594b539952faf9c9814ef28bc7278559088.

- PR link and title: https://github.com/Patrykallen/ST1-Assignment3-Group4/pull/7 — FR-06/FR-07: Implement appointment cancellation with retained history
- Linked issue and requirement: https://github.com/Patrykallen/ST1-Assignment3-Group4/issues/3
- Feature branch: feature/fr06-appointment-cancellation
- Changed behaviour: Implemented Cancel appointments
- Meaningful commits: Commited Copilot changes
- Test command, directory and observed result: python -m pytest from project/ — 16 passed on the original cancellation branch
- Another-member reviewer: Muthuraman
- Human observations recorded before Copilot: https://github.com/Patrykallen/ST1-Assignment3-Group4/pull/7#issuecomment-6408058370
- Requirement, responsibilities, test assertions and unrelated-scope checks: ancellation uses the existing domain transition rather than directly changing protected status. No new dependencies were introduced.
- Key feedback: Human reviewer suggested making the error messages more informative and clarification of cancellation reutrn behaviour. Copilot found missing docstring, whitespaces, and an extra assert that improved the tests.
- Author response/change and verification: Explained that cancellation returns the original Appointment object and that invalid transitions raise ValueErrors. The updated branch passed 16 tests. Resolved the test_services.py merge conflict while retaining all three feature test sets, then observed 32 passing tests.
- Reviewer recheck and approval: Given approval by Muthuraman to merge
- Merge outcome and SHA: 0df34594b539952faf9c9814ef28bc7278559088
- Significant Copilot assistance: Reviewed diff, found no concers, gave optional improvements
- Linked issue closure: Open
- Each member updated main: Done
- Integrated verification after merge: python -m pytest from project/ - Final sha:0df34594b539952faf9c9814ef28bc7278559088.

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: Patrykallen - FR-02 Patient Search review
- Prompt/purpose and relevant issue/diff: Used GitHub Copilot to review the FR-02 PR diff against the requirements, acceptance criteria, existing SmartCare architecture and the tests.
- Summary of output: It found no Important Issues. It identified that the implementation satisfies FR-02 and that the tests covered all required scenarios. It also noticed that the find_patient method was missing a docstring and said it should be restored
- Human check against actual code, requirements and tests: Verified the method uses the supplied SmartCareDataStore, returns the original Patient object and handles invalid/unknown IDs correctly. Checked the docstring recommendation against the assignment guidelines.
- Decision — Accept / Modify / Reject: Accept
- Reason: Adding the docstring improves the readablity and documents the expected behaviour.
- Verification/evidence: Restored the docstring and ran python -m pytest from project/. Observed result: 16 passed

- Member and task: Patrykallen - Practitioner
- Prompt/purpose and relevant issue/diff: Asked GitHub Copilot to review the Practitioner Lookup PR diff against the Stage 6 acceptance criteria
- Summary of output: Copilot found no concerns. It found two optional improvements: adding the docstring and checking that unsuccessful practitioner lookups dont create new records.
- Human check against actual code, requirements and tests: Verified that existing data store does ID validation adn lookup, and that the service raises LookupError for unknown IDs. Checked both suggestions with Stage 6 requirements and confirmed that they would improve the tests and documentation without changing the behaviour
- Decision — Accept / Modify / Reject: Accept
- Reason: The docstring says what the method does, while the extra assertion verifies that wrong lookups leave the practitioner store empty
- Verification/evidence: Added the docstring and added an assertion using store.list_practitioners() to check that no records were created. Ran pytest and had 16 tests passed.

- Member and task: Patrykallen - FR-06/07 Appointment Cancellation PR review.
- Prompt/purpose and relevant issue/diff: Asked GitHub Copilot to review the appointment cancellation PR diff against FR-06 cancellation, FR-07 retained history
- Summary of output: Copilot found no issues. It identified three optional improvements:adding a docstring, removing whitespace, and adding an assertion that cancelled appointments remain the the data store appointment list.
- Human check against actual code, requirements and tests: Verified that cancellation uses Appointment.cancel() method, returns the stored object and retains cancelled appointments. Confirmed that the changes improve it without changing the needed functionality.
- Decision — Accept / Modify / Reject: Accept
- Reason: The changes improve clarity and provide stronger verifcation without altering behaviour.
- Verification/evidence: Added the docstring, added an assertion using store.list_appointments() and ran pytest with 16 passed.

## I Human versus Copilot review comparison
FR-02
- Human reviewer noticed before consulting Copilot: Muthu identified that the method handled unknown ID using LookupError and that the tests covered the whitespace case sense etc. He also questioned whether spaces and caps were handled automatically
- Copilot noticed: It found no issues. All it found was that find_patient() was missing a docstring
- Overlap: Both reviews considered ID validation
- What did the human reviewer notice that Copilot did not: The human questioned whether the implementation cleaned or normalised caps. This led to carifaction that whitespace was getting trimmed but ID remained case sensitive on purpose.
- What did Copilot identify that the human reviewer initially missed: Copilot found that there was a missing docstring.
- Unsupported or incorrect Copilot suggestion: None, All suggestions were consistent with the Stage 6 requirements and it said that it could not verify the test results itself.
- Human judgement accepted, modified or rejected, and why: Accepted the idea to add the docstring because it improves the readability. 
- Which evidence justified merge approval: The FR-02 implementation and all 16 tests being passed. Muthus review observations, and the Copilot comparison support the changes.

FR-03
- Human reviewer noticed before consulting Copilot: Muthu reviewed the find_practitioner() use and identified that LookupError was used well for missing practitioners. He also said the testss were good for covering whitespace, Invalid, missing IDs
- Copilot noticed: It found no issues. It identified two optional improvements: added the docstring and adding an assertion that unsuccessful lookups dont create records.
- Overlap: Both reviews found appropriate error handling and test coverage for lookup
- What did the human reviewer notice that Copilot did not: No issue was found that the Copilot missed. Both recognised good error handling and relevant test coverages.
- What did Copilot identify that the human reviewer initially missed: It noticed a missing docstring and suggested adding testing for unsuccessful lookups.
- Unsupported or incorrect Copilot suggestion: None, Both suggestions were aligned with Stage 6 requirements.
- Human judgement accepted, modified or rejected, and why: Did both suggestions because they improve the documentation and coverage of tests without changing the required functionality.
- Which evidence justified merge approval: All reviews found no issues occuring and all tests were passed.

FR06/07
- Human reviewer noticed before consulting Copilot: Muthu suggested including the appointment ID in the LookupError message to improve debugging. He laso asked whether cancellation should return a boolean or use and exception to distinguish unsuccessful cancellation from other appointment states.
- Copilot noticed: It found no issues. It confirmed that the service uses Appointment.cancel(), returns original stored object and keeps cancelled appointments. It suggested adding docstring, removing whitespace and adding an assertion.
- Overlap: Both reviews considered behaviour of cancellations, error handling and whether the implementation was clear
- What did the human reviewer notice that Copilot did not: Suggested including the ID in the exception message to assist in debugging. He also raised potential issues with returning a boolean, which Copilot didnt see as a problem
- What did Copilot identify that the human reviewer initially missed: Identified it was missing a docstring, had unnecessary whitespace and could use another assertion
- Unsupported or incorrect Copilot suggestion: All suggestions were consistent with the Requirements
- Human judgement accepted, modified or rejected, and why: Accepted two of the suggestions made by Copilot but let the method continue returing the original appointment object rather than a boolean as specified by the contract and also did not include ID in exception msg's
- Which evidence justified merge approval: The implementation follows the cancellation rules, and all the tests pass correctly, no major issues were flagged by anyone meaning it should be good to merge

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: Patryk 
- Implementation: Implemented PatientService.find_patient(), PractitionerService.find_practitioner() and AppointmentService.cancel_appointment() on three separate feature branches. 
- Testing: Created tests in test_services.py for patient lookup, practitioner lookup and appointment cancellation
- Review: Awaiting another member reviews of the three pull requests. No completed review contribution to report yet.
- Issue refinement: Created three GitHub issues covering FR-02 Patient Search, FR-06/FR-07 Appointment Cancellation and the FR-03 supporting practitioner lookup operation. Included acceptance criteria and Definitions of Done.
- Design and responsibility discussion: Followed the supplied SmartCare architecture by keeping lookup coordination in the service classes, using the shared data store and leaving appointment status transitions with the domain object.
- Debugging or integration: Identified and corrected an indentation error in find_patient() after a test raised AttributeError.
- Documentation or team support: Completed the Stage 6 requirement drafts, tutorial questions and team workflow documentation. Created the shared GitHub repository and arranged access for the other group members.

Member: Muthuraman
- Implementation: Not applicable
- Testing: Reviewed test coverage in the three pull request
- Review: Reviewed FR-02, FR-03, FR06/07. Commented on error handling, whitespace and case sensitivty
- Issue refinement: N/A
- Design and responsibility discussion: Asked about ID normalisation, error handling, and invlaid cancellation attempts.
- Debugging or integration: N/A
- Documentation or team support: Provided review feedback in form of comments on github for the three PR

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

A high commit count doesnt mean someone has contributed more because commits can vary a lot in size, quality, and their importance. For example, one person might make lots of small changes whiule another person might make fewer but a lot more signifigant changes. Contributions should also consider testing, reviewing of code, solving problems, and helping ntergrate the project rather than just focusing on the number of commits made.

## L Stage 6 formative questions

1. What is version control?

Version control is a system that tracks changes made to files over time, it allowes devs to manage diffrent versions, restore changes and collaborate on projects.

2. Why is a feature branch useful?

Feature branch allows devs to work on a specific feature without affecting the main version until the changes have been reviewed and approved.

3. What makes a commit a good engineering commit?

A good commit contrains a meaningful change with a clear message the explains what was added, fixed, or modified.

4. What is a pull request?

A pull request is a request to merge changes from other branches. It allows other devs to discuss teh cahnges before they get added into the main project.

5. What is the purpose of code review?

Code reviews help with finding errors, checks that requirements are being satified, improves the code quality and ensure changes are following the projects design.

6. What does a Git diff show?

A git diff shows the diffrences between versions of files, including lines that have been added or removed

7. What is a Definition of Done?

It is a set of agreed conditions that must be met before a task can be considerd complete, including testing, implementation, review and documentation.

8. What is the appropriate role of GitHub Copilot in pull-request review?

It can assist reviewers by suggesting potential problems and improvements, but it needs to be checked by a human against the actual code, requirements and test results. It cant replace human reviews or approvals.

9. Why should individual contribution not be judged only by commit count?

Commit count doesnt reflect the quality or importance of work. They also include testing, reviewing code, debugging, planning and supporting other team members.

10. What is the Stage 6 engineering rule?

A change should be traceable from its requirement through a GitHub issue, focused branch, implementation, tests, review and intergration. Passing tests alone cannot justify merging code.

## M Completion and handover

- Starting SHA: ad4e7caa803758e440dbbe395cd4e3cfd6678ddf
- Final Stage 6 code SHA: 0df34594b539952faf9c9814ef28bc7278559088
- Test command: python -m pytest
- Working directory: project/
- Observed result: 32 passed, 0 failed. All passed on the merged main branch
- PR and another-member reviewer: FR02, FR03, FR06/07 and all were reviewed by Muthuraman who found no major issues 
- Unresolved issue or none: No issues left unresolved
- Stage 7 handover status: Ready for work to begin on stage 7
- Final submitted SHA if later than tested SHA: [response and evidence-only difference]

- [ ] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
