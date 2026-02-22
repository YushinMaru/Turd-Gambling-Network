#!/bin/bash
# Reference Validator for Refactoring
# Author: NEUR-ARC-011
# Version: 1.0.0
# Created: 2025-05-07
# Extended from reference-validator.sh to support refactoring operations

# Define base paths
BASE_DIR="/mnt/z/Turdbot/Turd History"
REGISTRY_FILE="${BASE_DIR}/registry/reference-registry.md"
REPORTS_DIR="${BASE_DIR}/systems/reports"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
REPORT_FILE="${REPORTS_DIR}/refactoring-validation-report-${TIMESTAMP}.md"
MIGRATION_PLAN_FILE="${REPORTS_DIR}/reference-migration-plan-${TIMESTAMP}.md"
UPDATE_COMMANDS_FILE="${REPORTS_DIR}/reference-update-commands-${TIMESTAMP}.sh"

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Global variables
REFACTORING_PLAN=""
REFACTORING_ID=""
REFACTORING_DESCRIPTION=""
REFACTORING_AUTHOR=""
FILE_MAPPINGS=()
AFFECTED_REFERENCES=()
BROKEN_REFERENCES=()
TOTAL_REFERENCES=0
AFFECTED_COUNT=0
MIGRATION_ACTIONS=()

# Function to print colored header
print_header() {
    echo -e "${BLUE}====================================================================${NC}"
    echo -e "${BLUE}= Turd Bird Universe - Reference Validator for Refactoring         =${NC}"
    echo -e "${BLUE}= Version 1.0.0                                                    =${NC}"
    echo -e "${BLUE}====================================================================${NC}"
    echo ""
}

# Function to load refactoring plan from JSON file
load_refactoring_plan() {
    local plan_file="$1"
    
    if [ ! -f "$plan_file" ]; then
        echo -e "${RED}Error: Refactoring plan file not found: $plan_file${NC}"
        exit 1
    }
    
    echo -e "${CYAN}Loading refactoring plan: $plan_file${NC}"
    
    # Check if jq is installed
    if ! command -v jq &> /dev/null; then
        echo -e "${RED}Error: jq is required but not installed. Please install jq to parse JSON files.${NC}"
        exit 1
    }
    
    # Extract metadata
    REFACTORING_ID=$(jq -r '.metadata.refactoring_id // "UNKNOWN"' "$plan_file")
    REFACTORING_DESCRIPTION=$(jq -r '.metadata.description // "No description provided"' "$plan_file")
    REFACTORING_AUTHOR=$(jq -r '.metadata.created_by // "UNKNOWN"' "$plan_file")
    
    echo -e "${CYAN}Refactoring ID: ${NC}${REFACTORING_ID}"
    echo -e "${CYAN}Description: ${NC}${REFACTORING_DESCRIPTION}"
    echo -e "${CYAN}Author: ${NC}${REFACTORING_AUTHOR}"
    echo ""
    
    # Extract file mappings
    local mapping_count=$(jq '.file_mappings | length' "$plan_file")
    echo -e "${CYAN}Found $mapping_count file mapping(s) in refactoring plan${NC}"
    
    for ((i=0; i<mapping_count; i++)); do
        local original=$(jq -r ".file_mappings[$i].original" "$plan_file")
        local refactored_count=$(jq ".file_mappings[$i].refactored | length" "$plan_file")
        
        echo -e "${CYAN}File mapping ${i+1}: ${YELLOW}$original${NC} -> ${GREEN}$refactored_count destination(s)${NC}"
        
        for ((j=0; j<refactored_count; j++)); do
            local refactored_path=$(jq -r ".file_mappings[$i].refactored[$j].path" "$plan_file")
            echo -e "  - ${GREEN}$refactored_path${NC}"
            
            # Extract section mappings if available
            if jq -e ".file_mappings[$i].refactored[$j].sections" "$plan_file" > /dev/null; then
                echo -e "    ${CYAN}Section mappings:${NC}"
                jq -r ".file_mappings[$i].refactored[$j].sections | to_entries[] | \"      - \\(.key) -> \\(.value)\"" "$plan_file"
            fi
        done
        
        # Store file mapping
        FILE_MAPPINGS+=("$original")
    done
    
    echo ""
    REFACTORING_PLAN="$plan_file"
}

