#!/bin/bash
# Reference Pattern Validator
# Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)
#
# This script validates references in Turd Bird Universe documentation
# Ensuring compliance with reference pattern standards

# Configuration
BASEDIR="/mnt/z/Turdbot/Turd History"
PATTERN_STANDARDS="${BASEDIR}/systems/reference-pattern-standards.md"
REFERENCE_REGISTRY="${BASEDIR}/registry/reference-registry.md"

# Text formatting for nicer output
BOLD=$(tput bold)
NORMAL=$(tput sgr0)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
BLUE=$(tput setaf 4)
RED=$(tput setaf 1)

# Display usage information
usage() {
    echo "${BOLD}Reference Pattern Validator${NORMAL}"
    echo "Validates references against standardized patterns for the Turd Bird Universe"
    echo ""
    echo "Usage: $0 [OPTIONS] [file_path]"
    echo ""
    echo "Options:"
    echo "  -a, --all            Validate all files in the repository"
    echo "  -t, --type TYPE      Validate specific content type (character, timeline, corporate, product)"
    echo "  -r, --registry       Check registry integrity against actual references"
    echo "  -v, --verbose        Show detailed validation information"
    echo "  -f, --fix            Attempt to fix invalid references (use with caution)"
    echo "  -h, --help           Display this help message"
    echo ""
    echo "Examples:"
    echo "  $0 /mnt/z/Turdbot/Turd History/characters/fred-turd/_profile/character-fred-turd-overview.md"
    echo "  $0 --all"
    echo "  $0 --type character"
    exit 1
}

# Extract references from a file
extract_references() {
    local file_path="$1"
    grep -n "<reference" "$file_path" | while read -r line; do
        line_num=$(echo "$line" | cut -d: -f1)
        ref_line=$(echo "$line" | cut -d: -f2-)
        
        # Extract reference attributes
        target=$(echo "$ref_line" | grep -o 'target="[^"]*"' | sed 's/target="//;s/"//')
        type=$(echo "$ref_line" | grep -o 'type="[^"]*"' | sed 's/type="//;s/"//')
        direction=$(echo "$ref_line" | grep -o 'direction="[^"]*"' | sed 's/direction="//;s/"//')
        
        echo "$line_num:$target:$type:$direction"
    done
}

