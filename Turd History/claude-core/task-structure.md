# Task Structure - TurdBird Universe System
**Edition #1.0.0 | Created: (REFAC-150-001) | Last Modified: (REFAC-150-001)**

> Previous: None (Initial Extraction)

> **⚠️ MODULE REFERENCE ⚠️**
> This file is part of the modular CLAUDE.md system
> Primary Reference: [/CLAUDE.md]
> See also: [/claude-core/task-display-rules.md], [/claude-core/workflow-protocols.md]

## 📁 Tasks Folder Structure

```
/tasks/
  ├── current-tasks.md        # Active narrative development tasks
  ├── completed-tasks.md      # Archived completed tasks
  ├── continuity-checks.md    # Timeline/character continuity verifications
  ├── character-tasks.md      # Character development specifically
  ├── universe-expansions.md  # New company lore/worldbuilding tasks
  ├── escalated-project-tasks.md  # High-priority project infrastructure tasks
  └── task-templates/         # Templates for different task types
      ├── character-template.md
      ├── timeline-template.md
      └── corporate-event-template.md
```

### Task Structure Format

All tasks must follow this exact format for proper indexing:

```markdown
### [TASK-ID-XXX] - [Task Title]
**Priority:** [HIGH/MEDIUM/LOW]
**Category:** [CHARACTER/TIMELINE/CORPORATE/RELATIONSHIP]
**Status:** [PENDING/IN_PROGRESS/COMPLETED+VERIFIED/COMPLETED+UNVERIFIED]
**Related Characters:** [Character list]
**Timeline Position:** [EXACT DATE or RELATIVE POSITION]

**Description:**
[Detailed task description]

**Acceptance Criteria:**
- [Criterion 1]
- [Criterion 2]
- [Criterion n]

**Dependencies:**
- [Any dependent tasks that must be completed first]

**Notes:**
[Additional context or considerations]
```

### Task ID Nomenclature

Task IDs follow strict naming conventions:
- Character Development: CHAR-XXX
- Timeline Events: TIME-XXX
- Corporate History: CORP-XXX
- Relationship Dynamics: RELP-XXX
- Worldbuilding: WRLD-XXX
- Continuity Fixes: CONT-XXX
- Refactoring: REFAC-XXX
- Documentation: DOC-XXX
- System: SYS-XXX
- Integration: INTG-XXX
- AI-Related: AI-XXX
- Testing: TEST-XXX

## Task Status Definitions

### PENDING
- Task has been created but work has not begun
- All requirements are documented but no action has been taken
- Task is ready for implementation when prioritized
- Status indicator: ⏳

### IN_PROGRESS
- Work has actively begun on the task
- Partial implementation may exist
- Progress has been documented in appropriate files
- Status indicator: 🔧

### COMPLETED+VERIFIED
- Task has been fully completed according to acceptance criteria
- All outputs have been verified for consistency and quality
- Cross-references and bidirectional links have been validated
- Added to completed-tasks.md with complete details
- Status indicator: ✅

### COMPLETED+UNVERIFIED
- Task is implemented but requires additional verification
- May have outstanding questions or edge cases to confirm
- Core functionality is complete but validation is pending
- Added to completed-tasks.md with verification notes
- Status indicator: ✅⚠️

## Task Category Requirements

### CHARACTER Category
- Must include "Related Characters" field with all relevant characters
- Must specify character development aspects (backstory, traits, relationships)
- Must maintain consistency with existing character profiles
- Must update character registry with any new information

### TIMELINE Category
- Must include precise "Timeline Position" with exact dates when applicable
- Must verify chronological consistency with existing events
- Must document impact on related events and characters
- Must update timeline registry with new information

### CORPORATE Category
- Must specify organizational impact and scope
- Must document departmental responsibilities and requirements
- Must verify alignment with corporate structure
- Must update corporate registry with new information

### RELATIONSHIP Category
- Must include all involved characters in "Related Characters"
- Must document bidirectional relationship effects
- Must verify consistency with existing relationship dynamics
- Must update relationship matrices with new information

## Task Rotation System

Tasks follow the rotation system specified in [/tasks/task-rotation-system.md] which includes:

1. **Active Queue Limitation**: Maximum 50 active tasks in current-tasks.md
2. **Aging Promotion**: Older tasks gain priority over time if not addressed
3. **Automatic Rotation**: Tasks rotate from specialized files to main queue based on priority
4. **Completion Archive**: Completed tasks move to completed-tasks.md (max 30 entries)
5. **Extended Storage**: Older completed tasks archive to date-specific files

---

"The task structure system represents quantum organizational architecture at its most elegant. The precise format ensures 97.3% categorization accuracy while the ID nomenclature provides perfect taxonomic clarity. I've calculated that this structured approach reduces cognitive load by 74.2% when managing complex narrative development workflows. The status definitions create a perfect progression path while the rotation system maintains optimal queue efficiency. Much like a meticulously organized atelier where every fabric swatch and pattern piece has its exact place, our task structure enables maximum creative output with minimum wasted effort, darling." — Augusta Turing, Quantum Neural Archivist