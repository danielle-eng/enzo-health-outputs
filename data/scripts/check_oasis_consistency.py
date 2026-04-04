#!/usr/bin/env python3
"""
OASIS Consistency Checker

Validates visit notes for presence of required OASIS-related documentation
elements before being archived in the clinical-qa workspace.

Checks for:
  - Homebound status documentation
  - Functional status observations (ambulation, ADLs)
  - Pain assessment
  - Medication management
  - Device and equipment information
  - Safety assessment

Outputs consistency score (0-100%) and missing element flags.

Usage:
    python check_oasis_consistency.py --note-file 2026-04-03-PT001-note.md
    python check_oasis_consistency.py /path/to/note.md --score-only
"""

import argparse
import json
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional


# ============================================================================
# Configuration
# ============================================================================

# Required OASIS elements to check for
OASIS_ELEMENTS = {
    'homebound_status': {
        'name': 'Homebound Status',
        'keywords': ['homebound', 'confined to home', 'unable to leave home', 'primarily resides'],
        'importance': 'critical'
    },
    'ambulation': {
        'name': 'Ambulation/Mobility (M01800)',
        'keywords': ['ambulation', 'mobility', 'gait', 'walking', 'wheelchair', 'walker', 'cane'],
        'importance': 'critical'
    },
    'adl_toileting': {
        'name': 'Toileting (M01820)',
        'keywords': ['toilet', 'toileting', 'bowel', 'bladder', 'catheter', 'ostomy'],
        'importance': 'critical'
    },
    'adl_transferring': {
        'name': 'Transferring (M01850)',
        'keywords': ['transfer', 'bed transfer', 'chair', 'move to/from'],
        'importance': 'critical'
    },
    'adl_bathing': {
        'name': 'Bathing (M01880)',
        'keywords': ['bathe', 'bathing', 'shower', 'bath', 'wash'],
        'importance': 'critical'
    },
    'adl_dressing': {
        'name': 'Dressing (M01900)',
        'keywords': ['dress', 'dressing', 'clothes', 'clothing'],
        'importance': 'critical'
    },
    'pain_assessment': {
        'name': 'Pain Assessment',
        'keywords': ['pain', 'discomfort', 'pain level', 'pain scale', 'pain management'],
        'importance': 'important'
    },
    'medication_management': {
        'name': 'Medication Management',
        'keywords': ['medication', 'med reconciliation', 'pharmacy', 'prescription', 'drug'],
        'importance': 'important'
    },
    'devices_equipment': {
        'name': 'Devices and Equipment',
        'keywords': ['device', 'equipment', 'oxygen', 'monitor', 'pump', 'cpap'],
        'importance': 'important'
    },
    'safety_assessment': {
        'name': 'Safety Assessment',
        'keywords': ['safety', 'fall risk', 'hazard', 'home safety', 'precaution'],
        'importance': 'important'
    }
}

# Paths
WORKSPACE_ROOT = Path(__file__).parent.parent.parent


# ============================================================================
# Logging Setup
# ============================================================================

def setup_logging() -> logging.Logger:
    """Configure logging."""
    logger = logging.getLogger('check_oasis_consistency')
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
# OASIS Element Checking
# ============================================================================

def read_note_file(filepath: Path) -> str:
    """
    Read a note file.

    Args:
        filepath: Path to note file

    Returns:
        Full file content as string
    """
    with open(filepath, 'r') as f:
        return f.read()


def normalize_text(text: str) -> str:
    """
    Normalize text for searching (lowercase, remove punctuation).

    Args:
        text: Raw text

    Returns:
        Normalized text
    """
    # Convert to lowercase
    text = text.lower()
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text


def check_element_present(note_content: str, element_key: str) -> bool:
    """
    Check if an OASIS element is documented in the note.

    Args:
        note_content: Full note content
        element_key: Element key from OASIS_ELEMENTS

    Returns:
        True if element appears to be documented
    """
    if element_key not in OASIS_ELEMENTS:
        return False

    element = OASIS_ELEMENTS[element_key]
    keywords = element['keywords']
    normalized_content = normalize_text(note_content)

    # Check if any keyword appears in the note
    for keyword in keywords:
        if keyword.lower() in normalized_content:
            return True

    return False


