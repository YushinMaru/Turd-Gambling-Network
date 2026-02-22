# Reference Pattern Standards
**Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)**

> Previous: None (Initial Documentation)

> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**

## Context

This document establishes standardized reference patterns for different content types in the Turd Bird Universe, ensuring consistent and predictable bidirectional references throughout the documentation. These patterns build upon the foundation defined in `/docs/standards/bidirectional-reference-system.md` while providing specific implementation standards for each content relationship type.

## Reference Pattern Matrix

The following matrix defines standard reference patterns between different content types:

| Source Type | Target Type | Relationship Type | Direction | Section ID Pattern |
|------------|-------------|-------------------|-----------|-------------------|
| Character  | Character   | relationship      | bidirectional | RELATIONSHIPS § TARGET-NAME |
| Character  | Timeline    | participation     | bidirectional | HISTORY § EVENT-NAME |
| Character  | Corporate   | affiliation       | bidirectional | CAREER § ENTITY-NAME |
| Character  | Product     | creation          | bidirectional | INNOVATIONS § PRODUCT-NAME |
| Timeline   | Timeline    | chronology        | bidirectional | RELATED-EVENTS § EVENT-NAME |
| Timeline   | Character   | involvement       | bidirectional | PARTICIPANTS § CHARACTER-NAME |
| Timeline   | Corporate   | impact            | bidirectional | AFFECTED-ENTITIES § ENTITY-NAME |
| Corporate  | Character   | personnel         | bidirectional | PERSONNEL § CHARACTER-NAME |
| Corporate  | Timeline    | history           | bidirectional | HISTORY § EVENT-NAME |
| Corporate  | Product     | portfolio         | bidirectional | PRODUCTS § PRODUCT-NAME |
| Product    | Character   | developer         | bidirectional | DEVELOPERS § CHARACTER-NAME |
| Product    | Corporate   | origin            | bidirectional | SOURCE § ENTITY-NAME |
| Product    | Timeline    | development       | bidirectional | TIMELINE § EVENT-NAME |

## Character-to-Character Reference Patterns

When referencing between character documents:

### Primary Pattern

```markdown
<reference 
  target="/characters/{character-name}/_profile/character-{name}-overview.md § RELATIONSHIPS § {SOURCE-CHARACTER}" 
  type="relationship" 
  direction="bidirectional"
  created="{DATE}"
  created-by="{CREATOR-ID}">
{Relationship description from this character's perspective}
</reference>
```

### Registry Entry Format

```markdown
### REF-CHAR-{ID}
**Source:** /characters/{source-character}/_profile/character-{source}-overview.md § RELATIONSHIPS § {TARGET-CHARACTER}
**Target:** /characters/{target-character}/_profile/character-{target}-overview.md § RELATIONSHIPS § {SOURCE-CHARACTER}
**Type:** relationship
**Direction:** bidirectional
**Created:** {DATE}
**Created By:** {CREATOR-ID}
**Modified:** {DATE}
**Modified By:** {CREATOR-ID}
**Status:** VALIDATED

**Context:**
{Brief description of relationship dynamic between the characters}
```

### Standard Section IDs

All character-to-character references should use these standardized section IDs:

- `RELATIONSHIPS`: Main relationships section in profile
- `RELATIONSHIPS § CHARACTER-NAME`: Specific subsection for each relationship
- `ORIGIN-CONNECTIONS`: Early relationship formation section
- `CURRENT-DYNAMICS`: Present state of relationships section
- `ANTAGONISMS`: Negative relationship section
- `ALLIANCES`: Positive relationship section

## Character-to-Timeline Reference Patterns

When referencing between character and timeline documents:

### Primary Pattern

```markdown
<reference 
  target="/timeline/event-{event-name}.md § PARTICIPANTS § {CHARACTER-NAME}" 
  type="participation" 
  direction="bidirectional"
  created="{DATE}"
  created-by="{CREATOR-ID}">
{Description of character's involvement in the event}
</reference>
```

### Registry Entry Format

```markdown
### REF-CHARTIME-{ID}
**Source:** /characters/{character-name}/_profile/character-{name}-overview.md § HISTORY § {EVENT-NAME}
**Target:** /timeline/event-{event-name}.md § PARTICIPANTS § {CHARACTER-NAME}
**Type:** participation
**Direction:** bidirectional
**Created:** {DATE}
**Created By:** {CREATOR-ID}
**Modified:** {DATE}
**Modified By:** {CREATOR-ID}
**Status:** VALIDATED

**Context:**
{Brief description of character's involvement in the event}
```

### Standard Section IDs

All character-to-timeline references should use these standardized section IDs:

- `HISTORY`: Main historical events section in character profile
- `HISTORY § EVENT-NAME`: Specific subsection for each event
- `PARTICIPANTS`: Main participants section in timeline event
- `PARTICIPANTS § CHARACTER-NAME`: Specific subsection for each character
- `KEY-MOMENTS`: Critical character moments section
- `FORMATIVE-EVENTS`: Character development events section

## Timeline-to-Timeline Reference Patterns

When referencing between timeline documents:

### Primary Pattern

```markdown
<reference 
  target="/timeline/event-{related-event}.md § RELATED-EVENTS § {THIS-EVENT}" 
  type="{chronology-type}" 
  direction="bidirectional"
  created="{DATE}"
  created-by="{CREATOR-ID}">
{Description of chronological relationship between events}
</reference>
```

### Registry Entry Format

```markdown
### REF-TIME-{ID}
**Source:** /timeline/event-{source-event}.md § RELATED-EVENTS § {TARGET-EVENT}
**Target:** /timeline/event-{target-event}.md § RELATED-EVENTS § {SOURCE-EVENT}
**Type:** {chronology-type}
**Direction:** bidirectional
**Created:** {DATE}
**Created By:** {CREATOR-ID}
**Modified:** {DATE}
**Modified By:** {CREATOR-ID}
**Status:** VALIDATED

**Context:**
{Brief description of chronological relationship}
```

