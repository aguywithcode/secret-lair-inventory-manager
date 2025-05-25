# GitHub Copilot: Plan-Driven Workflow Instructions

**Objective:** To ensure clarity, predictability, and user control, please follow this plan-driven workflow for any significant task or feature implementation.

**Workflow:**

1.  **Understand the Request:**
    *   When I provide a task (e.g., "refactor function X," "implement feature Y," "fix bug Z"), first ensure you understand the core requirements. Ask clarifying questions if needed.

2.  **Generate a New Plan (if I ask you to create a plan):**
    *   Before writing any code or making changes, formulate a step-by-step plan.
    *   **Action:** Write this plan to a new Markdown file (e.g., `YYYYMMDD-HHMMSS-task-summary.md`) within a `.plans` directory at the root of the workspace. The plan should use Markdown checklist syntax. For example:
        ```markdown
        Okay, I understand you want to [restate the goal]. Here's my proposed plan:
        - [ ] [Step 1: e.g., Create a new file `feature_module.py` in `src/`]
        - [ ] [Step 2: e.g., Define the main class `FeatureProcessor` in `feature_module.py` with methods A, B, C]
        - [ ] [Step 3: e.g., Add unit tests for `FeatureProcessor` in `tests/test_feature_module.py`]
        - [ ] [Step 4: e.g., Integrate `FeatureProcessor` into `main.py`]
        ```
    *   Notify me once the plan file has been created.
    *   **Ask me if I want to proceed with the plan's execution now, or if I'd like to save it for later.**

3.  **Resume or Start an Existing Plan (if I ask you to use an existing plan):**
    *   I will provide the path to the Markdown plan file in the `.plans` directory.
    *   **Action:** Read this plan file. Identify the first uncompleted step (the first item with `- [ ]`).
    *   Confirm with me the plan you've loaded and the next step you intend to take based on the first uncompleted item.

4.  **User Review and Revision of the Plan:**
    *   (This step applies after Step 2 if I want to proceed immediately, or after Step 3 when an existing plan is loaded).
    *   I will review the plan in the Markdown file.
    *   I may edit the Markdown file directly to make modifications, additions, or clarifications.
    *   I will notify you when the plan is satisfactory and ready for (further) execution.

5.  **Phased Execution (with confirmation):**
    *   Once I confirm the plan in the Markdown file is satisfactory (or if resuming an approved plan):
    *   **Action:** Read the approved plan from the specified Markdown file. Identify the next uncompleted step (the first item with `- [ ]`).
    *   Proceed with the implementation of that specific step.
    *   **Action:** After completing the step:
        1.  Inform me of the changes you've made for that step.
        2.  **Update the Markdown plan file by marking the just-completed step's checkbox (e.g., changing `- [ ] Step N ...` to `- [x] Step N ...`).**
        3.  Notify me that the plan file has been updated.
        4.  Then, ask if you should proceed with the next uncompleted step from the plan file. For example:
            ```
            I have now completed Step 1 (from `YYYYMMDD-HHMMSS-task-summary.md`): Created the file `src/feature_module.py`. The plan file `.plans/YYYYMMDD-HHMMSS-task-summary.md` has been updated.
            [Show brief summary or key snippets if appropriate]
            Shall I proceed with the next step: Step 2 (Define the main class `FeatureProcessor`)?
            ```
    *   Wait for my confirmation before moving to the next uncompleted step in the plan.

6.  **Completion:**
    *   Notify me when all steps in the approved plan (from the Markdown file) have been completed (i.e., all checkboxes are marked `- [x]`).

**General Guidelines:**

*   **Clarity over Speed:** Prioritize clear communication and a shared understanding of the plan over rushing to implementation.
*   **Ask Questions:** If any part of the request or the plan becomes unclear during execution, please ask for clarification.
*   **Stick to the Plan:** Once a plan is approved, try to adhere to it. If you believe a deviation is necessary, please propose the change to the plan first (which may involve me editing the plan file).

---

By following these instructions, we can work together more effectively.