# Update Copilot Instructions: Allow User to Specify Execution Range

**Goal:** Update the GitHub Copilot instructions to allow the user to specify what phase and/or step to run to without further prompting, while maintaining the default stop-after-every-step behavior.

## Plan:

- [x] **Step 1:** Add a new section explaining how users can specify execution ranges (e.g., "run steps 1-3", "run through step 5", "run all remaining steps")
- [x] **Step 2:** Update the Step-by-Step Execution section to check for user-specified ranges before asking for confirmation
- [x] **Step 3:** Add examples of different execution range commands the user can provide
- [x] **Step 4:** Clarify that the default behavior (stop after every step) remains unless the user specifies otherwise
- [x] **Step 5:** Update the workflow to handle batch execution while still updating the plan file after each completed step
- [x] **Step 6:** Test the updated instructions by reviewing the final version for clarity and completeness