# Function to extract references from a file
extract_references() {
    local file_path="$1"
    local reference_pattern="<reference[^>]*target=\"([^\"]+)\"[^>]*type=\"([^\"]+)\"[^>]*direction=\"([^\"]+)\"[^>]*registry-id=\"([^\"]+)\"[^>]*>"
    
    grep -oP "$reference_pattern" "$file_path" 2>/dev/null < /dev/null | while read -r reference; do
        target=$(echo "$reference" | grep -oP "target=\"([^\"]+)\"" | cut -d '"' -f 2)
        type=$(echo "$reference" | grep -oP "type=\"([^\"]+)\"" | cut -d '"' -f 2)
        direction=$(echo "$reference" | grep -oP "direction=\"([^\"]+)\"" | cut -d '"' -f 2)
        registry_id=$(echo "$reference" | grep -oP "registry-id=\"([^\"]+)\"" | cut -d '"' -f 2)
        
        echo "SOURCE:$file_path|TARGET:$target|TYPE:$type|DIRECTION:$direction|REGISTRY_ID:$registry_id"
        TOTAL_REFERENCES=$((TOTAL_REFERENCES + 1))
    done
}

# Function to check if a reference is affected by the refactoring plan
is_reference_affected() {
    local reference_data="$1"
    local source=$(echo "$reference_data" | cut -d'|' -f1 | cut -d':' -f2-)
    local target=$(echo "$reference_data" | cut -d'|' -f2 | cut -d':' -f2-)
    local registry_id=$(echo "$reference_data" | cut -d'|' -f5 | cut -d':' -f2-)
    
    # Extract file path and section from target
    local target_file="${target%% §*}"
    local target_section=""
    if [[ "$target" == *" § "* ]]; then
        target_section=$(echo "$target" | sed -E 's/.*§ ([^ @]+).*/\1/')
    fi
    
    # Check if target file is being refactored
    for original in "${FILE_MAPPINGS[@]}"; do
        if [[ "$target_file" == "$original" ]]; then
            # This reference is affected by the refactoring
            echo "AFFECTED|$source|$target|$registry_id|$original"
            return 0
        fi
    done
    
    # Also check if source file is being refactored (for bidirectional references)
    for original in "${FILE_MAPPINGS[@]}"; do
        if [[ "$source" == "$original" ]]; then
            # This reference is affected by the refactoring (source side)
            echo "AFFECTED|$source|$target|$registry_id|$original"
            return 0
        fi
    done
    
    # Not affected
    echo "UNAFFECTED|$source|$target|$registry_id"
    return 1
}

# Function to get the new path for a file being refactored
get_refactored_path() {
    local original_file="$1"
    local original_section="$2"
    
    if [ -z "$REFACTORING_PLAN" ]; then
        echo "$original_file"
        return
    }
    
    # Find the matching original file in the refactoring plan
    local idx=0
    for ((i=0; i<$(jq '.file_mappings | length' "$REFACTORING_PLAN"); i++)); do
        local original=$(jq -r ".file_mappings[$i].original" "$REFACTORING_PLAN")
        
        if [[ "$original" == "$original_file" ]]; then
            idx=$i
            break
        fi
    done
    
    # If original section is specified, try to find which refactored file contains it
    if [ -n "$original_section" ]; then
        local refactored_count=$(jq ".file_mappings[$idx].refactored | length" "$REFACTORING_PLAN")
        
        for ((j=0; j<refactored_count; j++)); do
            # Check if this refactored file has section mappings
            if jq -e ".file_mappings[$idx].refactored[$j].sections" "$REFACTORING_PLAN" > /dev/null; then
                # Check if the original section is mapped
                if jq -e ".file_mappings[$idx].refactored[$j].sections | has(\"$original_section\")" "$REFACTORING_PLAN" > /dev/null; then
                    # Found the mapping for this section
                    local new_path=$(jq -r ".file_mappings[$idx].refactored[$j].path" "$REFACTORING_PLAN")
                    local new_section=$(jq -r ".file_mappings[$idx].refactored[$j].sections[\"$original_section\"]" "$REFACTORING_PLAN")
                    echo "$new_path § $new_section"
                    return
                fi
            fi
        done
    fi
    
    # If we couldn't find a specific section mapping or no section was specified,
    # just return the first refactored file path
    if jq -e ".file_mappings[$idx].refactored[0]" "$REFACTORING_PLAN" > /dev/null; then
        local default_new_path=$(jq -r ".file_mappings[$idx].refactored[0].path" "$REFACTORING_PLAN")
        
        if [ -n "$original_section" ]; then
            echo "$default_new_path § $original_section"
        else
            echo "$default_new_path"
        fi
    else
        # Fallback to original if no refactored paths found
        if [ -n "$original_section" ]; then
            echo "$original_file § $original_section"
        else
            echo "$original_file"
        fi
    fi
}

