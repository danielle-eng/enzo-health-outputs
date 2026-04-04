#!/bin/bash

################################################################################
# ENZO HEALTH: Agent Pipeline Orchestrator
################################################################################
#
# Description:
#   Orchestrates the complete Enzo Health agent pipeline in the correct order.
#   Handles data ingestion, quality flagging, risk modeling, and reporting.
#
# Usage:
#   ./run_agent_workflow.sh [OPTIONS]
#
# Options:
#   --agency-id AGENCY_ID     Agency identifier (e.g., SUNRISE, MAVERICK)
#   --quarter QUARTER         Quarter code (e.g., Q1, Q2, Q3, Q4)
#   --year YEAR              Year (e.g., 2026)
#   --dry-run                Skip git operations (for testing)
#   --verbose                Enable verbose output
#   --help                   Show this help message
#
# Environment Variables:
#   ENZO_DATA_DIR            Base data directory (default: ./data)
#   ENZO_LOG_DIR             Log directory (default: ./logs)
#   ENZO_GITHUB_TOKEN        GitHub authentication token
#   ENZO_SLACK_WEBHOOK       Slack webhook for notifications
#
# Exit Codes:
#   0 - All steps completed successfully
#   1 - One or more steps failed (see run_history.json for details)
#
################################################################################

set -o pipefail  # Pipe failure causes script to fail

# Default configuration
AGENCY_ID=""
QUARTER=""
YEAR=""
DRY_RUN=false
VERBOSE=false
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DATA_DIR="${ENZO_DATA_DIR:-$PROJECT_ROOT/data}"
LOG_DIR="${ENZO_LOG_DIR:-$PROJECT_ROOT/logs}"
OUTCOMES_DIR="$DATA_DIR/outcomes"

# Ensure directories exist
mkdir -p "$LOG_DIR" "$OUTCOMES_DIR" "$DATA_DIR/cache"

# Log file setup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/agent_workflow_${TIMESTAMP}.log"
RUN_HISTORY_FILE="$DATA_DIR/run_history.json"

# Color codes for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'  # No Color

################################################################################
# UTILITY FUNCTIONS
################################################################################

log_info() {
    echo -e "${BLUE}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $*" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $*" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $*" | tee -a "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $*" | tee -a "$LOG_FILE"
}

verbose_log() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${BLUE}[VERBOSE]${NC} $*" | tee -a "$LOG_FILE"
    fi
}

show_help() {
    sed -n '/^################################################################################/,/^################################################################################/{
        /^################################################################################/d
        /^# /p
    }' "$0" | sed 's/^# //'
}

print_divider() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG_FILE"
}

################################################################################
# STEP TRACKING
################################################################################

# Initialize results tracking
declare -A STEP_RESULTS
declare -A STEP_ERRORS
declare -a STEP_ORDER=(
    "pull_latest_data"
    "intake_screening"
    "oasis_qa_check"
    "pdgm_billing_review"
    "scheduling_compliance"
    "recert_discharge_eval"
    "aggregate_quarterly_data"
    "flag_high_risk_patients"
    "hhvbp_model"
    "star_rating_estimator"
    "git_push_outputs"
    "log_completion"
)

run_step() {
    local step_name="$1"
    local step_description="$2"
    local step_command="$3"

    print_divider
    log_info "Step: $step_description"
    verbose_log "Command: $step_command"

    STEP_RESULTS[$step_name]="running"
    START_TIME=$(date +%s)

    # Execute the step, capturing stdout/stderr
    if output=$(eval "$step_command" 2>&1); then
        STEP_RESULTS[$step_name]="success"
        log_success "$step_description completed"
        verbose_log "Output: $output"
        return 0
    else
        local exit_code=$?
        STEP_RESULTS[$step_name]="failed"
        STEP_ERRORS[$step_name]="$output (exit code: $exit_code)"
        log_error "$step_description failed with exit code $exit_code"
        verbose_log "Error output: $output"
        return 1
    fi
}

################################################################################
# PIPELINE STEPS
################################################################################

