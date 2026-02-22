# Task Rotation System
**Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)**

> Previous: None (Initial Documentation)

## Overview

The Task Rotation System manages the flow of tasks between the active task queue and extended storage, ensuring the primary task list never exceeds 50 lines while maintaining priority-based organization of all pending work. This system enables Augusta "Gust" Turing to manage an unlimited number of tasks while keeping the active queue manageable and focused on the highest-priority items.

## Core Components

### 1. Active Task Queue

The primary visible task list displayed to users:

- **Maximum Size:** 50 lines total
- **Display Format:** Numbered list with status symbols
- **Location:** `/tasks/current-tasks.md`
- **Composition:** Highest priority tasks from all categories
- **Task Limit:** Approximately 10 tasks depending on description length
- **Selection Method:** Priority-based algorithm with domain balancing

The active queue is the focal point for all task management and user interaction.

### 2. Extended Task Storage

Repository for tasks waiting to enter the active queue:

- **Organization:** Domain-specific files with priority sections
- **Location:** `/tasks/extended/{domain}-tasks.md`
- **Structure:** Prioritized sections with complete task entries
- **Metadata:** Additional tracking information for rotation management
- **Size:** Unlimited capacity with efficient organization
- **Access:** Available for reference but not displayed in primary interface

Extended storage maintains all tasks not currently in the active queue.

### 3. Recent Completed Tasks

Collection of recently completed tasks for reference:

- **Maximum Size:** 30 completed tasks
- **Display Format:** Reverse chronological order with completion dates
- **Location:** `/tasks/completed-tasks.md`
- **Structure:** Grouped by month with full task documentation
- **Purpose:** Provides context and reference for recent work
- **Retention:** Most recent 30 completed tasks regardless of timeframe

Recent completed tasks provide valuable context for ongoing work.

### 4. Archived Completed Tasks

Long-term storage for historical task completions:

- **Organization:** Monthly archive files
- **Location:** `/tasks/archives/{year}-{month}-completed.md`
- **Structure:** Complete task entries with metadata and outcomes
- **Purpose:** Permanent record of all completed narrative work
- **Access:** Available for reference and historical analysis
- **Automated Migration:** Tasks automatically moved from completed-tasks.md when limit exceeded

Archives maintain a complete historical record of all narrative development.

### 5. Rotation Manager

System that controls task movement between storage locations:

- **Trigger Conditions:** Rules for when to move tasks
- **Selection Algorithm:** Logic for choosing which tasks to move
- **Balance Control:** Ensures representation from all domains
- **Aging Management:** Gradually increases priority of waiting tasks
- **Dependency Handling:** Ensures prerequisites appear before dependent tasks
- **Emergency Override:** Allows critical tasks to bypass rotation rules

The rotation manager ensures the right tasks are in the active queue at all times.

### 6. Task Registry

Master record of all tasks regardless of storage location:

- **Location:** `/registry/task-registry.md`
- **Content:** Complete listing of all tasks with metadata
- **Tracking:** Current storage location and status
- **History:** Record of rotation events and priority changes
- **Access:** Reference for task management operations
- **Validation:** Source of truth for task existence and status

The registry ensures no tasks are lost during rotation operations.

## Operational Mechanics

### Queue Size Management

The system actively controls active queue size:

- **Continuous Monitoring:** Tracks line count in active queue
- **Threshold Alerts:** Triggers actions at approaching capacity (45+ lines)
- **Overflow Prevention:** Proactively rotates tasks when limit is approached
- **Size Calculation:** Includes task descriptions and metadata in line count
- **Format Standardization:** Ensures consistent task formatting for predictable sizing
- **Emergency Compression:** Can apply more compact formatting in critical situations

These mechanisms prevent the active queue from exceeding 50 lines.

### Completed Task Management

The system manages completed tasks through these operations:

1. **Initial Placement:**
   - Completed tasks are immediately moved to completed-tasks.md
   - Full task details preserved including completion date and summary
   - Tasks organized in reverse chronological order (newest first)

2. **Size Monitoring:**
   - System regularly checks completed-tasks.md size
   - When count exceeds 30 completed tasks, oldest are identified for archiving
   - Maintains exact limit of 30 most recent completions

3. **Archiving Process:**
   - Tasks beyond 30-item limit are moved to monthly archive files
   - Archive files named by year-month (e.g., 2025-05-completed.md)
   - Full task details including outcome documentation preserved
   - Archive files stored in /tasks/archives/ directory
   - Metadata updated in task registry to reflect new location

4. **Archive Organization:**
   - Monthly archives contain all tasks completed in that month
   - Multiple archive files created as needed
   - Consistent format maintained for search and reference
   - Cross-references updated to reflect archived status