# Function to create a reference migration action
create_migration_action() {
    local source="$1"
    local old_target="$2"
    local new_target="$3"
    local registry_id="$4"
    
    MIGRATION_ACTIONS+=("SOURCE:$source|OLD_TARGET:$old_target|NEW_TARGET:$new_target|REGISTRY_ID:$registry_id")
}

# Function to analyze a reference for refactoring impact
analyze_reference_for_refactoring() {
    local reference_data="$1"
    local impact_result=$(is_reference_affected "$reference_data")
    local impact_status=$(echo "$impact_result" | cut -d'|' -f1)
    
    if [[ "$impact_status" == "AFFECTED" ]]; then
        local source=$(echo "$impact_result" | cut -d'|' -f2)
        local target=$(echo "$impact_result" | cut -d'|' -f3)
        local registry_id=$(echo "$impact_result" | cut -d'|' -f4)
        local original_file=$(echo "$impact_result" | cut -d'|' -f5)
        
        # Extract target file and section
        local target_file="${target%% §*}"
        local target_section=""
        local target_version=""
        
        if [[ "$target" == *" § "* ]]; then
            if [[ "$target" == *" @ "* ]]; then
                # Has both section and version
                target_section=$(echo "$target" | sed -E 's/.*§ ([^ @]+).*/\1/')
                target_version=$(echo "$target" | sed -E 's/.*@ (v[0-9]+\.[0-9]+\.[0-9]+).*/\1/')
            else
                # Has section but no version
                target_section=$(echo "$target" | sed -E 's/.*§ ([^ ]+).*/\1/')
            fi
        elif [[ "$target" == *" @ "* ]]; then
            # Has version but no section
            target_version=$(echo "$target" | sed -E 's/.*@ (v[0-9]+\.[0-9]+\.[0-9]+).*/\1/')
        fi
        
        # Determine new target path based on refactoring plan
        local new_target_path=$(get_refactored_path "$target_file" "$target_section")
        
        # Increment version if specified
        local new_version=""
        if [ -n "$target_version" ]; then
            # Parse version components
            local major=$(echo "$target_version" | sed -E 's/v([0-9]+)\.[0-9]+\.[0-9]+/\1/')
            local minor=$(echo "$target_version" | sed -E 's/v[0-9]+\.([0-9]+)\.[0-9]+/\1/')
            local patch=$(echo "$target_version" | sed -E 's/v[0-9]+\.[0-9]+\.([0-9]+)/\1/')
            
            # Increment minor version for refactoring
            minor=$((minor + 1))
            patch=0
            
            new_version="v${major}.${minor}.${patch}"
        fi
        
        # Construct full new target
        local full_new_target=""
        if [ -n "$target_version" ]; then
            full_new_target="${new_target_path} @ ${new_version}"
        else
            full_new_target="${new_target_path}"
        fi
        
        # Check if the new target path would be valid
        local new_target_file="${new_target_path%% §*}"
        local full_new_target_path="${BASE_DIR}/${new_target_file}"
        
        if [ -f "$full_new_target_path" ] || grep -q "$new_target_file" "$REFACTORING_PLAN"; then
            # Reference can be updated
            AFFECTED_REFERENCES+=("VALID|$source|$target|$full_new_target|$registry_id")
            create_migration_action "$source" "$target" "$full_new_target" "$registry_id"
        else
            # Reference would be broken
            BROKEN_REFERENCES+=("BROKEN|$source|$target|$full_new_target|$registry_id")
        fi
        
        AFFECTED_COUNT=$((AFFECTED_COUNT + 1))
        
        echo "Affected reference in $source - $registry_id"
        echo "  Old target: $target"
        echo "  New target: $full_new_target"
        if [[ -f "$full_new_target_path" || grep -q "$new_target_file" "$REFACTORING_PLAN" ]]; then
            echo -e "  Status: ${GREEN}Updatable${NC}"
        else
            echo -e "  Status: ${RED}Would be broken${NC}"
        fi
        echo ""
    fi
}

