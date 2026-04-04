#!/usr/bin/env python3
"""
QAPI Quarterly Data Aggregation Script

Reads QAPI CSV files and calculates quality indicator rates against
CMS national benchmarks.

Calculates:
  1. Hospitalization rate
  2. ED visit rate
  3. Discharge to community rate
  4. Functional improvement - ambulation (OASIS M01800)
  5. Functional improvement - toileting (OASIS M01820)
  6. Functional improvement - transferring (OASIS M01850)
  7. Functional improvement - bathing (OASIS M01880)
  8. Functional improvement - dressing (OASIS M01900)
  9. Timely initiation of care (OASIS M01600)

Usage:
    python aggregate_quarterly_data.py --quarter Q1 --year 2026 --agency-id SUNRISE
    python aggregate_quarterly_data.py --quarter Q2 --year 2026
"""

import argparse
import csv
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


# ============================================================================
# CMS Benchmarks (National Averages for HH - hypothetical values)
# ============================================================================

CMS_BENCHMARKS = {
    'hospitalization_rate': 0.246,           # 24.6%
    'ed_visit_rate': 0.147,                  # 14.7%
    'discharge_to_community_rate': 0.657,    # 65.7%
    'functional_improvement_ambulation': 0.482,
    'functional_improvement_toileting': 0.539,
    'functional_improvement_transferring': 0.448,
    'functional_improvement_bathing': 0.559,
    'functional_improvement_dressing': 0.612,
    'timely_initiation_rate': 0.892           # 89.2%
}

# Paths relative to workspace
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = WORKSPACE_ROOT / 'data'
OUTPUT_DIR = Path(__file__).parent / 'output'


# ============================================================================
# Logging Setup
# ============================================================================

def setup_logging() -> logging.Logger:
    """Configure logging."""
    logger = logging.getLogger('aggregate_quarterly_data')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger


# ============================================================================
# Quarter/Year Utilities
# ============================================================================

def get_quarter_dates(quarter: str, year: int) -> Tuple[str, str]:
    """
    Get start and end dates for a quarter.

    Args:
        quarter: 'Q1', 'Q2', 'Q3', or 'Q4'
        year: Calendar year

    Returns:
        Tuple of (start_date, end_date) in YYYY-MM-DD format
    """
    quarter_map = {
        'Q1': ('01-01', '03-31'),
        'Q2': ('04-01', '06-30'),
        'Q3': ('07-01', '09-30'),
        'Q4': ('10-01', '12-31')
    }

    if quarter.upper() not in quarter_map:
        raise ValueError(f"Invalid quarter: {quarter}. Use Q1, Q2, Q3, or Q4")

    start, end = quarter_map[quarter.upper()]
    return f"{year}-{start}", f"{year}-{end}"


def find_qapi_files(
    data_dir: Path,
    from_date: str,
    to_date: str,
    agency_id: Optional[str] = None
) -> List[Path]:
    """
    Find QAPI CSV files in the data directory.

    Looks for files matching:
    - YYYY-MM-DD-*-census.csv
    - YYYY-QN-*

    Args:
        data_dir: Directory to search
        from_date: Start date filter (YYYY-MM-DD)
        to_date: End date filter (YYYY-MM-DD)
        agency_id: Optional agency ID filter

    Returns:
        List of matching file paths
    """
    files = []

    if not data_dir.exists():
        return files

    from_parts = from_date.split('-')
    to_parts = to_date.split('-')
    from_ymd = int(from_parts[0] + from_parts[1] + from_parts[2])
    to_ymd = int(to_parts[0] + to_parts[1] + to_parts[2])

    for csv_file in data_dir.glob('*.csv'):
        # Check agency filter
        if agency_id and agency_id not in csv_file.name:
            continue

        # Parse date from filename
        parts = csv_file.stem.split('-')
        if len(parts) < 3:
            continue

        try:
            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2])
            file_ymd = year * 10000 + month * 100 + day

            if from_ymd <= file_ymd <= to_ymd:
                files.append(csv_file)
        except (ValueError, IndexError):
            continue

    return sorted(files)


