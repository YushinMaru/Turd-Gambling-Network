#!/bin/bash
# Content Template Application Script
# Author: NEUR-ARC-001
# Version: 1.0.0
# Created: 2025-05-06

# Define base paths
BASE_DIR="/mnt/z/Turdbot/Turd History"
TEMPLATE_DIR="${BASE_DIR}/systems/templates"
CREATOR_ID="NEUR-ARC-001"
DATE_TODAY=$(date +"%Y-%m-%d")

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to convert string to kebab case
to_kebab_case() {
    echo "$1" | tr '[:upper:]' '[:lower:]' | sed -e 's/[^[:alnum:]]/-/g' -e 's/--*/-/g' -e 's/^-//' -e 's/-$//'
}

# Function to print colored header
print_header() {
    echo -e "${BLUE}====================================================================${NC}"
    echo -e "${BLUE}= Turd Bird Universe - Content Template Application Tool           =${NC}"
    echo -e "${BLUE}= Version 1.0.0                                                    =${NC}"
    echo -e "${BLUE}====================================================================${NC}"
    echo ""
}

# Function to show available templates
show_templates() {
    echo -e "${CYAN}Available Templates:${NC}"
    echo ""
    echo -e "${YELLOW}Character Templates:${NC}"
    echo "1. Character Profile"
    echo "2. Character Overview Brief"
    echo "3. Character Physical Attributes"
    echo "4. Character Personality Attributes"
    echo "5. Character Development"
    echo ""
    echo -e "${YELLOW}Relationship Templates:${NC}"
    echo "6. Character Relationship"
    echo ""
    echo -e "${YELLOW}Timeline Templates:${NC}"
    echo "7. Timeline Event"
    echo ""
    echo -e "${YELLOW}Corporate Templates:${NC}"
    echo "8. Corporate Entity"
    echo "9. Product/Innovation"
    echo ""
}

# Function to select template
select_template() {
    local choice
    read -p "Enter template number (1-9): " choice
    
    case $choice in
        1) echo "character-profile-template.md";;
        2) echo "character-overview-brief.template";;
        3) echo "character-attributes-physical.template";;
        4) echo "character-attributes-personality.template";;
        5) echo "character-development-template.md";;
        6) echo "relationship-template.md";;
        7) echo "timeline-event-template.md";;
        8) echo "corporate-entity-template.md";;
        9) echo "product-innovation-template.md";;
        *) echo "Invalid choice"; return 1;;
    esac
}