def check_consistency(note_content: str) -> Dict[str, any]:
    """
    Check overall OASIS consistency of a note.

    Args:
        note_content: Full note content

    Returns:
        Dictionary with consistency details
    """
    results = {
        'timestamp': datetime.now().isoformat(),
        'elements_checked': len(OASIS_ELEMENTS),
        'elements_present': {},
        'elements_missing': {},
        'score': 0.0,
        'status': 'incomplete',
        'recommendations': []
    }

    present_count = 0
    critical_missing = []
    important_missing = []

    # Check each element
    for element_key, element_info in OASIS_ELEMENTS.items():
        is_present = check_element_present(note_content, element_key)

        if is_present:
            results['elements_present'][element_key] = element_info['name']
            present_count += 1
        else:
            results['elements_missing'][element_key] = element_info['name']

            # Track missing critical elements
            if element_info['importance'] == 'critical':
                critical_missing.append(element_info['name'])
            else:
                important_missing.append(element_info['name'])

    # Calculate score
    results['score'] = round((present_count / len(OASIS_ELEMENTS)) * 100, 1)

    # Determine status
    if len(critical_missing) == 0 and len(important_missing) == 0:
        results['status'] = 'complete'
    elif len(critical_missing) == 0:
        results['status'] = 'mostly_complete'
    else:
        results['status'] = 'incomplete'

    # Generate recommendations
    if critical_missing:
        results['recommendations'].append(
            f"CRITICAL: Add documentation for: {', '.join(critical_missing)}"
        )

    if important_missing:
        results['recommendations'].append(
            f"RECOMMENDED: Add documentation for: {', '.join(important_missing)}"
        )

    if results['score'] == 100:
        results['recommendations'].append("Complete - Ready for archival")

    return results


# ============================================================================
# Output Generation
# ============================================================================

def generate_report(
    note_filepath: Path,
    consistency_results: Dict[str, any]
) -> str:
    """
    Generate a human-readable consistency report.

    Args:
        note_filepath: Path to the note file
        consistency_results: Results from check_consistency()

    Returns:
        Formatted report string
    """
    lines = []

    lines.append("=" * 70)
    lines.append("OASIS Consistency Check Report")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"File: {note_filepath.name}")
    lines.append(f"Checked: {consistency_results['timestamp']}")
    lines.append("")

    lines.append("SCORE: {:.1f}%".format(consistency_results['score']))
    lines.append(f"STATUS: {consistency_results['status'].upper()}")
    lines.append("")

    lines.append(f"Elements Present: {len(consistency_results['elements_present'])}")
    for key, name in consistency_results['elements_present'].items():
        lines.append(f"  ✓ {name}")

    if consistency_results['elements_missing']:
        lines.append("")
        lines.append(f"Elements Missing: {len(consistency_results['elements_missing'])}")
        for key, name in consistency_results['elements_missing'].items():
            element = OASIS_ELEMENTS.get(key, {})
            importance = element.get('importance', 'unknown')
            icon = "⚠" if importance == 'critical' else "ℹ"
            lines.append(f"  {icon} {name} [{importance.upper()}]")

    if consistency_results['recommendations']:
        lines.append("")
        lines.append("Recommendations:")
        for recommendation in consistency_results['recommendations']:
            lines.append(f"  • {recommendation}")

    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)


def save_consistency_report(
    note_filepath: Path,
    consistency_results: Dict[str, any]
) -> str:
    """
    Save consistency check results as JSON metadata file.

    Args:
        note_filepath: Path to the note file
        consistency_results: Results from check_consistency()

    Returns:
        Path to saved JSON file
    """
    # Create companion JSON file with same name
    json_filepath = note_filepath.with_suffix('.consistency.json')

    with open(json_filepath, 'w') as f:
        json.dump(consistency_results, f, indent=2)

    return str(json_filepath)


# ============================================================================
# Main Logic
# ============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Check OASIS consistency of visit notes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python check_oasis_consistency.py --note-file 2026-04-03-PT001-note.md
  python check_oasis_consistency.py --note-file /path/to/note.md --score-only
  python check_oasis_consistency.py --note-file note.md --json
        """
    )

    parser.add_argument(
        '--note-file',
        required=True,
        type=str,
        help='Path to note file (or filename in clinical-qa/notes)'
    )
    parser.add_argument(
        '--score-only',
        action='store_true',
        help='Output only the score (useful for automation)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    parser.add_argument(
        '--save-metadata',
        action='store_true',
        help='Save consistency metadata alongside note file'
    )

    args = parser.parse_args()

    # Setup logging
    logger = setup_logging()

    try:
        # Resolve note file path
        note_path = Path(args.note_file)
        if not note_path.is_absolute():
            note_path = WORKSPACE_ROOT / 'clinical-qa' / 'notes' / note_path

        if not note_path.exists():
            logger.error(f"Note file not found: {note_path}")
            return 1

        logger.info(f"Checking: {note_path}")

        # Read note
        note_content = read_note_file(note_path)

        # Check consistency
        results = check_consistency(note_content)

        # Output results
        if args.score_only:
            print(f"{results['score']}")
        elif args.json:
            print(json.dumps(results, indent=2))
        else:
            # Generate and print human-readable report
            report = generate_report(note_path, results)
            print(report)

        # Save metadata if requested
        if args.save_metadata:
            json_file = save_consistency_report(note_path, results)
            logger.info(f"Metadata saved to: {json_file}")

        # Exit with appropriate code
        if results['status'] == 'complete':
            return 0
        elif results['status'] == 'mostly_complete':
            return 0
        else:
            return 1

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