# Validate a single reference
validate_reference() {
    local file_path="$1"
    local line_num="$2"
    local target="$3"
    local type="$4"
    local direction="$5"
    local verbose="$6"
    
    local file_type=""
    local target_type=""
    local valid=true
    local error_message=""
    
    # Determine file type
    if [[ "$file_path" == *"/characters/"* ]]; then
        file_type="character"
    elif [[ "$file_path" == *"/timeline/"* ]]; then
        file_type="timeline"
    elif [[ "$file_path" == *"/corporate/"* ]]; then
        file_type="corporate"
    elif [[ "$file_path" == *"/products/"* ]]; then
        file_type="product"
    else
        file_type="unknown"
    fi
    
    # Determine target type
    if [[ "$target" == *"/characters/"* ]]; then
        target_type="character"
    elif [[ "$target" == *"/timeline/"* ]]; then
        target_type="timeline"
    elif [[ "$target" == *"/corporate/"* ]]; then
        target_type="corporate"
    elif [[ "$target" == *"/products/"* ]]; then
        target_type="product"
    else
        target_type="unknown"
    fi
    
    # Validate reference pattern based on file and target types
    case "$file_type-$target_type" in
        "character-character")
            if [[ "$type" != "relationship" ]]; then
                valid=false
                error_message="Invalid relationship type for character-to-character reference. Expected 'relationship', found '$type'"
            fi
            
            if [[ "$target" != *"§ RELATIONSHIPS §"* ]]; then
                valid=false
                error_message="$error_message\nInvalid section ID for character-to-character reference. Expected '§ RELATIONSHIPS § CHARACTER-NAME', found '$target'"
            fi
            ;;
        "character-timeline")
            if [[ "$type" != "participation" ]]; then
                valid=false
                error_message="Invalid relationship type for character-to-timeline reference. Expected 'participation', found '$type'"
            fi
            
            if [[ "$target" != *"§ PARTICIPANTS §"* ]]; then
                valid=false
                error_message="$error_message\nInvalid section ID for character-to-timeline reference. Expected '§ PARTICIPANTS § CHARACTER-NAME', found '$target'"
            fi
            ;;
        "timeline-timeline")
            if [[ "$type" != "precedes" && "$type" != "follows" && "$type" != "causes" && "$type" != "caused-by" && "$type" != "concurrent" && "$type" != "alternative" ]]; then
                valid=false
                error_message="Invalid relationship type for timeline-to-timeline reference. Expected one of 'precedes', 'follows', 'causes', 'caused-by', 'concurrent', 'alternative', found '$type'"
            fi
            
            if [[ "$target" != *"§ RELATED-EVENTS §"* ]]; then
                valid=false
                error_message="$error_message\nInvalid section ID for timeline-to-timeline reference. Expected '§ RELATED-EVENTS § EVENT-NAME', found '$target'"
            fi
            ;;
        "corporate-character")
            if [[ "$type" != "affiliation" ]]; then
                valid=false
                error_message="Invalid relationship type for corporate-to-character reference. Expected 'affiliation', found '$type'"
            fi
            
            if [[ "$target" != *"§ CAREER §"* ]]; then
                valid=false
                error_message="$error_message\nInvalid section ID for corporate-to-character reference. Expected '§ CAREER § ENTITY-NAME', found '$target'"
            fi
            ;;
        "product-character")
            if [[ "$type" != "creation" ]]; then
                valid=false
                error_message="Invalid relationship type for product-to-character reference. Expected 'creation', found '$type'"
            fi
            
            if [[ "$target" != *"§ INNOVATIONS §"* ]]; then
                valid=false
                error_message="$error_message\nInvalid section ID for product-to-character reference. Expected '§ INNOVATIONS § PRODUCT-NAME', found '$target'"
            fi
            ;;
        *)
            # Handle other combinations as needed
            ;;
    esac
    
    # Validate directionality
    if [[ "$direction" != "bidirectional" ]]; then
        valid=false
        error_message="$error_message\nInvalid direction for reference. Expected 'bidirectional', found '$direction'"
    fi
    
    # Output validation result
    if [[ "$valid" == true ]]; then
        if [[ "$verbose" == "true" ]]; then
            echo "${GREEN}✓ Valid reference at line $line_num: $file_type → $target_type ($type)${NORMAL}"
        fi
    else
        echo "${RED}✗ Invalid reference at line $line_num in $file_path:${NORMAL}"
        echo -e "$error_message" | sed 's/^/    /'
    fi
    
    return $([ "$valid" == true ] && echo 0 || echo 1)
}

# Validate bidirectional reference integrity
check_bidirectional() {
    local file_path="$1"
    local target="$2"
    local verbose="$3"
    
    # Extract target file and section
    target_file=$(echo "$target" | sed 's/ § .*//')
    
    # Check if target file exists
    if [ ! -f "$BASEDIR/$target_file" ]; then
        echo "${RED}✗ Broken reference: Target file does not exist: $target_file${NORMAL}"
        return 1
    fi
    
    # Check if target file has a reference back to the source
    source_relative=$(echo "$file_path" | sed "s|$BASEDIR/||")
    if ! grep -q "$source_relative" "$BASEDIR/$target_file"; then
        echo "${RED}✗ Missing bidirectional reference: $target_file does not reference $source_relative${NORMAL}"
        return 1
    fi
    
    if [[ "$verbose" == "true" ]]; then
        echo "${GREEN}✓ Bidirectional reference integrity verified: $file_path ↔ $target_file${NORMAL}"
    fi
    
    return 0
}

# Check registry entry exists for reference
check_registry() {
    local file_path="$1"
    local target="$2"
    local verbose="$3"
    
    source_relative=$(echo "$file_path" | sed "s|$BASEDIR/||")
    target_file=$(echo "$target" | sed 's/ § .*//')
    
    if ! grep -q "$source_relative" "$REFERENCE_REGISTRY" || ! grep -q "$target_file" "$REFERENCE_REGISTRY"; then
        echo "${RED}✗ Missing registry entry: Reference between $source_relative and $target_file is not registered${NORMAL}"
        return 1
    fi
    
    if [[ "$verbose" == "true" ]]; then
        echo "${GREEN}✓ Registry entry found for reference: $source_relative → $target_file${NORMAL}"
    fi
    
    return 0
}

