# Relationship Type Standards
**Edition #1.0.0 | Created: (NEUR-ARC-011) | Last Modified: (NEUR-ARC-011)**

> Previous: None (Initial Documentation)

> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**

## Context

This document establishes standardized relationship types for reference connections between different content types within the Turd Bird Universe. These relationship types ensure semantic consistency across all bidirectional references and provide clear meaning to the relationships between narrative elements.

## Relationship Type Matrix

The following matrix defines all standardized relationship types between major content categories:

| Source Type | Target Type | Relationship Types | Bidirectional Type Pairs |
|-------------|-------------|-------------------|--------------------------|
| Character   | Character   | allies-with, antagonistic-toward, subordinate-to, superior-to, familial-with, romantic-with, professional-with, ambivalent-toward, mentors, mentored-by, rivals-with | (allies-with, allies-with), (antagonistic-toward, antagonistic-toward), (subordinate-to, superior-to), (mentors, mentored-by), (rivals-with, rivals-with) |
| Character   | Timeline    | participates-in, influences, witnesses, affected-by, orchestrates, victimized-by | (participates-in, involves), (influences, influenced-by), (witnesses, witnessed-by), (affected-by, affects), (orchestrates, orchestrated-by), (victimized-by, victimizes) |
| Character   | Corporate   | founded, employed-by, consults-for, invests-in, manages, shareholds-in, opposes | (founded, founded-by), (employed-by, employs), (consults-for, consulting-by), (invests-in, invested-by), (manages, managed-by), (shareholds-in, shareholding-by), (opposes, opposed-by) |
| Character   | Product     | created, uses, maintains, markets, inspired, sabotages | (created, created-by), (uses, used-by), (maintains, maintained-by), (markets, marketed-by), (inspired, inspired-by), (sabotages, sabotaged-by) |
| Timeline    | Timeline    | precedes, follows, causes, caused-by, concurrent-with, alternative-to, diverges-from | (precedes, follows), (causes, caused-by), (concurrent-with, concurrent-with), (alternative-to, alternative-to), (diverges-from, diverged-by) |
| Timeline    | Corporate   | transforms, created-in, dissolves, restructures | (transforms, transformed-by), (created-in, creation-of), (dissolves, dissolved-in), (restructures, restructured-in) |
| Timeline    | Product     | launches, discontinues, improves, inspires | (launches, launched-in), (discontinues, discontinued-in), (improves, improved-in), (inspires, inspired-by) |
| Corporate   | Corporate   | parent-of, subsidiary-of, partners-with, competes-with, supplies, supplied-by, acquires, merged-with | (parent-of, subsidiary-of), (partners-with, partners-with), (competes-with, competes-with), (supplies, supplied-by), (acquires, acquired-by), (merged-with, merged-with) |
| Corporate   | Product     | produces, distributes, develops, discontinues, launches | (produces, produced-by), (distributes, distributed-by), (develops, developed-by), (discontinues, discontinued-by), (launches, launched-by) |
| Product     | Product     | derived-from, replaced-by, compatible-with, component-of, competes-with | (derived-from, basis-for), (replaced-by, replaces), (compatible-with, compatible-with), (component-of, contains), (competes-with, competes-with) |

## Relationship Type Definitions

### Character-to-Character Relationships

| Relationship Type | Definition | Reciprocal Type |
|------------------|------------|-----------------|
| allies-with | Cooperative, supportive relationship with aligned goals | allies-with |
| antagonistic-toward | Adversarial, oppositional relationship with conflicting goals | antagonistic-toward |
| subordinate-to | Reports to or takes direction from in hierarchical relationship | superior-to |
| superior-to | Directs or manages in hierarchical relationship | subordinate-to |
| familial-with | Blood relation or legal family connection | familial-with |
| romantic-with | Intimate personal relationship, current or historical | romantic-with |
| professional-with | Formal working relationship without personal elements | professional-with |
| ambivalent-toward | Complex mixed relationship with both positive and negative aspects | ambivalent-toward |
| mentors | Provides guidance, wisdom, and development | mentored-by |
| mentored-by | Receives guidance, wisdom, and development | mentors |
| rivals-with | Competes with in a specific domain or context | rivals-with |

### Character-to-Timeline Relationships

| Relationship Type | Definition | Reciprocal Type |
|------------------|------------|-----------------|
| participates-in | Takes active part in the event | involves |
| influences | Shapes or affects the outcome or nature of the event | influenced-by |
| witnesses | Observes but does not materially affect the event | witnessed-by |
| affected-by | Changed or impacted by the event's outcomes | affects |
| orchestrates | Plans and executes the event | orchestrated-by |
| victimized-by | Suffers negative consequences from the event | victimizes |

### Character-to-Corporate Relationships

| Relationship Type | Definition | Reciprocal Type |
|------------------|------------|-----------------|
| founded | Established or created the organization | founded-by |
| employed-by | Works for the organization in formal capacity | employs |
| consults-for | Provides expert advice without formal employment | consulting-by |
| invests-in | Provides financial resources in exchange for ownership | invested-by |
| manages | Directs a department or division | managed-by |
| shareholds-in | Owns equity without operational involvement | shareholding-by |
| opposes | Works against the organization's interests | opposed-by |

