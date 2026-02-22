#!/bin/bash
# Ultra-Refactored Character Directory Generator
# Edition #1.1.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)
#
# This script implements SYS-012: Create Standardized Directory Template Structure
# It generates directory structures for all character types (primary, secondary, minor)
# Implements ultra-refactored file structure with bidirectional references

# Configuration
BASEDIR="/mnt/z/Turdbot/Turd History"
CHARACTER_DIR="${BASEDIR}/characters"
TEMPLATE_DIR="${BASEDIR}/systems/templates"
CREATOR_ID="NEUR-ARC-001"
CREATED_DATE=$(date +%Y-%m-%d)

# Text formatting for nicer output
BOLD=$(tput bold)
NORMAL=$(tput sgr0)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
BLUE=$(tput setaf 4)
RED=$(tput setaf 1)

# Display usage information
usage() {
    echo "${BOLD}Ultra-Refactored Character Directory Generator${NORMAL}"
    echo "Creates standardized directory structure for Turd Bird Universe characters"
    echo ""
    echo "Usage: $0 [OPTIONS] character-name"
    echo ""
    echo "Options:"
    echo "  -t, --type TYPE     Character type: primary, secondary, or minor (default: primary)"
    echo "  -c, --category CAT  Category for minor character (e.g., corporate-rivals)"
    echo "                     Required for minor character type"
    echo "  -i, --id ID        Creator ID for metadata (default: ${CREATOR_ID})"
    echo "  -h, --help         Display this help message"
    echo ""
    echo "Examples:"
    echo "  $0 fred-turd                       # Create primary character"
    echo "  $0 -t secondary augusta-turing     # Create secondary character"
    echo "  $0 -t minor -c corporate-rivals sunny-demetris  # Create minor character"
    exit 1
}

# Convert string to kebab-case
to_kebab_case() {
    echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//'
}

# Convert string to proper case
to_proper_case() {
    echo "$1" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1'
}

# Convert string to uppercase with dashes
to_upper_case_with_dashes() {
    echo "$1" | tr '[:lower:]' '[:upper:]'
}

# Create a file with standard header
create_file() {
    local file_path="$1"
    local title="$2"
    local section="$3"
    local context="$4"
    
    local directory=$(dirname "$file_path")
    mkdir -p "$directory"
    
    cat > "$file_path" << EOF
# ${title}
**Edition #1.0.0 | Created: (${CREATOR_ID}) | Last Modified: (${CREATOR_ID})**

> Previous: None (Initial Documentation)

> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**

## Context
${context}

## ${section}

[Content to be added here following the ultra-refactored file structure guidelines]

## References
[Add appropriate bidirectional references here]

## Version History
### v1.0.0 - ${CREATED_DATE}
- Initial documentation created via ultra-refactored directory template generator
EOF

    echo "${GREEN}Created file:${NORMAL} $file_path"
}

