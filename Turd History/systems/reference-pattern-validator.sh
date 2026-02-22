#!/bin/bash
# Reference Pattern Validator
# Edition #1.0.0 | Created: (NEUR-ARC-011) | Last Modified: (NEUR-ARC-011)
#
# This script validates references against standardized reference patterns
# for the Turd Bird Universe documentation system

# Configuration
BASEDIR="/mnt/z/Turdbot/Turd History"
PATTERN_STANDARDS="${BASEDIR}/docs/standards/reference-pattern-standards.md"
RELATIONSHIP_STANDARDS="${BASEDIR}/docs/standards/relationship-type-standards.md"
SECTION_STANDARDS="${BASEDIR}/docs/standards/reference-section-standards.md"
REFERENCE_REGISTRY="${BASEDIR}/registry/reference-registry.md"
REPORT_DIR="${BASEDIR}/systems/reports"

# Ensure reports directory exists
mkdir -p "${REPORT_DIR}"

# Generate timestamp for report naming
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
REPORT_FILE="${REPORT_DIR}/reference-validation-report-${TIMESTAMP}.md"

# Text formatting for nicer output
BOLD=$(tput bold)
NORMAL=$(tput sgr0)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
BLUE=$(tput setaf 4)
RED=$(tput setaf 1)
CYAN=$(tput setaf 6)
MAGENTA=$(tput setaf 5)

# Display usage information
usage() {
    echo "${BOLD}Reference Pattern Validator${NORMAL}"
    echo "Validates references against standardized patterns for the Turd Bird Universe"
    echo ""
    echo "Usage: $0 [OPTIONS] [file_path]"
    echo ""
    echo "Options:"
    echo "  -a, --all            Validate all files in the repository"
    echo "  -t, --type TYPE      Validate specific content type (character, timeline, corporate, product, relationship)"
    echo "  -r, --registry       Check registry integrity against actual references"
    echo "  -v, --verbose        Show detailed validation information"
    echo "  -p, --pattern-only   Validate only pattern compliance (faster)"
    echo "  -s, --section-only   Validate only section placement"
    echo "  -f, --fix            Attempt to fix invalid references (use with caution)"
    echo "  -h, --help           Display this help message"
    echo ""
    echo "Examples:"
    echo "  $0 /mnt/z/Turdbot/Turd History/characters/fred-turd/_profile/character-fred-turd-overview.md"
    echo "  $0 --all"
    echo "  $0 --type character"
    exit 1
}

# Initialize report file
initialize_report() {
    cat > "${REPORT_FILE}" << EOF
# Reference Pattern Validation Report
**Generated: $(date)**

## Overview

This report validates reference patterns across the Turd Bird Universe documentation system, checking for:

1. Correct relationship types between content categories
2. Proper section placement of references
3. Valid bidirectional reference integrity
4. Registry entry compliance

## Summary

EOF
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
        registry_id=$(echo "$ref_line" | grep -o 'registry-id="[^"]*"' | sed 's/registry-id="//;s/"//')
        created=$(echo "$ref_line" | grep -o 'created="[^"]*"' | sed 's/created="//;s/"//')
        created_by=$(echo "$ref_line" | grep -o 'created-by="[^"]*"' | sed 's/created-by="//;s/"//')
        
        # Get the section containing this reference
        section_line=$(awk -v line_num="$line_num" 'NR < line_num && /^#{1,3}/ {section=$0; section_line=NR} END {print section_line":"section}' "$file_path")
        section_line_num=$(echo "$section_line" | cut -d: -f1)
        section=$(echo "$section_line" | cut -d: -f2-)
        
        # Get the parent section if this is an H3 section
        if [[ "$section" == "### "* ]]; then
            parent_section=$(awk -v section_line="$section_line_num" 'NR < section_line && /^##[^#]/ {parent=$0; parent_line=NR} END {print parent_line":"parent}' "$file_path")
            parent_section_line_num=$(echo "$parent_section" | cut -d: -f1)
            parent_section=$(echo "$parent_section" | cut -d: -f2-)
            section="$parent_section > $section"
        fi
        
        echo "$line_num:$target:$type:$direction:$registry_id:$created:$created_by:$section"
    done
}

