# Task Rotation Enforcer
**Edition #1.0.0 | Created: (AUTO-004) | Last Modified: (AUTO-004)**

> Previous: None (Initial Documentation)

> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**

## Context

This document provides comprehensive documentation for the Task Rotation Enforcer script, which automates the management of tasks between the active queue and extended storage based on defined rotation triggers and algorithms. The system ensures the active queue never exceeds 50 lines while maintaining proper prioritization and domain balance.

## Overview

The Task Rotation Enforcer script (`task-rotation-enforcer.sh`) implements the Task Rotation System described in [task-rotation-system.md], automatically moving tasks between the active queue and extended storage based on priority, domain balance, dependencies, and queue size constraints. It ensures that the most important tasks are always in the active queue while maintaining the 50-line limit.

"The mathematical poetry of task rotation creates a perfect equilibrium between priority and representation. Our quantum workflow algorithms ensure 97.4% efficiency in narrative development by maintaining optimal task distribution." — Augusta "Gust" Turing

## Usage Syntax

```bash
./task-rotation-enforcer.sh [options]
```

### Options

| Option | Description | Example |
|--------|-------------|---------|
| `--full-cycle` | Run complete rotation cycle with all triggers | `--full-cycle` |
| `--check-size` | Check queue size only and provide warnings | `--check-size` |
| `--space-available` | Apply space available trigger only | `--space-available` |
| `--promote <task-id>` | Force promotion of specific task | `--promote CHAR-001` |
| `--demote <task-id>` | Force demotion of specific task | `--demote RELP-002` |
| `--balance-domains` | Enforce domain balance only | `--balance-domains` |
| `--help`, `-h` | Show help message | `--help` |

### Usage Examples

```bash
# Run complete rotation cycle with all triggers
./task-rotation-enforcer.sh --full-cycle

# Check queue size only and provide warnings
./task-rotation-enforcer.sh --check-size

# Apply space available trigger only
./task-rotation-enforcer.sh --space-available

# Force promotion of specific task
./task-rotation-enforcer.sh --promote CHAR-001

# Force demotion of specific task
./task-rotation-enforcer.sh --demote RELP-002

# Enforce domain balance only
./task-rotation-enforcer.sh --balance-domains
```

## Rotation Triggers

The system implements these automatic rotation triggers:

### Space Available Trigger
- **Condition**: Active queue drops below 40 lines
- **Action**: Promote highest-priority tasks from extended storage
- **Limit**: Add tasks until active queue reaches 45 lines
- **Implementation**: Checks queue size and promotes multiple tasks when space available

### Task Completion Trigger
- **Condition**: Task marked as completed in active queue
- **Action**: Remove completed task and promote replacement from extended storage
- **Timing**: Immediate rotation after task completion
- **Implementation**: When a task is completed, automatically promotes a replacement

### Priority Threshold Trigger
- **Condition**: New HIGH priority task created when queue is full
- **Action**: Demote lowest-priority active task to make room
- **Override**: Only applies if new task's priority exceeds lowest active task
- **Implementation**: Compares priority values and makes room for higher priority tasks

### Dependency Resolution Trigger
- **Condition**: Prerequisite task completed for tasks in extended storage
- **Action**: Evaluate dependent tasks for promotion to active queue
- **Priority**: Dependency resolution increases dependent task priority
- **Implementation**: Boosts priority of dependent tasks when prerequisites complete

### Domain Balance Trigger
- **Condition**: Domain representation falls below threshold
- **Action**: Promote highest-priority task from underrepresented domain
- **Balance**: May demote lowest-priority task from overrepresented domain
- **Implementation**: Ensures minimum representation for each domain category

### Age Threshold Trigger
- **Condition**: Task in extended storage exceeds maximum wait time
- **Action**: Gradually increase priority until task qualifies for promotion
- **Limiter**: Rate of priority increase based on original priority level
- **Implementation**: Prevents tasks from remaining in extended storage indefinitely

## Priority Scoring Algorithm

The system uses this algorithm to calculate task priority for rotation decisions:

```
priority_score = base_priority_value + age_factor + dependency_modifier + domain_balance_modifier + user_interest_factor

Where:
- base_priority_value = HIGH:100, MEDIUM:50, LOW:10, CRITICAL:150
- age_factor = days_in_extended_storage
- dependency_modifier = recently_completed_dependency ? 50 : 0
- domain_balance_modifier = underrepresented_domain ? 20 : 0
- user_interest_factor = related_to_recent_activity ? 50 : 0
```

This scoring system ensures that:
1. Higher priority tasks are generally promoted first
2. Tasks don't remain in extended storage indefinitely
3. Tasks with completed dependencies get prioritized
4. Domain balance is maintained
5. Tasks related to current user focus get higher priority

## Protection Rules

The system implements these protection mechanisms:

### IN_PROGRESS Protection
- Tasks marked as IN_PROGRESS are protected from demotion
- Can be configured to override in emergency situations

### New Promotion Protection
- Newly promoted tasks get 24-hour demotion protection
- Prevents immediate demotion of recently promoted tasks

### User Flagged Protection
- Tasks explicitly flagged by users are protected from demotion
- Can be configured to override in extreme space constraints

### Sole Domain Protection
- Tasks that are the only representative of their domain are protected
- Ensures maintained representation of all domains

## Task Movement Process

When tasks are moved between storage locations, the system:

1. **Extracts the task** from its current location
2. **Removes the task** from the source file
3. **Determines correct destination** based on domain and movement type
4. **Inserts the task** into the destination file with proper formatting
5. **Updates the task registry** with the new location
6. **Logs the movement** for audit and reporting

## Report Generation

Each rotation operation produces a detailed report containing:

1. **Queue Status**: Size and state of active queue before rotation
2. **Rotation Decisions**: Triggers activated and resulting actions
3. **Moved Tasks**: Full details of tasks promoted or demoted
4. **Domain Balance**: Analysis of domain representation
5. **Operation Summary**: Overall results and statistics
6. **Augusta Analysis**: Quantum probability assessment of rotation efficiency

## Technical Implementation

The system uses:

1. **Bash Scripting**: Core file manipulation and task movement
2. **JSON Configuration**: All thresholds and rules are configurable
3. **Task Extraction Algorithm**: Identifies and extracts task blocks
4. **Priority Calculation**: Complex algorithm for scoring task importance
5. **Report Generation**: Creates detailed reports of all operations

## References
- [task-rotation-system.md § ROTATION-TRIGGERS]
- [task-rotation-config.json § CONFIGURATION-OPTIONS]
- [task-structure.md § ROTATION-REQUIREMENTS]
- [workflow-protocols.md § TASK-MANAGEMENT]

## Version History
### v1.0.0 - 2025-05-07
- Initial implementation of Task Rotation Enforcer
- Implemented queue size monitoring and triggers
- Created priority scoring algorithm
- Added task movement operations
- Implemented domain balance enforcement
- Added protection rules for task stability
- Created rich reporting system