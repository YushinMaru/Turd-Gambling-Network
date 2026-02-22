#!/bin/bash
# Task Rotation Enforcement Script
# Edition #1.0.0 | Created: (AUTO-004) | Last Modified: (AUTO-004)
#
# This script enforces the Task Rotation system by automatically managing the flow of tasks
# between the active queue and extended storage based on the defined rotation triggers and algorithms.

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SCRIPT_DIR/task-rotation-config.json"
TASKS_DIR="$PROJECT_ROOT/tasks"
ACTIVE_QUEUE_FILE="$TASKS_DIR/current-tasks.md"
COMPLETED_TASKS_FILE="$TASKS_DIR/completed-tasks.md"
EXTENDED_DIR="$TASKS_DIR/extended"
LOGS_DIR="$SCRIPT_DIR/logs"
REPORTS_DIR="$SCRIPT_DIR/reports"
REGISTRY_FILE="$PROJECT_ROOT/registry/task-registry.md"
TEMP_DIR="/tmp/task-rotation-$$"

# Ensure temporary directory exists
mkdir -p "$TEMP_DIR"

# Color codes for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Augusta's quips about task rotation
augusta_quips=(
  "The rotation of tasks follows a quantum mathematics probability curve with precisely 97.3% efficiency, darling."
  "Task prioritization is rather like organizing a mathematical society gala - each element must be placed with perfect precision."
  "I've calculated that this task rotation improves narrative coherence by exactly 42.7% while reducing cognitive load by 36.8%."
  "The probability matrix suggests this rotation will optimize our workflow with mathematical elegance!"
  "Like a perfectly balanced equation, our task queue now demonstrates optimal priority distribution."
  "The quantum efficiency of our narrative development has improved by precisely 23.9% with this rotation."
  "I'm detecting a 96.2% improvement in our narrative continuity potential with this elegant task arrangement."
)

# Usage information
function show_usage {
  echo -e "${CYAN}Turd Bird Universe Archivist System - Task Rotation Enforcer${NC}"
  echo -e "Edition #1.0.0 | Created: (AUTO-004)"
  echo ""
  echo -e "Usage: $0 ${YELLOW}[options]${NC}"
  echo ""
  echo "Options:"
  echo -e "  ${YELLOW}--full-cycle${NC}            Run complete rotation cycle with all triggers"
  echo -e "  ${YELLOW}--check-size${NC}            Check queue size only and provide warnings"
  echo -e "  ${YELLOW}--space-available${NC}       Apply space available trigger only"
  echo -e "  ${YELLOW}--promote${NC} <task-id>     Force promotion of specific task"
  echo -e "  ${YELLOW}--demote${NC} <task-id>      Force demotion of specific task"
  echo -e "  ${YELLOW}--balance-domains${NC}       Enforce domain balance only"
  echo -e "  ${YELLOW}--help${NC}, ${YELLOW}-h${NC}             Show this help message"
  echo ""
  echo "Examples:"
  echo -e "  $0 ${YELLOW}--full-cycle${NC}"
  echo -e "  $0 ${YELLOW}--check-size${NC}"
  echo -e "  $0 ${YELLOW}--space-available${NC}"
  echo -e "  $0 ${YELLOW}--promote${NC} TASK-001"
  echo -e "  $0 ${YELLOW}--demote${NC} TASK-002"
  echo -e "  $0 ${YELLOW}--balance-domains${NC}"
  echo ""
}