step_pull_latest_data() {
    log_info "Pulling latest data from APIs..."

    if [[ ! -f "$DATA_DIR/.env" ]]; then
        log_warn "Skipping API data pull: .env file not found (API credentials may not be configured)"
        return 0
    fi

    # Source environment for API credentials
    # shellcheck source=/dev/null
    source "$DATA_DIR/.env"

    if [[ -z "$ENZO_SCRIBE_BASE_URL" ]]; then
        log_warn "ENZO_SCRIBE_BASE_URL not set - skipping Scribe API pull"
    else
        log_info "Pulling from Scribe API: $ENZO_SCRIBE_BASE_URL"
        # Example: python "$DATA_DIR/scripts/scribe_connector.py" \
        #     --agency-id "$AGENCY_ID" \
        #     --output "$DATA_DIR/raw/scribe_${TIMESTAMP}.json" \
        #     --since-last-run
    fi

    return 0
}

step_intake_screening() {
    log_info "Running intake screening processor for agency: $AGENCY_ID"

    if [[ ! -f "$DATA_DIR/scripts/intake_screening_processor.py" ]]; then
        log_error "intake_screening_processor.py not found"
        return 1
    fi

    python "$DATA_DIR/scripts/intake_screening_processor.py" \
        --agency-id "$AGENCY_ID" \
        --sample-run \
        || return 1
}

step_oasis_qa_check() {
    log_info "Running OASIS QA check for agency: $AGENCY_ID"

    if [[ ! -f "$DATA_DIR/scripts/oasis_qa_checker.py" ]]; then
        log_error "oasis_qa_checker.py not found"
        return 1
    fi

    python "$DATA_DIR/scripts/oasis_qa_checker.py" \
        --agency-id "$AGENCY_ID" \
        || return 1
}

step_pdgm_billing_review() {
    log_info "Running PDGM billing review for agency: $AGENCY_ID"

    if [[ ! -f "$DATA_DIR/scripts/pdgm_billing_checker.py" ]]; then
        log_error "pdgm_billing_checker.py not found"
        return 1
    fi

    python "$DATA_DIR/scripts/pdgm_billing_checker.py" \
        --agency-id "$AGENCY_ID" \
        --test-all \
        || return 1
}

step_scheduling_compliance() {
    log_info "Running scheduling compliance check for agency: $AGENCY_ID"

    if [[ ! -f "$DATA_DIR/scripts/scheduling_compliance_checker.py" ]]; then
        log_error "scheduling_compliance_checker.py not found"
        return 1
    fi

    python "$DATA_DIR/scripts/scheduling_compliance_checker.py" \
        --agency-id "$AGENCY_ID" \
        || return 1
}

step_recert_discharge_eval() {
    log_info "Running recert/discharge evaluation for agency: $AGENCY_ID"

    if [[ ! -f "$DATA_DIR/scripts/recert_discharge_processor.py" ]]; then
        log_error "recert_discharge_processor.py not found"
        return 1
    fi

    python "$DATA_DIR/scripts/recert_discharge_processor.py" \
        --agency-id "$AGENCY_ID" \
        || return 1
}

step_aggregate_quarterly_data() {
    log_info "Aggregating quarterly data for agency: $AGENCY_ID"

    if [[ ! -f "$DATA_DIR/scripts/aggregate_quarterly_data.py" ]]; then
        log_error "aggregate_quarterly_data.py not found"
        return 1
    fi

    python "$DATA_DIR/scripts/aggregate_quarterly_data.py" \
        --agency-id "$AGENCY_ID" \
        --quarter "$QUARTER" \
        --year "$YEAR" \
        --output "$OUTCOMES_DIR/quarterly_aggregate_${AGENCY_ID}_${QUARTER}${YEAR}.json" \
        || return 1
}

step_flag_high_risk_patients() {
    log_info "Flagging high-risk patients for agency: $AGENCY_ID"

    if [[ ! -f "$DATA_DIR/scripts/flag_high_risk_patients.py" ]]; then
        log_error "flag_high_risk_patients.py not found"
        return 1
    fi

    python "$DATA_DIR/scripts/flag_high_risk_patients.py" \
        --agency-id "$AGENCY_ID" \
        --input "$OUTCOMES_DIR/quarterly_aggregate_${AGENCY_ID}_${QUARTER}${YEAR}.json" \
        --output "$OUTCOMES_DIR/high-risk/high_risk_patients_${AGENCY_ID}_${TIMESTAMP}.json" \
        || return 1

    # Send Slack notification if high-risk patients detected
    if [[ -n "$ENZO_SLACK_WEBHOOK" ]]; then
        local high_risk_count=$(jq '.patients[] | select(.risk_score >= 4) | .risk_score' \
            "$OUTCOMES_DIR/high-risk/high_risk_patients_${AGENCY_ID}_${TIMESTAMP}.json" 2>/dev/null | wc -l)

        if [[ $high_risk_count -gt 0 ]]; then
            log_warn "Found $high_risk_count patients with risk score >= 4"
            # Slack notification would be sent here
        fi
    fi
}

