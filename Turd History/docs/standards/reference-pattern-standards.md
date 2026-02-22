# Reference Pattern Standards
**Edition #1.0.0 | Created: (NEUR-ARC-012) | Last Modified: (NEUR-ARC-012)**

> Previous: None (Initial Documentation)

> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**

## Context

This document establishes comprehensive standards for reference patterns between different content types in the Turd Bird Universe. These standards ensure consistent and predictable bidirectional references throughout the narrative documentation.

## Core Principles

### 1. Semantic Relationship Types

All references must use semantic relationship types that clearly define the nature of the connection between documents:

- **Relationship types must be semantic** - Describe the actual relationship, not just "linked-to"
- **Bidirectional pairs must be defined** - Each relationship type must have a defined counterpart
- **Content type restrictions apply** - Specific relationship types are valid only for certain content pairs
- **Consistent terminology is required** - Use standardized relationship types from the catalog

### 2. Standard Section Placement

References must appear in standard sections within each document type:

- **Primary section name**: "## References" (primary heading level)
- **Grouping by content type**: Group references by content category
- **Ordered presentation**: Character → Timeline → Corporate → Relationship
- **Placement in document**: References section after main content, before version history

### 3. Reference Format Consistency

All references must follow the standard format:

```markdown
- [/path/to/document.md § SECTION-ID] - Relationship type: brief context
```

- **Absolute paths required** - Always use full paths from repository root
- **Section identifiers mandatory** - Target specific sections with § SECTION-ID
- **Relationship type labeled** - Include relationship type after the reference
- **Brief context optional** - Short explanation of relationship relevance

## Relationship Type Catalog

### Character-to-Character Relationships

| Type | Bidirectional Pair | Definition |
|------|-------------------|------------|
| allied-with | allied-with | Strategic or personal alliance (symmetric) |
| antagonistic-toward | antagonistic-toward | Direct conflict or opposition (symmetric) |
| mentors | mentored-by | Provides guidance or teaching |
| reports-to | supervises | Hierarchical reporting relationship |
| rivals-with | rivals-with | Competitive relationship (symmetric) |
| friends-with | friends-with | Personal friendly relationship (symmetric) |
| related-to | related-to | Family or genetic relationship (symmetric) |
| manipulates | manipulated-by | Deceptive or controlling relationship |
| influenced-by | influences | Shaped by actions or characteristics |
| protects | protected-by | Provides security or defense |
| threatened-by | threatens | Experiences threat or danger from |

### Character-to-Timeline Relationships

| Type | Bidirectional Pair | Definition |
|------|-------------------|------------|
| participates-in | involves | Active participant in event |
| witnesses | witnessed-by | Observes but doesn't affect event |
| affected-by | impacts | Changed by event without participation |
| causes | caused-by | Directly precipitates event |
| prevents | prevented-by | Stops event from occurring or escalating |
| learns-from | teaches | Gains knowledge or insight from event |
| discovers-during | discovery-context-for | Makes significant finding during event |
| transforms-during | transformation-context-for | Undergoes fundamental change during event |

### Character-to-Corporate Relationships

| Type | Bidirectional Pair | Definition |
|------|-------------------|------------|
| affiliated-with | affiliates | General connection to organization |
| founded | founded-by | Created or established organization |
| employed-by | employs | Works for organization |
| owns | owned-by | Has ownership or control of entity |
| advises | advised-by | Provides guidance without authority |
| represents | represented-by | Acts as official face or spokesperson |
| consults-for | contracts | Provides specialized services |

### Timeline-to-Timeline Relationships

| Type | Bidirectional Pair | Definition |
|------|-------------------|------------|
| precedes | follows | Happens before without causal link |
| causes | caused-by | Directly precipitates following event |
| prevents | prevented-by | Stops another event from occurring |
| concurrent-with | concurrent-with | Occurs simultaneously (symmetric) |
| related-to | related-to | Thematically connected (symmetric) |
| escalates | escalated-by | Intensifies situation without direct causation |

### Timeline-to-Corporate Relationships

| Type | Bidirectional Pair | Definition |
|------|-------------------|------------|
| impacts | impacted-by | Affects organization significantly |
| creates | created-by | Results in formation of organization |
| restructures | restructured-by | Changes organizational structure |
| references | referenced-in | Mentions or documents organization |
| benefits | benefited-by | Provides advantage to organization |

### Corporate-to-Corporate Relationships

