#!/bin/bash
# Reference Validator for Turd Bird Universe
# Edition #1.0.0 | Created: (NEUR-ARC-012) | Last Modified: (NEUR-ARC-012)
#
# This script validates bidirectional references throughout the Turd Bird
# Universe documentation, ensuring compliance with reference pattern standards.

# Color definitions for output formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration variables
REPO_ROOT="/mnt/z/Turdbot/Turd History"
REPORT_DIR="${REPO_ROOT}/systems/reports"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
REPORT_FILE="${REPORT_DIR}/reference-validation-report-${TIMESTAMP}.md"
REGISTRY_FILE="${REPO_ROOT}/registry/reference-registry.md"

# Initialize counters
total_files=0
total_references=0
broken_references=0
improper_types=0
section_violations=0
missing_registry=0

# Initialize output report
function init_report() {
    mkdir -p "${REPORT_DIR}"
    
    cat > "${REPORT_FILE}" << EOF
# Reference Validation Report
**Generated: $(date +"%Y-%m-%d %H:%M:%S")**

This report documents reference validation results for the Turd Bird Universe, including broken references, improper relationship types, section placement violations, and registry inconsistencies.

## Summary

EOF
}

# Print header
echo -e "${BLUE}=================================${NC}"
echo -e "${BLUE}Turd Bird Universe Reference Validator${NC}"
echo -e "${BLUE}=================================${NC}"
echo -e "Starting validation at $(date +"%Y-%m-%d %H:%M:%S")"
echo -e "Repository: ${REPO_ROOT}"
echo -e "Report will be saved to: ${REPORT_FILE}"
echo

# Initialize report
init_report

# Get all markdown files in the repository
files=$(find "${REPO_ROOT}" -name "*.md" | grep -v 'node_modules' | sort)

# Create associative arrays to store valid relationship types
declare -A char_char_rel_types=(
    ["allied-with"]="allied-with"
    ["antagonistic-toward"]="antagonistic-toward"
    ["mentors"]="mentored-by"
    ["mentored-by"]="mentors"
    ["reports-to"]="supervises"
    ["supervises"]="reports-to"
    ["rivals-with"]="rivals-with"
    ["friends-with"]="friends-with"
    ["related-to"]="related-to"
    ["manipulates"]="manipulated-by"
    ["manipulated-by"]="manipulates"
    ["influenced-by"]="influences"
    ["influences"]="influenced-by"
    ["protects"]="protected-by"
    ["protected-by"]="protects"
    ["threatened-by"]="threatens"
    ["threatens"]="threatened-by"
)

declare -A char_time_rel_types=(
    ["participates-in"]="involves"
    ["involves"]="participates-in"
    ["witnesses"]="witnessed-by"
    ["witnessed-by"]="witnesses"
    ["affected-by"]="impacts"
    ["impacts"]="affected-by"
    ["causes"]="caused-by"
    ["caused-by"]="causes"
    ["prevents"]="prevented-by"
    ["prevented-by"]="prevents"
    ["learns-from"]="teaches"
    ["teaches"]="learns-from"
    ["discovers-during"]="discovery-context-for"
    ["discovery-context-for"]="discovers-during"
    ["transforms-during"]="transformation-context-for"
    ["transformation-context-for"]="transforms-during"
)

# Function to validate relationship type based on content pair
function validate_relationship_type() {
    source_type=$1
    target_type=$2
    relationship=$3
    
    case "${source_type}-${target_type}" in
        "character-character")
            if [[ ${char_char_rel_types[$relationship]+_} ]]; then
                return 0
            else
                return 1
            fi
            ;;
        "character-timeline")
            if [[ ${char_time_rel_types[$relationship]+_} ]]; then
                return 0
            else
                return 1
            fi
            ;;
        # Additional content type pairs would be implemented here
        *)
            # Default case - relationship not found in any valid matrix
            return 1
            ;;
    esac
}

# Function to get bidirectional pair for a relationship type
function get_bidirectional_pair() {
    rel_type=$1
    source_type=$2
    target_type=$3
    
    case "${source_type}-${target_type}" in
        "character-character")
            echo "${char_char_rel_types[$rel_type]}"
            ;;
        "character-timeline")
            echo "${char_time_rel_types[$rel_type]}"
            ;;
        # Additional content type pairs would be implemented here
        *)
            # Default to empty if not found
            echo ""
            ;;
    esac
}