step_hhvbp_model() {
    log_info "Running HHVBP (Home Health Value-Based Purchasing) model for agency: $AGENCY_ID"

    if [[ ! -f "$DATA_DIR/scripts/hhvbp_model.py" ]]; then
        log_error "hhvbp_model.py not found"
        return 1
    fi

    python "$DATA_DIR/scripts/hhvbp_model.py" \
        --agency-id "$AGENCY_ID" \
        --quarter "$QUARTER" \
        --year "$YEAR" \
        --input "$OUTCOMES_DIR/quarterly_aggregate_${AGENCY_ID}_${QUARTER}${YEAR}.json" \
        --output "$OUTCOMES_DIR/hhvbp/model_output_${AGENCY_ID}_${QUARTER}${YEAR}.json" \
        || return 1
}

step_star_rating_estimator() {
    log_info "Calculating Star Rating estimates for agency: $AGENCY_ID"

    if [[ ! -f "$DATA_DIR/scripts/star_rating_estimator.py" ]]; then
        log_error "star_rating_estimator.py not found"
        return 1
    fi

    python "$DATA_DIR/scripts/star_rating_estimator.py" \
        --agency-id "$AGENCY_ID" \
        --quarter "$QUARTER" \
        --year "$YEAR" \
        --input "$OUTCOMES_DIR/quarterly_aggregate_${AGENCY_ID}_${QUARTER}${YEAR}.json" \
        --output "$OUTCOMES_DIR/star-ratings/estimate_${AGENCY_ID}_${QUARTER}${YEAR}.json" \
        || return 1
}

step_git_push_outputs() {
    log_info "Pushing outputs to GitHub..."

    if [[ "$DRY_RUN" == "true" ]]; then
        log_warn "DRY RUN: Skipping git push"
        return 0
    fi

    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_warn "Not in a git repository - skipping git push"
        return 0
    fi

    cd "$PROJECT_ROOT" || return 1

    # Stage all outputs
    git add "$OUTCOMES_DIR/" || log_warn "Failed to stage outcomes directory"

    # Check if there are any changes to commit
    if ! git diff-index --quiet HEAD --; then
        local commit_message="[agent-run] $AGENCY_ID Q$QUARTER $YEAR - $TIMESTAMP"
        git commit -m "$commit_message" || return 1
        log_success "Committed outputs to git"

        # Push to remote if configured
        if git remote get-url origin > /dev/null 2>&1; then
            git push origin HEAD || log_warn "Failed to push to remote (may not have credentials)"
        fi
    else
        log_info "No changes to commit"
    fi
}

step_log_completion() {
    log_info "Logging run completion to history..."

    # Build results JSON
    local results_json="{
        \"timestamp\": \"$(date -Iseconds)\",
        \"agency_id\": \"$AGENCY_ID\",
        \"quarter\": \"$QUARTER\",
        \"year\": \"$YEAR\",
        \"overall_status\": \"pending\",
        \"steps\": {}
    }"

    # Add step results
    for step in "${STEP_ORDER[@]}"; do
        local status="${STEP_RESULTS[$step]:-skipped}"
        local error="${STEP_ERRORS[$step]:-}"

        local step_json="{\"status\": \"$status\""
        if [[ -n "$error" ]]; then
            step_json="$step_json, \"error\": \"$(echo "$error" | jq -Rs .)\""
        fi
        step_json="$step_json}"

        results_json=$(echo "$results_json" | jq ".steps.$step = $step_json")
    done

    # Determine overall status
    local failed_count=0
    for step in "${STEP_ORDER[@]}"; do
        if [[ "${STEP_RESULTS[$step]}" == "failed" ]]; then
            ((failed_count++))
        fi
    done

    if [[ $failed_count -eq 0 ]]; then
        results_json=$(echo "$results_json" | jq '.overall_status = "success"')
    else
        results_json=$(echo "$results_json" | jq ".overall_status = \"failed ($failed_count steps)\"")
    fi

    # Append to run history (create if doesn't exist)
    if [[ ! -f "$RUN_HISTORY_FILE" ]]; then
        echo "[]" > "$RUN_HISTORY_FILE"
    fi

    # Append new run to history
    local updated_history
    updated_history=$(jq ". += [$results_json]" "$RUN_HISTORY_FILE")
    echo "$updated_history" > "$RUN_HISTORY_FILE"

    log_success "Run history logged to $RUN_HISTORY_FILE"
}

