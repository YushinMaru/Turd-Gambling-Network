# Standard Content Type Templates
**Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)**

> Previous: None (Initial Documentation)

> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**

## Context

This document catalogs standardized template files for all content types used in the Turd Bird Universe. These templates ensure consistency in structure, metadata, and reference implementation across all narrative documentation.

## Available Templates

The following template files have been created for standard content types:

### Character Templates

| Template File | Purpose | Key Sections |
|---------------|---------|-------------|
| [character-profile-template.md](/mnt/z/Turdbot/Turd History/systems/templates/character-profile-template.md) | Complete character documentation | Overview, Physical Appearance, Personality, History, Relationships, Quotes |
| [character-overview-brief.template](/mnt/z/Turdbot/Turd History/systems/templates/character-overview-brief.template) | Concise character summary with component references | Core Identity, Component Structure, Overview Visualization |
| [character-attributes-physical.template](/mnt/z/Turdbot/Turd History/systems/templates/character-attributes-physical.template) | Detailed physical appearance documentation | Age/Build, Features, Attire, Accessories, Presence |
| [character-attributes-personality.template](/mnt/z/Turdbot/Turd History/systems/templates/character-attributes-personality.template) | Comprehensive personality documentation | Core Traits, Motivation, Intelligence, Risk Approach, Ethics, Quirks |

### Relationship Templates

| Template File | Purpose | Key Sections |
|---------------|---------|-------------|
| [relationship-template.md](/mnt/z/Turdbot/Turd History/systems/templates/relationship-template.md) | Character relationship documentation | Overview, Attributes, Development, Key Interactions, Narrative Impact |

### Timeline Templates

| Template File | Purpose | Key Sections |
|---------------|---------|-------------|
| [timeline-event-template.md](/mnt/z/Turdbot/Turd History/systems/templates/timeline-event-template.md) | Chronological event documentation | Overview, Participants, Development, Perspectives, Consequences |

### Corporate Templates

| Template File | Purpose | Key Sections |
|---------------|---------|-------------|
| [corporate-entity-template.md](/mnt/z/Turdbot/Turd History/systems/templates/corporate-entity-template.md) | Corporate structure documentation | Overview, Identity, Organization, History, Products, Facilities |
| [product-innovation-template.md](/mnt/z/Turdbot/Turd History/systems/templates/product-innovation-template.md) | Product/service documentation | Specifications, Development, Market Impact, Incidents, Evolution |

## Directory Templates

Additionally, the following directory structure templates are available for different character types:

| Template File | Purpose | Directory Structure |
|---------------|---------|---------------------|
| [character-directory-primary.template](/mnt/z/Turdbot/Turd History/systems/templates/character-directory-primary.template) | Primary character directory structure | Comprehensive with all subdirectories |
| [character-directory-secondary.template](/mnt/z/Turdbot/Turd History/systems/templates/character-directory-secondary.template) | Secondary character directory structure | Intermediate level detail |
| [character-directory-minor.template](/mnt/z/Turdbot/Turd History/systems/templates/character-directory-minor.template) | Minor character directory structure | Minimal structure in grouped categories |

## Template Usage Guidelines

### Selection Process

1. **Identify Content Type**: Determine the appropriate template category for the new content
2. **Assess Detail Level**: Select the template with appropriate depth based on narrative significance
3. **Consider Dependencies**: Ensure any referenced components or parent structures exist or are planned

### Customization Protocols

1. **Replace Placeholders**: Fill in all placeholders ({{PLACEHOLDER_TEXT}}) with specific content
2. **Maintain Structure**: Preserve the sectional organization of the template
3. **Implement References**: Create all bidirectional references to related content
4. **Version Properly**: Maintain correct versioning in document header and history

### Implementation Workflow

1. **Copy Template**: Use the template as the foundation for new content
2. **Configure Metadata**: Set appropriate edition, creation info, and version history
3. **Populate Content**: Fill in all sections with appropriate detail and references
4. **Validate References**: Ensure all bidirectional references are implemented correctly
5. **Verify Size Limit**: Confirm the final file remains under the 150-line limit

## Template File Naming Conventions

All template files follow these naming conventions:

1. **Template Designator**: All templates use `.template` extension or `-template.md` suffix
2. **Content Type Prefix**: Templates begin with the content type (e.g., `character-`, `relationship-`)
3. **Specificity Indicator**: Templates include descriptor of purpose (e.g., `-overview-`, `-attributes-`)
4. **Template Sequence**: Related templates are organized alphabetically by specificity

## Template Maintenance

Templates are versioned and updated as the narrative architecture evolves:

1. **Backward Compatibility**: Template updates maintain compatibility with existing content
2. **Announcement Process**: Template changes are announced via the task system
3. **Migration Protocol**: Content created with outdated templates is updated systematically
4. **Template Registry**: All templates are registered in this central documentation

## References

- [/docs/standards/modular-content-guidelines.md § CONTENT-TYPES]
- [/docs/standards/documentation-naming-standards.md § TEMPLATE-NAMING]
- [/docs/standards/bidirectional-reference-system.md § TEMPLATE-REFERENCES]
- [/registry/reference-registry.md § TEMPLATE-REF-001]

## Version History

### v1.0.0 - 2025-05-06
- Initial documentation of standard content type templates
- Created comprehensive template catalog with usage guidelines
- Established reference structure for template maintenance