# Create primary character directory structure
create_primary_character() {
    local char_name="$1"
    local kebab_name=$(to_kebab_case "$char_name")
    local proper_name=$(to_proper_case "$char_name")
    local base_dir="${CHARACTER_DIR}/${kebab_name}"
    
    echo "${BLUE}Creating primary character directory structure for: ${BOLD}$proper_name${NORMAL}"
    
    # Check if directory already exists
    if [ -d "$base_dir" ]; then
        echo "${RED}Error: Directory for character '$kebab_name' already exists at $base_dir${NORMAL}"
        exit 1
    fi
    
    # Create main directories
    mkdir -p "${base_dir}/_profile/attributes"
    mkdir -p "${base_dir}/_profile/function"
    mkdir -p "${base_dir}/_profile/development"
    mkdir -p "${base_dir}/origins/phases"
    mkdir -p "${base_dir}/origins/psychology"
    mkdir -p "${base_dir}/origins/incidents"
    mkdir -p "${base_dir}/development"
    mkdir -p "${base_dir}/relationships"
    mkdir -p "${base_dir}/capabilities"
    mkdir -p "${base_dir}/states"
    mkdir -p "${base_dir}/expressions"
    mkdir -p "${base_dir}/possessions"
    mkdir -p "${base_dir}/impact"
    
    # Create core profile files
    create_file "${base_dir}/_profile/character-${kebab_name}-overview-brief.md" \
                "$proper_name - Brief Overview" \
                "Core Identity" \
                "This document provides a concise overview of $proper_name, including essential information about their identity, role, and significance within the Turd Bird Universe. It serves as the central reference point connecting to more detailed component files."
    
    create_file "${base_dir}/_profile/attributes/character-${kebab_name}-attributes-physical.md" \
                "$proper_name - Physical Attributes" \
                "Physical Characteristics" \
                "This document details the physical appearance and characteristics of $proper_name, including distinctive features, mannerisms, and visual presentation."
    
    create_file "${base_dir}/_profile/attributes/character-${kebab_name}-attributes-personality.md" \
                "$proper_name - Personality Attributes" \
                "Personality Traits" \
                "This document details the psychological characteristics, behavioral patterns, and personality traits of $proper_name."
    
    create_file "${base_dir}/_profile/function/character-${kebab_name}-function-narrative.md" \
                "$proper_name - Narrative Function" \
                "Narrative Role" \
                "This document examines the narrative function and significance of $proper_name within the Turd Bird Universe, including their role in driving story elements and relationships to major themes."
    
    # Create origins files
    create_file "${base_dir}/origins/character-${kebab_name}-childhood.md" \
                "$proper_name - Childhood" \
                "Early Development" \
                "This document details the childhood and formative years of $proper_name, establishing the foundation for their character development."
    
    create_file "${base_dir}/origins/character-${kebab_name}-education.md" \
                "$proper_name - Education" \
                "Educational Development" \
                "This document details the educational background and intellectual development of $proper_name."
    
    create_file "${base_dir}/origins/character-${kebab_name}-early-career.md" \
                "$proper_name - Early Career" \
                "Professional Development" \
                "This document details the early professional development and career progression of $proper_name before their current role."
    
    create_file "${base_dir}/origins/phases/character-${kebab_name}-origins-phase-early.md" \
                "$proper_name - Early Phase Development" \
                "Formative Period" \
                "This document provides detailed examination of $proper_name's early developmental phase, focusing on formative experiences and initial character establishment."
    
    create_file "${base_dir}/origins/psychology/character-${kebab_name}-origins-psychology.md" \
                "$proper_name - Psychological Development" \
                "Psychological Formation" \
                "This document details the psychological development and formation of $proper_name's core traits and behavioral patterns."
    
    # Create development files
    create_file "${base_dir}/development/character-${kebab_name}-pivotal-events.md" \
                "$proper_name - Pivotal Events" \
                "Transformative Experiences" \
                "This document details the key pivotal moments and transformative experiences that shaped $proper_name's character development."
    
    create_file "${base_dir}/development/character-${kebab_name}-arc-primary.md" \
                "$proper_name - Primary Character Arc" \
                "Core Development" \
                "This document details the primary character arc and developmental trajectory of $proper_name."
    
    # Create relationship files
    create_file "${base_dir}/relationships/relationship-${kebab_name}-network-overview.md" \
                "$proper_name - Relationship Network" \
                "Relationship Ecosystem" \
                "This document provides an overview of $proper_name's complete relationship network and interpersonal connections within the Turd Bird Universe."
    
    # Create relationship files for primary characters
    for main_char in "fred-turd" "larry-bird" "pneumonia-pete" "the-board"; do
        if [ "$main_char" != "$kebab_name" ]; then
            main_char_proper=$(to_proper_case "$main_char")
            
            create_file "${base_dir}/relationships/relationship-${kebab_name}-${main_char}-primary.md" \
                "$proper_name and $main_char_proper Relationship" \
                "Relationship Dynamics" \
                "This document details the relationship dynamics between $proper_name and $main_char_proper, examining their interactions, history, and significance to the narrative."
        fi
    done
    
    # Create capabilities files
    create_file "${base_dir}/capabilities/character-${kebab_name}-skills-overview.md" \
                "$proper_name - Skills Overview" \
                "Core Capabilities" \
                "This document details the notable skills, abilities, and areas of expertise possessed by $proper_name."
    
    # Create states files
    create_file "${base_dir}/states/character-${kebab_name}-state-current.md" \
                "$proper_name - Current State" \
                "Present Condition" \
                "This document captures the current state and status of $proper_name, serving as a temporal snapshot of their present condition in the narrative."
    
    create_file "${base_dir}/states/character-${kebab_name}-state-origin.md" \
                "$proper_name - Origin State" \
                "Initial Condition" \
                "This document captures the initial state of $proper_name at their introduction to the narrative."
    
    # Create expressions files
    create_file "${base_dir}/expressions/character-${kebab_name}-quotes.md" \
                "$proper_name - Memorable Quotes" \
                "Significant Statements" \
                "This document collects and categorizes memorable quotes and significant statements made by $proper_name."
    
    create_file "${base_dir}/expressions/character-${kebab_name}-communication-style.md" \
                "$proper_name - Communication Style" \
                "Expression Patterns" \
                "This document details the speaking patterns, communication methods, and linguistic characteristics of $proper_name."
    
    # Create possessions files
    create_file "${base_dir}/possessions/character-${kebab_name}-signature-items.md" \
                "$proper_name - Signature Items" \
                "Notable Possessions" \
                "This document details the significant items, possessions, and environments associated with $proper_name."
    
    # Create impact files
    create_file "${base_dir}/impact/character-${kebab_name}-legacy-overview.md" \
                "$proper_name - Legacy Overview" \
                "Narrative Impact" \
                "This document examines the long-term impact and legacy of $proper_name within the Turd Bird Universe narrative."
    
    echo "${BOLD}${GREEN}Primary character directory structure created successfully!${NORMAL}"
}