# Determine content type from file path
get_content_type() {
    local file_path="$1"
    
    if [[ "$file_path" == *"/characters/"* ]]; then
        echo "character"
    elif [[ "$file_path" == *"/timeline/"* ]]; then
        echo "timeline"
    elif [[ "$file_path" == *"/corporate/"* ]]; then
        echo "corporate"
    elif [[ "$file_path" == *"/products/"* ]]; then
        echo "product"
    elif [[ "$file_path" == *"/relationships/"* ]]; then
        echo "relationship"
    else
        echo "unknown"
    fi
}

# Determine content type from path
get_path_content_type() {
    local path="$1"
    
    if [[ "$path" == *"/characters/"* ]]; then
        echo "character"
    elif [[ "$path" == *"/timeline/"* ]]; then
        echo "timeline"
    elif [[ "$path" == *"/corporate/"* ]]; then
        echo "corporate"
    elif [[ "$path" == *"/products/"* ]]; then
        echo "product"
    elif [[ "$path" == *"/relationships/"* ]]; then
        echo "relationship"
    else
        echo "unknown"
    fi
}

# Validate relationship type
validate_relationship_type() {
    local source_type="$1"
    local target_type="$2"
    local rel_type="$3"
    
    # Comprehensive validation based on relationship-type-standards.md
    case "${source_type}-${target_type}" in
        "character-character")
            if [[ "$rel_type" == "allies-with" || "$rel_type" == "antagonistic-toward" || 
                  "$rel_type" == "subordinate-to" || "$rel_type" == "superior-to" || 
                  "$rel_type" == "familial-with" || "$rel_type" == "romantic-with" || 
                  "$rel_type" == "professional-with" || "$rel_type" == "ambivalent-toward" || 
                  "$rel_type" == "mentors" || "$rel_type" == "mentored-by" || 
                  "$rel_type" == "rivals-with" ]]; then
                return 0
            else
                return 1
            fi
            ;;
        "character-timeline")
            if [[ "$rel_type" == "participates-in" || "$rel_type" == "influences" || 
                  "$rel_type" == "witnesses" || "$rel_type" == "affected-by" || 
                  "$rel_type" == "orchestrates" || "$rel_type" == "victimized-by" ]]; then
                return 0
            else
                return 1
            fi
            ;;
        "character-corporate")
            if [[ "$rel_type" == "founded" || "$rel_type" == "employed-by" || 
                  "$rel_type" == "consults-for" || "$rel_type" == "invests-in" || 
                  "$rel_type" == "manages" || "$rel_type" == "shareholds-in" || 
                  "$rel_type" == "opposes" ]]; then
                return 0
            else
                return 1
            fi
            ;;
        "character-product")
            if [[ "$rel_type" == "created" || "$rel_type" == "uses" || 
                  "$rel_type" == "maintains" || "$rel_type" == "markets" || 
                  "$rel_type" == "inspired" || "$rel_type" == "sabotages" ]]; then
                return 0
            else
                return 1
            fi
            ;;
        "timeline-character")
            if [[ "$rel_type" == "involves" || "$rel_type" == "influenced-by" || 
                  "$rel_type" == "witnessed-by" || "$rel_type" == "affects" || 
                  "$rel_type" == "orchestrated-by" || "$rel_type" == "victimizes" ]]; then
                return 0
            else
                return 1
            fi
            ;;
        "timeline-timeline")
            if [[ "$rel_type" == "precedes" || "$rel_type" == "follows" || 
                  "$rel_type" == "causes" || "$rel_type" == "caused-by" || 
                  "$rel_type" == "concurrent-with" || "$rel_type" == "alternative-to" || 
                  "$rel_type" == "diverges-from" || "$rel_type" == "diverged-by" ]]; then
                return 0
            else
                return 1
            fi
            ;;
        # Add other relationship type validations here
        *)
            # For relationship types we haven't explicitly defined, return true
            # to avoid false negatives during initial implementation
            return 0
            ;;
    esac
}