################################################################################
# MAIN EXECUTION
################################################################################

parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --agency-id)
                AGENCY_ID="$2"
                shift 2
                ;;
            --quarter)
                QUARTER="$2"
                shift 2
                ;;
            --year)
                YEAR="$2"
                shift 2
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

validate_inputs() {
    if [[ -z "$AGENCY_ID" ]]; then
        log_error "Agency ID is required (--agency-id)"
        exit 1
    fi
    if [[ -z "$QUARTER" ]]; then
        log_error "Quarter is required (--quarter)"
        exit 1
    fi
    if [[ -z "$YEAR" ]]; then
        log_error "Year is required (--year)"
        exit 1
    fi
}

print_summary() {
    print_divider
    log_info "PIPELINE EXECUTION SUMMARY"
    print_divider
    log_info "Agency: $AGENCY_ID"
    log_info "Quarter: $QUARTER"
    log_info "Year: $YEAR"
    log_info "Execution Time: $(date)"
    log_info "Log File: $LOG_FILE"
    print_divider

    local success_count=0
    local failed_count=0

    for step in "${STEP_ORDER[@]}"; do
        local status="${STEP_RESULTS[$step]:-skipped}"
        case "$status" in
            success)
                log_success "$step: SUCCESS"
                ((success_count++))
                ;;
            failed)
                log_error "$step: FAILED - ${STEP_ERRORS[$step]}"
                ((failed_count++))
                ;;
            *)
                log_warn "$step: SKIPPED"
                ;;
        esac
    done

    print_divider
    log_info "Summary: $success_count successful, $failed_count failed"

    if [[ $failed_count -gt 0 ]]; then
        log_error "Pipeline execution failed"
        return 1
    else
        log_success "Pipeline execution completed successfully"
        return 0
    fi
}

main() {
    parse_arguments "$@"
    validate_inputs

    log_info "Starting Enzo Health agent workflow pipeline"
    log_info "Project Root: $PROJECT_ROOT"
    log_info "Data Directory: $DATA_DIR"

    # Run each step in order, continuing even if steps fail
    run_step "pull_latest_data" "Step 1: Pull latest data from APIs" "step_pull_latest_data"
    run_step "intake_screening" "Step 2: Intake Screening Processor" "step_intake_screening"
    run_step "oasis_qa_check" "Step 3: OASIS QA Checker" "step_oasis_qa_check"
    run_step "pdgm_billing_review" "Step 4: PDGM Billing Checker" "step_pdgm_billing_review"
    run_step "scheduling_compliance" "Step 5: Scheduling Compliance Checker" "step_scheduling_compliance"
    run_step "recert_discharge_eval" "Step 6: Recert/Discharge Processor" "step_recert_discharge_eval"
    run_step "aggregate_quarterly_data" "Step 7: Aggregate quarterly data" "step_aggregate_quarterly_data"
    run_step "flag_high_risk_patients" "Step 8: Flag high-risk patients" "step_flag_high_risk_patients"
    run_step "hhvbp_model" "Step 9: Run HHVBP model" "step_hhvbp_model"
    run_step "star_rating_estimator" "Step 10: Calculate Star Rating estimates" "step_star_rating_estimator"
    run_step "git_push_outputs" "Step 11: Push outputs to GitHub" "step_git_push_outputs"
    run_step "log_completion" "Step 12: Log completion to history" "step_log_completion"

    # Print execution summary and exit with appropriate code
    print_summary
    exit_code=$?

    exit $exit_code
}

# Execute main function with all arguments
main "$@"
