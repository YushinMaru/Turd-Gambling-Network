#!/bin/bash
# Line Count Analyzer Tool for Turd Bird Universe
# Edition #1.0.0 | Created: (NEUR-ARC-001) | Last Modified: (NEUR-ARC-001)
#
# This tool analyzes file line counts across the Turd Bird Universe documentation,
# generating reports on files approaching or exceeding the 150-line limit
# to proactively identify refactoring candidates.

# Configuration
ROOT_DIR="/mnt/z/Turdbot/Turd History"
REPORT_DIR="${ROOT_DIR}/systems/reports"
REPORT_FILE="${REPORT_DIR}/line-count-report-$(date +%Y%m%d-%H%M%S).md"
APPROACHING_THRESHOLD=120
EXCEEDING_THRESHOLD=150
FILE_PATTERN="*.md"

# Create report directory if it doesn't exist
mkdir -p "${REPORT_DIR}"

# Function to count lines in a file
count_lines() {
  wc -l "$1" | awk '{print $1}'
}

# Function to classify a file based on line count
classify_file() {
  local file=$1
  local lines=$2
  
  if [ "$lines" -gt "$EXCEEDING_THRESHOLD" ]; then
    echo "EXCEEDING"
  elif [ "$lines" -gt "$APPROACHING_THRESHOLD" ]; then
    echo "APPROACHING"
  else
    echo "ACCEPTABLE"
  fi
}

# Function to generate segmentation recommendations
generate_segmentation_plan() {
  local file=$1
  local lines=$2
  local filename=$(basename "$file")
  local dirname=$(dirname "$file")
  
  # Extract content category from filename (e.g., character, timeline, etc.)
  local category=$(echo "$filename" | cut -d'-' -f1)
  
  # Simple segmentation suggestion based on file type
  case "$category" in
    character)
      echo "- Consider splitting into chronological segments (childhood, education, career phases)"
      echo "- Consider separating attributes (physical, personality, abilities)"
      echo "- Consider isolating quotes, relationships, or special characteristics"
      ;;
    timeline)
      echo "- Consider segmenting by time periods (decades, eras, or critical events)"
      echo "- Consider separating by related character involvement"
      echo "- Consider dividing by location or corporate division"
      ;;
    relationship)
      echo "- Consider dividing by relationship phases or evolution"
      echo "- Consider segmenting by interaction contexts (professional, personal)"
      echo "- Consider splitting by relationship dynamics (conflicts, alliances)"
      ;;
    corporate)
      echo "- Consider separating by department or division"
      echo "- Consider splitting by initiative or project"
      echo "- Consider segmenting by corporate timeline"
      ;;
    *)
      echo "- Consider analyzing content for natural breaking points"
      echo "- Consider identifying distinct topic sections that can be separated"
      echo "- Consider extracting reference sections to dedicated files"
      ;;
  esac
  
  # Calculate ideal segments
  if [ "$lines" -gt "$EXCEEDING_THRESHOLD" ]; then
    local num_segments=$(( ($lines / 100) + 1 ))
    local lines_per_segment=$(( $lines / $num_segments ))
    echo "- Recommendation: Split into approximately $num_segments files of ~$lines_per_segment lines each"
  fi
}

# Function to scan directory and get file line counts
scan_directory() {
  local dir=$1
  local temp_file=$(mktemp)
  
  # Find all markdown files and count their lines
  find "$dir" -type f -name "$FILE_PATTERN" | while read file; do
    lines=$(count_lines "$file")
    classification=$(classify_file "$file" "$lines")
    echo "$lines|$classification|$file" >> "$temp_file"
  done
  
  # Sort files by line count (descending)
  sort -t '|' -k1,1nr "$temp_file"
  
  # Cleanup
  rm "$temp_file"
}

# Generate report header
generate_report_header() {
  cat << EOF > "$REPORT_FILE"
# Line Count Analysis Report
**Generated:** $(date '+%Y-%m-%d %H:%M:%S')
**Analyzed Directory:** $ROOT_DIR
**Configuration:**
- Approaching Threshold: $APPROACHING_THRESHOLD lines
- Exceeding Threshold: $EXCEEDING_THRESHOLD lines

## Summary

EOF
}