# Validate references in a single file
validate_file() {
    local file_path="$1"
    local verbose="$2"
    local check_bidir="$3"
    local check_reg="$4"
    
    if [[ "$verbose" == "true" ]]; then
        echo "${BLUE}Validating references in: $file_path${NORMAL}"
    fi
    
    local references=$(extract_references "$file_path")
    local has_errors=false
    
    if [ -z "$references" ]; then
        if [[ "$verbose" == "true" ]]; then
            echo "${YELLOW}No references found in: $file_path${NORMAL}"
        fi
        return 0
    fi
    
    while IFS=: read -r line_num target type direction; do
        validate_reference "$file_path" "$line_num" "$target" "$type" "$direction" "$verbose"
        if [ $? -ne 0 ]; then
            has_errors=true
        fi
        
        if [[ "$check_bidir" == "true" ]]; then
            check_bidirectional "$file_path" "$target" "$verbose"
            if [ $? -ne 0 ]; then
                has_errors=true
            fi
        fi
        
        if [[ "$check_reg" == "true" ]]; then
            check_registry "$file_path" "$target" "$verbose"
            if [ $? -ne 0 ]; then
                has_errors=true
            fi
        fi
    done <<< "$references"
    
    if [[ "$has_errors" == "false" ]]; then
        if [[ "$verbose" == "true" ]]; then
            echo "${GREEN}All references in $file_path are valid.${NORMAL}"
        else
            echo "${GREEN}✓ $file_path${NORMAL}"
        fi
        return 0
    else
        return 1
    fi
}

# Validate references in all files of a specific type
validate_type() {
    local type="$1"
    local verbose="$2"
    local check_bidir="$3"
    local check_reg="$4"
    local pattern=""
    
    case "$type" in
        "character")
            pattern="$BASEDIR/characters/**/*.md"
            ;;
        "timeline")
            pattern="$BASEDIR/timeline/**/*.md"
            ;;
        "corporate")
            pattern="$BASEDIR/corporate/**/*.md"
            ;;
        "product")
            pattern="$BASEDIR/products/**/*.md"
            ;;
        *)
            echo "${RED}Invalid content type: $type${NORMAL}"
            return 1
            ;;
    esac
    
    echo "${BLUE}Validating all $type files...${NORMAL}"
    
    find $BASEDIR -path "$pattern" -type f | while read -r file; do
        validate_file "$file" "$verbose" "$check_bidir" "$check_reg"
    done
}

# Validate all references in the repository
validate_all() {
    local verbose="$1"
    local check_bidir="$2"
    local check_reg="$3"
    
    echo "${BLUE}Validating all references in the repository...${NORMAL}"
    
    validate_type "character" "$verbose" "$check_bidir" "$check_reg"
    validate_type "timeline" "$verbose" "$check_bidir" "$check_reg"
    validate_type "corporate" "$verbose" "$check_bidir" "$check_reg"
    validate_type "product" "$verbose" "$check_bidir" "$check_reg"
}

# Main script execution
VALIDATE_ALL=false
CONTENT_TYPE=""
CHECK_REGISTRY=false
VERBOSE=false
FIX_ISSUES=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -a|--all)
            VALIDATE_ALL=true
            shift
            ;;
        -t|--type)
            CONTENT_TYPE="$2"
            shift 2
            ;;
        -r|--registry)
            CHECK_REGISTRY=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -f|--fix)
            FIX_ISSUES=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        -*)
            echo "${RED}Unknown option: $1${NORMAL}"
            usage
            ;;
        *)
            FILE_PATH="$1"
            shift
            ;;
    esac
done

# Execute validation based on provided arguments
if [[ "$VALIDATE_ALL" == "true" ]]; then
    validate_all "$VERBOSE" true "$CHECK_REGISTRY"
elif [[ -n "$CONTENT_TYPE" ]]; then
    validate_type "$CONTENT_TYPE" "$VERBOSE" true "$CHECK_REGISTRY"
elif [[ -n "$FILE_PATH" ]]; then
    validate_file "$FILE_PATH" "$VERBOSE" true "$CHECK_REGISTRY"
else
    usage
fi

# Make the script executable
chmod +x "$0"