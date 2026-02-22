# Quick Save Metadata Schema
**Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)**

> Previous: None (Initial Documentation)

> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**

## Context

This document defines the metadata schema for Quick Save points in the Turd Bird Universe Archivist system. This structured approach ensures consistent organization of save states and enables sophisticated retrieval, analysis, and continuity management.

## Schema Definition

Each Quick Save implements this comprehensive metadata structure:

```json
{
  "save_id": "QS-{YYYYMMDD}-{HHMMSS}",
  "timestamp": "{ISO8601 timestamp}",
  "creator": "{creator-id}",
  "descriptor": "{brief-description}",
  "task_context": {
    "current_task_id": "{task-id}",
    "task_status": "pending|in_progress|partially_completed",
    "completion_percentage": 0-100,
    "next_steps": [
      {"step": "Step description", "estimated_time": "estimated time in minutes"},
      {"step": "Step description", "estimated_time": "estimated time in minutes"}
    ]
  },
  "narrative_state": {
    "focal_characters": [
      {"name": "Character name", "aspect": "Relevant aspect being developed"}
    ],
    "focal_timeline_points": [
      {"time": "Temporal marker", "event": "Event description"}
    ],
    "developing_elements": [
      {"element_type": "character|relationship|event|product", "element_name": "Name", "aspect": "Aspect being developed"}
    ],
    "key_decisions": [
      {"decision": "Decision description", "impact": "Impact on narrative"}
    ]
  },
  "reference_context": {
    "essential_docs": [
      {"file_path": "Path to document", "relevance": "Relevance to current task"}
    ],
    "related_content": [
      {"file_path": "Path to document", "relevance": "Relevance to current task"}
    ]
  },
  "continuation_markers": {
    "precise_position": "{location-in-task}",
    "creative_direction": "{development-intention}"
  },
  "expiration": {
    "policy": "session|day|week|persistent",
    "timestamp": "{ISO8601 expiration}"
  }
}
```

## Field Definitions

### Core Metadata

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| save_id | String | Unique identifier with timestamp | "QS-20250506-143021" |
| timestamp | String | ISO8601 timestamp of creation | "2025-05-06T14:30:21Z" |
| creator | String | ID of creator | "NEUR-ARC-001" |
| descriptor | String | Brief description of save content | "Fred-Larry childhood antagonism development" |

### Task Context

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| current_task_id | String | ID of task in progress | "RELP-001" |
| task_status | String | Current progress state | "in_progress" |
| completion_percentage | Number | Estimated percentage complete | 65 |
| next_steps | Array | List of immediate next actions | [{"step": "Document Schmidt family incidents", "estimated_time": "30"}] |

### Narrative State

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| focal_characters | Array | Characters central to current development | [{"name": "Fred Turd", "aspect": "Childhood bullying tactics"}] |
| focal_timeline_points | Array | Relevant time points | [{"time": "1969", "event": "First Schmidt family confrontation"}] |
| developing_elements | Array | Elements being actively developed | [{"element_type": "relationship", "element_name": "Fred-Larry antagonism", "aspect": "Psychological foundation"}] |
| key_decisions | Array | Narrative choices made | [{"decision": "Fred's bullying is calculated rather than impulsive", "impact": "Establishes character consistency with adult behavior"}] |

### Reference Context

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| essential_docs | Array | Documents required for continuation | [{"file_path": "/characters/fred-turd/origins/character-fred-turd-childhood.md", "relevance": "Primary development document"}] |
| related_content | Array | Supporting documents | [{"file_path": "/characters/larry-bird/_profile/character-larry-bird-overview.md", "relevance": "Target character perspective"}] |

### Continuation Markers

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| precise_position | String | Exact continuation point | "Completing 'Strategic Manipulation' section" |
| creative_direction | String | Intended development path | "Developing Fred's systematic testing of Larry's emotional triggers" |

### Expiration Configuration

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| policy | String | Retention policy type | "week" |
| timestamp | String | Expiration timestamp | "2025-05-13T14:30:21Z" |

## Index Schema

The Quick Save Index follows this structure:

```json
{
  "active_saves": [
    {
      "save_id": "QS-20250506-143021",
      "descriptor": "Fred-Larry childhood antagonism development",
      "task_id": "RELP-001",
      "timestamp": "2025-05-06T14:30:21Z",
      "expiration": "2025-05-13T00:00:00Z"
    }
  ],
  "expired_saves": [
    {
      "save_id": "QS-20250505-091514",
      "descriptor": "Pete's 92 pneumonia cases documentation",
      "task_id": "CHAR-003",
      "timestamp": "2025-05-05T09:15:14Z",
      "expired_at": "2025-05-06T00:00:00Z",
      "archive_location": "/systems/quick-save/archives/may2025/QS-20250505-091514.md"
    }
  ],
  "statistics": {
    "total_saves_created": 42,
    "active_saves": 5,
    "expired_saves": 37,
    "most_saved_task": "CHAR-003",
    "average_save_frequency": "1.75 per day",
    "save_success_rate": 98.3
  }
}
```

## Save Point Document Template

Each save point document follows this template:

```markdown
# Quick Save: {descriptor}
**Save ID: {save_id} | Created: {timestamp} | Expires: {expiration}**

> Task: {task_id} - {task_title}
> Status: {task_status} ({completion_percentage}% complete)

## Narrative Context

{Brief description of current narrative development focus}

### Focal Elements
- **Characters:** {focal_characters with aspects}
- **Timeline:** {focal_timeline_points}
- **Developing:** {developing_elements}

### Key Decisions
{List of narrative decisions made}

## Continuation Instructions

### Current Position
{precise_position}

### Next Steps
{Detailed list of next steps with estimated time}

### Creative Direction
{creative_direction with specific guidance}

## Essential References
{List of essential documents with relevance notes}

## Related Content
{List of related content with relevance notes}

## Technical Metadata
```json
{Full JSON metadata}
```
```

## References
- [quick-save-system.md § SAVE-POINT-SCHEMA]
- [quick-save-protocols.md § METADATA-IMPLEMENTATION]
- [systems/quick-save-system.md § ADVANCED-FEATURES]

## Version History
### v1.0.0 - 2025-05-06
- Initial documentation of Quick Save metadata schema
- Established field definitions and structure
- Created save point document template
- Defined index schema for save management