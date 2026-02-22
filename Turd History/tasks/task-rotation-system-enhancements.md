# Enhanced Task Rotation System
**Edition #1.0.0 | Created: (NEUR-ARC-002) | Last Modified: (NEUR-ARC-002)**

> Previous: None (Initial Documentation)

> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**

## Overview

The Enhanced Task Rotation System builds upon the established task-rotation-system.md to provide a more sophisticated approach to managing narrative development tasks. This system ensures optimal focus on high-priority tasks while maintaining comprehensive tracking of all narrative elements.

"The probability matrix becomes elegantly balanced when we maintain precisely 50 active tasks, darling. Any more and the quantum narrative coherence begins to degrade at an exponential rate. Any fewer and we sacrifice narrative richness. It's a mathematically exquisite equilibrium." - Augusta "Gust" Turing

## System Architecture Enhancements

### 1. Three-Tier Task Organization

The enhanced system implements a three-tier approach:

1. **Primary Tasks** (50 tasks maximum in current-tasks.md)
   - Highest priority narrative development tasks
   - Active continuity verification requirements
   - In-progress tasks regardless of other factors

2. **Extended Tasks** (Unlimited tasks in /tasks/extended/)
   - Category-specific extended storage files:
     - /tasks/extended/character-tasks.md
     - /tasks/extended/timeline-tasks.md
     - /tasks/extended/relationship-tasks.md
     - /tasks/extended/worldbuilding-tasks.md
   - Comprehensive organization by narrative domain
   - Preserved task formatting and metadata

3. **Completed Tasks** (30 tasks maximum in completed-tasks.md)
   - Most recent task completions for immediate reference
   - Automatically archived to /tasks/archives/{year}-{month}-completed.md
   - Comprehensive completion metadata and narrative impact

### 2. Enhanced Rotation Algorithm

The rotation mechanism follows these sophisticated rules:

1. **Trigger Conditions**:
   - **Overflow Rotation**: Triggered when current-tasks.md exceeds 50 tasks
   - **Deficit Promotion**: Triggered when current-tasks.md falls below 40 tasks
   - **Manual Promotion**: Triggered by `<PROMOTE>` tag for specific tasks
   - **Priority Promotion**: Triggered by priority elevation of extended tasks

2. **Task Selection Logic**:
   - Tasks selected for primary file based on:
     - Status (IN_PROGRESS tasks always remain)
     - Priority (HIGH → MEDIUM → LOW)
     - Narrative domain (CHARACTER → TIMELINE → CORPORATE → RELATIONSHIP)
     - Task age (older pending tasks prioritized)
     - Narrative dependencies (related tasks kept together)
     - User interaction frequency (frequently accessed tasks prioritized)

3. **Rotation Process Enhancement**:
   - Tasks are rotated to category-specific extended files
   - Full task metadata and formatting preserved
   - Bidirectional references maintained between primary and extended files
   - Automatic creation of reference pointers in both locations
   - Quantum timestamp markers for tracking task movement history

4. **Promotion Optimization**:
   - Tasks can be manually promoted with `<PROMOTE>` tag
   - Automated promotion based on dependency analysis
   - Priority elevation triggers automatic promotion
   - Related tasks are co-promoted to maintain narrative coherence
   - Promotion events logged with quantified rationale

## Implementation Guidelines

### 1. Storage Requirements

- **Primary file** must contain AT MOST 50 tasks
- Maintain AT LEAST 40 tasks in primary file for optimal narrative development
- Extended files organized by narrative domain with NO size limit
- Completed tasks file limited to 30 most recent completions
- Regular archiving to `/tasks/archives/{year}-{month}-completed.md`

### 2. Metadata Enhancements

- **Extended Task Metadata**:
  - Original creation timestamp
  - Rotation history with timestamps
  - Priority change tracking
  - Narrative dependency map
  - Access frequency metrics
  - Promotion eligibility score

- **Rotation Event Metadata**:
  - Comprehensive task movement logs
  - Quantified rationale for each rotation
  - Dependency impact analysis
  - Narrative continuity verification
  - Task state preservation confirmation

### 3. Priority Management

- **Dynamic Priority Adjustment**:
  - Age-based priority elevation (older tasks increase in priority)
  - Dependency-based priority inheritance
  - Continuity impact assessment for priority calculation
  - Task completion patterns influence priority
  - Narrative domain distribution balance factor

- **Priority Distribution Balance**:
  - Maintain optimal distribution across priority levels
  - Ensure representation of all narrative domains
  - Balance character development with timeline progression
  - Prevent starvation of lower-priority tasks through forced promotion
  - Monitor and adjust balance metrics after each rotation

## Interaction With Other Systems

### Integration With Quick Save System

The Enhanced Rotation System is fully integrated with the Quick Save System:

1. **Save-Aware Rotation**:
   - Tasks with active save points receive promotion consideration
   - Save metadata includes task location information
   - Rotation events trigger save point index updates

2. **Extended Task Resumption**:
   - Save points for extended tasks remain accessible
   - Resuming an extended task automatically promotes it to primary file
   - Task rotation history includes save point creation events

### Integration With Quantum Scanner

The Enhanced Rotation System works with the Quantum Scanner:

1. **Scan-Based Task Creation**:
   - New tasks identified by scanner added to appropriate location
   - Scanner categorizes and assigns initial priority
   - Continuity issues prioritized for immediate promotion
   - Scanner-identified dependencies influence task grouping

2. **Scanner-Driven Rotation**:
   - Quarterly deep scans trigger rotation system assessment
   - Scanner metrics influence priority distribution targets
   - Narrative coherence metrics adjust rotation algorithms
   - Gap analysis informs automated promotion

## Performance Metrics

The system tracks these key performance indicators:

1. **Task Flow Metrics**:
   - Average time in primary file before completion
   - Extended storage duration statistics
   - Promotion frequency and patterns
   - Priority distribution over time
   - Narrative domain balance measurements

2. **Efficiency Metrics**:
   - Narrative development velocity by domain
   - Task completion rate by priority level
   - Time-to-promotion for extended tasks
   - Manual vs. automated promotion ratio
   - Priority-to-completion correlation

---

"Task rotation is rather like my digital tea service - each cup must be perfectly placed for optimal accessibility while maintaining an aesthetically pleasing arrangement. One wouldn't want the Earl Grey narrative thread hidden behind the Darjeeling character development, would one? The mathematical precision of proper task organization is what separates elegant neural architecture from sartorially offensive data structures, darling." - Augusta "Gust" Turing, Neural Archivist