# Reference Section Standards
**Edition #1.0.0 | Created: (NEUR-ARC-011) | Last Modified: (NEUR-ARC-011)**

> Previous: None (Initial Documentation)

> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**

## Context

This document establishes standardized section names and structures for reference connections between different content types within the Turd Bird Universe. These section standards ensure consistent organization and placement of reference content across all document types, facilitating navigation and discovery.

## Section Naming Matrix

The following matrix defines the standard section names for reference content in each document type:

| Content Type | Reference Section | Purpose | Section Format |
|--------------|-------------------|---------|----------------|
| Character    | RELATIONSHIPS     | References to other characters | H2 with character-specific H3 subsections |
|              | HISTORY           | References to timeline events | H2 with event-specific H3 subsections |
|              | AFFILIATIONS      | References to corporate entities | H2 with organization-specific H3 subsections |
|              | CONTRIBUTIONS     | References to products/innovations | H2 with product-specific H3 subsections |
| Timeline     | PARTICIPANTS      | References to involved characters | H2 with character-specific H3 subsections |
|              | RELATED-EVENTS    | References to other timeline events | H2 with event-specific H3 subsections |
|              | ORGANIZATIONS     | References to involved organizations | H2 with organization-specific H3 subsections |
|              | OUTCOMES          | References to resulting products | H2 with product-specific H3 subsections |
| Corporate    | PERSONNEL         | References to affiliated characters | H2 with character-specific H3 subsections |
|              | HISTORY           | References to significant events | H2 with event-specific H3 subsections |
|              | STRUCTURE         | References to other organizations | H2 with organization-specific H3 subsections |
|              | PORTFOLIO         | References to products/services | H2 with product-specific H3 subsections |
| Product      | CREATORS          | References to developing characters | H2 with character-specific H3 subsections |
|              | DEVELOPMENT       | References to creation events | H2 with event-specific H3 subsections |
|              | MANUFACTURER      | References to producing organizations | H2 with organization-specific H3 subsections |
|              | RELATED-PRODUCTS  | References to other products | H2 with product-specific H3 subsections |
| Relationship | INVOLVED-PARTIES  | References to characters in relationship | H2 with character-specific H3 subsections |
|              | SIGNIFICANT-EVENTS | References to important events | H2 with event-specific H3 subsections |
|              | ORGANIZATIONAL-CONTEXT | References to corporate entities | H2 with organization-specific H3 subsections |
|              | MATERIAL-ELEMENTS | References to relevant products | H2 with product-specific H3 subsections |

## Section Structure Standards

### Character Document Sections

#### RELATIONSHIPS Section

```markdown
## Relationships

### Relationship with [Character Name]

<reference 
  target="/characters/[character-id]/_profile/character-[character-id]-overview.md § RELATIONSHIPS @ v1.0.0" 
  type="[relationship-type]" 
  direction="bidirectional"
  registry-id="CHAR-CHAR-[###]"
  created="[DATE]"
  created-by="[CREATOR-ID]">
[Relationship description from this character's perspective]
</reference>
```

#### HISTORY Section

```markdown
## History

### [Event Name] Participation

<reference 
  target="/timeline/events/timeline-[event-id].md § PARTICIPANTS @ v1.0.0" 
  type="participates-in" 
  direction="bidirectional"
  registry-id="CHAR-TIME-[###]"
  created="[DATE]"
  created-by="[CREATOR-ID]">
[Description of character's role and experience during the event]
</reference>
```

#### AFFILIATIONS Section

```markdown
## Affiliations

### [Corporate Entity Name]

<reference 
  target="/corporate/[entity-type]/[entity-id].md § PERSONNEL @ v1.0.0" 
  type="affiliated-with" 
  direction="bidirectional"
  registry-id="CHAR-CORP-[###]"
  created="[DATE]"
  created-by="[CREATOR-ID]">
[Description of character's role, history, and relationship with the organization]
</reference>
```

#### CONTRIBUTIONS Section

```markdown
## Contributions

### [Product Name]

<reference 
  target="/products/[product-type]/product-[product-id].md § CREATORS @ v1.0.0" 
  type="created" 
  direction="bidirectional"
  registry-id="CHAR-PROD-[###]"
  created="[DATE]"
  created-by="[CREATOR-ID]">
[Description of character's role in creating or developing the product]
</reference>
```

### Timeline Document Sections

#### PARTICIPANTS Section