# Function to scan entire repository for references
scan_repository_for_references() {
    echo -e "${CYAN}Scanning repository for references...${NC}"
    echo ""
    
    local total_files=0
    local files_with_references=0
    
    while read -r file; do
        total_files=$((total_files + 1))
        
        local references=$(extract_references "$file")
        if [ -n "$references" ]; then
            files_with_references=$((files_with_references + 1))
            
            while read -r reference; do
                if [ -n "$reference" ]; then
                    analyze_reference_for_refactoring "$reference"
                fi
            done <<< "$references"
        fi
    done < <(find "${BASE_DIR}" -type f -name "*.md" 2>/dev/null | sort)
    
    echo -e "${CYAN}Repository Scan Summary:${NC}"
    echo -e " - Total files scanned: $total_files"
    echo -e " - Files with references: $files_with_references"
    echo -e " - Total references found: $TOTAL_REFERENCES"
    echo -e " - ${YELLOW}References affected by refactoring: $AFFECTED_COUNT${NC}"
    echo -e " - ${GREEN}References updateable: ${#AFFECTED_REFERENCES[@]}${NC}"
    echo -e " - ${RED}References potentially broken: ${#BROKEN_REFERENCES[@]}${NC}"
    echo ""
}

# Function to generate reference update commands
generate_update_commands() {
    local commands_file="$1"
    
    echo "#!/bin/bash" > "$commands_file"
    echo "# Reference Update Commands for $REFACTORING_ID" >> "$commands_file"
    echo "# Generated: $(date +%Y-%m-%d)" >> "$commands_file"
    echo "" >> "$commands_file"
    echo "BASE_DIR=\"${BASE_DIR}\"" >> "$commands_file"
    echo "" >> "$commands_file"
    
    # Group actions by source file
    declare -A file_actions
    
    for action in "${MIGRATION_ACTIONS[@]}"; do
        local source=$(echo "$action" | cut -d'|' -f1 | cut -d':' -f2-)
        local old_target=$(echo "$action" | cut -d'|' -f2 | cut -d':' -f2-)
        local new_target=$(echo "$action" | cut -d'|' -f3 | cut -d':' -f2-)
        local registry_id=$(echo "$action" | cut -d'|' -f4 | cut -d':' -f2-)
        
        # Add to file actions
        if [ -n "${file_actions[$source]}" ]; then
            file_actions[$source]="${file_actions[$source]}
$old_target|$new_target|$registry_id"
        else
            file_actions[$source]="$old_target|$new_target|$registry_id"
        fi
    done
    
    # Generate sed commands for each file
    for source in "${!file_actions[@]}"; do
        echo "# Update references in $source" >> "$commands_file"
        
        while read -r action; do
            if [ -n "$action" ]; then
                local old_target=$(echo "$action" | cut -d'|' -f1)
                local new_target=$(echo "$action" | cut -d'|' -f2)
                local registry_id=$(echo "$action" | cut -d'|' -f3)
                
                # Escape special characters for sed
                local old_escaped=$(echo "$old_target" | sed 's/[\/&]/\\&/g')
                local new_escaped=$(echo "$new_target" | sed 's/[\/&]/\\&/g')
                
                echo "sed -i 's|<reference target=\"$old_escaped\"|<reference target=\"$new_escaped\"|g' \"\${BASE_DIR}/$source\"" >> "$commands_file"
            fi
        done <<< "${file_actions[$source]}"
        
        echo "" >> "$commands_file"
    done
    
    # Generate registry update commands
    echo "# Update registry entries" >> "$commands_file"
    for action in "${MIGRATION_ACTIONS[@]}"; do
        local old_target=$(echo "$action" | cut -d'|' -f2 | cut -d':' -f2-)
        local new_target=$(echo "$action" | cut -d'|' -f3 | cut -d':' -f2-)
        local registry_id=$(echo "$action" | cut -d'|' -f4 | cut -d':' -f2-)
        
        # Extract file and section
        local old_file="${old_target%% §*}"
        local old_section=""
        if [[ "$old_target" == *" § "* ]]; then
            if [[ "$old_target" == *" @ "* ]]; then
                old_section=$(echo "$old_target" | sed -E 's/.*§ ([^ @]+).*/\1/')
            else
                old_section=$(echo "$old_target" | sed -E 's/.*§ ([^ ]+).*/\1/')
            fi
        fi
        
        local new_file="${new_target%% §*}"
        local new_section=""
        if [[ "$new_target" == *" § "* ]]; then
            if [[ "$new_target" == *" @ "* ]]; then
                new_section=$(echo "$new_target" | sed -E 's/.*§ ([^ @]+).*/\1/')
            else
                new_section=$(echo "$new_target" | sed -E 's/.*§ ([^ ]+).*/\1/')
            fi
        fi
        
        # Escape special characters for sed
        local old_escaped=$(echo "$old_file § $old_section" | sed 's/[\/&]/\\&/g')
        local new_escaped=$(echo "$new_file § $new_section" | sed 's/[\/&]/\\&/g')
        
        echo "sed -i 's|**Target:** $old_escaped|**Target:** $new_escaped|g' \"\${BASE_DIR}/registry/reference-registry.md\"" >> "$commands_file"
    done
    
    echo "" >> "$commands_file"
    echo "echo \"Reference updates completed for $REFACTORING_ID\"" >> "$commands_file"
    
    # Make the file executable
    chmod +x "$commands_file"
    
    echo -e "${GREEN}Reference update commands generated: $commands_file${NC}"
}