| Type | Bidirectional Pair | Definition |
|------|-------------------|------------|
| subsidiary-of | parent-of | Hierarchical ownership relationship |
| partners-with | partners-with | Collaborative relationship (symmetric) |
| competes-with | competes-with | Market or resource competition (symmetric) |
| supplies | supplied-by | Provides resources or materials |
| customer-of | serves | Receives products or services |
| invested-in | funded-by | Financial stake without control |
| regulates | regulated-by | Provides oversight or rules |

## Reference Pattern Matrix

The following matrix defines valid relationship types for each content type pair:

| Source Type | Target Type | Valid Relationship Types |
|-------------|-------------|-------------------------|
| Character | Character | allied-with, antagonistic-toward, mentors, reports-to, rivals-with, friends-with, related-to, manipulates, influenced-by, protects, threatened-by |
| Character | Timeline | participates-in, witnesses, affected-by, causes, prevents, learns-from, discovers-during, transforms-during |
| Character | Corporate | affiliated-with, founded, employed-by, owns, advises, represents, consults-for |
| Character | Relationship | documented-in, detailed-by, exemplified-by |
| Timeline | Timeline | precedes, follows, causes, prevents, concurrent-with, related-to, escalates |
| Timeline | Character | involves, witnessed-by, impacts, caused-by, prevented-by, teaches, discovery-context-for, transformation-context-for |
| Timeline | Corporate | impacts, creates, restructures, references, benefits |
| Timeline | Relationship | documents, illustrates, exemplifies |
| Corporate | Corporate | subsidiary-of, parent-of, partners-with, competes-with, supplies, customer-of, invested-in, regulates |
| Corporate | Character | affiliates, founded-by, employs, owned-by, advised-by, represented-by, contracts |
| Corporate | Timeline | impacted-by, created-by, restructured-by, referenced-in, benefited-by |
| Relationship | Character | details, chronicles, connects |
| Relationship | Timeline | refers-to, contextualizes, frames |
| Relationship | Corporate | involves, describes, reveals |

## Implementation Guidelines

### Adding New References

When adding a new reference, follow these steps:

1. **Determine content types** - Identify source and target document types
2. **Select appropriate relationship type** - Choose from matrix of valid types
3. **Format reference correctly** - Follow standard format with path and section ID
4. **Place in correct section** - Add to appropriate references grouping
5. **Create bidirectional pair** - Add corresponding reference in target document
6. **Update reference registry** - Add entry to registry with complete metadata

### Example Implementation

#### Character-to-Timeline Reference:

```markdown
## References

### Timeline Events
- [/timeline/events/timeline-2015-thursday-incident.md § PARTICIPANTS] - participates-in: Initiated confrontation with Larry Bird over ReAnimus presentation
```

#### Corresponding Timeline-to-Character Reference:

```markdown
## Related Documentation

### Key Participants
- [/characters/fred-turd/_profile/character-fred-turd-overview.md § HISTORY] - involves: Central figure who initiated confrontation with Larry Bird
```

### Reference Registry Entry:

```markdown
### CHAR-TIME-PART-001
**Source:** characters/fred-turd/_profile/character-fred-turd-overview.md § HISTORY
**Target:** timeline/events/timeline-2015-thursday-incident.md § PARTICIPANTS
**Type:** participates-in
**Direction:** bidirectional
**Created:** 2025-05-07
**Created By:** NEUR-ARC-012
**Modified:** 2025-05-07
**Modified By:** NEUR-ARC-012
**Status:** VALIDATED

**Context:**
Fred's participation in the Thursday Incident represents a pivotal moment in his conflict with Larry Bird, with significant repercussions throughout the corporate structure.
```

## Validation Process

All references must be verified for pattern compliance using the reference validation system:

1. **Run validation script** - Execute `/systems/reference-validator.sh`
2. **Review validation report** - Examine identified issues
3. **Address pattern violations** - Fix incorrect relationship types or section placement
4. **Verify bidirectional integrity** - Ensure all references have matching pairs
5. **Confirm registry entries** - Verify registry contains all references

## References

- [/docs/standards/modular-content-guidelines.md § REFERENCES]
- [/docs/standards/bidirectional-reference-system.md]
- [/systems/reference-validator.md]
- [/registry/reference-registry.md § REGISTRY-MANAGEMENT]

## Version History

### v1.0.0 - 2025-05-07
- Initial documentation of reference pattern standards
- Defined comprehensive relationship type catalog
- Created reference pattern matrix and implementation guidelines