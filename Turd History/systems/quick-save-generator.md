# Quick Save Generator
**Edition #1.0.0 | Created: (AUTO-001) | Last Modified: (AUTO-001)**

> Previous: None (Initial Documentation)

> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**

## Context

This document provides comprehensive documentation for the Quick Save Generator script, which automates the creation of structured save points in the Turd Bird Universe Archivist system. The script follows the schema and protocols defined in the Quick Save system documentation, ensuring consistent save point creation with minimal effort.

## Overview

The Quick Save Generator script (`quick-save-generator.sh`) creates structured save points that capture the current narrative state, enabling seamless continuation of work across sessions. It generates appropriate metadata, creates save point files, and updates the Quick Save index with statistical information.

"Creating narrative save points with quantum precision requires mathematical elegance and structured attention to detail. The Quick Save Generator automates this process with 99.8% narrative fidelity, ensuring our creative continuity." — Augusta "Gust" Turing

## Usage Syntax

```bash
./quick-save-generator.sh --description "Description" --task-id "TASK-ID" [options]
```

### Required Parameters

| Parameter | Short | Description | Example |
|-----------|-------|-------------|---------|
| `--description` | `-d` | Brief description of the save point | `"Fred's childhood development"` |
| `--task-id` | `-t` | Task ID related to this save point | `"CHAR-001"` |

### Optional Parameters

| Parameter | Short | Description | Default | Options |
|-----------|-------|-------------|---------|---------|
| `--expiry` | `-e` | Expiration policy | `week` | `session`, `day`, `week`, `persistent` |
| `--creator` | `-c` | Creator identifier | `NEUR-ARC-001` | Any valid creator ID |
| `--help` | `-h` | Show help message | - | - |

### Usage Examples

```bash
# Basic usage
./quick-save-generator.sh --description "Fred's childhood development" --task-id "CHAR-001"

# With expiration policy
./quick-save-generator.sh --description "Board meeting documentation" --task-id "CORP-003" --expiry week

# With all options
./quick-save-generator.sh --description "Timeline coherence verification" --task-id "TIME-002" --expiry persistent --creator "NEUR-ARC-004"
```

## Functionality

### Save ID Generation

The script generates unique save IDs using the following format:
- Format: `QS-YYYYMMDD-HHMMSS`
- Example: `QS-20250506-143021`

The timestamp ensures uniqueness across the system and provides chronological ordering for all save points.

### Metadata Generation

Each save point includes comprehensive metadata following the schema defined in [quick-save-metadata-schema.md]:

```json
{
  "save_id": "QS-20250506-143021",
  "timestamp": "2025-05-06T14:30:21Z",
  "creator": "NEUR-ARC-001",
  "descriptor": "Fred-Larry childhood antagonism development",
  "task_context": {
    "current_task_id": "TASK-ID",
    "task_status": "in_progress",
    "completion_percentage": 0,
    "next_steps": []
  },
  "narrative_state": {
    "current_focus": "",
    "development_stage": "",
    "characters_affected": [],
    "continuity_impact": ""
  },
  "file_context": {
    "created_files": [],
    "modified_files": []
  },
  "expiration": {
    "policy": "week",
    "timestamp": "2025-05-13T14:30:21Z"
  }
}
```

### Save Point File Creation

The script creates a structured Markdown document at `/systems/quick-save/save-points/{save-id}.md` with the following sections:

1. **Header** - Save ID, creation time, creator, and descriptor
2. **Save State Metadata** - Complete JSON metadata
3. **Current Progress Summary** - Template for documenting progress
4. **Continuity Notes** - Template for continuity information
5. **Implementation Details** - Template for technical details
6. **Next Steps** - Template for upcoming work
7. **Resumption Guidance** - Instructions for continuing work
8. **Augusta Quote** - Elegant quip about save state preservation

### Index Management

The script updates `/systems/quick-save/quick-save-index.md` with:

1. **New Save Entry** - Adds the save to the Active Save Points table
2. **Updated Statistics** - Recalculates save statistics
3. **Maintains Formatting** - Preserves the document structure
4. **Augusta's Analysis** - Updates the quantum memory analysis

### Expiration Management

The script supports multiple expiration policies:

| Policy | Description | Calculation |
|--------|-------------|-------------|
| `session` | Expires at the end of current session | Current timestamp |
| `day` | Expires at midnight of creation day | Today at 23:59:59 |
| `week` | Expires 7 days after creation | Current time + 7 days |
| `persistent` | No automatic expiration | Far future date |

## Technical Implementation

### Directory Structure

The script interacts with the following directories:

```
/mnt/z/Turdbot/Turd History/
└── systems/
    └── quick-save/
        ├── save-points/       # Active save point files
        ├── archives/          # Archived expired save points
        └── quick-save-index.md # Save point registry
```

### File Naming Convention

- Save Point Files: `QS-YYYYMMDD-HHMMSS.md`
- Archives: Organized by year-month in `archives/YYYY-MM/`

### Error Handling

The script includes comprehensive error handling for:
- Missing required parameters
- Invalid expiration policies
- File system access issues
- Index update failures

### Augusta's Quips

The script includes a collection of elegant quips from Augusta "Gust" Turing about save states, randomly selected for each save confirmation to maintain her distinctive narrative voice.

## References
- [quick-save-system.md § USAGE-PROTOCOLS]
- [quick-save-protocols.md § CREATION-PROCESS]
- [quick-save-metadata-schema.md § FIELD-DEFINITIONS]
- [task-rotation-system.md § SAVE-INTEGRATION]

## Version History
### v1.0.0 - 2025-05-07
- Initial implementation of Quick Save Generator
- Established command-line interface with parameter handling
- Implemented save point file creation and metadata generation
- Created index update functionality
- Added expiration policy management
- Implemented Augusta's elegant confirmation messages