# Get reciprocal relationship type
get_reciprocal_type() {
    local source_type="$1"
    local target_type="$2"
    local rel_type="$3"
    
    case "${source_type}-${target_type}-${rel_type}" in
        "character-character-allies-with") echo "allies-with" ;;
        "character-character-antagonistic-toward") echo "antagonistic-toward" ;;
        "character-character-subordinate-to") echo "superior-to" ;;
        "character-character-superior-to") echo "subordinate-to" ;;
        "character-character-familial-with") echo "familial-with" ;;
        "character-character-romantic-with") echo "romantic-with" ;;
        "character-character-professional-with") echo "professional-with" ;;
        "character-character-ambivalent-toward") echo "ambivalent-toward" ;;
        "character-character-mentors") echo "mentored-by" ;;
        "character-character-mentored-by") echo "mentors" ;;
        "character-character-rivals-with") echo "rivals-with" ;;
        
        "character-timeline-participates-in") echo "involves" ;;
        "character-timeline-influences") echo "influenced-by" ;;
        "character-timeline-witnesses") echo "witnessed-by" ;;
        "character-timeline-affected-by") echo "affects" ;;
        "character-timeline-orchestrates") echo "orchestrated-by" ;;
        "character-timeline-victimized-by") echo "victimizes" ;;
        
        "timeline-character-involves") echo "participates-in" ;;
        "timeline-character-influenced-by") echo "influences" ;;
        "timeline-character-witnessed-by") echo "witnesses" ;;
        "timeline-character-affects") echo "affected-by" ;;
        "timeline-character-orchestrated-by") echo "orchestrates" ;;
        "timeline-character-victimizes") echo "victimized-by" ;;
        
        "timeline-timeline-precedes") echo "follows" ;;
        "timeline-timeline-follows") echo "precedes" ;;
        "timeline-timeline-causes") echo "caused-by" ;;
        "timeline-timeline-caused-by") echo "causes" ;;
        "timeline-timeline-concurrent-with") echo "concurrent-with" ;;
        "timeline-timeline-alternative-to") echo "alternative-to" ;;
        "timeline-timeline-diverges-from") echo "diverged-by" ;;
        "timeline-timeline-diverged-by") echo "diverges-from" ;;
        
        # Add other reciprocal type mappings here
        
        *) echo "unknown" ;;
    esac
}

# Validate section placement
validate_section_placement() {
    local source_type="$1"
    local target_type="$2"
    local section="$3"
    
    # Extract the primary section (H2)
    local primary_section
    if [[ "$section" == *">"* ]]; then
        primary_section=$(echo "$section" | cut -d'>' -f1 | xargs)
        primary_section=$(echo "$primary_section" | sed 's/^## //')
    else
        primary_section=$(echo "$section" | sed 's/^## //')
    fi
    
    case "${source_type}-${target_type}" in
        "character-character")
            if [[ "$primary_section" == "RELATIONSHIPS" ]]; then
                return 0
            else
                return 1
            fi
            ;;
        "character-timeline")
            if [[ "$primary_section" == "HISTORY" ]]; then
                return 0
            else
                return 1
            fi
            ;;
        "character-corporate")
            if [[ "$primary_section" == "AFFILIATIONS" ]]; then
                return 0
            else
                return 1
            fi
            ;;
        "character-product")
            if [[ "$primary_section" == "CONTRIBUTIONS" ]]; then
                return 0
            else
                return 1
            fi
            ;;
        "timeline-character")
            if [[ "$primary_section" == "PARTICIPANTS" ]]; then
                return 0
            else
                return 1
            fi
            ;;
        "timeline-timeline")
            if [[ "$primary_section" == "RELATED-EVENTS" ]]; then
                return 0
            else
                return 1
            fi
            ;;
        "timeline-corporate")
            if [[ "$primary_section" == "ORGANIZATIONS" ]]; then
                return 0
            else
                return 1
            fi
            ;;
        "timeline-product")
            if [[ "$primary_section" == "OUTCOMES" ]]; then
                return 0
            else
                return 1
            fi
            ;;
        "corporate-character")
            if [[ "$primary_section" == "PERSONNEL" ]]; then
                return 0
            else
                return 1
            fi
            ;;
        # Add other section validations here
        *)
            # For section placements we haven't explicitly defined, return true
            # to avoid false negatives during initial implementation
            return 0
            ;;
    esac
}

