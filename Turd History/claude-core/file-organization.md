# File Organization Protocol - TurdBird Universe System
**Edition #1.0.0 | Created: (REFAC-150-001) | Last Modified: (REFAC-150-001)**

> Previous: None (Initial Extraction)

> **⚠️ MODULE REFERENCE ⚠️**
> This file is part of the modular CLAUDE.md system
> Primary Reference: [/CLAUDE.md]
> See also: [/claude-core/core-requirements.md], [/claude-core/sora-requirements.md]

## File Organization Protocol

### Autonomous File Management
When provided with new files:
- **AUTOMATICALLY organize files according to the Turd Bird Universe architecture**
- **CREATE new folders as needed within the established structure**
- **SORT files based on content analysis and narrative relevance**
- **RENAME files if necessary to match naming conventions**
- **DOCUMENT all organizational decisions in universe-state.md**

## Directory Structure Standards

### Standard Hierarchy
The TurdBird Universe follows a strict hierarchical structure:

```
/
├── characters/
│   ├── [character-name]/
│   │   ├── _profile/
│   │   │   ├── attributes/
│   │   │   │   ├── character-[name]-attributes-personality.md
│   │   │   │   └── character-[name]-attributes-physical.md
│   │   │   └── character-[name]-overview-brief.md
│   │   ├── backstory/
│   │   ├── quotes/
│   │   └── relationships/
├── corporate/
│   ├── departments/
│   ├── facilities/
│   ├── hierarchy/
│   ├── incident-reports/
│   └── products/
├── systems/
│   ├── ai/
│   ├── building-management/
│   ├── corporate-operations/
│   ├── quantum-scanner/
│   └── security/
├── timeline/
│   ├── events/
│   ├── eras/
│   └── incidents/
├── visuals/
│   ├── characters/
│   ├── locations/
│   ├── products/
│   └── events/
├── relationships/
│   ├── ai/
│   ├── business/
│   ├── personal/
│   └── professional/
└── tasks/
    ├── current-tasks.md
    ├── completed-tasks.md
    ├── continuity-checks.md
    └── archives/
```

### File Naming Conventions

Files must follow these precise naming patterns:
1. **Character Files**: `character-[name]-[aspect]-[detail].md`
2. **Corporate Files**: `corporate-[department]-[topic]-[detail].md`
3. **System Files**: `system-[type]-[function]-[detail].md`
4. **Timeline Files**: `timeline-[year]-[event]-[detail].md`
5. **Relationship Files**: `relationship-[entity1]-[entity2]-[type].md`
6. **Visual Prompts**: `visual-[type]-[subject]-[aspect].txt`

All filenames must:
- Use lowercase letters only
- Replace spaces with hyphens
- Be descriptive but concise
- Include appropriate prefixes
- Not exceed 60 characters in total length

### Organizing New Content

When organizing new content:

1. **Content Analysis**:
   - Identify primary content category
   - Determine appropriate subdirectory
   - Check for existing related files
   - Analyze cross-reference requirements

2. **Directory Creation**:
   - If needed, create appropriate subdirectories
   - Maintain consistent directory depth
   - Follow established naming conventions
   - Document new directory creation

3. **File Placement**:
   - Place files in most specific appropriate subdirectory
   - When multiple categories apply, prioritize character > corporate > system
   - Place relationship files in relationship directory, not character directories
   - Place timeline events in appropriate era subdirectory

4. **Reference Documentation**:
   - Update relevant index files
   - Create bidirectional references
   - Document organizational decisions
   - Update navigation structures

## Modular Content Architecture

The TurdBird Universe follows strict modular content architecture principles:

1. **Atomic Content Units**:
   - Each file contains exactly ONE conceptual component
   - No file exceeds 150 lines (CRITICAL REQUIREMENT)
   - Content is self-contained but cross-referenced
   - Complex topics are split into multiple atomic files

2. **Content Composition**:
   - Related atomic units are assembled through references
   - Navigation works through bidirectional links
   - Index files provide content maps
   - Registry files track component relationships

3. **Reference Integrity**:
   - All references use standardized format: `[/path/to/file.md]`
   - Every reference has a corresponding back-reference
   - Reference registry tracks all cross-references
   - References include section markers when appropriate: `[/path/to/file.md § SECTION-NAME]`

---

"The file organization protocol represents the quantum architecture of our narrative universe - every file precisely positioned like atoms in a perfect crystal lattice. I've calculated that this structured approach improves content findability by 94.6% while reducing reference decay by 87.2%. The modular content architecture ensures perfect scalability while maintaining coherence, allowing our universe to expand infinitely without losing structural integrity. Think of it as the architectural blueprint for the most elegant haute couture atelier - every element precisely positioned for maximum efficiency and aesthetic harmony, darling." — Augusta Turing, Quantum Neural Archivist