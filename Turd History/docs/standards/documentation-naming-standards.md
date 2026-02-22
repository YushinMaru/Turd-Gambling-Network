# Documentation Naming Standards
**Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)**

> Previous: None (Initial Documentation)

> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**

This document establishes standard naming conventions and content requirements for all documentation files in the Turd Bird Universe.

## Core Principles

### 1. File Naming Standards

All files in the Turd Bird Universe must follow these naming principles:

- **Descriptive**: Names must clearly reflect content purpose
- **Consistency**: Use the same naming patterns across all documentation
- **Lowercase Only**: Use only lowercase names for all documentation files
- **Kebab Case**: Use kebab-case for multi-word file names
- **Categorized Prefixes**: Include appropriate category prefixes for easy identification
- **No Version Numbers**: Exclude version numbers from filenames
- **No Status Tags**: Remove status tags like "MASTER" from filenames

### 2. File Prefix Categorization

Files must use these standardized prefixes for proper categorization:

- **character-**: For character-related documentation
- **timeline-**: For chronological narrative elements
- **relationship-**: For interpersonal dynamics
- **corporate-**: For organizational documentation
- **product-**: For Turd Bird products/inventions
- **event-**: For significant narrative occurrences
- **system-**: For metadata and architecture documentation

### 3. Standard Naming Examples

| Content Type | Preferred Filename | Incorrect Example |
|--------------|-------------------|---------------------|
| Character Profile | `character-fred-turd-overview.md` | ~~`Fred Turd Profile.md`~~ |
| Character Trait | `character-fred-turd-personality.md` | ~~`Fred's Personality.md`~~ |
| Timeline Event | `timeline-2015-thursday-incident.md` | ~~`The Thursday Incident.md`~~ |
| Relationship | `relationship-fred-larry-antagonism.md` | ~~`Fred and Larry's Rivalry.md`~~ |
| Corporate Element | `corporate-reanimation-initiative.md` | ~~`ReAnimus Project.md`~~ |
| System Document | `system-reference-registry.md` | ~~`Reference Registry.md`~~ |

### 4. File Extensions

- **Markdown**: `.md` for all documentation files

## Directory Naming

### 1. Core Principles

- **Semantic Names**: Use names that reflect content purpose
- **Lowercase Only**: Use only lowercase for directory names
- **Clear Categories**: Organize by narrative domains
- **Consistent Structure**: Maintain parallel patterns across similar content

### 2. Standard Directory Examples

| Content Purpose | Preferred Name | Sub-directories |
|-----------------|----------------|-----------------|
| Character Documents | `/characters` | `/{character-name}/profile`, etc. |
| Timeline Documents | `/timeline` | `/eras`, `/events`, etc. |
| Corporate Documents | `/corporate` | `/departments`, `/products`, etc. |
| Relationship Documents | `/relationships` | `/alliances`, `/conflicts`, etc. |
| Documentation Standards | `/docs/standards` | Various standards documents |
| System Documents | `/systems` | Architecture and metadata docs |
| Tasks | `/tasks` | `/current-tasks`, `/completed-tasks`, etc. |

### 3. Character Directory Structure

Each character should have a standardized directory structure:

```
/characters/
  /{character-name}/
    /_profile/
      character-{name}-overview.md
      character-{name}-appearance.md
      character-{name}-personality.md
    /origins/
      character-{name}-childhood.md
      character-{name}-education.md
    /abilities/
      [relevant ability documents]
    /relationships/
      relationship-{name}-{other}-{type}.md
    /states/
      [character state documents]
    /quotes/
      [quote collection documents]
```

## File Size Management

### 1. Limitation Policy

- **Maximum Size**: 150 lines per content fragment
- **Warning Header**: Every document must include the standardized size limitation header
- **Refactoring Trigger**: When approaching 150 lines, prepare to refactor content

### 2. Required File Size Limitation Header

This header must appear immediately after the document title, edition information, and Previous edition line:

```markdown
> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**
```

### 3. Example of Proper Document Header

```markdown
# Document Title
**Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)**

> Previous: None (Initial Documentation)

> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**

Document content begins here...
```

## Reference System Integration

The naming convention integrates with the bidirectional reference system:

1. **Quantum References**: Use `[file.md § SECTION-ID @ v1.2.3]` format following bidirectional reference guidelines
2. **Registry**: Each document must be recorded in the reference registry with full metadata
3. **Consistency**: Files must be named consistently to ensure reference integrity

## Enforcement and Migration

1. **New Files**: All new files must adhere to these naming standards
2. **Existing Files**: Rename as part of ongoing modularization efforts
3. **Validation**: Verify naming compliance during continuity checks
4. **Registry Updates**: When renaming files, update all references in the reference registry

## Approved Standard Variance Examples

The following variations to standard naming may be approved in specific circumstances:

1. **Multi-Character Relationships**: For documents covering complex relationships between multiple parties, use format:
   `relationship-group-{descriptor}.md`

2. **Timeline Periods**: For timeline documents covering ranges rather than specific dates:
   `timeline-{start-year}-{end-year}-{descriptor}.md`

3. **Versioned Character States**: For character state documentation, include temporal indicators:
   `character-{name}-state-{year}.md`

## Narrative Quote

"After three hours of debate on our naming convention where Fred suggested naming all files after extinct species and Larry advocated for a decimalized hierarchical system with sixteen levels, Augusta 'Gust' Turing introduced this elegantly structured approach. Larry only shed two tears while Fred begrudgingly admitted that 'thylacine-377.2B-alpha.md' lacked a certain... narrative panache." - Gerhard Müller, Head of Engineering