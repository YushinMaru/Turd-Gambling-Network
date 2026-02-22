# Image Prompt Generation Workflow
**Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)**

## Context
This document provides the step-by-step workflow for generating AI image prompts for any new content in the Turd Bird Universe. Follow this workflow to ensure all content has comprehensive visual representation through detailed AI image prompts.

## Workflow Steps

### 1. Content Assessment
- Identify the content type (character, location, product, event, document, corporate)
- Determine required visualization categories based on content type
- Review all content details to identify key visual elements
- Note any specific visual requirements or unique features

### 2. Content Element Extraction
Create a structured list of key visual elements to include:

#### For Characters:
- Physical appearance (face, body, distinctive features)
- Clothing and accessories (style, materials, special items)
- Expressions and body language (typical poses, emotional traits)
- Environmental context (where they're typically found)
- Key relationships (who they interact with)
- Signature actions/abilities (what makes them unique)
- Personal items or equipment (tools, weapons, devices)

#### For Locations:
- Architectural style and physical dimensions
- Materials and construction details
- Environmental context (surroundings, weather, time of day)
- Functional elements (purpose-specific features)
- Distinctive visual elements (unique identifying features)
- Activity patterns (how the space is used)
- Atmospheric qualities (lighting, mood, sensory elements)

#### For Products:
- Physical dimensions and shape
- Materials and construction
- Functional elements and features
- Design aesthetics and styling
- Usage context and environment
- Technical specifications
- Unique selling points and special capabilities

#### For Events:
- Key participants and their positioning
- Physical setting and environment
- Emotional atmosphere and tensions
- Action sequence or pivotal moment
- Visual indicators of significance
- Preceding and following elements
- Historical context indicators

### 3. Template Selection
- Choose the appropriate template from `/visuals/prompt-templates/`
- Review template structure to ensure it matches content needs
- Customize template if necessary for unique content requirements

### 4. Prompt Generation
For each required visualization type, generate a detailed prompt that includes:

- Precise physical descriptions with measurements and materials
- Comprehensive environmental details
- Specific lighting conditions
- Supporting characters with full detail
- Emotional/psychological elements
- Technical specifications for the image
- Atmospheric qualities

### 5. Quality Verification
Ensure each prompt includes:
- Minimum 300 words of detailed description
- Extreme detail on all physical elements
- Clear environmental context
- Precise lighting description
- Supporting characters where appropriate
- Technical specifications
- No formatting, headers, or additional notes - raw prompt text only

### 6. File Creation and Storage
- Create file with `.txt` extension
- Use naming convention: `[descriptive_name].txt`
- Store in appropriate directory under `/visuals/[content_type]/[entity_name]/`
- Ensure file contains ONLY raw prompt text for easy copy-paste use

### 7. Reference Integration
- Add reference to prompt files in source content documentation
- Update master prompt index with new entries
- Create bidirectional references between related prompts

## Example Implementation

### Character Prompt Generation Example

For a new character "Dr. Thaddeus Void":

1. **Required visualizations:**
   - `primary.txt` - Definitive portrait
   - `environmental.txt` - In philosophy department
   - `action.txt` - Ethical justification process
   - `emotional.txt` - Key emotional states
   - `interaction.txt` - With Fred Turd

2. **Extract visual elements:**
   - Physical: Tall, gaunt, 60s, silver goatee, asymmetrical glasses
   - Clothing: Academic robes, specialized ethics calculator watch
   - Environment: Mobile office with philosophical texts, ethical matrices
   - Actions: Ethical justification process using specialized equipment
   - Relationships: Professional respect from Fred, debates with Augusta

3. **Generate each prompt with extreme detail**

4. **Save to:**
   `/visuals/characters/dr-thaddeus-void/`

5. **Add reference:**
   "Visualization prompts available at `/visuals/characters/dr-thaddeus-void/`"

## Generated Prompt Structure

Each prompt should follow this structure:

```
Hyperrealistic [image type] of [subject], [brief description]. [Detailed physical description]. [Clothing/accessories details]. [Environmental elements]. [Action/pose/expression]. [Other characters if applicable]. [Lighting details]. [Atmospheric elements]. [Technical specifications].
```

Always conclude with:
```
8K resolution, photorealistic, [appropriate lighting type], [appropriate perspective].
```

## Special Requirements

### Consistency Requirements
- Maintain consistent physical descriptions across all visualizations of same entity
- Ensure environmental details match established universe elements
- Maintain consistent scale and proportion descriptions
- Use precise color descriptions (specific named colors, not generic terms)

### Extreme Detail Requirement
All prompt text must include maximum detail for optimal fidelity:
- Every aspect of physical appearance described thoroughly
- All materials specified with exact properties
- All dimensions provided where relevant
- All colors described with specific nomenclature
- All lighting described with source, quality, direction, and effect
- All environmental elements positioned and contextualized

### Technical Requirements
- File must contain ONLY the prompt text - no headers, formatting or notes
- Prompt should be comprehensive enough to generate consistent results
- Length should be sufficient to provide full context (typically 300-500 words)
- Technical specifications should be included (resolution, style, perspective)