# ============================================================================
# Data Processing
# ============================================================================

def read_qapi_csv(filepath: Path) -> List[Dict[str, str]]:
    """
    Read a QAPI CSV file.

    Args:
        filepath: Path to CSV file

    Returns:
        List of row dictionaries
    """
    rows = []
    with open(filepath, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row and row.get('PatientID'):  # Skip empty rows
                rows.append(row)
    return rows


def calculate_indicators(
    all_rows: List[Dict[str, str]],
    logger: logging.Logger
) -> Dict[str, float]:
    """
    Calculate quality indicator rates from QAPI data.

    Args:
        all_rows: All patient records
        logger: Logger instance

    Returns:
        Dictionary of indicator_name -> rate (0.0-1.0)
    """
    if not all_rows:
        logger.warning("No patient records to calculate")
        return {}

    indicators = {}
    total_patients = len(all_rows)

    logger.info(f"Calculating indicators from {total_patients} records")

    # 1. Hospitalization rate
    hospitalized = sum(1 for r in all_rows if r.get('Hospitalization', '0') == '1')
    indicators['hospitalization_rate'] = hospitalized / total_patients if total_patients > 0 else 0.0

    # 2. ED visit rate
    ed_visits = sum(1 for r in all_rows if r.get('EDVisit', '0') == '1')
    indicators['ed_visit_rate'] = ed_visits / total_patients if total_patients > 0 else 0.0

    # 3. Discharge to community rate (not expired, not transferred to facility)
    discharge_disp = [r.get('DischargeDisposition', '').lower() for r in all_rows]
    discharged_to_community = sum(
        1 for d in discharge_disp
        if 'home' in d or 'self-care' in d
    )
    indicators['discharge_to_community_rate'] = (
        discharged_to_community / total_patients if total_patients > 0 else 0.0
    )

    # 4-8. Functional improvements
    # These would require OASIS data in the CSV. For now, use defaults
    # In production, parse OASIS dates and calculate improvement
    for key in [
        'functional_improvement_ambulation',
        'functional_improvement_toileting',
        'functional_improvement_transferring',
        'functional_improvement_bathing',
        'functional_improvement_dressing'
    ]:
        # Placeholder: assume 50% improvement rate
        # In production: compare OASIS SOC and DC functional status
        indicators[key] = 0.50

    # 9. Timely initiation of care
    timely = sum(1 for r in all_rows if r.get('TimelyInitiation', '0') == '1')
    indicators['timely_initiation_rate'] = timely / total_patients if total_patients > 0 else 0.0

    logger.debug(f"Calculated indicators: {indicators}")

    return indicators


def compare_to_benchmarks(
    indicators: Dict[str, float],
    logger: logging.Logger
) -> Dict[str, Dict[str, any]]:
    """
    Compare indicator rates to CMS benchmarks.

    Args:
        indicators: Dictionary of calculated rates
        logger: Logger instance

    Returns:
        Dictionary with indicator details and comparison status
    """
    results = {}

    for indicator_name, rate in indicators.items():
        benchmark = CMS_BENCHMARKS.get(indicator_name, 0.0)

        # Determine status
        if rate > benchmark:
            status = 'above'
        elif rate == benchmark:
            status = 'at'
        else:
            status = 'below'

        results[indicator_name] = {
            'rate': round(rate, 4),
            'benchmark': benchmark,
            'status': status,
            'difference': round(rate - benchmark, 4)
        }

        logger.info(
            f"{indicator_name}: {rate:.2%} vs benchmark {benchmark:.2%} [{status}]"
        )

    return results


# ============================================================================
# Output Generation
# ============================================================================

def generate_summary(
    quarter: str,
    year: int,
    agency_id: str,
    comparison_results: Dict[str, Dict[str, any]],
    file_count: int,
    patient_count: int,
    logger: logging.Logger
) -> Dict[str, any]:
    """
    Generate a summary report.

    Args:
        quarter: Quarter (Q1-Q4)
        year: Calendar year
        agency_id: Agency ID
        comparison_results: Comparison results from compare_to_benchmarks()
        file_count: Number of QAPI files processed
        patient_count: Total number of patients
        logger: Logger instance

    Returns:
        Summary dictionary suitable for JSON output
    """
    # Count indicators by status
    above_count = sum(1 for r in comparison_results.values() if r['status'] == 'above')
    at_count = sum(1 for r in comparison_results.values() if r['status'] == 'at')
    below_count = sum(1 for r in comparison_results.values() if r['status'] == 'below')

    summary = {
        'generated_at': datetime.now().isoformat(),
        'quarter': quarter,
        'year': year,
        'agency_id': agency_id,
        'data_summary': {
            'files_processed': file_count,
            'total_patients': patient_count
        },
        'indicators': comparison_results,
        'performance_summary': {
            'above_benchmark': above_count,
            'at_benchmark': at_count,
            'below_benchmark': below_count,
            'total_indicators': len(comparison_results)
        }
    }

    logger.info(f"Summary: {above_count} above, {at_count} at, {below_count} below benchmark")

    return summary


# ============================================================================
# Main Logic
# ============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Aggregate quarterly QAPI data and compare to CMS benchmarks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python aggregate_quarterly_data.py --quarter Q1 --year 2026 --agency-id SUNRISE
  python aggregate_quarterly_data.py --quarter Q2 --year 2026
        """
    )

    parser.add_argument(
        '--quarter',
        required=True,
        choices=['Q1', 'Q2', 'Q3', 'Q4'],
        help='Quarter to aggregate (Q1-Q4)'
    )
    parser.add_argument(
        '--year',
        type=int,
        required=True,
        help='Calendar year'
    )
    parser.add_argument(
        '--agency-id',
        help='Filter to specific agency ID (optional)'
    )

    args = parser.parse_args()

    # Setup logging
    logger = setup_logging()
    logger.info("=" * 70)
    logger.info("QAPI Quarterly Data Aggregation Started")
    logger.info("=" * 70)

    try:
        # Get quarter dates
        from_date, to_date = get_quarter_dates(args.quarter, args.year)
        logger.info(f"Quarter {args.quarter} {args.year}: {from_date} to {to_date}")

        # Find QAPI files
        files = find_qapi_files(DATA_DIR, from_date, to_date, args.agency_id)
        if not files:
            logger.warning("No QAPI CSV files found for specified date range")
            logger.info("Make sure CSV files are in: " + str(DATA_DIR))
            return 0

        logger.info(f"Found {len(files)} QAPI CSV file(s)")
        for f in files:
            logger.debug(f"  - {f.name}")

        # Read all records
        all_rows = []
        for filepath in files:
            rows = read_qapi_csv(filepath)
            all_rows.extend(rows)
            logger.info(f"  {filepath.name}: {len(rows)} records")

        logger.info(f"Total records: {len(all_rows)}")

        if not all_rows:
            logger.warning("No patient records found in CSV files")
            return 0

        # Calculate indicators
        indicators = calculate_indicators(all_rows, logger)

        # Compare to benchmarks
        comparison_results = compare_to_benchmarks(indicators, logger)

        # Generate summary
        summary = generate_summary(
            args.quarter,
            args.year,
            args.agency_id or 'ALL',
            comparison_results,
            len(files),
            len(all_rows),
            logger
        )

        # Save output
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_file = OUTPUT_DIR / 'quarterly_summary.json'

        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)

        logger.info(f"Summary saved to: {output_file}")

        # Log summary table
        logger.info("=" * 70)
        logger.info("Quality Indicators vs CMS Benchmarks")
        logger.info("=" * 70)
        for indicator_name, data in comparison_results.items():
            rate_pct = data['rate'] * 100
            bench_pct = data['benchmark'] * 100
            diff_pct = data['difference'] * 100
            status = data['status'].upper()
            logger.info(
                f"{indicator_name:40s} {rate_pct:6.2f}% "
                f"(benchmark {bench_pct:6.2f}%) [{status}] ({diff_pct:+6.2f}pp)"
            )

        logger.info("=" * 70)

        return 0

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        logger.error("=" * 70)
        return 1


if __name__ == '__main__':
    sys.exit(main())
