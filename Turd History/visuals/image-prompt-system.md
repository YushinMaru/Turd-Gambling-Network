# AI Image Generation System for Turd Bird Universe
**Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)**

> Previous: None (Initial Documentation)

## Context
This document outlines the comprehensive system for generating visual representations of the Turd Bird Universe through AI image generation prompts. Each entity in the universe (characters, locations, products, events) will have standardized prompts enabling consistent visual representation across multiple contexts.

## Folder Structure

```
/visuals/
  ├── prompt-templates/                # Standardized templates for different entity types
  │   ├── character-prompt-template.md # Template for character prompts
  │   ├── location-prompt-template.md  # Template for location prompts
  │   ├── product-prompt-template.md   # Template for product prompts
  │   └── event-prompt-template.md     # Template for event prompts
  │
  ├── characters/                      # Character visualization prompts
  │   ├── fred-turd/                   # Organized by character
  │   │   ├── primary-portrait.md      # Standard view
  │   │   ├── emotional-range.md       # Various emotional states
  │   │   ├── environmental.md         # Character in their environment
  │   │   ├── action-ability.md        # Demonstrating key abilities
  │   │   └── chronological.md         # Character at different ages/eras
  │   ├── larry-bird/                  # Next character
  │   └── [other characters]/
  │
  ├── locations/                       # Location visualization prompts
  │   ├── headquarters/                # Organized by location
  │   │   ├── lighthouse-era.md
  │   │   ├── industrial-era.md
  │   │   ├── modern-campus/
  │   │   │   ├── aerial-view.md
  │   │   │   ├── admin-ring.md
  │   │   │   ├── innovation-ring.md
  │   │   │   ├── quantum-ring.md
  │   │   │   └── the-labyrinth.md
  │   ├── arctic-facility/
  │   └── [other locations]/
  │
  ├── products/                        # Product visualization prompts
  │   ├── weaponized-kitchenware/
  │   │   ├── tactical-spork.md
  │   │   ├── combat-knives.md
  │   │   └── tactical-dinnerware.md
  │   └── [other products]/
  │
  ├── events/                          # Event visualization prompts
  │   ├── thursday-incident.md
  │   └── [other events]/
  │
  └── scenes/                          # Complex scene prompts
      ├── fred-larry-confrontation.md
      ├── board-meeting-chaos.md
      └── [other scenes]/
```

## Prompt Standards

### Universal Format
All image prompts will follow this standardized format:

```
# [ENTITY NAME] - [PROMPT TYPE]
**Style:** [Consistent style directive for Turd Bird Universe]
**Focus:** [What aspect this specific prompt emphasizes]
**Usage Context:** [Where/how this visualization would be used]

## Core Prompt
[The complete, detailed prompt for image generation]

## Element Breakdown
- **Subject:** [Main subject description]
- **Environment:** [Setting/background details]
- **Lighting:** [Light conditions and effects]
- **Perspective:** [Camera angle/viewpoint]
- **Action/Pose:** [What the subject is doing]
- **Emotional Tone:** [The feeling the image should convey]
- **Technical Specifics:** [Resolution, aspect ratio, etc.]

## Variations
1. [Alternative A - minor variation description]
2. [Alternative B - minor variation description]
3. [Alternative C - minor variation description]

## References
- [Relevant narrative documents for this entity]
```

### Style Consistency Directives
All Turd Bird Universe visualizations should maintain these style elements:

- **Hyperrealistic base** with subtle surrealist elements
- **Corporate aesthetics** juxtaposed with chaotic innovation
- **Rich color contrasts** between order (blues/grays) and chaos (reds/oranges)
- **Detailed textures** that emphasize tactile qualities
- **Dramatic lighting** creating strong shadow definition
- **Cinematic composition** with intentional framing
- **Easter eggs** - subtle references to other universe elements

## Character Visualization Requirements

Each character must have these five prompt categories:

1. **Primary Portrait**
   - Definitive visual representation
   - Full character in iconic pose
   - Key physical characteristics clearly displayed
   - Signature clothing/accessories
   - Neutral but characteristic expression
   - Environmental hints to role/personality

