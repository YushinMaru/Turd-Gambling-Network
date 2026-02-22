#!/bin/bash
# GitHub Push Script for Turd Bird Universe
# Author: NEUR-ARC-001
# Version: 1.1.0
# Created: 2025-05-06
# Modified: 2025-05-07 by NEUR-ARC-011

# CRITICAL: This script ONLY pushes files in the Turd History folder
# NEVER push changes to TurdAI or any other folder outside Turd History

# Define base paths and variables
BASE_DIR="/mnt/z/Turdbot/Turd History"
LOG_FILE="${BASE_DIR}/systems/github-push.log"
DATE=$(date +"%Y-%m-%d %H:%M:%S")
COMMIT_PREFIX="TURD-AUTO"
BRANCH=$(git -C "$BASE_DIR" rev-parse --abbrev-ref HEAD)

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to log messages
log_message() {
    echo "[$DATE] $1" >> "$LOG_FILE"
    echo -e "$1"
}

# Function to check git status
check_git_status() {
    log_message "${BLUE}Checking git status...${NC}"
    
    # Check if we're in a git repository
    if ! git -C "$BASE_DIR" rev-parse --is-inside-work-tree &>/dev/null; then
        log_message "${RED}Error: Not in a git repository.${NC}"
        return 1
    fi
    
    # Check if there are any changes to commit
    if git -C "$BASE_DIR" diff --quiet && git -C "$BASE_DIR" diff --staged --quiet; then
        log_message "${YELLOW}No changes to commit.${NC}"
        return 2
    fi
    
    return 0
}

# Function to get list of changed files
get_changed_files() {
    git -C "$BASE_DIR" status --porcelain | sed 's/^...//'
}

# Function to get list of completed tasks since last push
get_completed_tasks() {
    # This simple implementation checks the recent entries in completed-tasks.md
    grep -A 10 "###" "$BASE_DIR/tasks/completed-tasks.md" | grep "\[" | head -3
}

# Function to create commit message
create_commit_message() {
    local changed_files=$(get_changed_files)
    local completed_tasks=$(get_completed_tasks)
    local file_count=$(echo "$changed_files" | wc -l)
    
    # Create the commit message
    echo "${COMMIT_PREFIX}: Update ${file_count} files on $(date +"%Y-%m-%d")" > /tmp/commit_msg.txt
    echo "" >> /tmp/commit_msg.txt
    echo "Recently completed tasks:" >> /tmp/commit_msg.txt
    echo "$completed_tasks" >> /tmp/commit_msg.txt
    echo "" >> /tmp/commit_msg.txt
    echo "IMPORTANT: This commit affects ONLY files in the Turd History folder." >> /tmp/commit_msg.txt
    echo "" >> /tmp/commit_msg.txt
    echo "Changed files:" >> /tmp/commit_msg.txt
    echo "$changed_files" | sort | head -10 >> /tmp/commit_msg.txt
    
    # If there are more than 10 changed files, add a note
    if [ "$file_count" -gt 10 ]; then
        echo "... and $(($file_count - 10)) more files" >> /tmp/commit_msg.txt
    fi
    
    cat /tmp/commit_msg.txt
}

# Function to check for changes outside Turd History
check_outside_changes() {
    log_message "${BLUE}Checking for changes outside Turd History folder...${NC}"
    
    # Check if there are any changes outside of Turd History
    if git status --porcelain | grep -v "^??" | grep -q "^.* \.\./"; then
        log_message "${RED}ERROR: Changes detected outside of Turd History folder.${NC}"
        log_message "${RED}Affected files:${NC}"
        git status --porcelain | grep -v "^??" | grep "^.* \.\./.*"
        return 1
    fi
    
    log_message "${GREEN}No changes outside Turd History folder detected.${NC}"
    return 0
}

# Function to stage changes
stage_changes() {
    log_message "${BLUE}Staging changes...${NC}"
    
    # Check for changes outside Turd History
    check_outside_changes || {
        log_message "${RED}Aborting: Changes outside Turd History folder detected.${NC}"
        return 1
    }
    
    # Stage all changes
    if git -C "$BASE_DIR" add .; then
        log_message "${GREEN}Changes staged successfully.${NC}"
        return 0
    else
        log_message "${RED}Error staging changes.${NC}"
        return 1
    fi
}

# Function to commit changes
commit_changes() {
    log_message "${BLUE}Committing changes...${NC}"
    
    # Create commit message
    create_commit_message
    
    # Commit changes
    if git -C "$BASE_DIR" commit -F /tmp/commit_msg.txt; then
        log_message "${GREEN}Changes committed successfully.${NC}"
        return 0
    else
        log_message "${RED}Error committing changes.${NC}"
        return 1
    fi
}

# Function to push changes
push_changes() {
    log_message "${BLUE}Pushing changes to remote repository...${NC}"
    
    # Push changes
    if git -C "$BASE_DIR" push origin "$BRANCH"; then
        log_message "${GREEN}Changes pushed successfully.${NC}"
        return 0
    else
        log_message "${RED}Error pushing changes.${NC}"
        return 1
    fi
}

# Main function
main() {
    log_message "${CYAN}=== Starting GitHub Push Operation (${DATE}) ===${NC}"
    
    # Change to base directory
    cd "$BASE_DIR" || {
        log_message "${RED}Error: Could not change to base directory.${NC}"
        return 1
    }
    
    # Check git status
    check_git_status
    status=$?
    
    if [ $status -eq 1 ]; then
        log_message "${RED}Aborting push due to repository issues.${NC}"
        return 1
    elif [ $status -eq 2 ]; then
        log_message "${YELLOW}No changes to push. Operation completed.${NC}"
        return 0
    fi
    
    # Stage changes
    stage_changes || return 1
    
    # Commit changes
    commit_changes || return 1
    
    # Push changes
    push_changes || return 1
    
    log_message "${CYAN}=== GitHub Push Operation Completed Successfully ===${NC}"
    return 0
}

# Execute main function
main "$@"
exit $?