# Create secondary character directory structure
create_secondary_character() {
    local char_name="$1"
    local kebab_name=$(to_kebab_case "$char_name")
    local proper_name=$(to_proper_case "$char_name")
    local base_dir="${CHARACTER_DIR}/${kebab_name}"
    
    echo "${BLUE}Creating secondary character directory structure for: ${BOLD}$proper_name${NORMAL}"
    
    # Check if directory already exists
    if [ -d "$base_dir" ]; then
        echo "${RED}Error: Directory for character '$kebab_name' already exists at $base_dir${NORMAL}"
        exit 1
    fi
    
    # Create main directories
    mkdir -p "${base_dir}/_profile"
    mkdir -p "${base_dir}/origins"
    mkdir -p "${base_dir}/development"
    mkdir -p "${base_dir}/relationships"
    mkdir -p "${base_dir}/capabilities"
    mkdir -p "${base_dir}/states"
    mkdir -p "${base_dir}/expressions"
    
    # Create profile files
    create_file "${base_dir}/_profile/character-${kebab_name}-overview.md" \
                "$proper_name - Overview" \
                "Core Identity" \
                "This document provides a comprehensive overview of $proper_name, including essential information about their identity, role, and significance within the Turd Bird Universe."
    
    create_file "${base_dir}/_profile/character-${kebab_name}-appearance.md" \
                "$proper_name - Appearance" \
                "Physical Characteristics" \
                "This document details the physical appearance and characteristics of $proper_name, including distinctive features, mannerisms, and visual presentation."
    
    create_file "${base_dir}/_profile/character-${kebab_name}-personality.md" \
                "$proper_name - Personality" \
                "Personality Traits" \
                "This document details the psychological characteristics, behavioral patterns, and personality traits of $proper_name."
    
    # Create origins files
    create_file "${base_dir}/origins/character-${kebab_name}-background.md" \
                "$proper_name - Background" \
                "Consolidated Origins" \
                "This document provides a consolidated overview of $proper_name's background, including childhood, education, and early career."
    
    # Create development files
    create_file "${base_dir}/development/character-${kebab_name}-arc-primary.md" \
                "$proper_name - Primary Character Arc" \
                "Core Development" \
                "This document details the primary character arc and developmental trajectory of $proper_name."
    
    # Create relationship files for primary characters
    for main_char in "fred-turd" "larry-bird" "pneumonia-pete"; do
        main_char_proper=$(to_proper_case "$main_char")
        
        create_file "${base_dir}/relationships/relationship-${kebab_name}-${main_char}-primary.md" \
            "$proper_name and $main_char_proper Relationship" \
            "Relationship Dynamics" \
            "This document details the relationship dynamics between $proper_name and $main_char_proper, examining their interactions, history, and significance to the narrative."
    done
    
    # Create capabilities files
    create_file "${base_dir}/capabilities/character-${kebab_name}-skills-overview.md" \
                "$proper_name - Skills Overview" \
                "Core Capabilities" \
                "This document details the notable skills, abilities, and areas of expertise possessed by $proper_name."
    
    # Create states files
    create_file "${base_dir}/states/character-${kebab_name}-state-current.md" \
                "$proper_name - Current State" \
                "Present Condition" \
                "This document captures the current state and status of $proper_name, serving as a temporal snapshot of their present condition in the narrative."
    
    create_file "${base_dir}/states/character-${kebab_name}-state-origin.md" \
                "$proper_name - Origin State" \
                "Initial Condition" \
                "This document captures the initial state of $proper_name at their introduction to the narrative."
    
    # Create expressions files
    create_file "${base_dir}/expressions/character-${kebab_name}-quotes.md" \
                "$proper_name - Quotes" \
                "Memorable Statements" \
                "This document collects and categorizes memorable quotes and significant statements made by $proper_name."
    
    echo "${BOLD}${GREEN}Secondary character directory structure created successfully!${NORMAL}"
}

