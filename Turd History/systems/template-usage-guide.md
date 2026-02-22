# Template Usage Guide
**Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)**

> Previous: None (Initial Documentation)

> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**

## Context

This document provides comprehensive guidance for using the standardized templates in the Turd Bird Universe. It includes step-by-step instructions, best practices, and examples to ensure consistent implementation across all content types.

## Template Selection Process

### Content Type Identification

First, determine which content type template is appropriate:

| If you need to document... | Use this template... |
|---------------------------|----------------------|
| A character's complete profile | [character-profile-template.md] |
| A concise character overview | [character-overview-brief.template] |
| A character's physical attributes | [character-attributes-physical.template] |
| A character's personality traits | [character-attributes-personality.template] |
| A relationship between characters | [relationship-template.md] |
| A timeline event | [timeline-event-template.md] |
| A corporate entity | [corporate-entity-template.md] |
| A product or innovation | [product-innovation-template.md] |

### Detail Level Assessment

Select the appropriate detail level based on narrative significance:

1. **Primary Elements** (main characters, pivotal events, core entities):
   - Use the most detailed templates with full sections
   - Complete all optional sections
   - Include comprehensive references

2. **Secondary Elements** (supporting characters, notable events, significant entities):
   - Use standard templates but simplify optional sections
   - Focus on narrative relevance
   - Include targeted references to primary elements

3. **Tertiary Elements** (minor characters, background events, peripheral entities):
   - Use minimal templates or consolidated documentation
   - Focus only on essential information
   - References should connect to higher-significance elements

## Template Implementation Walkthrough

### Step 1: Copy Template File

```bash
cp /mnt/z/Turdbot/Turd History/systems/templates/character-profile-template.md /mnt/z/Turdbot/Turd History/characters/new-character/_profile/character-new-character-overview.md
```

### Step 2: Configure Metadata

Replace the following metadata elements:
- `{{CHARACTER_NAME}}` with the character's full name
- `{{CREATOR_ID}}` with your creator ID (e.g., NEUR-ARC-001)
- Set the Edition as 1.0.0 for new content
- Ensure the "Previous" section indicates "None (Initial Documentation)"

Example:
```markdown
# Maxwell Scumbaum - Character Profile
**Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)**

> Previous: None (Initial Documentation)
```

### Step 3: Replace All Placeholders

Systematically replace all placeholder text (indicated by {{PLACEHOLDER_TEXT}}) with appropriate content:

1. Begin with core identity elements (role, status, etc.)
2. Complete all main sections sequentially
3. Pay special attention to references, ensuring correct paths
4. Ensure all placeholder substitutions maintain correct formatting

### Step 4: Implement Bidirectional References

For each reference to another document:
1. Verify the target document exists (or will be created)
2. Use the correct reference format: [/path/to/file.md § SECTION-ID]
3. Ensure the referenced document includes a reciprocal reference back
4. Update the reference registry with the new connections

Example:
```markdown
## References
- [/characters/fred-turd/_profile/character-fred-turd-overview.md § RELATIONSHIPS]
- [/timeline/thursday-incident.md § PARTICIPANTS]
- [registry/reference-registry.md § CHAR-REF-003]
```

### Step 5: Verify Content Structure

1. Maintain all section headings from the original template
2. Keep the hierarchical structure intact
3. If a section is not applicable, mark it as "N/A" rather than removing it
4. Ensure all tables maintain their structure (add/remove rows as needed)

### Step 6: Validate Line Count

1. Confirm the document remains under 150 lines
2. If approaching the limit, consider refactoring into component files
3. Update component references if refactoring occurs

## Template Customization Guidelines

### Adding Sections

If additional sections are required:

1. Create new sections at the same hierarchical level as similar content
2. Follow the established heading pattern
3. Document the customization in the Version History
4. Consider suggesting a template update if the section is broadly applicable

### Removing Sections

If sections are not applicable:

1. Mark as "N/A" rather than deleting for first-level sections
2. Secondary sections can be removed if truly not applicable
3. Document removed sections in Version History

### Formatting Standards

Maintain consistent formatting:

1. Use `**Bold**` for field labels and emphasis
2. Use `*Italic*` for terms being defined or subtle emphasis
3. Use blockquotes (`>`) for special notes or commentary
4. Use code blocks for technical specifications or examples
5. Use bulleted lists for unordered collections
6. Use numbered lists for sequential processes
7. Use tables for structured data with clear relationships

## Implementation Examples

### Character Profile Example

```markdown
# Maxwell "Max" Scumbaum - Character Profile
**Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)**

> Previous: None (Initial Documentation)

## Overview

**Role:** Host and Executive Producer, "Corporate Underbelly"
**Status:** Active
**First Appearance:** 2012 (The Humiliation)
**Timeline Position:** Present (43 years old)

## Physical Appearance

- **Age/Build:** 43, 5'9", wiry with hunched posture
- **Hair:** Thinning brown, meticulously combed over bald spot
- **Eyes:** Small, darting, watery blue
- **Face:** Perpetual smirk, pointed features, pancake makeup on-camera
- **Attire:** Cheap suits off-camera, expensive suits on-camera
- **Key Accessories:** Press badge, hidden recording devices, breath mints
- **Presence:** Invasive, uncomfortable proximity to subjects
```

### Relationship Example

```markdown
# Relationship: Fred Turd & Larry Bird - Antagonism
**Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)**

## Context

This document details the antagonistic relationship between Fred Turd and Larry Bird, including its history, dynamics, and narrative significance within the Turd Bird Universe.

## Relationship Overview

**Core Dynamic:** Chaos vs. Order
**Current Status:** Cold war / proxy conflicts
**Origin Point:** 1960s (Childhood Bullying)
**Timeline Scope:** 1960s-Present
```

## Troubleshooting Common Issues

### Missing References

If a referenced document doesn't exist:
1. Create a placeholder file with minimal structure
2. Mark the file for future completion in the task system
3. Ensure references use correct format despite being incomplete

### Exceeding Line Limit

If content exceeds 150 lines:
1. Identify logical segmentation points
2. Create component files for specific aspects
3. Update the overview file with references to components
4. Update all bidirectional references to point to new locations

### Inconsistent Formatting

If formatting issues appear:
1. Review markdown syntax in the problematic section
2. Compare to template for correct structure
3. Ensure tables have consistent column counts
4. Verify list formatting is consistent

## References

- [/systems/content-type-templates.md § AVAILABLE-TEMPLATES]
- [/docs/standards/modular-content-guidelines.md § IMPLEMENTATION]
- [/docs/standards/bidirectional-reference-system.md § USAGE]
- [/registry/reference-registry.md § TEMPLATE-USAGE-REF-001]

## Version History

### v1.0.0 - 2025-05-06
- Initial template usage guide documentation
- Created comprehensive implementation walkthrough
- Provided examples and troubleshooting guidance