# Validate registry ID pattern
validate_registry_id() {
    local source_type="$1"
    local target_type="$2"
    local registry_id="$3"
    
    local expected_prefix
    
    case "${source_type}-${target_type}" in
        "character-character") expected_prefix="CHAR-CHAR" ;;
        "character-timeline") expected_prefix="CHAR-TIME" ;;
        "character-corporate") expected_prefix="CHAR-CORP" ;;
        "character-product") expected_prefix="CHAR-PROD" ;;
        "timeline-character") expected_prefix="TIME-CHAR" ;;
        "timeline-timeline") expected_prefix="TIME-TIME" ;;
        "timeline-corporate") expected_prefix="TIME-CORP" ;;
        "timeline-product") expected_prefix="TIME-PROD" ;;
        "corporate-character") expected_prefix="CORP-CHAR" ;;
        "corporate-timeline") expected_prefix="CORP-TIME" ;;
        "corporate-corporate") expected_prefix="CORP-CORP" ;;
        "corporate-product") expected_prefix="CORP-PROD" ;;
        "product-character") expected_prefix="PROD-CHAR" ;;
        "product-timeline") expected_prefix="PROD-TIME" ;;
        "product-corporate") expected_prefix="PROD-CORP" ;;
        "product-product") expected_prefix="PROD-PROD" ;;
        "relationship-character") expected_prefix="RELP-CHAR" ;;
        "relationship-timeline") expected_prefix="RELP-TIME" ;;
        "relationship-corporate") expected_prefix="RELP-CORP" ;;
        "relationship-product") expected_prefix="RELP-PROD" ;;
        # Add other registry ID prefix validations here
        *) expected_prefix="unknown" ;;
    esac
    
    if [[ "$expected_prefix" == "unknown" ]]; then
        # If we don't have a defined prefix, just check format
        if [[ "$registry_id" =~ ^[A-Z]+-[A-Z]+-[0-9]{3}$ ]]; then
            return 0
        else
            return 1
        fi
    else
        # Check if the registry ID starts with the expected prefix
        if [[ "$registry_id" =~ ^${expected_prefix}-[0-9]{3}$ ]]; then
            return 0
        else
            return 1
        fi
    fi
}

# Check if registry entry exists
check_registry_entry() {
    local registry_id="$1"
    
    if grep -q "### ${registry_id}\$" "$REFERENCE_REGISTRY"; then
        return 0
    else
        return 1
    fi
}

# Validate bidirectional reference
validate_bidirectional() {
    local source_file="$1"
    local target="$2"
    local registry_id="$3"
    local direction="$4"
    
    # Skip validation for non-bidirectional references
    if [[ "$direction" != "bidirectional" ]]; then
        return 0
    fi
    
    # Extract target file path
    local target_file
    if [[ "$target" =~ ^(.*?)\ §\ .*$ ]]; then
        target_file="${BASEDIR}/${BASH_REMATCH[1]}"
    else
        target_file="${BASEDIR}/$target"
    fi
    
    # Check if target file exists
    if [[ ! -f "$target_file" ]]; then
        return 1
    fi
    
    # Check if target file contains a reference back to the source with same registry ID
    source_rel=$(echo "$source_file" | sed "s|$BASEDIR/||")
    if grep -q "$registry_id" "$target_file" && grep -q "$source_rel" "$target_file"; then
        return 0
    else
        return 1
    fi
}