# Function to generate migration plan
generate_migration_plan() {
    local plan_file="$1"
    
    cat > "$plan_file" << EOF
# Reference Migration Plan for $REFACTORING_ID
**Edition #1.0.0 | Created: ($REFACTORING_AUTHOR) | Last Modified: ($REFACTORING_AUTHOR)**

## Context
This document outlines the reference migration plan for $REFACTORING_DESCRIPTION.

## Reference Updates Required
EOF

    # Group actions by source file
    declare -A file_actions
    
    for action in "${MIGRATION_ACTIONS[@]}"; do
        local source=$(echo "$action" | cut -d'|' -f1 | cut -d':' -f2-)
        local old_target=$(echo "$action" | cut -d'|' -f2 | cut -d':' -f2-)
        local new_target=$(echo "$action" | cut -d'|' -f3 | cut -d':' -f2-)
        local registry_id=$(echo "$action" | cut -d'|' -f4 | cut -d':' -f2-)
        
        # Add to file actions
        if [ -n "${file_actions[$source]}" ]; then
            file_actions[$source]="${file_actions[$source]}
$old_target|$new_target|$registry_id"
        else
            file_actions[$source]="$old_target|$new_target|$registry_id"
        fi
    done
    
    # Generate detailed migration plan
    for source in "${!file_actions[@]}"; do
        echo "" >> "$plan_file"
        echo "### File: $source" >> "$plan_file"
        echo "" >> "$plan_file"
        echo "#### Original References" >> "$plan_file"
        
        while read -r action; do
            if [ -n "$action" ]; then
                local old_target=$(echo "$action" | cut -d'|' -f1)
                local registry_id=$(echo "$action" | cut -d'|' -f3)
                
                echo "- \`<reference target=\"$old_target\" type=\"supports\" direction=\"bidirectional\" registry-id=\"$registry_id\">\`" >> "$plan_file"
            fi
        done <<< "${file_actions[$source]}"
        
        echo "" >> "$plan_file"
        echo "#### Updated References" >> "$plan_file"
        
        while read -r action; do
            if [ -n "$action" ]; then
                local new_target=$(echo "$action" | cut -d'|' -f2)
                local registry_id=$(echo "$action" | cut -d'|' -f3)
                
                echo "- \`<reference target=\"$new_target\" type=\"supports\" direction=\"bidirectional\" registry-id=\"$registry_id\">\`" >> "$plan_file"
            fi
        done <<< "${file_actions[$source]}"
    done
    
    # Add registry updates
    echo "" >> "$plan_file"
    echo "### File: registry/reference-registry.md" >> "$plan_file"
    echo "" >> "$plan_file"
    
    for action in "${MIGRATION_ACTIONS[@]}"; do
        local source=$(echo "$action" | cut -d'|' -f1 | cut -d':' -f2-)
        local old_target=$(echo "$action" | cut -d'|' -f2 | cut -d':' -f2-)
        local new_target=$(echo "$action" | cut -d'|' -f3 | cut -d':' -f2-)
        local registry_id=$(echo "$action" | cut -d'|' -f4 | cut -d':' -f2-)
        
        # Extract file and section
        local old_file="${old_target%% §*}"
        local old_section=""
        if [[ "$old_target" == *" § "* ]]; then
            if [[ "$old_target" == *" @ "* ]]; then
                old_section=$(echo "$old_target" | sed -E 's/.*§ ([^ @]+).*/\1/')
            else
                old_section=$(echo "$old_target" | sed -E 's/.*§ ([^ ]+).*/\1/')
            fi
        fi
        
        local new_file="${new_target%% §*}"
        local new_section=""
        if [[ "$new_target" == *" § "* ]]; then
            if [[ "$new_target" == *" @ "* ]]; then
                new_section=$(echo "$new_target" | sed -E 's/.*§ ([^ @]+).*/\1/')
            else
                new_section=$(echo "$new_target" | sed -E 's/.*§ ([^ ]+).*/\1/')
            fi
        fi
        
        echo "#### Original Entry for $registry_id" >> "$plan_file"
        echo '```markdown' >> "$plan_file"
        echo "### $registry_id" >> "$plan_file"
        echo "**Source:** $(basename $source) § SECTION-ID" >> "$plan_file"
        echo "**Target:** $old_file § $old_section" >> "$plan_file"
        echo "**Type:** supports" >> "$plan_file"
        echo "**Direction:** bidirectional" >> "$plan_file"
        echo '```' >> "$plan_file"
        echo "" >> "$plan_file"
        
        echo "#### Updated Entry for $registry_id" >> "$plan_file"
        echo '```markdown' >> "$plan_file"
        echo "### $registry_id" >> "$plan_file"
        echo "**Source:** $(basename $source) § SECTION-ID" >> "$plan_file"
        echo "**Target:** $new_file § $new_section" >> "$plan_file"
        echo "**Type:** supports" >> "$plan_file"
        echo "**Direction:** bidirectional" >> "$plan_file"
        echo '```' >> "$plan_file"
        echo "" >> "$plan_file"
    done
    
    # Add broken references section if any
    if [ ${#BROKEN_REFERENCES[@]} -gt 0 ]; then
        echo "## Potential Reference Issues" >> "$plan_file"
        echo "" >> "$plan_file"
        echo "The following references may be broken after refactoring and require special attention:" >> "$plan_file"
        echo "" >> "$plan_file"
        
        for broken in "${BROKEN_REFERENCES[@]}"; do
            local source=$(echo "$broken" | cut -d'|' -f2)
            local old_target=$(echo "$broken" | cut -d'|' -f3)
            local new_target=$(echo "$broken" | cut -d'|' -f4)
            local registry_id=$(echo "$broken" | cut -d'|' -f5)
            
            echo "### $registry_id in $source" >> "$plan_file"
            echo "- **Original Target:** \`$old_target\`" >> "$plan_file"
            echo "- **Mapped Target:** \`$new_target\`" >> "$plan_file"
            echo "- **Issue:** Target file not found in refactoring plan or filesystem" >> "$plan_file"
            echo "" >> "$plan_file"
        done
    fi
    
    # Add workflow section
    cat >> "$plan_file" << EOF
## Implementation Workflow

1. Create backup copies of all affected files
2. Execute the reference update commands in the generated script
3. Verify reference integrity using the reference validator
4. Verify content consistency in updated references
5. Update the reference registry as indicated above
6. Run a full validation scan after all updates are complete
EOF
    
    echo -e "${GREEN}Reference migration plan generated: $plan_file${NC}"
}

# Function to generate validation report
generate_validation_report() {
    local report_file="$1"
    
    cat > "$report_file" << EOF
# Refactoring Reference Validation Report
**Generated:** $(date +%Y-%m-%d %H:%M:%S)
**Refactoring Plan:** $REFACTORING_ID - $REFACTORING_DESCRIPTION
**Refactoring Author:** $REFACTORING_AUTHOR

## Summary

- **Total References Analyzed:** $TOTAL_REFERENCES
- **References Affected by Refactoring:** $AFFECTED_COUNT
- **References Updateable:** ${#AFFECTED_REFERENCES[@]}
- **References Potentially Broken:** ${#BROKEN_REFERENCES[@]}

## Reference Update Actions

| Registry ID | Source File | Original Target | New Target | Status |
|-------------|-------------|-----------------|------------|--------|
EOF

    # Add affected references to report
    for action in "${MIGRATION_ACTIONS[@]}"; do
        local source=$(echo "$action" | cut -d'|' -f1 | cut -d':' -f2-)
        local old_target=$(echo "$action" | cut -d'|' -f2 | cut -d':' -f2-)
        local new_target=$(echo "$action" | cut -d'|' -f3 | cut -d':' -f2-)
        local registry_id=$(echo "$action" | cut -d'|' -f4 | cut -d':' -f2-)
        
        echo "| $registry_id | $source | $old_target | $new_target | ✅ Updateable |" >> "$report_file"
    done

    # Add broken references to report
    for broken in "${BROKEN_REFERENCES[@]}"; do
        local source=$(echo "$broken" | cut -d'|' -f2)
        local old_target=$(echo "$broken" | cut -d'|' -f3)
        local new_target=$(echo "$broken" | cut -d'|' -f4)
        local registry_id=$(echo "$broken" | cut -d'|' -f5)
        
        echo "| $registry_id | $source | $old_target | $new_target | ❌ Broken |" >> "$report_file"
    done

    # Add implementation guide
    cat >> "$report_file" << EOF

## Implementation Files

The following files have been generated to support the refactoring process:

1. **Migration Plan:** $MIGRATION_PLAN_FILE
   - Detailed breakdown of all reference changes
   - Registry update instructions
   - Implementation workflow

2. **Update Commands:** $UPDATE_COMMANDS_FILE
   - Executable script for automated reference updates
   - Registry update commands
   - Ready for execution after review

## Implementation Steps

1. **Review this validation report** to understand the scope of reference changes
2. **Examine the migration plan** for detailed reference update information
3. **Back up all affected files** before proceeding
4. **Execute the update commands** script to implement reference changes
5. **Verify reference integrity** using the standard reference validator
6. **Document the completed refactoring** in your implementation summary

## About This Report

This report was automatically generated by the Reference Validator for Refactoring tool.
The tool analyzes how a planned refactoring will impact references throughout the
Turd Bird Universe documentation and provides a comprehensive plan for maintaining
bidirectional reference integrity during the refactoring process.

### Usage Instructions

To run the Reference Validator for Refactoring:

1. Create a refactoring plan JSON file
2. Run \`./systems/reference-validator-refactoring.sh -p refactoring-plan.json\`
3. Review the generated validation report
4. Follow the implementation steps to maintain reference integrity
EOF

    echo -e "${GREEN}Validation report generated: $report_file${NC}"
}

# Main script execution
print_header

# Check command line arguments
if [ $# -eq 0 ]; then
    echo -e "${YELLOW}Usage:${NC}"
    echo "  $0 -p <refactoring_plan.json>   # Validate references against refactoring plan"
    echo "  $0 -h                           # Show this help message"
    exit 1
fi

while getopts "p:h" opt; do
    case $opt in
        p)
            REFACTORING_PLAN_FILE="$OPTARG"
            load_refactoring_plan "$REFACTORING_PLAN_FILE"
            scan_repository_for_references
            generate_migration_plan "$MIGRATION_PLAN_FILE"
            generate_update_commands "$UPDATE_COMMANDS_FILE"
            generate_validation_report "$REPORT_FILE"
            ;;
        h)
            echo -e "${YELLOW}Usage:${NC}"
            echo "  $0 -p <refactoring_plan.json>   # Validate references against refactoring plan"
            echo "  $0 -h                           # Show this help message"
            exit 0
            ;;
        \?)
            echo -e "${RED}Invalid option: -$OPTARG${NC}" >&2
            exit 1
            ;;
        :)
            echo -e "${RED}Option -$OPTARG requires an argument.${NC}" >&2
            exit 1
            ;;
    esac
done

echo -e "${BLUE}====================================================================${NC}"
echo -e "${BLUE}= Reference validation for refactoring complete                    =${NC}"
echo -e "${BLUE}====================================================================${NC}"