# Automated AI Image Prompt Generation System
**Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)**

## Context
This document outlines the automated system for generating AI image prompts for all Turd Bird Universe content. Every time a new entity is created (character, location, product, event, document, etc.), corresponding image prompts will be automatically generated to ensure comprehensive visual representation.

## Content Types & Required Visualizations

### Characters
Every character must have the following visualization prompts:
1. **Primary Portrait** - Definitive visual representation
2. **Environmental Context** - Character in their primary setting
3. **Action/Ability** - Character demonstrating signature abilities
4. **Emotional Range** - Character displaying key emotional states
5. **Interaction** - Character in relationship with other key characters

### Locations
Every location must have the following visualization prompts:
1. **Establishing Shot** - Overall view (exterior or context)
2. **Interior Detail** - Key interior spaces and features
3. **Active Usage** - Location during typical activity
4. **Detail Highlights** - Unique architectural or functional elements
5. **Night/Alternative Perspective** - Location under different conditions

### Products
Every product must have the following visualization prompts:
1. **Showcase Display** - Product in ideal presentation
2. **Technical Detail** - Close-up showing key features
3. **In Use - Standard** - Product being used for primary purpose
4. **In Use - Tactical** - Product being used in tactical/emergency scenario
5. **Manufacturing/Design** - Product during creation/design phase

### Events
Every event must have the following visualization prompts:
1. **Pivotal Moment** - The critical turning point
2. **Lead-Up** - The circumstances preceding the event
3. **Aftermath** - The immediate consequences
4. **Participant Perspective** - View from key character's viewpoint
5. **Historical Context** - Event placed in timeline context

### Documents
Every significant document must have the following visualization prompts:
1. **Physical Representation** - The document as physical object
2. **Content Highlight** - Key information or section
3. **Creation Context** - Document being written/developed
4. **Impact Visualization** - Effects of the document's contents
5. **Historical Evolution** - Document changes over time

### Corporate Elements
Every corporate element must have the following visualization prompts:
1. **Brand Visualization** - Visual representation of corporate identity
2. **Organizational Structure** - Visualization of hierarchies/relationships
3. **Market Impact** - Corporate element in broader context
4. **Development History** - Evolution over time
5. **Future Projection** - Speculative future state

## Implementation Workflow

### Automated Prompt Generation Process
1. When any new content is created, identify content type
2. Reference appropriate prompt template from `/visuals/prompt-templates/`
3. Generate all required visualization prompts based on content details
4. Save prompts to corresponding folder in `/visuals/` directory structure
5. Update image prompt index to include new entries
6. Create bidirectional references between content and visualization prompts

### Standardized Directory Structure
```
/visuals/
  ├── characters/
  │   ├── [character-name]/
  │   │   ├── primary.txt
  │   │   ├── environmental.txt
  │   │   ├── action.txt
  │   │   ├── emotional.txt
  │   │   └── interaction.txt
  │   └── ...
  ├── locations/
  │   ├── [location-name]/
  │   │   ├── establishing.txt
  │   │   ├── interior.txt
  │   │   ├── active.txt
  │   │   ├── details.txt
  │   │   └── alternative.txt
  │   └── ...
  ├── products/
  ├── events/
  ├── documents/
  ├── corporate/
  └── prompt-templates/
```

### Prompt Quality Verification Checklist
Every generated prompt must include:
- Extreme physical detail (appearance, materials, dimensions)
- Comprehensive environmental context (surroundings, atmosphere, conditions)
- Precise lighting description (sources, quality, shadows, time of day)
- Clear emotional/psychological elements (expressions, tensions, relationships)
- Supporting characters with adequate detail
- Technical specifications (resolution, perspective, style)
- Atmospheric qualities (mood, air quality, weather, ambiance)
- Time-specific elements (era, historical context, temporal qualities)

## Integration With Content Creation

### Content Creation Workflow Update
1. At the beginning of content creation, identify all visualization needs
2. Create content document in appropriate location
3. Automatically generate all required visualization prompts
4. Save prompts to corresponding directory
5. Add references to visualization prompts in content documentation
6. Include note about available visualizations in content summary

### Example Implementation
When creating a new character:
```
1. Create character documentation in /characters/[name]/
2. Extract key visual elements from character description
3. Generate all five required visualization prompts
4. Save prompts to /visuals/characters/[name]/
5. Add reference to visualization prompts in character documentation
6. Note "Visualization prompts available at /visuals/characters/[name]/"
```

## Continuous Improvement
- Regularly audit prompt effectiveness with actual AI image generation
- Refine templates based on generation results
- Expand prompt variations for key elements
- Develop specialized templates for unique content categories
- Maintain consistent stylistic approach across all visualizations

## Reference System Integration
- All content documentation should reference available visualization prompts
- All visualization prompts should reference source content documentation
- Cross-reference visualization prompts for related entities
- Maintain master index of all visualization prompts
- Update reference registry when new prompts are created

## Note on Usage
EACH PROMPT FILE MUST CONTAIN ONLY THE RAW PROMPT TEXT FOR EASY COPY-PASTE USE - no formatting, headers, or additional notes.