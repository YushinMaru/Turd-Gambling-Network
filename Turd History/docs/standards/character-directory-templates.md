# Character Directory Templates
**Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)**

> Previous: None (Initial Documentation)

> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**

## Context
This document provides standardized directory templates for all character types (primary, secondary, minor) within the Turd Bird Universe. These templates ensure consistent organization of character documentation across the universe while adhering to modular content architecture principles and supporting the bidirectional reference system.

## Primary Character Directory Structure

Primary characters represent the core narrative pillars of the Turd Bird Universe and require the most comprehensive documentation structure. Each primary character should have the following standardized directory structure:

```
/characters/
  /{character-name}/           # Kebab-case name (e.g., fred-turd)
    /_profile/                 # Core identity documentation
      character-{name}-overview.md         # Essential character summary (<150 lines)
      character-{name}-appearance.md       # Physical attributes and presentation
      character-{name}-personality.md      # Psychological makeup and behavioral patterns
      character-{name}-narrative-function.md # Role within the universe structure
    
    /origins/                  # Character backstory and formation
      character-{name}-childhood.md        # Early formative experiences
      character-{name}-education.md        # Academic and intellectual development
      character-{name}-early-career.md     # Initial professional development
    
    /development/              # Character evolution over time
      character-{name}-pivotal-events.md   # Transformative experiences
      character-{name}-arc-{descriptor}.md # Specific developmental trajectories
      character-{name}-evolution-{trait}.md # How specific traits changed over time
    
    /relationships/            # Interpersonal dynamics
      relationship-{name}-{other}-{type}.md # Individual relationship documentation
      relationship-{name}-network-overview.md # Complete relationship ecosystem
    
    /capabilities/             # Notable abilities and skills
      character-{name}-skills-{category}.md # Domain-specific abilities
      character-{name}-expertise-{area}.md  # Areas of unusual competence
      character-{name}-methods-{approach}.md # Distinctive methodologies
    
    /states/                   # Temporal character snapshots
      character-{name}-state-{year}.md     # Character state at specific time points
      character-{name}-state-{event}.md    # Character state relative to events
    
    /expressions/              # Character voice and communication
      character-{name}-quotes-{theme}.md   # Thematically organized quotations
      character-{name}-philosophy-{topic}.md # Character beliefs and worldview
      character-{name}-communication-style.md # Speaking patterns and methods
    
    /possessions/              # Significant items and environments
      character-{name}-signature-items.md  # Iconic possessions
      character-{name}-residence-{location}.md # Living/working environments
      character-{name}-technology-{category}.md # Technology associated with character
    
    /impact/                   # Narrative influence
      character-{name}-legacy-{area}.md    # Long-term influence on universe
      character-{name}-influence-{domain}.md # Specific areas of narrative impact
```

### Key Implementation Notes for Primary Characters

1. **Comprehensiveness Requirement**: Primary characters MUST have complete documentation across all core sections (_profile, origins, relationships)

2. **Profile Prioritization**: Always develop the _profile section first to establish character foundation

3. **Temporal Continuity**: States directory should maintain snapshots along major timeline points

4. **Relationship Documentation**: All significant relationships must have dedicated documentation files

5. **Reference Structure**: All character files must implement bidirectional references to related characters, events, and timeline elements

6. **Version Tracking**: All character development must maintain clear versioning to support the versioned character state system

7. **Evolution Emphasis**: Primary character documentation must clearly illustrate character development over time

## Secondary Character Directory Structure

Secondary characters represent important but less central narrative elements. They require substantial but more focused documentation. Each secondary character should have the following standardized directory structure:

```
/characters/
  /{character-name}/           # Kebab-case name (e.g., augusta-turing)
    /_profile/                 # Core identity documentation
      character-{name}-overview.md         # Essential character summary (<150 lines)
      character-{name}-appearance.md       # Physical attributes and presentation
      character-{name}-personality.md      # Psychological makeup and behavioral patterns
    
    /origins/                  # Condensed backstory
      character-{name}-background.md       # Consolidated origin information
    
    /development/              # Key evolutionary points
      character-{name}-arc-{descriptor}.md # Primary developmental trajectory
    
    /relationships/            # Primary relationships only
      relationship-{name}-{other}-{type}.md # Documentation for significant relationships
    
    /capabilities/             # Notable abilities
      character-{name}-skills-overview.md  # Consolidated skills documentation
    
    /states/                   # Fewer temporal snapshots
      character-{name}-state-current.md    # Current character state
      character-{name}-state-origin.md     # Original introduction state
    
    /expressions/              # Character voice
      character-{name}-quotes.md           # Consolidated quotations
```

### Key Implementation Notes for Secondary Characters

1. **Selective Documentation**: Secondary characters require selective rather than comprehensive documentation

2. **Primary Connection Focus**: Documentation should emphasize connections to primary characters and events

3. **Consolidated Structure**: Some directories may contain fewer, more consolidated documents

4. **Profile Requirement**: All secondary characters MUST have complete _profile documentation

5. **Relationship Selectivity**: Only document significant relationships that impact the narrative

6. **Bidirectional References**: All documented relationships must maintain bidirectional references

## Minor Character Directory Structure

Minor characters represent peripheral narrative elements that require focused, minimal documentation. Each minor character should have the following standardized directory structure:

```
/characters/
  /minor-characters/            # Group directory for all minor characters
    /{group-category}/          # Organizational category (e.g., corporate-rivals)
      /{character-name}/        # Individual minor character directory
        character-{name}-overview.md       # Combined profile and relevant details
        relationship-{name}-{primary}-{type}.md # Connection to primary characters
```

### Key Implementation Notes for Minor Characters

1. **Grouped Organization**: Minor characters should be organized by category rather than having equal directory status

2. **Minimal Documentation**: Documentation focuses on essential details and primary character connections

3. **Consolidated Files**: Profile information should be consolidated in the overview document

4. **Relationship Focus**: Document only relationships with primary characters that advance the narrative

5. **Bidirectional References**: All documented relationships must maintain bidirectional references to primary characters

## Directory Naming Standards

All character directories must follow these naming standards:

1. **Character Directory Names**: 
   - Use kebab-case (lowercase with hyphens)
   - Use full character name (e.g., `fred-turd`, not `fred` or `f-turd`)
   - For composite names, include all parts (e.g., `pneumonia-pete` not just `pete`)

2. **File Naming Pattern**:
   - Follow `{type}-{character}-{aspect}[-qualifier].md` format
   - Examples: `character-fred-turd-childhood.md`, `relationship-fred-larry-antagonism.md`

3. **Group Categories for Minor Characters**:
   - `corporate-rivals`: Business competitors and antagonists
   - `associates`: Professional connections without personal relationship
   - `historical-figures`: Characters relevant to backstory but no longer active
   - `family-members`: Relatives with minimal narrative presence
   - `government-officials`: Regulatory or political connections

## References
- [modular-content-guidelines.md § FILE-NAMING-CONVENTIONS]
- [documentation-naming-standards.md § DIRECTORY-NAMING]
- [bidirectional-reference-system.md § IMPLEMENTATION]
- [versioned-character-state.md § DIRECTORY-STRUCTURE]

## Version History
### v1.0.0 - 2025-05-06
- Initial documentation of standardized character directory templates
- Established comprehensive structure for primary, secondary, and minor characters
- Defined implementation notes and naming standards