# Function to determine output path based on template type and user input
determine_output_path() {
    local template="$1"
    local name="$2"
    local kebab_name=$(to_kebab_case "$name")
    local output_path
    
    case $template in
        "character-profile-template.md")
            read -p "Enter character directory (e.g., fred-turd): " char_dir
            if [ -z "$char_dir" ]; then char_dir="$kebab_name"; fi
            output_path="${BASE_DIR}/characters/${char_dir}/_profile/character-${kebab_name}-overview.md"
            ;;
        "character-overview-brief.template")
            read -p "Enter character directory (e.g., fred-turd): " char_dir
            if [ -z "$char_dir" ]; then char_dir="$kebab_name"; fi
            output_path="${BASE_DIR}/characters/${char_dir}/_profile/character-${kebab_name}-overview-brief.md"
            ;;
        "character-attributes-physical.template")
            read -p "Enter character directory (e.g., fred-turd): " char_dir
            if [ -z "$char_dir" ]; then char_dir="$kebab_name"; fi
            output_path="${BASE_DIR}/characters/${char_dir}/_profile/attributes/character-${kebab_name}-attributes-physical.md"
            ;;
        "character-attributes-personality.template")
            read -p "Enter character directory (e.g., fred-turd): " char_dir
            if [ -z "$char_dir" ]; then char_dir="$kebab_name"; fi
            output_path="${BASE_DIR}/characters/${char_dir}/_profile/attributes/character-${kebab_name}-attributes-personality.md"
            ;;
        "character-development-template.md")
            read -p "Enter character directory (e.g., fred-turd): " char_dir
            if [ -z "$char_dir" ]; then char_dir="$kebab_name"; fi
            output_path="${BASE_DIR}/characters/${char_dir}/development/character-${kebab_name}-development-arc.md"
            ;;
        "relationship-template.md")
            read -p "Enter first character (kebab-case): " char1
            read -p "Enter second character (kebab-case): " char2
            read -p "Enter relationship type (e.g., antagonism): " rel_type
            rel_type=$(to_kebab_case "$rel_type")
            output_path="${BASE_DIR}/relationships/relationship-${char1}-${char2}-${rel_type}.md"
            ;;
        "timeline-event-template.md")
            read -p "Enter event name (e.g., thursday-incident): " event_name
            event_name=$(to_kebab_case "$event_name")
            output_path="${BASE_DIR}/timeline/event-${event_name}.md"
            ;;
        "corporate-entity-template.md")
            read -p "Enter corporate entity name (e.g., turdbird-industries): " entity_name
            entity_name=$(to_kebab_case "$entity_name")
            output_path="${BASE_DIR}/corporate/entity-${entity_name}.md"
            ;;
        "product-innovation-template.md")
            read -p "Enter product category (e.g., weaponized-kitchenware): " category
            read -p "Enter product name (e.g., tactical-spork): " product_name
            category=$(to_kebab_case "$category")
            product_name=$(to_kebab_case "$product_name")
            output_path="${BASE_DIR}/products/${category}/product-${product_name}.md"
            ;;
        *)
            echo "Unknown template type"
            return 1
            ;;
    esac
    
    echo "$output_path"
}

# Function to create required directories
create_directories() {
    local dir_path=$(dirname "$1")
    mkdir -p "$dir_path"
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Could not create directory structure.${NC}"
        exit 1
    fi
    echo -e "${GREEN}Created directory structure: ${dir_path}${NC}"
}

# Function to apply template
apply_template() {
    local template_path="$1"
    local output_path="$2"
    local content_name="$3"
    
    cp "$template_path" "$output_path"
    
    # Replace placeholders
    sed -i "s/{{CHARACTER_NAME}}/$content_name/g" "$output_path"
    sed -i "s/{{CREATOR_ID}}/$CREATOR_ID/g" "$output_path"
    sed -i "s/{{CREATION_DATE}}/$DATE_TODAY/g" "$output_path"
    
    echo -e "${GREEN}Template applied successfully to: ${output_path}${NC}"
    echo ""
    echo -e "${YELLOW}Next Steps:${NC}"
    echo "1. Open the file and replace all remaining placeholders"
    echo "2. Add appropriate bidirectional references"
    echo "3. Verify the file structure and content"
    echo "4. Check the line count to ensure it's under 150 lines"
    echo ""
}

# Main script execution
print_header
show_templates
template=$(select_template)

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Invalid template selection.${NC}"
    exit 1
fi

echo -e "${GREEN}Selected template: ${template}${NC}"
echo ""

read -p "Enter the name for your content (e.g., character name, event name): " content_name

if [ -z "$content_name" ]; then
    echo -e "${RED}Error: Content name cannot be empty.${NC}"
    exit 1
fi

output_path=$(determine_output_path "$template" "$content_name")

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Could not determine output path.${NC}"
    exit 1
fi

echo -e "${CYAN}Output path: ${output_path}${NC}"
read -p "Proceed with creation? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo -e "${YELLOW}Operation cancelled.${NC}"
    exit 0
fi

create_directories "$output_path"
apply_template "${TEMPLATE_DIR}/${template}" "$output_path" "$content_name"

echo -e "${MAGENTA}Template application complete. Enjoy creating narrative content!${NC}"
echo -e "${BLUE}====================================================================${NC}"