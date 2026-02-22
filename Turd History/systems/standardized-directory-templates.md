# Standardized Directory Templates
**Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)**

> Previous: None (Initial Documentation)

> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**

## Context
This document implements SYS-012 by providing comprehensive documentation of the standardized directory templates created for all character types (primary, secondary, minor) in the Turd Bird Universe. These templates ensure consistent organization, support modular content architecture, and maintain narrative coherence through bidirectional references.

## Implementation Overview

The standardized directory templates are implemented through:

1. **Template Definition Files**: Located in `/systems/templates/` directory
2. **Generator Script**: The `/systems/generate-character-directory-v2.sh` script automates the creation of character directories following these templates
3. **Example Implementations**: Working examples established for each character type

These components work together to provide a robust, scalable approach to character documentation that strictly adheres to the 150-line limit while maintaining narrative integrity through bidirectional references.

## Directory Template Specifications

### Primary Character Structure

Primary characters represent the core narrative pillars of the Turd Bird Universe and require the most comprehensive documentation. Their directory structure is organized to support extensive character development while maintaining modular content:

```
/{character-name}/           # Kebab-case name (e.g., fred-turd)
  /_profile/                 # Core identity documentation
    character-{name}-overview-brief.md         # Essential character summary (<150 lines)
    /attributes/
      character-{name}-attributes-physical.md   # Physical attributes and presentation
      character-{name}-attributes-personality.md # Psychological makeup and behavioral patterns
    /function/
      character-{name}-function-narrative.md    # Role within the universe structure
    /development/
      character-{name}-development-arc.md       # Character evolution summary
  
  /origins/                  # Character backstory and formation
    character-{name}-childhood.md        # Early formative experiences
    character-{name}-education.md        # Academic and intellectual development
    character-{name}-early-career.md     # Initial professional development
    /phases/
      character-{name}-origins-phase-early.md   # Detailed early phase development
      character-{name}-origins-phase-middle.md  # Detailed middle phase development
    /psychology/
      character-{name}-origins-psychology.md    # Psychological development
    /incidents/
      character-{name}-origins-incident-{descriptor}.md # Notable formative incidents
  
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

### Secondary Character Structure

Secondary characters represent important but less central narrative elements. They require substantial but more focused documentation structure:

```
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

### Minor Character Structure

Minor characters represent peripheral narrative elements that require focused, minimal documentation:

```
/minor-characters/            # Group directory for all minor characters
  /{group-category}/          # Organizational category (e.g., corporate-rivals)
    /{character-name}/        # Individual minor character directory
      character-{name}-overview.md       # Combined profile and relevant details
      relationship-{name}-{primary}-{type}.md # Connection to primary characters
```

## Implementation Components

### Generator Script

The standardized templates are automatically implemented through the `generate-character-directory-v2.sh` script, which:

1. Creates the appropriate directory structure based on character type
2. Generates template files with standard headers and section placeholders
3. Establishes context for each file based on its purpose
4. Includes placeholders for bidirectional references
5. Follows modular content architecture guidelines

### Usage Guidelines

The character directory generator should be used following these guidelines:

1. **Selection of Appropriate Type**: Choose the correct character type (primary, secondary, minor) based on narrative significance
2. **Proper Category Assignment**: For minor characters, select the appropriate category for organization
3. **Kebab-Case Naming**: Use consistent kebab-case for all character names (e.g., `fred-turd`, not `fredTurd` or `Fred_Turd`)
4. **Complete Template Filling**: Populate all required template files for the character type
5. **Reference Implementation**: Ensure all bidirectional references are properly established
6. **Character Registry Update**: Add new characters to the character registry

## Example Usage

To create a new primary character:

```bash
./systems/generate-character-directory-v2.sh new-character-name
```

To create a new secondary character:

```bash
./systems/generate-character-directory-v2.sh -t secondary supporting-character-name
```

To create a new minor character:

```bash
./systems/generate-character-directory-v2.sh -t minor -c corporate-rivals rival-executive-name
```

## Group Categories for Minor Characters

Minor characters are organized into the following standard categories:

- `corporate-rivals`: Business competitors and antagonists
- `associates`: Professional connections without personal relationship
- `historical-figures`: Characters relevant to backstory but no longer active
- `family-members`: Relatives with minimal narrative presence
- `government-officials`: Regulatory or political connections
- `misc`: Miscellaneous characters that don't fit other categories

## File Templates

Each file created by the generator includes standardized headers, sections, and reference placeholders that follow the bidirectional reference system guidelines. The core template includes:

```markdown
# [Character Name] - [File Purpose]
**Edition #1.0.0 | Created: (CREATOR-ID) | Last Modified: (CREATOR-ID)**

> Previous: None (Initial Documentation)

> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**

## Context
[Description of this file's purpose and relationship to the character documentation]

## [Primary Section]
[Content following ultra-refactored file structure guidelines]

## References
[Bidirectional references to related content]

## Version History
### v1.0.0 - [Creation Date]
- Initial documentation created via directory template generator
```

## References
- [/docs/standards/character-directory-templates.md § IMPLEMENTATION-NOTES]
- [/docs/standards/modular-content-guidelines.md § FILE-NAMING-CONVENTIONS]
- [/docs/standards/bidirectional-reference-system.md § IMPLEMENTATION]
- [/docs/standards/file-structure-refactoring.md § CORE-PRINCIPLES]

## Version History
### v1.0.0 - 2025-05-06
- Initial documentation of standardized directory templates
- Implemented templates for primary, secondary, and minor characters
- Created generator script with automated template implementation
- Documented group categories and usage guidelines