# Generate summary statistics
generate_summary() {
  local total_files=0
  local exceeding_files=0
  local approaching_files=0
  local acceptable_files=0
  
  while IFS='|' read -r lines classification file; do
    total_files=$((total_files + 1))
    case "$classification" in
      EXCEEDING)
        exceeding_files=$((exceeding_files + 1))
        ;;
      APPROACHING)
        approaching_files=$((approaching_files + 1))
        ;;
      ACCEPTABLE)
        acceptable_files=$((acceptable_files + 1))
        ;;
    esac
  done
  
  cat << EOF >> "$REPORT_FILE"
- **Total Files Analyzed:** $total_files
- **Files Exceeding Limit (>$EXCEEDING_THRESHOLD lines):** $exceeding_files
- **Files Approaching Limit ($APPROACHING_THRESHOLD-$EXCEEDING_THRESHOLD lines):** $approaching_files
- **Files Within Acceptable Range (<$APPROACHING_THRESHOLD lines):** $acceptable_files

EOF
}

# Generate detailed report
generate_detailed_report() {
  # Add exceeding files section
  cat << EOF >> "$REPORT_FILE"
## Files Exceeding Limit (>$EXCEEDING_THRESHOLD lines)

| File | Line Count | Refactoring Priority |
|------|------------|---------------------|
EOF
  
  while IFS='|' read -r lines classification file; do
    if [ "$classification" = "EXCEEDING" ]; then
      relative_path="${file#$ROOT_DIR/}"
      echo "| $relative_path | $lines | HIGH |" >> "$REPORT_FILE"
    fi
  done
  
  # Add approaching files section
  cat << EOF >> "$REPORT_FILE"

## Files Approaching Limit ($APPROACHING_THRESHOLD-$EXCEEDING_THRESHOLD lines)

| File | Line Count | Refactoring Priority |
|------|------------|---------------------|
EOF
  
  while IFS='|' read -r lines classification file; do
    if [ "$classification" = "APPROACHING" ]; then
      relative_path="${file#$ROOT_DIR/}"
      echo "| $relative_path | $lines | MEDIUM |" >> "$REPORT_FILE"
    fi
  done
}

# Generate recommendations for exceeding files
generate_recommendations() {
  cat << EOF >> "$REPORT_FILE"

## Refactoring Recommendations

EOF
  
  while IFS='|' read -r lines classification file; do
    if [ "$classification" = "EXCEEDING" ]; then
      relative_path="${file#$ROOT_DIR/}"
      cat << EOF >> "$REPORT_FILE"
### $relative_path ($lines lines)

**Suggested Segmentation:**
$(generate_segmentation_plan "$file" "$lines")

EOF
    fi
  done
}

# Main execution flow
echo "Starting Line Count Analysis..."
generate_report_header

# Run scan and collect results
scan_results=$(scan_directory "$ROOT_DIR")

# Generate report sections
echo "$scan_results" | generate_summary
echo "$scan_results" | generate_detailed_report
echo "$scan_results" | generate_recommendations

# Add report documentation
cat << EOF >> "$REPORT_FILE"
## About This Report

This report was automatically generated by the Line Count Analyzer Tool.
The tool scans all markdown files in the Turd Bird Universe documentation
and identifies files that are approaching or exceeding the 150-line limit.

### Usage Instructions

To run the Line Count Analyzer Tool:

1. Open a terminal in the Turd Bird Universe root directory
2. Run \`./systems/line-count-analyzer.sh\`
3. Review the generated report in \`systems/reports/\`

The tool can be configured by editing the thresholds at the top of the script.

### Scheduled Execution

This tool can be configured to run on a schedule using cron:

1. Add the following line to your crontab to run daily at midnight:
   \`0 0 * * * /mnt/z/Turdbot/Turd History/systems/line-count-analyzer.sh\`

2. For weekly scanning, add:
   \`0 0 * * 0 /mnt/z/Turdbot/Turd History/systems/line-count-analyzer.sh\`

3. For monthly scanning, add:
   \`0 0 1 * * /mnt/z/Turdbot/Turd History/systems/line-count-analyzer.sh\`
EOF

# Make script executable
chmod +x "${ROOT_DIR}/systems/line-count-analyzer.sh"

echo "Analysis complete! Report generated at: $REPORT_FILE"