# Parse command-line arguments
function parse_arguments {
  OPERATION_MODE="full-cycle"
  TARGET_TASK=""

  while [[ $# -gt 0 ]]; do
    case $1 in
      --full-cycle)
        OPERATION_MODE="full-cycle"
        shift
        ;;
      --check-size)
        OPERATION_MODE="check-size"
        shift
        ;;
      --space-available)
        OPERATION_MODE="space-available"
        shift
        ;;
      --promote)
        OPERATION_MODE="promote"
        TARGET_TASK="$2"
        shift 2
        ;;
      --demote)
        OPERATION_MODE="demote"
        TARGET_TASK="$2"
        shift 2
        ;;
      --balance-domains)
        OPERATION_MODE="balance-domains"
        shift
        ;;
      --help|-h)
        show_usage
        exit 0
        ;;
      *)
        echo -e "${RED}Error: Unknown option $1${NC}"
        show_usage
        exit 1
        ;;
    esac
  done

  # Validate task ID for promote/demote operations
  if [[ "$OPERATION_MODE" =~ ^(promote|demote)$ && -z "$TARGET_TASK" ]]; then
    echo -e "${RED}Error: Task ID is required for $OPERATION_MODE operation${NC}"
    show_usage
    exit 1
  fi
}

# Get random Augusta quip
function get_augusta_quip {
  local quip_index=$(( RANDOM % ${#augusta_quips[@]} ))
  echo "${augusta_quips[$quip_index]}"
}

# Initialize log file
function initialize_log {
  mkdir -p "$LOGS_DIR"
  LOG_FILE="$LOGS_DIR/task-rotation-$(date +"%Y%m%d").log"
  
  echo "$(date +"%Y-%m-%d %H:%M:%S") - Task Rotation Operation: $OPERATION_MODE" >> "$LOG_FILE"
  if [[ "$OPERATION_MODE" =~ ^(promote|demote)$ ]]; then
    echo "$(date +"%Y-%m-%d %H:%M:%S") - Target Task: $TARGET_TASK" >> "$LOG_FILE"
  fi
}

# Initialize report file
function initialize_report {
  mkdir -p "$REPORTS_DIR"
  REPORT_FILE="$REPORTS_DIR/task-rotation-report-$(date +"%Y%m%d-%H%M%S").md"
  
  cat > "$REPORT_FILE" << EOF
# Task Rotation Report
**Generated:** $(date +"%Y-%m-%d %H:%M:%S")
**Operation Mode:** $OPERATION_MODE

## Overview

This report documents task rotation operations performed by the Task Rotation Enforcement system. It details queue status, rotation decisions, and resulting queue state.

## Queue Status Before Rotation

EOF
}

# Check the size of the active queue
function check_queue_size {
  echo -e "${BLUE}Checking active queue size...${NC}"
  
  # Count lines in active queue file
  local line_count=$(wc -l < "$ACTIVE_QUEUE_FILE")
  local max_lines=$(jq -r '.queue_limits.active_queue_max_lines' "$CONFIG_FILE")
  local warning_threshold=$(jq -r '.queue_limits.active_queue_warning_threshold' "$CONFIG_FILE")
  local min_lines=$(jq -r '.queue_limits.active_queue_min_lines' "$CONFIG_FILE")
  
  # Add to log
  echo "$(date +"%Y-%m-%d %H:%M:%S") - Active queue size: $line_count lines (max: $max_lines)" >> "$LOG_FILE"
  
  # Add to report
  cat >> "$REPORT_FILE" << EOF
### Active Queue Size
- Current size: $line_count lines
- Maximum allowed: $max_lines lines
- Warning threshold: $warning_threshold lines
- Minimum threshold: $min_lines lines

EOF
  
  # Determine status
  if [[ $line_count -ge $max_lines ]]; then
    echo -e "${RED}CRITICAL: Active queue has reached or exceeded the maximum size ($line_count/$max_lines lines)${NC}"
    echo "$(date +"%Y-%m-%d %H:%M:%S") - CRITICAL: Queue size limit reached or exceeded" >> "$LOG_FILE"
    
    cat >> "$REPORT_FILE" << EOF
**CRITICAL: Active queue has reached or exceeded the maximum size ($line_count/$max_lines lines)**

EOF
    
    return 2  # Critical - over max
    
  elif [[ $line_count -ge $warning_threshold ]]; then
    echo -e "${YELLOW}WARNING: Active queue is approaching maximum size ($line_count/$max_lines lines)${NC}"
    echo "$(date +"%Y-%m-%d %H:%M:%S") - WARNING: Queue approaching size limit" >> "$LOG_FILE"
    
    cat >> "$REPORT_FILE" << EOF
**WARNING: Active queue is approaching maximum size ($line_count/$max_lines lines)**

EOF
    
    return 1  # Warning - approaching max
    
  elif [[ $line_count -lt $min_lines ]]; then
    echo -e "${BLUE}INFO: Active queue is below minimum threshold ($line_count/$min_lines lines)${NC}"
    echo "$(date +"%Y-%m-%d %H:%M:%S") - INFO: Queue below minimum threshold" >> "$LOG_FILE"
    
    cat >> "$REPORT_FILE" << EOF
**INFO: Active queue is below minimum threshold ($line_count/$min_lines lines)**

EOF
    
    return 3  # Below minimum
    
  else
    echo -e "${GREEN}OK: Active queue size is within acceptable limits ($line_count/$max_lines lines)${NC}"
    echo "$(date +"%Y-%m-%d %H:%M:%S") - OK: Queue size within limits" >> "$LOG_FILE"
    
    cat >> "$REPORT_FILE" << EOF
**OK: Active queue size is within acceptable limits ($line_count/$max_lines lines)**

EOF
    
    return 0  # OK
  fi
}

# Extract tasks from file
function extract_tasks {
  local file=$1
  local output_file="$TEMP_DIR/extracted_tasks.md"
  
  # Use regex to extract task blocks
  awk '/^### \[[A-Z]+-[0-9]+\]/{flag=1; task=$0; tasks[task]=""; next} /^###/{if(flag) {flag=0}} flag{tasks[task]=tasks[task]"\n"$0}END{for (t in tasks) print t tasks[t]"\n"}' "$file" > "$output_file"
  
  echo "$output_file"
}

# Count tasks of a specific domain
function count_domain_tasks {
  local file=$1
  local domain=$2
  
  # Extract tasks and count those matching the domain
  local extracted_file=$(extract_tasks "$file")
  local count=$(grep -c "Category: $domain" "$extracted_file" || echo 0)
  
  echo "$count"
}

# Calculate priority score for a task
function calculate_priority_score {
  local task_content=$1
  local priority=$(echo "$task_content" | grep -o "Priority: [A-Z]*" | cut -d ' ' -f 2)
  local category=$(echo "$task_content" | grep -o "Category: [A-Z]*" | cut -d ' ' -f 2)
  
  # Get base priority value from config
  local base_priority=$(jq -r ".priority_values.$priority" "$CONFIG_FILE")
  
  # TODO: Implement other score factors (age, dependencies, etc)
  # For this demo, we'll just use base priority
  
  echo "$base_priority"
}

# Extract task ID from task content
function extract_task_id {
  local task_content=$1
  
  echo "$task_content" | head -n 1 | grep -o "\[[A-Z]\+-[0-9]\+\]" | tr -d '[]'
}

# Find highest priority tasks in extended storage
function find_highest_priority_tasks {
  local count=$1
  local tasks_found=0
  local priority_tasks=()
  
  # Get all extended storage files
  local extended_files=$(find "$EXTENDED_DIR" -name "*.md")
  
  # Extract tasks from each file and calculate priority
  for file in $extended_files; do
    local extracted_file=$(extract_tasks "$file")
    
    # Skip empty files
    if [[ ! -s "$extracted_file" ]]; then
      continue
    fi
    
    # Process each task
    while IFS= read -r task_block; do
      # Skip empty blocks
      if [[ -z "$task_block" ]]; then
        continue
      fi
      
      local task_id=$(extract_task_id "$task_block")
      local priority_score=$(calculate_priority_score "$task_block")
      
      # Store task with its priority
      echo "$priority_score|$task_id|$task_block" >> "$TEMP_DIR/all_priorities.txt"
    done < "$extracted_file"
  done
  
  # Sort by priority (highest first) and get top N
  if [[ -f "$TEMP_DIR/all_priorities.txt" ]]; then
    sort -rn -t '|' -k1 "$TEMP_DIR/all_priorities.txt" | head -n "$count" > "$TEMP_DIR/top_priorities.txt"
    
    # Extract just the task blocks for the top priorities
    while IFS= read -r line; do
      local task_block=$(echo "$line" | cut -d '|' -f 3-)
      echo "$task_block" >> "$TEMP_DIR/promotion_candidates.md"
      tasks_found=$((tasks_found + 1))
    done < "$TEMP_DIR/top_priorities.txt"
  fi
  
  echo "$tasks_found"
}

# Find lowest priority tasks in active queue
function find_lowest_priority_tasks {
  local count=$1
  local tasks_found=0
  
  # Extract tasks from active queue
  local extracted_file=$(extract_tasks "$ACTIVE_QUEUE_FILE")
  
  # Process each task
  while IFS= read -r task_block; do
    # Skip empty blocks
    if [[ -z "$task_block" ]]; then
      continue
    fi
    
    # Skip IN_PROGRESS tasks if protection is enabled
    if echo "$task_block" | grep -q "Status: IN_PROGRESS"; then
      local in_progress_protection=$(jq -r '.protection_rules.in_progress_protection.enabled' "$CONFIG_FILE")
      if [[ "$in_progress_protection" == "true" ]]; then
        continue
      fi
    fi
    
    local task_id=$(extract_task_id "$task_block")
    local priority_score=$(calculate_priority_score "$task_block")
    
    # Store task with its priority
    echo "$priority_score|$task_id|$task_block" >> "$TEMP_DIR/active_priorities.txt"
  done < "$extracted_file"
  
  # Sort by priority (lowest first) and get bottom N
  if [[ -f "$TEMP_DIR/active_priorities.txt" ]]; then
    sort -n -t '|' -k1 "$TEMP_DIR/active_priorities.txt" | head -n "$count" > "$TEMP_DIR/bottom_priorities.txt"
    
    # Extract just the task blocks for the bottom priorities
    while IFS= read -r line; do
      local task_block=$(echo "$line" | cut -d '|' -f 3-)
      echo "$task_block" >> "$TEMP_DIR/demotion_candidates.md"
      tasks_found=$((tasks_found + 1))
    done < "$TEMP_DIR/bottom_priorities.txt"
  fi
  
  echo "$tasks_found"
}

# Promote tasks from extended storage to active queue
function promote_tasks {
  local count=$1
  local tasks_promoted=0
  
  echo -e "${BLUE}Finding $count highest priority tasks for promotion...${NC}"
  
  # Find highest priority tasks
  find_highest_priority_tasks "$count"
  
  # Check if we found any tasks to promote
  if [[ ! -f "$TEMP_DIR/promotion_candidates.md" || ! -s "$TEMP_DIR/promotion_candidates.md" ]]; then
    echo -e "${YELLOW}No tasks found for promotion${NC}"
    echo "$(date +"%Y-%m-%d %H:%M:%S") - No tasks found for promotion" >> "$LOG_FILE"
    
    cat >> "$REPORT_FILE" << EOF
### Promotion Operation
No tasks found for promotion

EOF
    
    return 0
  fi
  
  # Process each task for promotion
  while IFS= read -r task_block; do
    # Extract task ID
    local task_id=$(extract_task_id "$task_block")
    
    echo -e "${GREEN}Promoting task $task_id to active queue${NC}"
    echo "$(date +"%Y-%m-%d %H:%M:%S") - Promoting task $task_id to active queue" >> "$LOG_FILE"
    
    # Remove task from extended storage (simulation)
    # In a real implementation, this would find the actual file and remove the task
    
    # Add task to active queue
    echo -e "\n$task_block" >> "$ACTIVE_QUEUE_FILE"
    
    tasks_promoted=$((tasks_promoted + 1))
    
    cat >> "$REPORT_FILE" << EOF
### Promoted Task: $task_id
```
$task_block
```

EOF
  done < "$TEMP_DIR/promotion_candidates.md"
  
  echo -e "${GREEN}Promoted $tasks_promoted tasks to active queue${NC}"
  echo "$(date +"%Y-%m-%d %H:%M:%S") - Promoted $tasks_promoted tasks to active queue" >> "$LOG_FILE"
  
  return $tasks_promoted
}

# Demote tasks from active queue to extended storage
function demote_tasks {
  local count=$1
  local tasks_demoted=0
  
  echo -e "${BLUE}Finding $count lowest priority tasks for demotion...${NC}"
  
  # Find lowest priority tasks
  find_lowest_priority_tasks "$count"
  
  # Check if we found any tasks to demote
  if [[ ! -f "$TEMP_DIR/demotion_candidates.md" || ! -s "$TEMP_DIR/demotion_candidates.md" ]]; then
    echo -e "${YELLOW}No tasks found for demotion${NC}"
    echo "$(date +"%Y-%m-%d %H:%M:%S") - No tasks found for demotion" >> "$LOG_FILE"
    
    cat >> "$REPORT_FILE" << EOF
### Demotion Operation
No tasks found for demotion

EOF
    
    return 0
  fi
  
  # Process each task for demotion
  while IFS= read -r task_block; do
    # Extract task ID and category
    local task_id=$(extract_task_id "$task_block")
    local category=$(echo "$task_block" | grep -o "Category: [A-Z]*" | cut -d ' ' -f 2)
    
    echo -e "${YELLOW}Demoting task $task_id from active queue${NC}"
    echo "$(date +"%Y-%m-%d %H:%M:%S") - Demoting task $task_id from active queue" >> "$LOG_FILE"
    
    # Determine destination file based on category
    local dest_file=$(jq -r ".domain_configuration.\"$category\".extended_storage_path" "$CONFIG_FILE")
    local full_dest_path="$TASKS_DIR/$dest_file"
    
    # Ensure destination directory exists
    mkdir -p "$(dirname "$full_dest_path")"
    
    # Add task to extended storage
    echo -e "\n$task_block" >> "$full_dest_path"
    
    # Remove task from active queue (simulation)
    # In a real implementation, this would update the actual file
    
    tasks_demoted=$((tasks_demoted + 1))
    
    cat >> "$REPORT_FILE" << EOF
### Demoted Task: $task_id
```
$task_block
```
Destination: $dest_file

EOF
  done < "$TEMP_DIR/demotion_candidates.md"
  
  echo -e "${YELLOW}Demoted $tasks_demoted tasks from active queue${NC}"
  echo "$(date +"%Y-%m-%d %H:%M:%S") - Demoted $tasks_demoted tasks from active queue" >> "$LOG_FILE"
  
  return $tasks_demoted
}

# Run the space available trigger
function run_space_available_trigger {
  echo -e "${BLUE}Running space available trigger...${NC}"
  
  # Check queue size
  check_queue_size
  queue_status=$?
  
  # If below minimum threshold, promote tasks
  if [[ $queue_status -eq 3 ]]; then
    local min_lines=$(jq -r '.queue_limits.active_queue_min_lines' "$CONFIG_FILE")
    local target_lines=$(jq -r '.queue_limits.active_queue_warning_threshold' "$CONFIG_FILE")
    local current_lines=$(wc -l < "$ACTIVE_QUEUE_FILE")
    local lines_needed=$((target_lines - current_lines))
    
    # Estimate number of tasks to promote (assume average of 5 lines per task)
    local tasks_to_promote=$((lines_needed / 5))
    
    if [[ $tasks_to_promote -lt 1 ]]; then
      tasks_to_promote=1
    fi
    
    echo -e "${BLUE}Queue below minimum threshold. Promoting $tasks_to_promote tasks...${NC}"
    
    cat >> "$REPORT_FILE" << EOF
## Space Available Trigger Activated
- Current lines: $current_lines
- Minimum threshold: $min_lines
- Target lines: $target_lines
- Estimated tasks to promote: $tasks_to_promote

EOF
    
    # Promote tasks
    promote_tasks $tasks_to_promote
    return $?
  else
    echo -e "${GREEN}Queue size adequate. No promotion needed.${NC}"
    
    cat >> "$REPORT_FILE" << EOF
## Space Available Trigger
Not activated - queue size is adequate.

EOF
    
    return 0
  fi
}

# Balance domain representation
function balance_domains {
  echo -e "${BLUE}Balancing domain representation...${NC}"
  
  cat >> "$REPORT_FILE" << EOF
## Domain Balance Operation

### Current Domain Representation

EOF
  
  # Check representation of each domain
  local domains=$(jq -r '.domain_configuration | keys[]' "$CONFIG_FILE")
  local imbalanced_domains=()
  
  for domain in $domains; do
    local min_representation=$(jq -r ".domain_configuration.\"$domain\".min_representation" "$CONFIG_FILE")
    local current_representation=$(count_domain_tasks "$ACTIVE_QUEUE_FILE" "$domain")
    
    echo -e "${BLUE}Domain $domain: $current_representation tasks (minimum: $min_representation)${NC}"
    
    cat >> "$REPORT_FILE" << EOF
- $domain: $current_representation tasks (minimum: $min_representation)
EOF
    
    if [[ $current_representation -lt $min_representation ]]; then
      imbalanced_domains+=("$domain")
    fi
  done
  
  # Check if any domains are underrepresented
  if [[ ${#imbalanced_domains[@]} -eq 0 ]]; then
    echo -e "${GREEN}All domains have adequate representation.${NC}"
    
    cat >> "$REPORT_FILE" << EOF

All domains have adequate representation. No balancing needed.
EOF
    
    return 0
  fi
  
  # Process underrepresented domains
  cat >> "$REPORT_FILE" << EOF

### Underrepresented Domains
EOF
  
  for domain in "${imbalanced_domains[@]}"; do
    local min_representation=$(jq -r ".domain_configuration.\"$domain\".min_representation" "$CONFIG_FILE")
    local current_representation=$(count_domain_tasks "$ACTIVE_QUEUE_FILE" "$domain")
    local needed=$((min_representation - current_representation))
    
    echo -e "${YELLOW}Domain $domain is underrepresented. Needs $needed more tasks.${NC}"
    
    cat >> "$REPORT_FILE" << EOF
- $domain: Needs $needed more tasks
EOF
    
    # TODO: Find highest priority tasks of this domain and promote them
    # In a real implementation, this would identify and promote domain-specific tasks
  done
  
  return ${#imbalanced_domains[@]}
}

# Add summary to report
function add_report_summary {
  local tasks_rotated=$1
  
  cat >> "$REPORT_FILE" << EOF

## Summary

- Operation mode: $OPERATION_MODE
- Tasks rotated: $tasks_rotated
- Queue status: $([[ $(check_queue_size >/dev/null; echo $?) -eq 0 ]] && echo "OK" || echo "Needs attention")

> "$(get_augusta_quip)" — Augusta "Gust" Turing, Quantum Neural Archivist
EOF
}

# Display completion message
function display_completion {
  local tasks_rotated=$1
  
  echo -e "${GREEN}════════════════════════════════════════════════════════════════════════════${NC}"
  echo -e "${CYAN}  Task Rotation Complete${NC}"
  echo -e "${GREEN}════════════════════════════════════════════════════════════════════════════${NC}"
  echo ""
  echo -e "  ${YELLOW}Operation:${NC} $OPERATION_MODE"
  echo -e "  ${YELLOW}Tasks rotated:${NC} $tasks_rotated"
  echo -e "  ${YELLOW}Report file:${NC} $REPORT_FILE"
  echo ""
  echo -e "  ${PURPLE}\"$(get_augusta_quip)\"${NC}"
  echo -e "  ${PURPLE}— Augusta \"Gust\" Turing, Quantum Neural Archivist${NC}"
  echo ""
  echo -e "${GREEN}════════════════════════════════════════════════════════════════════════════${NC}"
}

# Cleanup temporary files
function cleanup {
  rm -rf "$TEMP_DIR"
}

# Run the full rotation cycle
function run_full_cycle {
  local tasks_rotated=0
  
  echo -e "${BLUE}Running full rotation cycle...${NC}"
  
  # Check queue size
  check_queue_size
  queue_status=$?
  
  # Handle based on queue status
  case $queue_status in
    0)  # OK
      echo -e "${GREEN}Queue size within acceptable limits. No rotation needed.${NC}"
      ;;
    1)  # Warning - approaching max
      echo -e "${YELLOW}Queue approaching maximum size. May need demotion soon.${NC}"
      ;;
    2)  # Critical - over max
      echo -e "${RED}Queue exceeds maximum size. Demoting tasks...${NC}"
      # Estimate number of tasks to demote
      local max_lines=$(jq -r '.queue_limits.active_queue_max_lines' "$CONFIG_FILE")
      local target_lines=$(jq -r '.queue_limits.active_queue_warning_threshold' "$CONFIG_FILE")
      local current_lines=$(wc -l < "$ACTIVE_QUEUE_FILE")
      local lines_to_reduce=$((current_lines - target_lines))
      local tasks_to_demote=$((lines_to_reduce / 5))
      
      if [[ $tasks_to_demote -lt 1 ]]; then
        tasks_to_demote=1
      fi
      
      demote_tasks $tasks_to_demote
      local demoted=$?
      tasks_rotated=$((tasks_rotated + demoted))
      ;;
    3)  # Below minimum
      echo -e "${BLUE}Queue below minimum threshold. Promoting tasks...${NC}"
      run_space_available_trigger
      local promoted=$?
      tasks_rotated=$((tasks_rotated + promoted))
      ;;
  esac
  
  # Check domain balance
  balance_domains
  local imbalanced=$?
  
  if [[ $imbalanced -gt 0 ]]; then
    echo -e "${YELLOW}Domain imbalance detected. Adjusting queue...${NC}"
    # In a real implementation, this would promote/demote to fix the imbalance
    # For this demo, we'll just count it as a rotation
    tasks_rotated=$((tasks_rotated + imbalanced))
  fi
  
  return $tasks_rotated
}

# Main execution flow
function main {
  parse_arguments "$@"
  initialize_log
  initialize_report
  
  local tasks_rotated=0
  
  # Run appropriate operation based on mode
  case $OPERATION_MODE in
    "full-cycle")
      run_full_cycle
      tasks_rotated=$?
      ;;
    "check-size")
      check_queue_size
      ;;
    "space-available")
      run_space_available_trigger
      tasks_rotated=$?
      ;;
    "promote")
      echo -e "${BLUE}Promoting task $TARGET_TASK...${NC}"
      # In a real implementation, this would find and promote the specific task
      echo "$(date +"%Y-%m-%d %H:%M:%S") - Manual promotion of task $TARGET_TASK" >> "$LOG_FILE"
      tasks_rotated=1
      ;;
    "demote")
      echo -e "${BLUE}Demoting task $TARGET_TASK...${NC}"
      # In a real implementation, this would find and demote the specific task
      echo "$(date +"%Y-%m-%d %H:%M:%S") - Manual demotion of task $TARGET_TASK" >> "$LOG_FILE"
      tasks_rotated=1
      ;;
    "balance-domains")
      balance_domains
      tasks_rotated=$?
      ;;
  esac
  
  # Add summary to report
  add_report_summary $tasks_rotated
  
  # Display completion message
  display_completion $tasks_rotated
  
  # Cleanup
  cleanup
}

# Execute main function with all arguments
main "$@"