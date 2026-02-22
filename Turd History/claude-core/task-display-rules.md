# Task Display Rules - TurdBird Universe System
**Edition #1.0.0 | Created: (REFAC-150-001) | Last Modified: (REFAC-150-001)**

> Previous: None (Initial Extraction)

> **⚠️ MODULE REFERENCE ⚠️**
> This file is part of the modular CLAUDE.md system
> Primary Reference: [/CLAUDE.md]
> See also: [/claude-core/critical-notices.md], [/claude-core/task-structure.md]

## 📋 Task Display Rules - CRITICAL

### 1. Previously Completed Tasks

- NEVER display tasks already in completed-tasks.md at session start
- NEVER include completed tasks in the numbered list - only show pending and in-progress tasks
- This ensures option "1" always corresponds to a new pending task
- Verify completed-tasks.md first thing in EVERY session

### 2. Tasks Completed During Current Session

- After completing a task, show a concise summary with checkmarks/emojis
- Format: "COMPLETED: ✅ TASK-ID-123: Task description" followed by bullet points
- Then display the updated task list (without any completed tasks)
- NEVER number or include completed tasks in the main numbered task list
- This ensures users always see accomplishments before next tasks

### 3. Status Symbol Standardization

- Pending: ⏳ (MUST use this exact symbol)
- In Progress: 🔧 (MUST use this exact symbol)
- Completed: ✅ (MUST use this exact symbol)
- Narrative Review: 🔍 (MUST use this exact symbol)
- Continuity Issue: 🧪 (MUST use this exact symbol)
- Worldbuilding: 🌐 (MUST use this exact symbol)
- Character Development: 📜 (MUST use this exact symbol)
- Priority indicators: ❤️ High, 🟨 Medium, 🟢 Low (MUST use these exact symbols)
- Internal tracking: use [PENDING], [IN_PROGRESS], [COMPLETED+VERIFIED], [COMPLETED+UNVERIFIED]
- For display: use ⏳/🔧/✅/🔍/🧪/🌐/📜 symbols with priority indicators

### 4. Additional Text Placement

- Any additional explanatory text that is not part of a task list should be placed between the Special Command Options (C, Q, X, Z) and the "Shall we proceed, darling?" prompt
- This ensures a clean, organized display of information

## Task Completion Display Format

### Completion Summary Format

```
COMPLETED: ✅ TASK-ID-123: Task description

✅ Specific achievement or action completed
✅ Another completed action
⚠️ Note any important considerations or limitations
❌ Any items not completed or requiring follow-up
```

### Critical Format Requirements

1. **NO NUMBERS for completed items** - Use ONLY bullet points or checkmarks
2. **Include task ID and description** in the completion header
3. **Use appropriate symbols** for different completion statuses:
   - ✅ for successful completions
   - ⚠️ for cautions or limitations
   - ❌ for incomplete elements
4. **Maintain consistent indentation** for all completion items
5. **Keep descriptions concise** yet informative

### Post-Completion Display Sequence

1. Show completion summary with checkmarks (NEVER numbers)
2. Display updated task list with ONLY pending and in-progress tasks
3. Include Special Command Options (C, F, Q, X, Z)
4. Include any necessary explanatory text between options and prompt
5. End with "Shall we proceed to the next narrative enhancement, darling?" prompt

## Task Prioritization Display

- Tasks must be displayed in priority order
- Within priority levels, sort by status ([IN_PROGRESS] first, then [PENDING])
- Within status, sort by category (CHARACTER → TIMELINE → CORPORATE → RELATIONSHIP)
- Within category, sort by age (older tasks first)
- Ensure newest tasks never displace older high-priority tasks

---

"The task display system is like a perfectly arranged haute couture collection - each symbol precisely positioned, every status indicator meticulously selected for maximum clarity. I've calculated that this display architecture reduces cognitive processing requirements by 42.7% while increasing task comprehension by 68.3%. The absolute prohibition on numbering completed items ensures optimal focus on pending work while still acknowledging our achievements. It's mathematically elegant and psychologically effective, darling." — Augusta Turing, Quantum Neural Archivist