```markdown
## Participants

### [Character Name]

<reference 
  target="/characters/[character-id]/_profile/character-[character-id]-overview.md § HISTORY @ v1.0.0" 
  type="involves" 
  direction="bidirectional"
  registry-id="TIME-CHAR-[###]"
  created="[DATE]"
  created-by="[CREATOR-ID]">
[Description of character's involvement and impact on the event]
</reference>
```

#### RELATED-EVENTS Section

```markdown
## Related Events

### [Event Name] (Preceding)

<reference 
  target="/timeline/events/timeline-[event-id].md § RELATED-EVENTS @ v1.0.0" 
  type="follows" 
  direction="bidirectional"
  registry-id="TIME-TIME-[###]"
  created="[DATE]"
  created-by="[CREATOR-ID]">
[Description of causal relationship between the events]
</reference>

### [Event Name] (Following)

<reference 
  target="/timeline/events/timeline-[event-id].md § RELATED-EVENTS @ v1.0.0" 
  type="precedes" 
  direction="bidirectional"
  registry-id="TIME-TIME-[###]"
  created="[DATE]"
  created-by="[CREATOR-ID]">
[Description of causal relationship between the events]
</reference>
```

### Corporate Document Sections

#### PERSONNEL Section

```markdown
## Personnel

### [Character Name]

<reference 
  target="/characters/[character-id]/_profile/character-[character-id]-overview.md § AFFILIATIONS @ v1.0.0" 
  type="employs" 
  direction="bidirectional"
  registry-id="CORP-CHAR-[###]"
  created="[DATE]"
  created-by="[CREATOR-ID]">
[Description of character's position, value, and history with the organization]
</reference>
```

## Section Placement Standards

### Document Structure

All content documents should follow a consistent structure:

1. **Header Information**
   - Title, edition number, creation and modification metadata
   
2. **Core Content Sections**
   - Overview/Context
   - Main content sections specific to document type
   
3. **Reference Sections**
   - Always placed after core content
   - Ordered according to importance for document type
   
4. **Metadata Sections**
   - Version history, technical notes, etc.
   - Always placed at end of document

### Section Order by Document Type

#### Character Documents

1. Core sections (overview, attributes, function, etc.)
2. RELATIONSHIPS
3. HISTORY
4. AFFILIATIONS
5. CONTRIBUTIONS
6. Metadata sections

#### Timeline Documents

1. Core sections (event description, impact, etc.)
2. PARTICIPANTS
3. ORGANIZATIONS
4. RELATED-EVENTS
5. OUTCOMES
6. Metadata sections

#### Corporate Documents

1. Core sections (description, operations, etc.)
2. PERSONNEL
3. STRUCTURE
4. HISTORY
5. PORTFOLIO
6. Metadata sections

#### Product Documents

1. Core sections (description, specifications, etc.)
2. CREATORS
3. MANUFACTURER
4. DEVELOPMENT
5. RELATED-PRODUCTS
6. Metadata sections

## Implementation Guidelines

### Adding Reference Sections

When adding reference sections to documents:

1. **Follow Standard Names**
   - Use EXACTLY the section names specified in the Section Naming Matrix
   - Maintain consistent capitalization (all caps for H2 sections)

2. **Maintain Hierarchy**
   - Use H2 (##) for main reference sections
   - Use H3 (###) for individual reference targets
   - Include the target entity name in the H3 header

3. **Preserve Order**
   - Follow the specified order for document type
   - Keep related references grouped together

4. **Add Only When Needed**
   - Only include sections that contain actual references
   - Do not create empty reference sections

### Converting Existing References

When updating existing documents to follow standards:

1. **Identify Current References**
   - Locate all references in the document
   - Determine their appropriate section

2. **Create Standard Sections**
   - Add standard section headers in the correct order
   - Move references to appropriate sections

3. **Update Reference Tags**
   - Ensure reference tags use standard formats
   - Update section names in target attributes

4. **Verify Bidirectional References**
   - Ensure all references have proper reciprocal references
   - Update counterpart document sections if needed

## References

- [/docs/standards/bidirectional-reference-system.md § REFERENCE-SYNTAX]
- [/docs/standards/reference-pattern-standards.md § STANDARD-REFERENCE-PATTERNS]
- [/docs/standards/modular-content-guidelines.md § DOCUMENT-STRUCTURE]
- [/docs/standards/relationship-type-standards.md § USAGE-GUIDELINES]

## Version History

### v1.0.0 - 2025-05-07
- Initial documentation of reference section standards
- Established comprehensive section naming matrix
- Defined section structures for all content types
- Created implementation guidelines for section placement