### Character-to-Product Relationships

| Relationship Type | Definition | Reciprocal Type |
|------------------|------------|-----------------|
| created | Invented, designed, or developed the product | created-by |
| uses | Utilizes the product for its intended purpose | used-by |
| maintains | Services, repairs, or updates the product | maintained-by |
| markets | Promotes or sells the product | marketed-by |
| inspired | Provided conceptual foundation for the product | inspired-by |
| sabotages | Deliberately damages or undermines the product | sabotaged-by |

### Timeline-to-Timeline Relationships

| Relationship Type | Definition | Reciprocal Type |
|------------------|------------|-----------------|
| precedes | Occurs before in chronological sequence | follows |
| follows | Occurs after in chronological sequence | precedes |
| causes | Directly leads to or triggers | caused-by |
| caused-by | Directly results from | causes |
| concurrent-with | Occurs simultaneously with | concurrent-with |
| alternative-to | Represents different version of same temporal point | alternative-to |
| diverges-from | Creates new timeline branch from shared point | diverged-by |

### Timeline-to-Corporate Relationships

| Relationship Type | Definition | Reciprocal Type |
|------------------|------------|-----------------|
| transforms | Fundamentally changes the organization | transformed-by |
| created-in | Establishes the organization's existence | creation-of |
| dissolves | Ends the organization's existence | dissolved-in |
| restructures | Significantly alters organizational structure | restructured-in |

### Timeline-to-Product Relationships

| Relationship Type | Definition | Reciprocal Type |
|------------------|------------|-----------------|
| launches | Introduces product to market | launched-in |
| discontinues | Ends product's market availability | discontinued-in |
| improves | Enhances product's capabilities | improved-in |
| inspires | Provides conceptual foundation for product | inspired-by |

### Corporate-to-Corporate Relationships

| Relationship Type | Definition | Reciprocal Type |
|------------------|------------|-----------------|
| parent-of | Owns controlling interest in | subsidiary-of |
| subsidiary-of | Controlled by | parent-of |
| partners-with | Collaborates with in formal arrangement | partners-with |
| competes-with | Contests for same market or resources | competes-with |
| supplies | Provides goods or services to | supplied-by |
| supplied-by | Receives goods or services from | supplies |
| acquires | Takes ownership of | acquired-by |
| merged-with | Combined operations with | merged-with |

### Corporate-to-Product Relationships

| Relationship Type | Definition | Reciprocal Type |
|------------------|------------|-----------------|
| produces | Manufactures or creates | produced-by |
| distributes | Delivers to market or customers | distributed-by |
| develops | Researches and creates | developed-by |
| discontinues | Ceases production or support | discontinued-by |
| launches | Introduces to market | launched-by |

### Product-to-Product Relationships

| Relationship Type | Definition | Reciprocal Type |
|------------------|------------|-----------------|
| derived-from | Created as evolution of | basis-for |
| replaced-by | Superseded in market by | replaces |
| compatible-with | Works together with | compatible-with |
| component-of | Forms part of | contains |
| competes-with | Serves similar market purpose | competes-with |

## Usage Guidelines

### Selecting Relationship Types

When creating references between content elements:

1. **Identify Content Categories**
   - Determine the source and target content types (Character, Timeline, Corporate, Product)
   - Consult the Relationship Type Matrix for appropriate relationship types

2. **Choose Most Specific Type**
   - Select the most precise relationship type that accurately describes the connection
   - Avoid general types when more specific ones apply

3. **Ensure Bidirectional Consistency**
   - Use the correct reciprocal type in the target document
   - Verify that both relationship types are compatible in the bidirectional pair

4. **Maintain Semantic Accuracy**
   - Ensure the relationship type accurately reflects the narrative relationship
   - Document any complex or unusual relationships in the reference description

### Extending Relationship Types

When existing relationship types don't fully capture the narrative relationship:

1. **Propose Extension**
   - Document the proposed relationship type with clear definition
   - Identify the reciprocal relationship type
   - Specify which content type pairs it applies to

2. **Review Process**
   - Submit for narrative review to ensure semantic clarity
   - Validate against existing relationship types for overlap
   - Test with example references to verify applicability

3. **Implementation**
   - Add to Relationship Type Matrix when approved
   - Update validation mechanisms to incorporate new type
   - Document in this standards file

## References

- [/docs/standards/bidirectional-reference-system.md § RELATIONSHIP-TYPES]
- [/docs/standards/reference-pattern-standards.md § STANDARD-REFERENCE-PATTERNS]
- [/registry/reference-registry.md § REFERENCE-ID-NAMING-CONVENTIONS]

## Version History

### v1.0.0 - 2025-05-07
- Initial documentation of relationship type standards
- Established comprehensive relationship type matrix
- Defined all relationship types with reciprocal pairs
- Created usage guidelines for relationship type selection