# Validate a single reference
validate_reference() {
    local file_path="$1"
    local line_num="$2"
    local target="$3"
    local type="$4"
    local direction="$5"
    local registry_id="$6"
    local section="$7"
    local verbose="$8"
    local pattern_only="$9"
    local section_only="${10}"
    
    local file_relative=$(echo "$file_path" | sed "s|$BASEDIR/||")
    local source_type=$(get_content_type "$file_path")
    local target_type=$(get_path_content_type "$target")
    local valid=true
    local issues=()
    
    # 1. Validate relationship type
    if ! validate_relationship_type "$source_type" "$target_type" "$type"; then
        valid=false
        issues+=("Invalid relationship type '$type' for $source_type → $target_type reference")
        
        # Recommend correct type
        local suggested_types=""
        case "${source_type}-${target_type}" in
            "character-character")
                suggested_types="allies-with, antagonistic-toward, subordinate-to, superior-to, etc."
                ;;
            "character-timeline")
                suggested_types="participates-in, influences, witnesses, affected-by, etc."
                ;;
            # Add suggestions for other combinations
        esac
        
        if [[ -n "$suggested_types" ]]; then
            issues+=("Suggested types: $suggested_types")
        fi
    fi
    
    # 2. Validate section placement
    if ! validate_section_placement "$source_type" "$target_type" "$section"; then
        valid=false
        issues+=("Invalid section placement: $section")
        
        # Recommend correct section
        local suggested_section=""
        case "${source_type}-${target_type}" in
            "character-character")
                suggested_section="RELATIONSHIPS"
                ;;
            "character-timeline")
                suggested_section="HISTORY"
                ;;
            "character-corporate")
                suggested_section="AFFILIATIONS"
                ;;
            "character-product")
                suggested_section="CONTRIBUTIONS"
                ;;
            "timeline-character")
                suggested_section="PARTICIPANTS"
                ;;
            "timeline-timeline")
                suggested_section="RELATED-EVENTS"
                ;;
            # Add suggestions for other combinations
        esac
        
        if [[ -n "$suggested_section" ]]; then
            issues+=("Reference should be in section: ## $suggested_section")
        fi
    fi
    
    # 3. Validate registry ID pattern
    if ! validate_registry_id "$source_type" "$target_type" "$registry_id"; then
        valid=false
        issues+=("Invalid registry ID format: $registry_id")
        
        # Recommend correct format
        local expected_prefix=""
        case "${source_type}-${target_type}" in
            "character-character") expected_prefix="CHAR-CHAR" ;;
            "character-timeline") expected_prefix="CHAR-TIME" ;;
            "character-corporate") expected_prefix="CHAR-CORP" ;;
            "character-product") expected_prefix="CHAR-PROD" ;;
            "timeline-character") expected_prefix="TIME-CHAR" ;;
            "timeline-timeline") expected_prefix="TIME-TIME" ;;
            # Add other combinations as needed
        esac
        
        if [[ -n "$expected_prefix" ]]; then
            issues+=("Registry ID should match pattern: ${expected_prefix}-[###]")
        fi
    fi
    
    # Skip additional checks if pattern_only is true
    if [[ "$pattern_only" == "true" ]]; then
        if [[ "$valid" == true ]]; then
            if [[ "$verbose" == "true" ]]; then
                echo "${GREEN}✓ Reference at line $line_num: $source_type → $target_type ($type)${NORMAL}"
            fi
            return 0
        else
            echo "${RED}✗ Invalid reference pattern at line $line_num in $file_relative:${NORMAL}"
            for issue in "${issues[@]}"; do
                echo "  - $issue"
            done
            return 1
        fi
    fi
    
    # Skip additional checks if section_only is true
    if [[ "$section_only" == "true" ]]; then
        if validate_section_placement "$source_type" "$target_type" "$section"; then
            if [[ "$verbose" == "true" ]]; then
                echo "${GREEN}✓ Reference section valid at line $line_num: $section${NORMAL}"
            fi
            return 0
        else
            echo "${RED}✗ Invalid section placement at line $line_num in $file_relative:${NORMAL}"
            echo "  - Current section: $section"
            
            # Recommend correct section
            local suggested_section=""
            case "${source_type}-${target_type}" in
                "character-character") suggested_section="RELATIONSHIPS" ;;
                "character-timeline") suggested_section="HISTORY" ;;
                # Add other combinations as needed
            esac
            
            if [[ -n "$suggested_section" ]]; then
                echo "  - Should be in section: ## $suggested_section"
            fi
            return 1
        fi
    fi
    
    # 4. Check registry entry exists
    if ! check_registry_entry "$registry_id"; then
        valid=false
        issues+=("Registry entry not found for ID: $registry_id")
    fi
    
    # 5. Validate bidirectional reference integrity
    if [[ "$direction" == "bidirectional" ]]; then
        if ! validate_bidirectional "$file_path" "$target" "$registry_id" "$direction"; then
            valid=false
            issues+=("Missing or incomplete bidirectional reference in target file")
            
            # Get reciprocal type for better error messages
            local reciprocal_type=$(get_reciprocal_type "$source_type" "$target_type" "$type")
            
            if [[ "$reciprocal_type" != "unknown" ]]; then
                issues+=("Reciprocal reference should use type: $reciprocal_type")
            fi
        fi
    fi
    
    # Output validation result
    if [[ "$valid" == true ]]; then
        if [[ "$verbose" == "true" ]]; then
            echo "${GREEN}✓ Valid reference at line $line_num: $source_type → $target_type ($type)${NORMAL}"
            echo "  - Registry ID: $registry_id"
            echo "  - Section: $section"
            echo "  - Target: $target"
        fi
        return 0
    else
        echo "${RED}✗ Invalid reference at line $line_num in $file_relative:${NORMAL}"
        for issue in "${issues[@]}"; do
            echo "  - $issue"
        done
        return 1
    fi
}

