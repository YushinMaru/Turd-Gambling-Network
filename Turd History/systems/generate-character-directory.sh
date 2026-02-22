#!/bin/bash
# Character Directory Generator
# Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)
#
# This script generates standardized directory structures for Turd Bird Universe characters
# Based on the templates defined in /docs/standards/character-directory-templates.md

# Configuration
BASEDIR="/mnt/z/Turdbot/Turd History"
CHARACTER_DIR="${BASEDIR}/characters"
TEMPLATE_FILE="${BASEDIR}/docs/standards/character-directory-templates.md"

# Display usage information
usage() {
    echo "Character Directory Generator for Turd Bird Universe"
    echo ""
    echo "Usage: $0 [OPTIONS] character-name"
    echo ""
    echo "Options:"
    echo "  -t, --type TYPE    Character type: primary, secondary, or minor (default: primary)"
    echo "  -c, --category CAT Category for minor character (e.g., corporate-rivals)"
    echo "                     Required for minor character type"
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

# Create file with standard header
create_file() {
    local file_path="$1"
    local title="$2"
    local file_dir=$(dirname "$file_path")
    
    # Create directory if it doesn't exist
    mkdir -p "$file_dir"
    
    # Create file with standard header
    cat > "$file_path" << EOF
# ${title}
**Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)**

> Previous: None (Initial Documentation)

> **⚠️ FILE SIZE LIMITATION: DO NOT CREATE ANY MORE LINES IN THIS DOCUMENT UNLESS NECESSARY.**
> **ANY NEW LARGE ADDITIONS SHOULD FOLLOW REFACTORING AFTER 150 LINES.**

## Context
[Add context description here]

## Content
[Add content here]

## References
[Add references here]

## Version History
### v1.0.0 - $(date +%Y-%m-%d)
- Initial documentation
EOF

    echo "Created file: $file_path"
}

# Create primary character directory structure
create_primary_character() {
    local char_name="$1"
    local kebab_name=$(to_kebab_case "$char_name")
    local base_dir="${CHARACTER_DIR}/${kebab_name}"
    
    echo "Creating primary character directory structure for: $kebab_name"
    
    # Create main directories
    mkdir -p "${base_dir}/_profile"
    mkdir -p "${base_dir}/origins"
    mkdir -p "${base_dir}/development"
    mkdir -p "${base_dir}/relationships"
    mkdir -p "${base_dir}/capabilities"
    mkdir -p "${base_dir}/states"
    mkdir -p "${base_dir}/expressions"
    mkdir -p "${base_dir}/possessions"
    mkdir -p "${base_dir}/impact"
    
    # Create profile files
    create_file "${base_dir}/_profile/character-${kebab_name}-overview.md" \
                "Frederick \"${char_name}\" - Character Overview"
    create_file "${base_dir}/_profile/character-${kebab_name}-appearance.md" \
                "Frederick \"${char_name}\" - Physical Appearance"
    create_file "${base_dir}/_profile/character-${kebab_name}-personality.md" \
                "Frederick \"${char_name}\" - Personality Profile"
    create_file "${base_dir}/_profile/character-${kebab_name}-narrative-function.md" \
                "Frederick \"${char_name}\" - Narrative Function"
    
    # Create origins files
    create_file "${base_dir}/origins/character-${kebab_name}-childhood.md" \
                "Frederick \"${char_name}\" - Childhood"
    create_file "${base_dir}/origins/character-${kebab_name}-education.md" \
                "Frederick \"${char_name}\" - Education"
    create_file "${base_dir}/origins/character-${kebab_name}-early-career.md" \
                "Frederick \"${char_name}\" - Early Career"
    
    # Create minimal examples of other directories
    create_file "${base_dir}/development/character-${kebab_name}-pivotal-events.md" \
                "Frederick \"${char_name}\" - Pivotal Events"
    create_file "${base_dir}/capabilities/character-${kebab_name}-skills-overview.md" \
                "Frederick \"${char_name}\" - Skills & Capabilities"
    create_file "${base_dir}/states/character-${kebab_name}-state-current.md" \
                "Frederick \"${char_name}\" - Current State"
    create_file "${base_dir}/expressions/character-${kebab_name}-quotes.md" \
                "Frederick \"${char_name}\" - Notable Quotes"
    
    echo "Primary character directory structure created successfully!"
}

# Create secondary character directory structure
create_secondary_character() {
    local char_name="$1"
    local kebab_name=$(to_kebab_case "$char_name")
    local base_dir="${CHARACTER_DIR}/${kebab_name}"
    
    echo "Creating secondary character directory structure for: $kebab_name"
    
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
                "${char_name} - Character Overview"
    create_file "${base_dir}/_profile/character-${kebab_name}-appearance.md" \
                "${char_name} - Physical Appearance"
    create_file "${base_dir}/_profile/character-${kebab_name}-personality.md" \
                "${char_name} - Personality Profile"
    
    # Create minimal examples of other directories
    create_file "${base_dir}/origins/character-${kebab_name}-background.md" \
                "${char_name} - Background"
    create_file "${base_dir}/capabilities/character-${kebab_name}-skills-overview.md" \
                "${char_name} - Skills & Capabilities"
    create_file "${base_dir}/states/character-${kebab_name}-state-current.md" \
                "${char_name} - Current State"
    create_file "${base_dir}/expressions/character-${kebab_name}-quotes.md" \
                "${char_name} - Notable Quotes"
    
    echo "Secondary character directory structure created successfully!"
}

# Create minor character directory structure
create_minor_character() {
    local char_name="$1"
    local category="$2"
    local kebab_name=$(to_kebab_case "$char_name")
    local kebab_category=$(to_kebab_case "$category")
    local base_dir="${CHARACTER_DIR}/minor-characters/${kebab_category}"
    
    echo "Creating minor character directory structure for: $kebab_name (category: $kebab_category)"
    
    # Create directory
    mkdir -p "${base_dir}/${kebab_name}"
    
    # Create files
    create_file "${base_dir}/${kebab_name}/character-${kebab_name}-overview.md" \
                "${char_name} - Overview"
    
    echo "Minor character directory structure created successfully!"
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
        -h|--help)
            usage
            ;;
        -*)
            echo "Unknown option: $1"
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
    echo "Error: Character name is required"
    usage
fi

# Check if category is provided for minor characters
if [ "$CHAR_TYPE" = "minor" ] && [ -z "$CATEGORY" ]; then
    echo "Error: Category is required for minor characters"
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
        echo "Error: Invalid character type: $CHAR_TYPE"
        usage
        ;;
esac

echo "Character directory generation complete!"