# Create minor character directory structure
create_minor_character() {
    local char_name="$1"
    local category="$2"
    local kebab_name=$(to_kebab_case "$char_name")
    local kebab_category=$(to_kebab_case "$category")
    local proper_name=$(to_proper_case "$char_name")
    local base_dir="${CHARACTER_DIR}/minor-characters/${kebab_category}"
    
    echo "${BLUE}Creating minor character directory structure for: ${BOLD}$proper_name${NORMAL} (category: $kebab_category)"
    
    # Check if directory already exists
    if [ -d "${base_dir}/${kebab_name}" ]; then
        echo "${RED}Error: Directory for character '$kebab_name' already exists at ${base_dir}/${kebab_name}${NORMAL}"
        exit 1
    fi
    
    # Create directory
    mkdir -p "${base_dir}/${kebab_name}"
    
    # Create files
    create_file "${base_dir}/${kebab_name}/character-${kebab_name}-overview.md" \
                "$proper_name - Overview" \
                "Character Summary" \
                "This document provides a consolidated overview of $proper_name, a minor character in the Turd Bird Universe, including their essential characteristics and narrative role."
    
    create_file "${base_dir}/${kebab_name}/relationship-${kebab_name}-fred-turd-primary.md" \
                "$proper_name and Fred Turd Relationship" \
                "Relationship Dynamics" \
                "This document details the relationship dynamics between $proper_name and Fred Turd, examining their interactions, history, and significance to the narrative."
    
    echo "${BOLD}${GREEN}Minor character directory structure created successfully!${NORMAL}"
}

# Function to display completion message with example
display_completion_message() {
    local char_type="$1"
    local char_name="$2"
    local kebab_name=$(to_kebab_case "$char_name")
    local proper_name=$(to_proper_case "$char_name")
    
    echo ""
    echo "${BOLD}${GREEN}Character directory structure successfully created!${NORMAL}"
    echo "- Character Name: $proper_name"
    echo "- Character Type: $char_type"
    echo "- Directory: ${CHARACTER_DIR}/${kebab_name}"
    echo ""
    echo "${YELLOW}Next steps:${NORMAL}"
    echo "1. Review and populate the template files with character information"
    echo "2. Update references to ensure bidirectional integrity"
    echo "3. Add character to character registry at /registry/character-registry.md"
    echo "4. Verify structure compliance with ultra-refactored file architecture"
    echo ""
    echo "${BLUE}Example command to add relationship with another character:${NORMAL}"
    
    if [ "$char_type" = "primary" ] || [ "$char_type" = "secondary" ]; then
        echo "$0 -t primary new-character-name"
        echo "Then edit: ${CHARACTER_DIR}/${kebab_name}/relationships/relationship-${kebab_name}-new-character-name-primary.md"
        echo "and create: ${CHARACTER_DIR}/new-character-name/relationships/relationship-new-character-name-${kebab_name}-primary.md"
    else
        echo "$0 -t minor -c $category another-minor-character"
    fi
}

# Main script execution starts here
CHAR_TYPE="primary"
CATEGORY=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--type)
            CHAR_TYPE="$2"
            shift 2
            ;;
        -c|--category)
            CATEGORY="$2"
            shift 2
            ;;
        -i|--id)
            CREATOR_ID="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        -*)
            echo "${RED}Unknown option: $1${NORMAL}"
            usage
            ;;
        *)
            CHAR_NAME="$1"
            shift
            ;;
    esac
done

# Check if character name is provided
if [ -z "$CHAR_NAME" ]; then
    echo "${RED}Error: Character name is required${NORMAL}"
    usage
fi

# Check if category is provided for minor characters
if [ "$CHAR_TYPE" = "minor" ] && [ -z "$CATEGORY" ]; then
    echo "${RED}Error: Category is required for minor characters${NORMAL}"
    usage
fi

# Create appropriate directory structure based on character type
case "$CHAR_TYPE" in
    primary)
        create_primary_character "$CHAR_NAME"
        ;;
    secondary)
        create_secondary_character "$CHAR_NAME"
        ;;
    minor)
        create_minor_character "$CHAR_NAME" "$CATEGORY"
        ;;
    *)
        echo "${RED}Error: Invalid character type: $CHAR_TYPE${NORMAL}"
        usage
        ;;
esac

# Display completion message
display_completion_message "$CHAR_TYPE" "$CHAR_NAME"

# Make the script executable
chmod +x "$0"