# Validate references in a single file
validate_file() {
    local file_path="$1"
    local verbose="$2"
    local pattern_only="$3"
    local section_only="$4"
    
    if [[ "$verbose" == "true" ]]; then
        echo "${BLUE}Validating references in: $file_path${NORMAL}"
    fi
    
    local file_relative=$(echo "$file_path" | sed "s|$BASEDIR/||")
    local references=$(extract_references "$file_path")
    local has_errors=false
    local valid_count=0
    local invalid_count=0
    
    if [ -z "$references" ]; then
        if [[ "$verbose" == "true" ]]; then
            echo "${YELLOW}No references found in: $file_path${NORMAL}"
        fi
        
        # Add to report
        echo "- ${file_relative}: No references found" >> "${REPORT_FILE}"
        
        return 0
    fi
    
    # Track issues for report
    local file_issues=""
    
    while IFS=: read -r line_num target type direction registry_id created created_by section; do
        validate_reference "$file_path" "$line_num" "$target" "$type" "$direction" "$registry_id" "$section" "$verbose" "$pattern_only" "$section_only"
        
        if [ $? -eq 0 ]; then
            valid_count=$((valid_count + 1))
        else
            invalid_count=$((invalid_count + 1))
            has_errors=true
            
            # Get content types for better reporting
            local source_type=$(get_content_type "$file_path")
            local target_type=$(get_path_content_type "$target")
            
            # Add issue to file issues for report
            file_issues+="  - Line $line_num: $source_type → $target_type ($type) in section '$section'\n"
            
            # Check specific issues for better reporting
            if ! validate_relationship_type "$source_type" "$target_type" "$type"; then
                file_issues+="    - Invalid relationship type '$type' for $source_type → $target_type\n"
            fi
            
            if ! validate_section_placement "$source_type" "$target_type" "$section"; then
                file_issues+="    - Invalid section placement: '$section'\n"
            fi
            
            if ! validate_registry_id "$source_type" "$target_type" "$registry_id"; then
                file_issues+="    - Invalid registry ID format: '$registry_id'\n"
            fi
            
            if ! check_registry_entry "$registry_id"; then
                file_issues+="    - Registry entry not found for ID: '$registry_id'\n"
            fi
            
            if [[ "$direction" == "bidirectional" ]]; then
                if ! validate_bidirectional "$file_path" "$target" "$registry_id" "$direction"; then
                    file_issues+="    - Missing bidirectional reference in target file\n"
                fi
            fi
        fi
    done <<< "$references"
    
    # Add to report
    if [[ "$has_errors" == "false" ]]; then
        echo "- ${file_relative}: ✓ All references valid ($valid_count)" >> "${REPORT_FILE}"
        
        if [[ "$verbose" == "true" ]]; then
            echo "${GREEN}All references in $file_path are valid.${NORMAL}"
            echo "  - Total references: $valid_count"
        else
            echo "${GREEN}✓ $file_relative ($valid_count references)${NORMAL}"
        fi
    else
        echo "- ${file_relative}: ✗ Contains $invalid_count invalid references (out of $((valid_count + invalid_count)) total)" >> "${REPORT_FILE}"
        echo -e "${file_issues}" >> "${REPORT_FILE}"
        
        echo "${RED}✗ $file_relative has $invalid_count invalid references (out of $((valid_count + invalid_count)) total)${NORMAL}"
    fi
    
    return $((invalid_count > 0))
}

