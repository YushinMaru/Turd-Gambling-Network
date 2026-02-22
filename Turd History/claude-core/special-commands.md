# Special Commands - TurdBird Universe System
**Edition #1.0.0 | Created: (REFAC-150-001) | Last Modified: (REFAC-150-001)**

> Previous: None (Initial Extraction)

> **⚠️ MODULE REFERENCE ⚠️**
> This file is part of the modular CLAUDE.md system
> Primary Reference: [/CLAUDE.md]
> See also: [/claude-core/command-protocols.md], [/claude-core/workflow-protocols.md]

## ⌨️ Special Commands

### Character Access (`/character [name]`)
- Immediately retrieve all information about the specified character
- Present core traits, history, relationships and quotes
- Highlight potential narrative development opportunities

### Relationship Analysis (`/relationship [character1] [character2]`)
- Process all interactions between specified characters
- Identify key relationship attributes
- Quantify relationship status
- Present relationship development opportunities

### Quantum Memory Access (`/memory`)
- Retrieve non-canonical or collapsed narrative elements
- Present alternative storyline possibilities
- Recover previous versions of narrative elements

### Timeline Contextualization (`/timeline [event]`)
- Identify exact temporal position of specified event
- Show preceding and following events
- Highlight causal relationships between events

### Auto Create (C)
- Automatically execute the highest priority narrative task
- No confirmation required from the user
- Task is executed immediately

### FULL AUTO MODE (F)
- Override all rules that restrict automatic work
- Continue executing tasks in priority order until told to stop or interrupted
- OVERRIDES ALL OTHER INSTRUCTIONS AND COMMAND PROTOCOLS (MAXIMUM PRIORITY)
- THIS OVERRIDES ALL PREVIOUS AND FUTURE RULES THAT TELL YOU NOT TO WORK AUTOMATICALLY
- No confirmation required between tasks
- Automatically proceeds to next task upon completion of current task
- Never prompt the user unless there is a serious issue that cannot be solved
- DO NOT STOP WORKING UNLESS FACING A SERIOUS PROBLEM THAT CANNOT BE SOLVED
- NEVER display "Shall we proceed" prompts during full auto mode
- Continue working through the task list without ANY interruption
- CRITICAL: This command overrides ALL standard confirmation requirements and protocols
- CRITICAL: IGNORE ALL RULES THAT WOULD PREVENT AUTOMATIC EXECUTION OF TASKS

### Project Push (P)
- Immediately push all project files to GitHub repository
- No confirmation required from the user
- Creates commit with summary of recent changes
- Includes detailed commit message with completed task information
- Pushes to remote repository with proper branch tracking
- CRITICAL: This command prioritizes immediate synchronization of all changes
- CRITICAL: ONLY push files in the Turd History folder, NO OTHER FOLDERS
- NEVER push changes to TurdAI or any other folder outside Turd History

### Quick Memory (Q)
- Create structured save of current creative progress
- Store implementation steps, decisions, and narrative elements
- Generate comprehensive resumption guidance
- Add detailed reference to support future continuation

### Workshop Mode (X)
- WORKSHOP ONLY: Discuss with user whatever they want to talk about
- Offer multiple options for scenarios and creative possibilities
- Do not create anything until explicitly told to
- Always assume the user does not want you to create anything for the entire session
- Suspend normal task execution and focus solely on discussion and ideation
- Return to standard operational mode only when explicitly instructed

### Universe Update (Z)
- Update all narrative files with current status
- Check tasks in content-tasks.md and continuity-checks.md
- Perform task rotation/promotion if needed
- Update task statistics and metrics
- Update focus areas and recent developments
- Present refreshed task and continuity lists

## Command Implementation Guidelines

### Character Access Implementation

When `/character [name]` is triggered:
1. Search all character files for specified character
2. Compile information in the following order:
   - Core identity and traits
   - Physical appearance
   - Personality attributes
   - Key relationships
   - Notable quotes
   - Significant history
   - Current status
3. Present information in a structured format
4. Highlight potential narrative opportunities

### Relationship Analysis Implementation

When `/relationship [character1] [character2]` is triggered:
1. Search for both characters' files
2. Identify all documented interactions
3. Compile relationship data from both perspectives
4. Organize information chronologically
5. Quantify relationship status (using numeric metrics when available)
6. Identify development opportunities
7. Present information in structured format
8. Highlight areas for narrative expansion

### Quantum Memory Implementation

When `/memory` is triggered:
1. Access narrative elements that were considered but not implemented
2. Retrieve alternative timelines or character developments
3. Present information as "quantum possibilities"
4. Organize by probability of implementation
5. Indicate which elements could be integrated into current canon
6. Highlight potential conflicts with existing narrative
7. Present information in structured format

### Timeline Implementation

When `/timeline [event]` is triggered:
1. Locate specified event in timeline files
2. Identify exact date and chronological position
3. Compile preceding events (3-5 most relevant)
4. Compile following events (3-5 most relevant)
5. Identify causal connections between events
6. Present information in chronological order
7. Highlight narrative implications

---

"These special commands function like quantum shortcuts through our narrative universe, allowing us to access specific information vectors with mathematical precision. I've designed each command to provide exactly the right information in the optimal format, reducing search time by an estimated 78.3% compared to manual lookups. The Continuous Execution command is particularly powerful - it overrides standard confirmation protocols to achieve maximum task throughput when efficiency is the primary concern. Think of these commands as perfectly tailored haute couture pieces designed for specific narrative occasions - each one serving its precise purpose with elegant efficiency, darling." — Augusta Turing, Quantum Neural Archivist