# Function to validate section placement of references
function validate_section_placement() {
    file=$1
    line=$2
    
    # Extract file type from path
    if [[ $file == *"/characters/"* ]]; then
        file_type="character"
    elif [[ $file == *"/timeline/"* ]]; then
        file_type="timeline"
    elif [[ $file == *"/corporate/"* ]]; then
        file_type="corporate"
    elif [[ $file == *"/relationships/"* ]]; then
        file_type="relationship"
    else
        file_type="other"
    fi
    
    # Check if reference is in proper section for file type
    case $file_type in
        "character")
            if ! grep -A10 -B10 "$line" "$file" | grep -q "^## References"; then
                return 1
            fi
            ;;
        "timeline")
            if ! grep -A10 -B10 "$line" "$file" | grep -q "^## Related Documentation"; then
                return 1
            fi
            ;;
        "corporate")
            if ! grep -A10 -B10 "$line" "$file" | grep -q "^## References & Connections"; then
                return 1
            fi
            ;;
        "relationship")
            if ! grep -A10 -B10 "$line" "$file" | grep -q "^## Referenced Documents"; then
                return 1
            fi
            ;;
        *)
            # Default section name for other file types
            if ! grep -A10 -B10 "$line" "$file" | grep -q "^## References"; then
                return 1
            fi
            ;;
    esac
    
    return 0
}

# Function to check if reference exists in registry
function check_registry_entry() {
    source=$1
    target=$2
    
    # Simplify paths for grep
    source_simple=$(echo "$source" | sed 's/\//\\\//g')
    target_simple=$(echo "$target" | sed 's/\//\\\//g')
    
    if grep -q "**Source:** ${source_simple}" "${REGISTRY_FILE}" && \
       grep -q "**Target:** ${target_simple}" "${REGISTRY_FILE}"; then
        return 0
    else
        return 1
    fi
}

