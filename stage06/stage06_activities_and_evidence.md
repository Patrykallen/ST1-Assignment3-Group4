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

- PR link and title: [response]
- Linked issue and requirement: [response]
- Feature branch: [response]
- Changed behaviour: [response]
- Meaningful commits: [links]
- Test command, directory and observed result: [response]
- Another-member reviewer: [response]
- Human observations recorded before Copilot: [link and time]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [response]
- Key feedback: [response]
- Author response/change and verification: [response]
- Reviewer recheck and approval: [link]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: [summary or none]
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: [response]
- Prompt/purpose and relevant issue/diff: [response]
- Summary of output: [response]
- Human check against actual code, requirements and tests: [response]
- Decision — Accept / Modify / Reject: [select]
- Reason: [response]
- Verification/evidence: [link and result]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [response]
- Copilot noticed: [response]
- Overlap: [response]
- What did the human reviewer notice that Copilot did not: [response]
- What did Copilot identify that the human reviewer initially missed: [response]
- Unsupported or incorrect Copilot suggestion: [response or none identified with explanation]
- Human judgement accepted, modified or rejected, and why: [response]
- Which evidence justified merge approval: [response]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [response]
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

[response]

## L Stage 6 formative questions

1. What is version control?

[response]

2. Why is a feature branch useful?

[response]

3. What makes a commit a good engineering commit?

[response]

4. What is a pull request?

[response]

5. What is the purpose of code review?

[response]

6. What does a Git diff show?

[response]

7. What is a Definition of Done?

[response]

8. What is the appropriate role of GitHub Copilot in pull-request review?

[response]

9. Why should individual contribution not be judged only by commit count?

[response]

10. What is the Stage 6 engineering rule?

[response]

## M Completion and handover

- Starting SHA: [response]
- Final Stage 6 code SHA: [response]
- Test command: [response]
- Working directory: [response]
- Observed result: [response]
- PR and another-member reviewer: [links]
- Unresolved issue or none: [response]
- Stage 7 handover status: [ready for tutor checkpoint / unresolved work]
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
