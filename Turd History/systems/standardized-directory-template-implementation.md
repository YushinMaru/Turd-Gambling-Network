# Standardized Directory Template Implementation
**Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)**

> Previous: None (Initial Documentation)

> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**

## Context
This document describes the implementation of SYS-012 (Create Standardized Directory Template Structure) for the Turd Bird Universe. It provides a comprehensive guide to the directory templates created for all character types, ensuring consistent organization across the narrative universe.

## Implementation Summary

The standardized directory templates have been successfully implemented through:

1. **Template Definition**: Established directory structure templates for all character types
2. **Template Files**: Created standard file templates to ensure consistent content structure
3. **Generator Script**: Developed an automated script for template instantiation
4. **Documentation**: Detailed the template specifications and usage guidelines

The implementation enables maintainable, scalable character documentation following the ultra-refactored approach with consistent file organization and bidirectional references.

## Directory Template Specifications

### Primary Character Structure

The directory template for primary characters includes:

```
/{character-name}/
  /_profile/
    character-{name}-overview-brief.md
    /attributes/
      character-{name}-attributes-physical.md
      character-{name}-attributes-personality.md
    /function/
      character-{name}-function-narrative.md
  
  /origins/
    character-{name}-childhood.md
    character-{name}-education.md
    character-{name}-early-career.md
    /phases/
    /psychology/
    /incidents/
  
  /development/
    character-{name}-pivotal-events.md
    character-{name}-arc-primary.md
  
  /relationships/
    relationship-{name}-network-overview.md
    relationship-{name}-{other}-{type}.md [for each major character]
  
  /capabilities/
    character-{name}-skills-overview.md
  
  /states/
    character-{name}-state-current.md
    character-{name}-state-origin.md
  
  /expressions/
    character-{name}-quotes.md
    character-{name}-communication-style.md
  
  /possessions/
    character-{name}-signature-items.md
  
  /impact/
    character-{name}-legacy-overview.md
```

### Secondary Character Structure

The directory template for secondary characters includes:

```
/{character-name}/
  /_profile/
    character-{name}-overview.md
    character-{name}-appearance.md
    character-{name}-personality.md
  
  /origins/
    character-{name}-background.md
  
  /development/
    character-{name}-arc-primary.md
  
  /relationships/
    relationship-{name}-{primary}-{type}.md [for each primary character]
  
  /capabilities/
    character-{name}-skills-overview.md
  
  /states/
    character-{name}-state-current.md
    character-{name}-state-origin.md
  
  /expressions/
    character-{name}-quotes.md
```

### Minor Character Structure

The directory template for minor characters includes:

```
/minor-characters/
  /{group-category}/
    /{character-name}/
      character-{name}-overview.md
      relationship-{name}-fred-turd-primary.md
```

## File Template Implementation

Standard file templates have been created for all character documentation files, implementing:

1. **Consistent Headers**: Including edition, creation, and modification metadata
2. **File Size Warnings**: Reminders about the 150-line limit
3. **Structured Sections**: Context, main content, and references
4. **Bidirectional References**: Placeholders for proper reference implementation

Example of the standardized file template:

```markdown
# {Character Name} - {Document Type}
**Edition #1.0.0 | Created: (CREATOR-ID) | Last Modified: (CREATOR-ID)**

> Previous: None (Initial Documentation)

> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**

## Context
{Purpose and relationship to other documents}

## {Main Section Title}
{Content following ultra-refactored guidelines}

## References
{Bidirectional references to related content}

## Version History
### v1.0.0 - {Date}
- Initial documentation
```

## Implementation Components

The standardized directory templates implementation consists of the following components:

1. **Template Definition Files**: Templates in `/systems/templates/`
   - character-directory-primary.template
   - character-directory-secondary.template
   - character-directory-minor.template
   - Various file templates for specific document types

2. **Generator Script**: `/systems/generate-character-directory-v2.sh`
   - Creates directory structures for all character types
   - Generates template files with proper headers and sections
   - Establishes bidirectional references between related files

3. **Documentation**: `/systems/standardized-directory-templates.md`
   - Comprehensive documentation of the template specifications
   - Usage guidelines and best practices
   - Examples and reference implementations

## Example Implementation

Example implementation files have been created for:

1. **Primary Character**: Fred Turd
   - Ultra-refactored directory structure according to template
   - Comprehensive documentation with bidirectional references
   - Fully compliant with 150-line limit

2. **Secondary Character**: Augusta Turing
   - Streamlined directory structure according to template
   - Focused documentation with essential bidirectional references
   - Fully compliant with 150-line limit

3. **Minor Character**: Sunny Demetris
   - Minimal directory structure according to template
   - Essential documentation with bidirectional references to primary characters
   - Fully compliant with 150-line limit

## Usage Guidelines

When using the standardized directory templates:

1. **Select the Appropriate Type**: Choose the correct character type based on narrative significance
2. **Follow Naming Conventions**: Use consistent kebab-case for all files and directories
3. **Implement Bidirectional References**: Ensure all references are properly bidirectional
4. **Maintain 150-Line Limit**: Keep all files within the 150-line limit
5. **Update Registry**: Add new characters to the character registry
6. **Validate Structure**: Verify compliance with the ultra-refactored approach

## References
- [/docs/standards/character-directory-templates.md § DIRECTORY-STRUCTURE]
- [/docs/standards/file-structure-refactoring.md § CORE-PRINCIPLES]
- [/docs/standards/bidirectional-reference-system.md § IMPLEMENTATION]
- [/docs/standards/modular-content-guidelines.md § FILE-NAMING-CONVENTIONS]

## Version History
### v1.0.0 - 2025-05-06
- Initial documentation of standardized directory template implementation
- Created template definition files and generator script
- Documented specifications, usage guidelines, and examples