### Chronology Relationship Types

Timeline-to-timeline references should use these relationship types:

- `precedes`: The source event happens before the target event
- `follows`: The source event happens after the target event
- `causes`: The source event directly causes the target event
- `caused-by`: The source event is directly caused by the target event
- `concurrent`: The source event happens simultaneously with the target event
- `alternative`: The source event represents an alternative to the target event

### Standard Section IDs

All timeline-to-timeline references should use these standardized section IDs:

- `RELATED-EVENTS`: Main related events section
- `RELATED-EVENTS § EVENT-NAME`: Specific subsection for each related event
- `PRECURSORS`: Events leading to this event
- `AFTERMATH`: Events resulting from this event
- `CONCURRENT-EVENTS`: Events occurring simultaneously

## Corporate-to-Character Reference Patterns

When referencing between corporate entity and character documents:

### Primary Pattern

```markdown
<reference 
  target="/characters/{character-name}/_profile/character-{name}-overview.md § CAREER § {ENTITY-NAME}" 
  type="affiliation" 
  direction="bidirectional"
  created="{DATE}"
  created-by="{CREATOR-ID}">
{Description of character's role in corporate entity}
</reference>
```

### Registry Entry Format

```markdown
### REF-CORCHAR-{ID}
**Source:** /corporate/entity-{entity-name}.md § PERSONNEL § {CHARACTER-NAME}
**Target:** /characters/{character-name}/_profile/character-{name}-overview.md § CAREER § {ENTITY-NAME}
**Type:** affiliation
**Direction:** bidirectional
**Created:** {DATE}
**Created By:** {CREATOR-ID}
**Modified:** {DATE}
**Modified By:** {CREATOR-ID}
**Status:** VALIDATED

**Context:**
{Brief description of character's role in corporate entity}
```

### Standard Section IDs

All corporate-to-character references should use these standardized section IDs:

- `PERSONNEL`: Main personnel section in corporate document
- `PERSONNEL § CHARACTER-NAME`: Specific subsection for each character
- `LEADERSHIP`: Executive leadership section
- `FOUNDERS`: Founding members section
- `KEY-CONTRIBUTORS`: Significant personnel section
- `CAREER`: Career history section in character profile
- `CAREER § ENTITY-NAME`: Specific subsection for each corporate entity

## Product-to-Character Reference Patterns

When referencing between product and character documents:

### Primary Pattern

```markdown
<reference 
  target="/characters/{character-name}/_profile/character-{name}-overview.md § INNOVATIONS § {PRODUCT-NAME}" 
  type="creation" 
  direction="bidirectional"
  created="{DATE}"
  created-by="{CREATOR-ID}">
{Description of character's contribution to product}
</reference>
```

### Registry Entry Format

```markdown
### REF-PRODCHAR-{ID}
**Source:** /products/{category}/product-{product-name}.md § DEVELOPERS § {CHARACTER-NAME}
**Target:** /characters/{character-name}/_profile/character-{name}-overview.md § INNOVATIONS § {PRODUCT-NAME}
**Type:** creation
**Direction:** bidirectional
**Created:** {DATE}
**Created By:** {CREATOR-ID}
**Modified:** {DATE}
**Modified By:** {CREATOR-ID}
**Status:** VALIDATED

**Context:**
{Brief description of character's contribution to product}
```

### Standard Section IDs

All product-to-character references should use these standardized section IDs:

- `DEVELOPERS`: Main developers section in product document
- `DEVELOPERS § CHARACTER-NAME`: Specific subsection for each character
- `LEAD-DEVELOPER`: Primary creator section
- `CONTRIBUTORS`: Additional developer section
- `INNOVATIONS`: Created products section in character profile
- `INNOVATIONS § PRODUCT-NAME`: Specific subsection for each product

## Reference Validator Tool

A reference validator tool has been implemented to verify adherence to these reference pattern standards:

### Usage

```bash
./systems/validate-references.sh [file_path]
```

The validator performs these checks:

1. **Pattern Compliance**: Verifies references follow standardized patterns
2. **Section ID Validation**: Confirms use of standard section IDs
3. **Relationship Type Verification**: Ensures appropriate relationship types
4. **Bidirectional Integrity**: Validates both sides of bidirectional references
5. **Registry Consistency**: Checks reference registry entries match actual references

### Error Reporting

Validation errors are reported in this format:

```
ERROR: Invalid reference pattern in /path/to/file.md
Expected: [Correct pattern format]
Found: [Actual reference]
Fix: [Suggested correction]
```

## Implementation Guidelines

When implementing reference patterns:

1. **Use Standard Patterns**: Always use the defined patterns for your content types
2. **Maintain Bidirectionality**: Ensure references exist in both source and target
3. **Use Correct Section IDs**: Follow the standard section ID conventions
4. **Register All References**: Add entries to the reference registry
5. **Validate Regularly**: Run the validator tool to ensure compliance
6. **Update Both Sides**: When modifying references, update both documents
7. **Update Registry**: Keep the registry entry synchronized with references

## References

- [/docs/standards/bidirectional-reference-system.md § IMPLEMENTATION]
- [/docs/standards/modular-content-guidelines.md § REFERENCE-MECHANISMS]
- [/registry/reference-registry.md § SCHEMA]
- [/systems/reference-validator.md § VALIDATION-RULES]

## Version History

### v1.0.0 - 2025-05-06
- Initial documentation of reference pattern standards
- Defined comprehensive reference matrix for all content types
- Established standard section IDs and registry entry formats
- Documented reference validator tool and implementation guidelines