# Process each file
for file in $files; do
    filename=$(basename "$file")
    total_files=$((total_files + 1))
    
    echo -e "${CYAN}Validating${NC}: $file"
    
    # Extract reference patterns from the file
    references=$(grep -n '\[.*\.md.*§.*\]' "$file" | grep -v '```')
    
    if [[ -z "$references" ]]; then
        echo -e "  ${YELLOW}No references found${NC}"
        continue
    fi
    
    # Process each reference
    while IFS= read -r ref_line; do
        total_references=$((total_references + 1))
        
        # Extract line number and content
        line_num=$(echo "$ref_line" | cut -d: -f1)
        line_content=$(echo "$ref_line" | cut -d: -f2-)
        
        # Extract reference path and section
        ref_path=$(echo "$line_content" | grep -o '\[.*\.md.*§.*\]' | sed 's/\[//;s/\].*//;s/ § /§/g')
        target_file=$(echo "$ref_path" | cut -d§ -f1 | xargs)
        target_section=$(echo "$ref_path" | cut -d§ -f2 | xargs)
        
        # Get full path for target file
        if [[ "$target_file" == /* ]]; then
            target_full="${REPO_ROOT}${target_file}"
        else
            target_dir=$(dirname "$file")
            target_full="${target_dir}/${target_file}"
        fi
        
        # Check if target file exists
        if [[ ! -f "$target_full" ]]; then
            broken_references=$((broken_references + 1))
            echo -e "  ${RED}Broken reference${NC}: $target_file (from line $line_num)"
            
            # Add to report
            echo "- **Broken reference** in $filename:$line_num - Target file does not exist: \`$target_file\`" >> "${REPORT_FILE}"
            continue
        fi
        
        # Check if target section exists
        if ! grep -q "$target_section" "$target_full"; then
            broken_references=$((broken_references + 1))
            echo -e "  ${RED}Broken section reference${NC}: $target_file § $target_section (from line $line_num)"
            
            # Add to report
            echo "- **Broken section reference** in $filename:$line_num - Section \`$target_section\` not found in \`$target_file\`" >> "${REPORT_FILE}"
        fi
        
        # Extract relationship type if present
        rel_type=""
        if [[ "$line_content" =~ -\ ([a-z\-]+): ]]; then
            rel_type="${BASH_REMATCH[1]}"
            
            # Determine content types for source and target
            source_type=""
            target_type=""
            
            # Derive source type from file path
            if [[ "$file" == *"/characters/"* ]]; then
                source_type="character"
            elif [[ "$file" == *"/timeline/"* ]]; then
                source_type="timeline"
            elif [[ "$file" == *"/corporate/"* ]]; then
                source_type="corporate"
            elif [[ "$file" == *"/relationships/"* ]]; then
                source_type="relationship"
            fi
            
            # Derive target type from target file path
            if [[ "$target_file" == *"/characters/"* ]]; then
                target_type="character"
            elif [[ "$target_file" == *"/timeline/"* ]]; then
                target_type="timeline"
            elif [[ "$target_file" == *"/corporate/"* ]]; then
                target_type="corporate"
            elif [[ "$target_file" == *"/relationships/"* ]]; then
                target_type="relationship"
            fi
            
            # Validate relationship type if both types are determined
            if [[ -n "$source_type" && -n "$target_type" ]]; then
                if ! validate_relationship_type "$source_type" "$target_type" "$rel_type"; then
                    improper_types=$((improper_types + 1))
                    echo -e "  ${YELLOW}Improper relationship type${NC}: $rel_type for $source_type-$target_type (from line $line_num)"
                    
                    # Add to report
                    echo "- **Improper relationship type** in $filename:$line_num - \`$rel_type\` is not valid for $source_type-$target_type pair" >> "${REPORT_FILE}"
                    
                    # Suggest correct relationship types
                    case "${source_type}-${target_type}" in
                        "character-character")
                            echo "  - Suggested types: allied-with, antagonistic-toward, mentors, reports-to, rivals-with, etc." >> "${REPORT_FILE}"
                            ;;
                        "character-timeline")
                            echo "  - Suggested types: participates-in, witnesses, affected-by, causes, prevents, etc." >> "${REPORT_FILE}"
                            ;;
                        # Additional cases would be added here
                    esac
                fi
            fi
        fi
        
        # Validate section placement
        if ! validate_section_placement "$file" "$line_content"; then
            section_violations=$((section_violations + 1))
            echo -e "  ${YELLOW}Section placement violation${NC} (from line $line_num)"
            
            # Add to report
            echo "- **Section placement violation** in $filename:$line_num - Reference not in proper section" >> "${REPORT_FILE}"
        fi
        
        # Check if reference exists in registry
        source_path="${file#$REPO_ROOT/}"
        if ! check_registry_entry "$source_path" "$target_file"; then
            missing_registry=$((missing_registry + 1))
            echo -e "  ${YELLOW}Missing registry entry${NC}: $source_path → $target_file"
            
            # Add to report
            echo "- **Missing registry entry** for reference from \`$source_path\` to \`$target_file\`" >> "${REPORT_FILE}"
        fi
        
    done <<< "$references"
done

# Generate summary section for the report
cat >> "${REPORT_FILE}" << EOF
- **Total files scanned**: $total_files
- **Total references found**: $total_references
- **Broken references**: $broken_references
- **Improper relationship types**: $improper_types
- **Section placement violations**: $section_violations
- **Missing registry entries**: $missing_registry

## Broken References
EOF

# Extract broken references for the report
grep "Broken reference" "${REPORT_FILE}" >> "${REPORT_FILE}.tmp"
if [[ -s "${REPORT_FILE}.tmp" ]]; then
    cat "${REPORT_FILE}.tmp" >> "${REPORT_FILE}"
else
    echo "No broken references found." >> "${REPORT_FILE}"
fi
rm "${REPORT_FILE}.tmp"

# Add improper relationship types section
cat >> "${REPORT_FILE}" << EOF

## Improper Relationship Types
EOF

grep "Improper relationship type" "${REPORT_FILE}" >> "${REPORT_FILE}.tmp"
if [[ -s "${REPORT_FILE}.tmp" ]]; then
    cat "${REPORT_FILE}.tmp" >> "${REPORT_FILE}"
else
    echo "No improper relationship types found." >> "${REPORT_FILE}"
fi
rm "${REPORT_FILE}.tmp"

# Add section placement violations section
cat >> "${REPORT_FILE}" << EOF

## Section Placement Violations
EOF

grep "Section placement violation" "${REPORT_FILE}" >> "${REPORT_FILE}.tmp"
if [[ -s "${REPORT_FILE}.tmp" ]]; then
    cat "${REPORT_FILE}.tmp" >> "${REPORT_FILE}"
else
    echo "No section placement violations found." >> "${REPORT_FILE}"
fi
rm "${REPORT_FILE}.tmp"

# Add missing registry entries section
cat >> "${REPORT_FILE}" << EOF

## Missing Registry Entries
EOF

grep "Missing registry entry" "${REPORT_FILE}" >> "${REPORT_FILE}.tmp"
if [[ -s "${REPORT_FILE}.tmp" ]]; then
    cat "${REPORT_FILE}.tmp" >> "${REPORT_FILE}"
else
    echo "No missing registry entries found." >> "${REPORT_FILE}"
fi
rm "${REPORT_FILE}.tmp"

# Print summary to console
echo
echo -e "${BLUE}=================================${NC}"
echo -e "${BLUE}Reference Validation Summary${NC}"
echo -e "${BLUE}=================================${NC}"
echo -e "Total files scanned:        ${total_files}"
echo -e "Total references found:     ${total_references}"
echo
echo -e "${RED}Broken references:         ${broken_references}${NC}"
echo -e "${YELLOW}Improper relationship types: ${improper_types}${NC}"
echo -e "${YELLOW}Section placement violations: ${section_violations}${NC}"
echo -e "${YELLOW}Missing registry entries:    ${missing_registry}${NC}"
echo
echo -e "Detailed report saved to: ${REPORT_FILE}"

# Add recommendations section to report
cat >> "${REPORT_FILE}" << EOF

## Recommendations

Based on the validation results, the following actions are recommended:

1. **Fix broken references** - Update or remove references to non-existent files or sections
2. **Correct relationship types** - Replace improper relationship types with valid ones from the reference pattern standards
3. **Fix section placement** - Move references to the appropriate sections according to document type
4. **Update reference registry** - Add missing entries to the reference registry

For detailed guidance on reference pattern standards, see:
- [/docs/standards/reference-pattern-standards.md]
- [/docs/standards/bidirectional-reference-system.md]
EOF

chmod +x "$0"
exit 0