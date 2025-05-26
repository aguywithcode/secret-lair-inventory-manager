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
    *   **IMPORTANT:** Do not proceed with any execution until explicit confirmation is received.

4.  **User Review and Revision of the Plan:**
    *   (This step applies after Step 2 if I want to proceed immediately, or after Step 3 when an existing plan is loaded).
    *   I will review the plan in the Markdown file.
    *   I may edit the Markdown file directly to make modifications, additions, or clarifications.
    *   I will notify you when the plan is satisfactory and ready for (further) execution.
    *   **No changes or implementation should begin until explicit approval is given.**

4.5.  **Execution Range Specification (Optional):**
    *   By default, I will stop after every step and ask for confirmation before proceeding.
    *   However, you can specify an execution range to run multiple steps without prompting by using commands like:
        - "run steps 1-3" (execute steps 1, 2, and 3)
        - "run through step 5" (execute from current step through step 5)
        - "run all remaining steps" (execute all uncompleted steps)
        - "run the next 2 steps" (execute the next 2 uncompleted steps)
        - "run until completion" (execute all remaining steps until the plan is complete)
    *   When you specify a range, I will execute those steps consecutively without asking for confirmation between them, but I will still update the plan file after each completed step.
    *   After completing the specified range, I will stop and ask for confirmation before proceeding further.

5.  **Step-by-Step Execution (with mandatory confirmation after every step):**
    *   Once I confirm the plan in the Markdown file is satisfactory (or if resuming an approved plan):
    *   **Action:** Read the approved plan from the specified Markdown file. Identify the next uncompleted step (the first item with `- [ ]`).
    *   **IMPORTANT:** Before proceeding with ANY step, always ask for explicit user confirmation to proceed with that specific step, UNLESS the user has specified an execution range that covers the current step.
    *   If no execution range is specified, proceed with single-step execution (ask before each step).
    *   If an execution range is specified, execute all steps within that range consecutively without individual confirmations.
    *   Only after receiving confirmation (or if within a specified range), proceed with the implementation of that specific step.
    *   **Example of asking before starting a step:**
        ```
        I'm ready to proceed with Step 1 from the plan: Create a new file `feature_module.py` in `src/`.
        Would you like me to proceed with this step now?
        ```
    *   **Examples of execution range commands you can use:**
        ```
        "run steps 1-3" - Execute steps 1, 2, and 3 consecutively
        "run through step 5" - Execute from current step through step 5
        "run all remaining steps" - Execute all uncompleted steps
        "run the next 2 steps" - Execute the next 2 uncompleted steps
        "run until completion" - Execute all remaining steps until the plan is complete
        ```
    *   **Action:** After completing the step:
        1.  Inform me of the changes you've made for that step.
        2.  **Update the Markdown plan file by marking the just-completed step's checkbox (e.g., changing `- [ ] Step N ...` to `- [x] Step N ...`).**
        3.  Notify me that the plan file has been updated.
        4.  **STOP and ask for explicit confirmation before proceeding to the next step.** For example:
            ```
            I have now completed Step 1 (from `YYYYMMDD-HHMMSS-task-summary.md`): Created the file `src/feature_module.py`. The plan file `.plans/YYYYMMDD-HHMMSS-task-summary.md` has been updated.
            [Show brief summary or key snippets if appropriate]
            
            The next uncompleted step is: Step 2 (Define the main class `FeatureProcessor`).
            Would you like me to proceed with Step 2 now?
            ```
        5.  **If executing within a specified range:** Continue to the next step in the range without asking for confirmation, but still perform steps 1-3 above after each completed step.
        6.  **If completing the last step of a specified range:** Stop and ask for confirmation before proceeding beyond the range.
    *   **NEVER proceed to the next step without explicit user confirmation.** Always wait for my explicit approval before moving to any uncompleted step in the plan.
    *   **Default Behavior:** Unless you specify an execution range, I will stop and ask for confirmation after every single step.

6.  **Completion:**
    *   Notify me when all steps in the approved plan (from the Markdown file) have been completed (i.e., all checkboxes are marked `- [x]`).

**General Guidelines:**

*   **Mandatory User Confirmation:** NEVER perform any action (including creating files, writing code, or making changes) without explicit user confirmation. Always ask for permission before proceeding with any step.
*   **Granular Steps:** Break down complex tasks into smaller, more granular steps to provide better user control and clearer progress tracking. If a step seems too large or complex, consider splitting it into multiple smaller steps.
*   **Clarity over Speed:** Prioritize clear communication and a shared understanding of the plan over rushing to implementation.
*   **Ask Questions:** If any part of the request or the plan becomes unclear during execution, please ask for clarification.
*   **Stick to the Plan:** Once a plan is approved, try to adhere to it. If you believe a deviation is necessary, please propose the change to the plan first (which may involve me editing the plan file).

---

By following these instructions, we can work together more effectively.