2. **Emotional Range**
   - Series showing character in different emotional states
   - Consistent physical appearance across emotions
   - Expressions appropriate to character personality
   - Subtle environmental shifts reflecting emotional state
   - Lighting variations supporting emotional tone

3. **Environmental Context**
   - Character in their primary environment
   - Interacting with environment in characteristic way
   - Environment reflecting character's role and status
   - Background elements providing narrative context
   - Secondary characters or elements where appropriate

4. **Action/Ability**
   - Character demonstrating signature ability/action
   - Dynamic composition showing motion or process
   - Focus on unique character traits in action
   - Environmental reaction to character's action
   - Capture key moment of signature action

5. **Chronological Variation**
   - Character at different points in timeline
   - Consistency of core traits across temporal changes
   - Age-appropriate modifications to appearance
   - Environmental/contextual changes reflecting era
   - Subtle references to character development arc

## Location Visualization Requirements

Each location must have these prompt categories:

1. **Establishing Shot**
   - Overall view showing full scope of location
   - Architectural/geographical distinctive features
   - Contextual elements showing scale and setting
   - Characteristic lighting conditions
   - Subtle indicators of function/purpose

2. **External Details**
   - Close-up views of distinctive external features
   - Material textures and structural elements
   - Entrance/access points with security features
   - Surrounding environment interaction
   - External systems or functional elements

3. **Internal Spaces**
   - Key internal areas with functional elements
   - Architectural style and spatial organization
   - Lighting and atmospheric qualities
   - Human-scale elements for proportion reference
   - Details showing actual use of space

4. **Functional Demonstration**
   - Location during characteristic activity
   - Key systems or features in operation
   - Personnel or equipment in active use
   - Dynamic elements showing primary purpose
   - Environmental responses to activity

## Product Visualization Requirements

Each product must have these prompt categories:

1. **Marketing Shot**
   - Idealized presentation of product
   - Clean background emphasizing product details
   - Optimal lighting showing key features
   - Professional product photography aesthetic
   - Subtle branding elements

2. **Technical Specification**
   - Detailed view showing mechanical/technical elements
   - Exploded view or cutaway revealing internal components
   - Annotations or focus on key functional aspects
   - Multiple angles showing different features
   - Scale reference if size is important

3. **In Use - Standard**
   - Product being used for intended primary purpose
   - Human interaction showing correct usage
   - Environmental context appropriate to function
   - Action moment demonstrating key capability
   - Lighting emphasizing practical application

4. **In Use - Tactical**
   - Product being used in emergency/tactical scenario
   - Dramatic context showing secondary capabilities
   - Dynamic action emphasizing versatility
   - Environmental stress conditions
   - Lighting creating tension and urgency

## Implementation Plan

### Phase 1: Template Development
- Create standardized templates for each entity type
- Develop style guide ensuring visual consistency
- Create sample prompts for one example of each entity type
- Test prompts with multiple AI generation systems for consistency

### Phase 2: Core Character Visualization
- Develop complete prompt sets for primary characters:
  - Fred Turd
  - Larry Bird
  - Pneumonia Pete
  - The Board (conceptual visualization)
  - Augusta Turing
  - Secondary characters

### Phase 3: Location Visualization
- Develop complete prompt sets for key locations:
  - Turd Bird Headquarters (all eras)
  - Arctic Facility
  - Fred's mansion
  - Other significant locations

### Phase 4: Product Visualization
- Develop complete prompt sets for key product lines:
  - Weaponized Kitchenware
  - ReAnimus technology
  - Other significant products

### Phase 5: Integration with Narrative Documentation
- Add visualization references to narrative documents
- Create standardized notation for indicating available visuals
- Develop presentation format combining narrative and visual elements

## References
- [CLAUDE.md § SORA-PROMPT-REQUIREMENTS]
- [docs/standards/character-directory-templates.md]
- [docs/standards/documentation-naming-standards.md]

## Version History
### v1.0.0 - 2025-05-06
- Initial documentation of AI Image Generation System
- Established folder structure and organization
- Created prompt standards and format templates
- Developed visualization requirements by entity type