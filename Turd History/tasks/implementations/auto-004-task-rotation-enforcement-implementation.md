# Task Rotation Enforcement Script Implementation
**Task ID:** AUTO-004
**Priority:** HIGH
**Status:** IN_PROGRESS
**Related Systems:** Task Management
**Created:** 2025-05-07

## Implementation Plan

This implementation document outlines the development of a bash script that enforces the Task Rotation system by automatically managing the flow of tasks between the active queue and extended storage based on the defined rotation triggers and algorithms.

### Components to Implement

1. **Queue Size Monitoring**
   - Check current-tasks.md line count against 50-line limit
   - Track approaching capacity thresholds (45+ lines)
   - Provide warnings when queue approaches capacity
   - Implement emergency handling for overflow situations

2. **Task Prioritization System**
   - Implement priority scoring algorithm for task selection
   - Calculate scores based on priority level, age, domain, dependencies
   - Apply appropriate weighting factors to each component
   - Sort tasks by priority score for rotation decisions

3. **Task Movement Mechanism**
   - Move tasks between active queue and extended storage
   - Preserve task formatting and metadata during moves
   - Handle rotation for different task categories
   - Maintain task continuity during transitions

4. **Task Registry Updates**
   - Update task registry with new task locations
   - Track rotation history for each task
   - Record rotation justification and triggers
   - Maintain consistent registry state

5. **Domain Balance Management**
   - Track representation of different task domains
   - Ensure minimum task count per domain
   - Apply domain balance modifiers to priority scores
   - Enforce minimum domain representation rules

6. **Protection System**
   - Implement protection for IN_PROGRESS tasks
   - Honor task protection flags
   - Apply demotion protection for newly promoted tasks
   - Handle conflict resolution when protected tasks cause overflow

## Implementation Approach

1. **Create Core Functions**
   - Implement line counting for queue size monitoring
   - Create task extraction and parsing utilities
   - Build priority score calculation function
   - Develop task movement operations

2. **Develop Rotation Logic**
   - Implement all rotation triggers
   - Create selection algorithms for promotion and demotion
   - Build decision workflow for rotation events
   - Develop logging for rotation operations

3. **Add Registry Management**
   - Implement registry update functions
   - Create rotation logging in registry
   - Develop historical tracking mechanisms
   - Add statistics for rotation operations

4. **Handle Edge Cases**
   - Implement emergency overflow handling
   - Create recovery mechanisms for interrupted rotations
   - Add safeguards against circular dependencies
   - Develop conflict resolution for protection violations

5. **Create User Interface**
   - Implement reporting on rotation operations
   - Add user-friendly status messages
   - Create rich feedback on rotation decisions
   - Add elegant Augusta-style rotation confirmations

## Rotation Triggers

The script will implement these rotation triggers:

1. **Space Available Trigger**
   - Condition: Active queue drops below 40 lines
   - Action: Promote highest-priority tasks from extended storage
   - Limit: Add tasks until active queue reaches 45 lines

2. **Task Completion Trigger**
   - Condition: Task marked as completed in active queue
   - Action: Remove completed task and promote replacement
   - Timing: Immediate rotation after task completion

3. **Priority Threshold Trigger**
   - Condition: New HIGH priority task created when queue is full
   - Action: Demote lowest-priority active task to make room
   - Override: Only applies if new task's priority exceeds lowest active task

4. **Dependency Resolution Trigger**
   - Condition: Prerequisite task completed for tasks in extended storage
   - Action: Evaluate dependent tasks for promotion
   - Priority: Increase dependent task priority

5. **Domain Balance Trigger**
   - Condition: Domain representation falls below threshold
   - Action: Promote highest-priority task from underrepresented domain
   - Balance: May demote lowest-priority task from overrepresented domain

6. **Age Threshold Trigger**
   - Condition: Task in extended storage exceeds maximum wait time
   - Action: Gradually increase priority until task qualifies for promotion
   - Limiter: Rate of priority increase based on original priority level

## Implementation Files

1. **Bash Script**
   - Path: `/mnt/z/Turdbot/Turd History/systems/task-rotation-enforcer.sh`
   - Purpose: Main script for task rotation enforcement

2. **Documentation**
   - Path: `/mnt/z/Turdbot/Turd History/systems/task-rotation-enforcer.md`
   - Purpose: User guide and reference for script usage

3. **Configuration File**
   - Path: `/mnt/z/Turdbot/Turd History/systems/task-rotation-config.json`
   - Purpose: Configurable parameters for rotation operation

## Technical Details

### Task File Structure Management

The script will maintain the task file structures:

```
/tasks/
├── current-tasks.md        # Active task queue (50-line limit)
├── completed-tasks.md      # Recently completed tasks (30 tasks limit)
├── archives/               # Archived completed tasks
│   └── {year}-{month}-completed.md
└── extended/               # Extended storage for pending tasks
    ├── character-tasks.md
    ├── timeline-tasks.md
    ├── corporate-tasks.md
    ├── relationship-tasks.md
    └── worldbuilding-tasks.md
```

### Priority Score Calculation

The script will implement this priority scoring algorithm:

```
priority_score = base_priority_value + age_factor + dependency_modifier + domain_balance_modifier + user_interest_factor

Where:
- base_priority_value = HIGH:100, MEDIUM:50, LOW:10
- age_factor = days_in_extended_storage
- dependency_modifier = recently_completed_dependency ? 50 : 0
- domain_balance_modifier = underrepresented_domain ? 20 : 0
- user_interest_factor = related_to_recent_activity ? 50 : 0
```

### Task Movement Operations

For task movement between files, the script will:

1. Extract task content from source file
2. Remove task from source file
3. Add task to destination file in proper location
4. Update task registry with new location
5. Log rotation in rotation history

### Registry Management

The script will update registry entries with:

1. Current location (active/extended/completed)
2. Last rotation timestamp
3. Rotation count
4. Current priority score
5. Protection status

## Usage Examples

```bash
# Run complete rotation cycle with all triggers
./task-rotation-enforcer.sh --full-cycle

# Check queue size only and provide warnings
./task-rotation-enforcer.sh --check-size

# Apply space available trigger only
./task-rotation-enforcer.sh --space-available

# Force promotion of specific task
./task-rotation-enforcer.sh --promote TASK-001

# Force demotion of specific task
./task-rotation-enforcer.sh --demote TASK-002

# Enforce domain balance only
./task-rotation-enforcer.sh --balance-domains
```

## Implementation Status

- [ ] Queue size monitoring
- [ ] Task prioritization system
- [ ] Task movement mechanism
- [ ] Task registry updates
- [ ] Domain balance management
- [ ] Protection system
- [ ] Rotation trigger implementation
- [ ] Documentation
- [ ] Testing and validation

## Notes

This implementation follows the architectural requirements outlined in the Task Rotation system documentation, focusing on maintaining the 50-line limit in the active queue while ensuring proper task prioritization and domain balance.