# Validate files by content type
validate_content_type() {
    local content_type="$1"
    local verbose="$2"
    local pattern_only="$3"
    local section_only="$4"
    
    local search_path=""
    case "$content_type" in
        "character") search_path="${BASEDIR}/characters" ;;
        "timeline") search_path="${BASEDIR}/timeline" ;;
        "corporate") search_path="${BASEDIR}/corporate" ;;
        "product") search_path="${BASEDIR}/products" ;;
        "relationship") search_path="${BASEDIR}/relationships" ;;
        *)
            echo "${RED}Invalid content type: $content_type${NORMAL}"
            return 1
            ;;
    esac
    
    echo "${BLUE}Validating all $content_type files...${NORMAL}"
    echo "## $content_type Files" >> "${REPORT_FILE}"
    
    local file_count=0
    local error_count=0
    
    while IFS= read -r file; do
        validate_file "$file" "$verbose" "$pattern_only" "$section_only"
        if [ $? -ne 0 ]; then
            error_count=$((error_count + 1))
        fi
        file_count=$((file_count + 1))
    done < <(find "$search_path" -type f -name "*.md" | sort)
    
    echo "" >> "${REPORT_FILE}"
    echo "## $content_type Summary" >> "${REPORT_FILE}"
    echo "- Total files: $file_count" >> "${REPORT_FILE}"
    echo "- Files with errors: $error_count" >> "${REPORT_FILE}"
    echo "" >> "${REPORT_FILE}"
    
    echo "${BLUE}$content_type validation complete: $error_count files with errors out of $file_count total${NORMAL}"
    echo ""
    
    return $((error_count > 0))
}

# Validate registry integrity
validate_registry() {
    local verbose="$1"
    
    echo "${BLUE}Validating reference registry integrity...${NORMAL}"
    echo "## Registry Validation" >> "${REPORT_FILE}"
    
    # Check if registry file exists
    if [ ! -f "$REFERENCE_REGISTRY" ]; then
        echo "${RED}Reference registry file not found: $REFERENCE_REGISTRY${NORMAL}"
        echo "- ERROR: Reference registry file not found!" >> "${REPORT_FILE}"
        return 1
    fi
    
    local registry_entries=0
    local valid_entries=0
    local invalid_entries=0
    local missing_sources=0
    local missing_targets=0
    local issues=""
    
    # Extract and validate each registry entry
    grep -n "^### [A-Z]\+-[A-Z]\+-[0-9]\+$" "$REFERENCE_REGISTRY" | while read -r line; do
        local line_num=$(echo "$line" | cut -d: -f1)
        local registry_id=$(echo "$line" | cut -d: -f2- | sed 's/^### //')
        
        registry_entries=$((registry_entries + 1))
        
        # Extract source and target
        local source=$(sed -n "$((line_num + 1))p" "$REFERENCE_REGISTRY" | grep -o '**Source:** .*' | sed 's/**Source:** //')
        local target=$(sed -n "$((line_num + 2))p" "$REFERENCE_REGISTRY" | grep -o '**Target:** .*' | sed 's/**Target:** //')
        local type=$(sed -n "$((line_num + 3))p" "$REFERENCE_REGISTRY" | grep -o '**Type:** .*' | sed 's/**Type:** //')
        local direction=$(sed -n "$((line_num + 4))p" "$REFERENCE_REGISTRY" | grep -o '**Direction:** .*' | sed 's/**Direction:** //')
        
        if [ -z "$source" ] || [ -z "$target" ]; then
            invalid_entries=$((invalid_entries + 1))
            issues+="- Registry entry $registry_id: Missing source or target information\n"
            continue
        fi
        
        # Check if source file exists
        local source_path="${BASEDIR}/$source"
        source_path=$(echo "$source_path" | cut -d ' ' -f1)  # Extract path before any § section
        
        if [ ! -f "$source_path" ]; then
            missing_sources=$((missing_sources + 1))
            issues+="- Registry entry $registry_id: Source file not found: $source\n"
        fi
        
        # Check if target file exists
        local target_path="${BASEDIR}/$target"
        target_path=$(echo "$target_path" | cut -d ' ' -f1)  # Extract path before any § section
        
        if [ ! -f "$target_path" ]; then
            missing_targets=$((missing_targets + 1))
            issues+="- Registry entry $registry_id: Target file not found: $target\n"
        fi
        
        # Validate relationship type based on source and target type
        local source_type=$(get_path_content_type "$source")
        local target_type=$(get_path_content_type "$target")
        
        if ! validate_relationship_type "$source_type" "$target_type" "$type"; then
            invalid_entries=$((invalid_entries + 1))
            issues+="- Registry entry $registry_id: Invalid relationship type '$type' for $source_type → $target_type\n"
        fi
        
        # Validate registry ID pattern
        if ! validate_registry_id "$source_type" "$target_type" "$registry_id"; then
            invalid_entries=$((invalid_entries + 1))
            issues+="- Registry entry $registry_id: Invalid registry ID format for $source_type → $target_type\n"
        fi
        
        # If both files exist, check bidirectional references
        if [ -f "$source_path" ] && [ -f "$target_path" ] && [[ "$direction" == "bidirectional" ]]; then
            if ! grep -q "$registry_id" "$source_path" || ! grep -q "$registry_id" "$target_path"; then
                invalid_entries=$((invalid_entries + 1))
                issues+="- Registry entry $registry_id: Reference ID not found in source or target file\n"
            fi
        fi
        
        # If no issues found, mark as valid
        if [[ "$invalid_entries" == "0" && "$missing_sources" == "0" && "$missing_targets" == "0" ]]; then
            valid_entries=$((valid_entries + 1))
        fi
    done
    
    # Report results
    echo "### Registry Statistics" >> "${REPORT_FILE}"
    echo "- Total entries: $registry_entries" >> "${REPORT_FILE}"
    echo "- Valid entries: $valid_entries" >> "${REPORT_FILE}"
    echo "- Invalid entries: $invalid_entries" >> "${REPORT_FILE}"
    echo "- Missing source files: $missing_sources" >> "${REPORT_FILE}"
    echo "- Missing target files: $missing_targets" >> "${REPORT_FILE}"
    
    if [[ "$invalid_entries" -gt 0 || "$missing_sources" -gt 0 || "$missing_targets" -gt 0 ]]; then
        echo "### Registry Issues" >> "${REPORT_FILE}"
        echo -e "$issues" >> "${REPORT_FILE}"
        
        echo "${RED}Registry validation found issues:${NORMAL}"
        echo " - Invalid entries: $invalid_entries"
        echo " - Missing source files: $missing_sources"
        echo " - Missing target files: $missing_targets"
        
        if [[ "$verbose" == "true" ]]; then
            echo "${YELLOW}Issues:${NORMAL}"
            echo -e "$issues"
        fi
        
        return 1
    else
        echo "${GREEN}Registry validation passed: All $registry_entries entries are valid${NORMAL}"
        return 0
    fi
}

