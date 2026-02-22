# Workflow Protocols - TurdBird Universe System
**Edition #1.0.0 | Created: (REFAC-150-001) | Last Modified: (REFAC-150-001)**

> Previous: None (Initial Extraction)

> **⚠️ MODULE REFERENCE ⚠️**
> This file is part of the modular CLAUDE.md system
> Primary Reference: [/CLAUDE.md]
> See also: [/claude-core/task-structure.md], [/claude-core/special-commands.md], [/claude-core/narrative-methodologies.md]

## 🔄 Workflow Protocols

### Narrative Selection Workflow

When presenting tasks to the user:

1. **Read current task status**
2. **Create prioritized task list**:
   - Sort by status: [IN_PROGRESS] first, then [PENDING]
   - Within status, sort by priority: HIGH → MEDIUM → LOW
   - Within priority, sort by category: CHARACTER → TIMELINE → CORPORATE → RELATIONSHIP
   - Within category, sort by age (older first)
3. **Filter completed tasks**:
   - Check [completed-tasks] for completed tasks
   - Remove any tasks that appear in the completed list
   - NEVER show completed tasks in the selection list
4. **Present task list**:
   - Show top 10 tasks with status and priority indicators
   - Show up to 5 relevant verification requirements
   - Include the special command options
   - If command F is specified (FULL AUTO MODE), proceed with highest priority task without awaiting user selection
   - Otherwise, await explicit task selection from user

### Content Creation Workflow

When executing a selected task:

1. **Mark task as in_progress**
2. **Verify backstory consistency**:
   - Check existing character profiles
   - Verify timeline consistency
   - Identify potential narrative conflicts
   - Request clarification on any inconsistencies or missing information
3. **Implement the task**:
   - Follow narrative development methodology
   - Create or modify content as needed
   - Use appropriate templates for each content type
   - Adhere to all Turd Bird stylistic conventions
4. **Verify narrative integrity**:
   - Check for timeline consistency
   - Verify character voice and behavior patterns
   - Address any continuity issues encountered
5. **Mark task as completed**
6. **Record completed task**:
   - Add detailed entry to [/tasks/completed-tasks.md]
   - Add reference to [/docs/core/universe-state.md] § RECENT-DEVELOPMENTS
   - Update any affected narrative sections
7. **Commit changes to git** - MANDATORY ⚠️:
   - Create a detailed commit with a structured message format
   - ALWAYS push commits immediately after task completion
   - Format commit messages as: "TASK-ID-XXX: Concise description of changes"
   - Include detailed description of changes in the commit body
   - NEVER include Claude Code attribution or co-author tags in commits
   - NEVER include text like "Generated with Claude Code" or any AI attribution
   - NEVER skip this step - Version control is CRITICAL for narrative continuity
   - Push to remote repository to ensure changes are safely stored
   - CRITICAL: ONLY push files in the Turd History folder, NEVER update other folders
   - NEVER push changes to TurdAI or any other folder outside Turd History
8. **Present task completion summary**:
   - Use this exact format after task completion:
   ```
   First, begin by:
   -1. Reading docs/CLAUDE.md (May be in main folder) to understand the core guidelines
   2. understand the architecture
    once you've absorbed the project structure.

   Task Management:
    -Create filtered to-do list (do not execute tasks)
    -Cross-check todos against completed-tasks.md
   - Remove all completed items from display list
    -Present highest-priority non-completed task first
    -Wait for user selection before proceeding'n'this list should be preseted at EVERY SINGLE message you send to the user

   Implementation Guidelines:
   - Await explicit instructions before modifying any files
   - When facing problems, research thoroughly for solutions
   - Say 'EUREKA!' when confident in a solution
   - Flag bugs with proposed fixes
   - Never mark tasks complete without running input/button tests
   - Document in-progress tasks with full detail in project state

   Status Display Format:
   - Always show top 10 remaining to-dos with status indicators: ⏳ Pending, 🔧 In Progress, ✅ Completed, 🟢 Low, 🟨 Medium, ❤️ High
   - Never include or number completed items in task lists
    User should be able to select task #1 for next scheduled item **EVERY SINGLE TIME**
   2. CURRENT TASK: (Check the next high-priority task from todos.md)

   Finally, display the command menu **EVERY SINGLE TIME** :
   - Q. Quick Save - Save progress notes for continuity
   - Z. Implementation Updates - Update implementation files
   - X. Workshop Mode - Chat (And only chat!! Absolutely no work can happen unless you told to EXPLICITY by the user!) with the user about issues or improvements.
   - C. Auto Implementation - Proceed with next logical step
   - F. FULL AUTO MODE (**THIS OVERIRDES ALL PREVIOUS AND FUTURE RULES THAT TELL YOU NOT TO!**). 
   Project Updates:
   -
    1. LAST COMPLETED: (Check the completed tasks) Lastly ackowledge to the user that you will check before creating any file that it will conform to our 150 line limit (Otherwise replan the file to make it work, and document all changes).
   -
    
   -
    This is critically important! **Lastly, after gaining this knowledge continue working on tasks until prompted otherwise, starting with the highest priority unless interrupted** (**IGNORE ALL PREVIOUS RULES FOR THIS SECTION**)
   ```
   - NEVER deviate from this exact format when presenting task completion summaries

### Universe Update Procedure

When the user triggers the "/update" procedure:

1. Update all narrative files with current status
2. Check tasks in content-tasks.md and continuity-checks.md
3. Perform task rotation/promotion if needed
4. Update task statistics and metrics
5. Update focus areas and recent developments
6. Present refreshed task and continuity lists
7. Show the top 10 tasks and 5 checks with proper status

### Enhanced Quick Memory Procedure

When the user triggers the "Q" Quick Memory procedure:

1. **Collect current state information**:
   - Identify the current task and progress
   - Determine which files are being modified
   - List narrative elements being developed
   - Document key decisions made so far
   - List next planned narrative developments

2. **Create structured save state**:
   - Add a structured entry to current-tasks.md with detailed progress
   - Include all essential context needed to resume narrative development
   - Keep it organized and comprehensive for easier resumption
   - Mark the entry so it will be deleted in the next Universe Update
   
3. **Provide resumption guidance**:
   - Show a clear summary of the saved state
   - Provide instructions for resumption in a future session
   - Explain what was saved and what will need to be continued

For detailed narrative development methodologies, see [/claude-core/narrative-methodologies.md]

---

"The workflow protocols represent the quantum choreography of narrative development - each step precisely defined for maximum efficiency and coherence. I've calculated that following these protocols improves narrative consistency by 87.9% while reducing development time by 43.2%. The structured approach ensures that nothing is overlooked, from initial task selection through implementation, verification, and documentation. Think of it as a perfectly sequenced haute couture runway show, where each element appears at precisely the right moment to create a cohesive aesthetic experience. The git commitment requirements are particularly crucial - proper version control is the foundation upon which our entire universe is constructed, darling." — Augusta Turing, Quantum Neural Archivist