5. **Reference Preservation:**
   - Any quantum references to completed tasks maintained
   - Registry updated with new location information
   - Search functionality extended to include archives
   - Historical task access maintained despite migration

### Rotation Triggers

Tasks move between storage locations based on these conditions:

1. **Space Available Trigger:**
   - Condition: Active queue drops below 40 lines
   - Action: Promote highest-priority tasks from extended storage
   - Limit: Add tasks until active queue reaches 45 lines

2. **Task Completion Trigger:**
   - Condition: Task marked as completed in active queue
   - Action: Remove completed task and promote replacement from extended storage
   - Timing: Immediate rotation after task completion

3. **Priority Threshold Trigger:**
   - Condition: New HIGH priority task created when queue is full
   - Action: Demote lowest-priority active task to make room for new high-priority task
   - Override: Only applies if new task's priority exceeds lowest active task

4. **Dependency Resolution Trigger:**
   - Condition: Prerequisite task completed for tasks in extended storage
   - Action: Evaluate dependent tasks for promotion to active queue
   - Priority: Dependency resolution increases dependent task priority

5. **Domain Balance Trigger:**
   - Condition: Domain representation falls below threshold (minimum 1 task per domain)
   - Action: Promote highest-priority task from underrepresented domain
   - Balance: May demote lowest-priority task from overrepresented domain

6. **Age Threshold Trigger:**
   - Condition: Task in extended storage exceeds maximum wait time
   - Action: Gradually increase priority until task qualifies for promotion
   - Limiter: Rate of priority increase based on original priority level

### Task Selection Algorithm

When promoting tasks from extended storage, the system uses this algorithm:

1. **Priority Score Calculation:**
   - Base priority value (HIGH=100, MEDIUM=50, LOW=10)
   - Age factor (1 point per day in extended storage)
   - Dependency multiplier (1.5x if dependencies recently completed)
   - Domain balance modifier (1.2x for underrepresented domains)
   - User interest factor (1.5x for tasks related to recent user activity)

2. **Selection Process:**
   - Rank all extended storage tasks by priority score
   - Check available space in active queue
   - Promote highest-scoring tasks that fit within space constraints
   - Ensure minimum domain representation
   - Verify no circular dependencies

3. **Conflict Resolution:**
   - When multiple tasks have identical priority scores
   - First tiebreaker: Original priority level
   - Second tiebreaker: Age in system
   - Third tiebreaker: Domain representation
   - Final tiebreaker: Alphabetical by task ID

### Demotion Selection Algorithm

When active queue exceeds capacity, the system uses this algorithm:

1. **Retention Score Calculation:**
   - Base priority value (HIGH=100, MEDIUM=50, LOW=10)
   - Progress factor (1.5x multiplier for IN_PROGRESS tasks)
   - Recent access modifier (1.3x for recently viewed tasks)
   - Dependency value (1.3x if other active tasks depend on this task)
   - Domain essentiality (1.2x if sole representative of domain)

2. **Selection Process:**
   - Rank all active tasks by retention score
   - Identify lowest-scoring tasks
   - Verify demotion won't break dependency chains
   - Ensure minimum domain representation maintained
   - Demote lowest-scoring eligible tasks

3. **Protected Tasks:**
   - IN_PROGRESS tasks are protected from demotion when possible
   - Tasks explicitly flagged by users are protected
   - Sole domain representatives are protected unless overridden by critical priority tasks
   - Recently promoted tasks have 24-hour demotion protection

## Implementation Details

### Extended Storage Structure

Each domain has a dedicated extended storage file:

```
/tasks/extended/
├── character-tasks.md     # Extended CHARACTER domain tasks
├── timeline-tasks.md      # Extended TIMELINE domain tasks
├── corporate-tasks.md     # Extended CORPORATE domain tasks
├── relationship-tasks.md  # Extended RELATIONSHIP domain tasks
└── worldbuilding-tasks.md # Extended WORLDBUILDING domain tasks
```

Within each file, tasks are organized by priority sections:

```markdown
# Extended Character Tasks
**Edition #X.Y.Z | Last Updated: YYYY-MM-DD**

## HIGH Priority Tasks
[Complete task entries]

## MEDIUM Priority Tasks
[Complete task entries]

## LOW Priority Tasks
[Complete task entries]
```

### Task Registry Structure

The task registry maintains complete records of all tasks:

```markdown
# Task Registry
**Edition #X.Y.Z | Last Updated: YYYY-MM-DD**

## Active Queue Tasks
[Task ID] | [Priority] | [Status] | [Domain] | [Creation Date] | [Last Rotation]

## Extended Storage Tasks
[Task ID] | [Priority] | [Status] | [Domain] | [Creation Date] | [Last Rotation] | [Storage Location]

## Completed Tasks
[Task ID] | [Priority] | [Domain] | [Creation Date] | [Completion Date] | [Duration]
```

### Rotation Log Structure

All rotation events are documented in the rotation log:

```markdown
# Task Rotation Log
**Edition #X.Y.Z | Last Updated: YYYY-MM-DD**

## Recent Rotations

### YYYY-MM-DD HH:MM:SS
**Trigger:** [Trigger Type]
**Promoted:** [Task IDs moved to active queue]
**Demoted:** [Task IDs moved to extended storage]
**Active Queue Status:** [Current line count] / 50 lines
```

## Task Status Transitions

Tasks follow this lifecycle through the rotation system:

1. **Creation:**
   - Task created with PENDING status
   - Evaluated for immediate active queue placement
   - Placed in either active queue or extended storage based on priority and space

2. **Pending in Extended Storage:**
   - Regular priority recalculation based on aging
   - Awaiting promotion trigger conditions
   - Metadata updated with wait duration

3. **Promotion to Active Queue:**
   - Moved from extended storage to active queue
   - Rotation logged with rationale
   - Registry updated with new location
   - Status remains PENDING

4. **Active Pending:**
   - Available for selection in active queue
   - Protected from immediate demotion (24-hour grace period)
   - Awaiting user selection or status change

5. **In Progress:**
   - User begins task implementation
   - Status changed to IN_PROGRESS
   - Priority protection applied
   - Extended protection from demotion

6. **Demotion (if necessary):**
   - Moved from active queue to extended storage
   - Rotation logged with rationale
   - Registry updated with new location
   - Status preserved (PENDING or IN_PROGRESS)

7. **Completion:**
   - User completes task implementation
   - Status changed to COMPLETED
   - Task removed from active queue
   - Registry updated with completion date
   - Task record moved to completed tasks file

## Usage Guide

### Managing Active Queue Size

To maintain the active queue within size limits:

1. **Monitor Size Indicators:**
   - System displays current line count in active queue header
   - Warning indicators appear as queue approaches capacity
   - Critical alerts trigger automatic rotation

2. **Preemptive Rotation:**
   - Use manual rotation command when queue reaches 45+ lines
   - Specify domain balance priorities for rotation
   - Review proposed rotations before confirmation

3. **Size Reduction Techniques:**
   - Complete tasks to reduce queue size
   - Mark lower-priority tasks for priority demotion
   - Address dependency chains to unlock task completion

### Accessing Extended Storage Tasks

To work with tasks in extended storage:

1. **Browsing Extended Storage:**
   - Use domain-specific commands to view extended tasks
   - Filter by priority, age, or keywords
   - Full task details available on demand

2. **Priority Adjustments:**
   - Manually adjust task priority to influence rotation
   - Flag tasks for promotion consideration
   - Add user interest markers to increase priority score

3. **Manual Promotion:**
   - Override automatic rotation for specific tasks
   - Swap active and extended tasks directly
   - Create space in active queue before promotion

### Rotation System Management

To optimize the rotation system:

1. **Configure Rotation Parameters:**
   - Adjust trigger thresholds for different conditions
   - Modify priority scoring factors
   - Set domain balance requirements

2. **Monitor Rotation Patterns:**
   - Review rotation log for frequency and triggers
   - Track average wait times in extended storage
   - Identify priority calculation anomalies

3. **Optimize Task Structure:**
   - Standardize task formats for predictable sizing
   - Create appropriate dependencies between related tasks
   - Balance task creation across domains

## Benefits

The Task Rotation System provides numerous advantages:

1. **Manageable Workload:** Active queue never overwhelms with too many options
2. **Priority Focus:** Highest-impact tasks always visible
3. **Unlimited Capacity:** No practical limit to number of managed tasks
4. **Fair Rotation:** No task remains in extended storage indefinitely
5. **Domain Balance:** All narrative areas receive attention
6. **Dependency Management:** Related tasks appear in appropriate sequence
7. **Complete Tracking:** No tasks lost or forgotten in rotation
8. **Efficient Organization:** Tasks stored logically by domain and priority

## Conclusion

The Task Rotation System transforms the Turd Bird Universe task management from a potentially overwhelming list into a strategic, priority-focused workflow. By maintaining a strict 50-line limit on the active queue while providing unlimited extended storage capacity, it enables Augusta "Gust" Turing to manage complex narrative development without information overload while ensuring all tasks—regardless of storage location—are properly tracked, prioritized, and ultimately addressed.