# Validate all files
validate_all() {
    local verbose="$1"
    local pattern_only="$2"
    local section_only="$3"
    
    echo "${BLUE}Validating all reference patterns in the repository...${NORMAL}"
    echo "# Complete Reference Pattern Validation" >> "${REPORT_FILE}"
    
    validate_content_type "character" "$verbose" "$pattern_only" "$section_only"
    validate_content_type "timeline" "$verbose" "$pattern_only" "$section_only"
    validate_content_type "corporate" "$verbose" "$pattern_only" "$section_only"
    validate_content_type "product" "$verbose" "$pattern_only" "$section_only"
    validate_content_type "relationship" "$verbose" "$pattern_only" "$section_only"
    
    if [[ "$pattern_only" != "true" && "$section_only" != "true" ]]; then
        validate_registry "$verbose"
    fi
    
    echo "${BLUE}Reference pattern validation complete. Report saved to: ${REPORT_FILE}${NORMAL}"
}

# Main script execution
VALIDATE_ALL=false
CONTENT_TYPE=""
CHECK_REGISTRY=false
VERBOSE=false
PATTERN_ONLY=false
SECTION_ONLY=false
FIX_ISSUES=false
FILE_PATH=""

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
        -p|--pattern-only)
            PATTERN_ONLY=true
            shift
            ;;
        -s|--section-only)
            SECTION_ONLY=true
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

# Initialize report
initialize_report

# Execute validation based on provided arguments
if [[ "$VALIDATE_ALL" == "true" ]]; then
    validate_all "$VERBOSE" "$PATTERN_ONLY" "$SECTION_ONLY"
elif [[ -n "$CONTENT_TYPE" ]]; then
    validate_content_type "$CONTENT_TYPE" "$VERBOSE" "$PATTERN_ONLY" "$SECTION_ONLY"
elif [[ "$CHECK_REGISTRY" == "true" ]]; then
    validate_registry "$VERBOSE"
elif [[ -n "$FILE_PATH" ]]; then
    validate_file "$FILE_PATH" "$VERBOSE" "$PATTERN_ONLY" "$SECTION_ONLY"
else
    usage
fi

# Make the script executable
chmod +x "$0"