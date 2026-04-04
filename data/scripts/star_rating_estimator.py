#!/usr/bin/env python3
"""
CMS OASIS-Based Star Rating Estimator
Author: Enzo Health Outcomes Analyst Agent
Date: April 4, 2026

This module implements a simplified version of CMS's star rating algorithm
for Home Health agencies, based on 7 OASIS-derived quality measures.

The star rating system uses a linear mean methodology:
1. Each measure is converted to a percentile score (0-100)
2. The percentile scores are averaged to create a composite quality score
3. The composite score is mapped to a 1-5 star rating using CMS thresholds

Star Rating Thresholds (approximate, based on CMS historical data):
- 5 stars: Composite Score >= 80 (top 10% of agencies)
- 4 stars: Composite Score 70-79.9 (60-80th percentile)
- 3 stars: Composite Score 60-69.9 (30-60th percentile)
- 2 stars: Composite Score 40-59.9 (10-30th percentile)
- 1 star: Composite Score < 40 (bottom 10% of agencies)

The 7 Star Rating Measures (CY 2026):
1. Improvement in Ambulation/Locomotion (4-point OASIS scale)
2. Improvement in Bathing (4-point OASIS scale)
3. Improvement in Transferring (4-point OASIS scale)
4. Improvement in Toileting (4-point OASIS scale)
5. Acute Care Hospitalization Measure (lower is better)
6. Emergency Department Utilization (lower is better)
7. Timely Initiation of Care (OASIS assessment timing)

Performance Analysis:
For each measure, the script:
- Compares agency performance to national benchmark
- Identifies which measures are pulling rating down vs. lifting up
- Calculates the weighted impact on overall star rating
- Provides "what-if" analysis for improving specific measures
"""

import json
import argparse
from datetime import datetime
from typing import Dict, List, Tuple


class StarRatingEstimator:
    """CMS OASIS-based star rating calculator."""

    # National Benchmarks (CY 2026 estimated from CMS published data)
    STAR_RATING_MEASURES = {
        'improvement_in_ambulation': {
            'benchmark': 53.2,
            'threshold_1_star': 35.0,
            'threshold_2_star': 42.0,
            'threshold_3_star': 50.0,
            'threshold_4_star': 58.0,
            'threshold_5_star': 65.0,
            'description': 'Improvement in Ambulation/Locomotion (0-4 scale)',
            'inverse': False,  # higher is better
        },
        'improvement_in_bathing': {
            'benchmark': 67.1,
            'threshold_1_star': 50.0,
            'threshold_2_star': 57.0,
            'threshold_3_star': 64.0,
            'threshold_4_star': 70.0,
            'threshold_5_star': 75.0,
            'description': 'Improvement in Bathing (0-4 scale)',
            'inverse': False,
        },
        'improvement_in_transferring': {
            'benchmark': 71.3,
            'threshold_1_star': 52.0,
            'threshold_2_star': 60.0,
            'threshold_3_star': 68.0,
            'threshold_4_star': 75.0,
            'threshold_5_star': 80.0,
            'description': 'Improvement in Transferring (0-4 scale)',
            'inverse': False,
        },
        'improvement_in_toileting': {
            'benchmark': 68.9,
            'threshold_1_star': 50.0,
            'threshold_2_star': 58.0,
            'threshold_3_star': 65.0,
            'threshold_4_star': 72.0,
            'threshold_5_star': 78.0,
            'description': 'Improvement in Toileting (0-4 scale)',
            'inverse': False,
        },
        'acute_care_hospitalization': {
            'benchmark': 14.7,
            'threshold_1_star': 25.0,
            'threshold_2_star': 20.0,
            'threshold_3_star': 17.0,
            'threshold_4_star': 12.0,
            'threshold_5_star': 8.0,
            'description': 'Acute Care Hospitalization Rate (% of patients)',
            'inverse': True,  # lower is better
        },
        'ed_utilization': {
            'benchmark': 8.2,
            'threshold_1_star': 14.0,
            'threshold_2_star': 11.0,
            'threshold_3_star': 9.0,
            'threshold_4_star': 6.0,
            'threshold_5_star': 3.0,
            'description': 'ED Use Without Hospitalization (% of patients)',
            'inverse': True,
        },
        'timely_initiation': {
            'benchmark': 96.3,
            'threshold_1_star': 88.0,
            'threshold_2_star': 91.0,
            'threshold_3_star': 94.0,
            'threshold_4_star': 97.0,
            'threshold_5_star': 99.0,
            'description': 'Timely Initiation of Care (% at SOC within 14 days)',
            'inverse': False,
        },
    }

    # Star rating composite thresholds (derived from percentile mapping)
    COMPOSITE_THRESHOLDS = {
        5: 80.0,
        4: 70.0,
        3: 60.0,
        2: 40.0,
        1: 0.0,
    }

    def __init__(self, agency_name: str = "Unnamed Agency"):
        """
        Initialize the star rating estimator.

        Args:
            agency_name: Name of the agency for reporting
        """
        self.agency_name = agency_name
        self.performance = {}  # measure_name -> agency_performance
        self.percentile_scores = {}  # measure_name -> percentile_score
        self.composite_score = None
        self.star_rating = None

    def set_performance(self, measure_name: str, agency_rate: float) -> None:
        """
        Set agency performance for a specific star rating measure.

        Args:
            measure_name: Name of the measure
            agency_rate: Agency's performance rate (percentage or absolute %)
        """
        if measure_name not in self.STAR_RATING_MEASURES:
            raise ValueError(f"Unknown measure: {measure_name}")
        self.performance[measure_name] = agency_rate

    def set_all_performance(self, performance_dict: Dict[str, float]) -> None:
        """Set all agency performance metrics at once."""
        for measure_name, rate in performance_dict.items():
            self.set_performance(measure_name, rate)

    def calculate_measure_percentile(self, measure_name: str) -> float:
        """
        Convert agency performance to a percentile score (0-100).

        Methodology:
        - 5-star threshold performance = 100th percentile (100 points)
        - 1-star threshold performance = 0th percentile (0 points)
        - Linear interpolation between thresholds

        For inverse measures (hospitalization, ED use), logic is inverted:
        - Lower performance (fewer hosp.) = higher percentile

        Args:
            measure_name: Name of the measure

        Returns:
            Percentile score (0-100)
        """
        if measure_name not in self.performance:
            raise ValueError(f"Performance data not provided for {measure_name}")

        agency_rate = self.performance[measure_name]
        measure_config = self.STAR_RATING_MEASURES[measure_name]
        is_inverse = measure_config['inverse']

        # Extract thresholds in order
        if is_inverse:
            # For inverse measures: lower threshold = higher percentile
            threshold_5 = measure_config['threshold_5_star']  # best (lowest)
            threshold_1 = measure_config['threshold_1_star']  # worst (highest)

            if agency_rate <= threshold_5:
                # Better than 5-star threshold
                percentile = 100.0
            elif agency_rate >= threshold_1:
                # Worse than 1-star threshold
                percentile = 0.0
            else:
                # Linear interpolation between thresholds
                percentile = (
                    (threshold_1 - agency_rate) /
                    (threshold_1 - threshold_5)
                ) * 100
        else:
            # For normal measures: higher threshold = higher percentile
            threshold_5 = measure_config['threshold_5_star']  # best (highest)
            threshold_1 = measure_config['threshold_1_star']  # worst (lowest)

            if agency_rate >= threshold_5:
                # Better than 5-star threshold
                percentile = 100.0
            elif agency_rate <= threshold_1:
                # Worse than 1-star threshold
                percentile = 0.0
            else:
                # Linear interpolation between thresholds
                percentile = (
                    (agency_rate - threshold_1) /
                    (threshold_5 - threshold_1)
                ) * 100

        self.percentile_scores[measure_name] = percentile
        return percentile

    def calculate_composite_score(self) -> float:
        """
        Calculate composite quality score from all measure percentiles.

        Linear Mean Methodology:
        - Average the percentile scores across all 7 measures
        - Result is a 0-100 composite score

        Returns:
            Composite quality score (0-100)
        """
        for measure_name in self.STAR_RATING_MEASURES.keys():
            if measure_name not in self.percentile_scores:
                self.calculate_measure_percentile(measure_name)

        total_percentile = sum(self.percentile_scores.values())
        num_measures = len(self.percentile_scores)

        self.composite_score = total_percentile / num_measures
        return self.composite_score

    def calculate_star_rating(self) -> int:
        """
        Map composite score to a 1-5 star rating.

        Thresholds:
        - 5 stars: >= 80
        - 4 stars: >= 70
        - 3 stars: >= 60
        - 2 stars: >= 40
        - 1 star: < 40

        Returns:
            Star rating (1-5)
        """
        if self.composite_score is None:
            self.calculate_composite_score()

        for stars in [5, 4, 3, 2, 1]:
            if self.composite_score >= self.COMPOSITE_THRESHOLDS[stars]:
                self.star_rating = stars
                return stars

        return 1  # fallback

    def get_measure_impact_analysis(self) -> Dict:
        """
        Analyze which measures are pulling the rating up vs. down.

        Returns:
            Dictionary with measures ranked by percentile contribution
        """
        analysis = []

        for measure_name in sorted(self.percentile_scores.keys()):
            percentile = self.percentile_scores[measure_name]
            measure_config = self.STAR_RATING_MEASURES[measure_name]
            benchmark = measure_config['benchmark']
            agency_rate = self.performance[measure_name]

            # Classify impact
            if percentile >= 80:
                impact = "LIFTING RATING"
                emoji = "🟢"
            elif percentile >= 60:
                impact = "NEUTRAL"
                emoji = "🟡"
            else:
                impact = "DRAGGING DOWN"
                emoji = "🔴"

            analysis.append({
                'measure': measure_name,
                'description': measure_config['description'],
                'agency_performance': agency_rate,
                'benchmark': benchmark,
                'percentile_score': percentile,
                'impact_classification': impact,
                'emoji': emoji,
                'gap_to_benchmark': agency_rate - benchmark,
            })

        # Sort by percentile score (ascending) to show weakest first
        analysis.sort(key=lambda x: x['percentile_score'])
        return analysis

    def what_if_improvement(self, measure_name: str,
                           improvement_points: float) -> Dict:
        """
        Run "what-if" analysis for improving a single measure.

        Args:
            measure_name: Measure to improve
            improvement_points: How many points to improve (e.g., +5 for +5%)

        Returns:
            Dictionary with baseline and improved scores
        """
        # Baseline
        baseline_percentile = self.percentile_scores.get(measure_name)
        if baseline_percentile is None:
            baseline_percentile = self.calculate_measure_percentile(measure_name)

        baseline_composite = self.composite_score or self.calculate_composite_score()
        baseline_stars = self.star_rating or self.calculate_star_rating()

        # Improvement
        original_performance = self.performance[measure_name]
        self.performance[measure_name] += improvement_points

        # Recalculate
        improved_percentile = self.calculate_measure_percentile(measure_name)
        improved_composite = self.calculate_composite_score()
        improved_stars = self.calculate_star_rating()

        # Restore
        self.performance[measure_name] = original_performance

        return {
            'measure': measure_name,
            'baseline_performance': original_performance,
            'improved_performance': original_performance + improvement_points,
            'improvement_points': improvement_points,
            'baseline_percentile': baseline_percentile,
            'improved_percentile': improved_percentile,
            'percentile_change': improved_percentile - baseline_percentile,
            'baseline_composite': baseline_composite,
            'improved_composite': improved_composite,
            'composite_change': improved_composite - baseline_composite,
            'baseline_stars': baseline_stars,
            'improved_stars': improved_stars,
            'stars_change': improved_stars - baseline_stars,
        }

    def generate_report(self) -> str:
        """Generate a comprehensive text report."""
        if self.composite_score is None:
            self.calculate_composite_score()
        if self.star_rating is None:
            self.calculate_star_rating()

        report = []
        report.append("=" * 80)
        report.append("STAR RATING ESTIMATOR — REPORT")
        report.append(f"Agency: {self.agency_name}")
        report.append(f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}")
        report.append("=" * 80)
        report.append("")

        # Executive Summary
        star_display = "⭐" * self.star_rating
        report.append("EXECUTIVE SUMMARY")
        report.append("-" * 80)
        report.append(f"Estimated Star Rating: {star_display} ({self.star_rating}/5)")
        report.append(f"Composite Quality Score: {self.composite_score:.1f} / 100")
        report.append("")

        if self.star_rating >= 4:
            assessment = "EXCELLENT - High-quality home health agency"
        elif self.star_rating == 3:
            assessment = "ADEQUATE - Performing near national average"
        else:
            assessment = "NEEDS IMPROVEMENT - Below-average quality performance"

        report.append(f"Assessment: {assessment}")
        report.append("")

        # Measure Performance
        report.append("MEASURE-BY-MEASURE ANALYSIS")
        report.append("-" * 80)

        impact_analysis = self.get_measure_impact_analysis()

        for measure_data in impact_analysis:
            report.append(f"\n{measure_data['emoji']} {measure_data['description']}")
            report.append(f"  Agency Performance:  {measure_data['agency_performance']:.1f}%")
            report.append(f"  National Benchmark:  {measure_data['benchmark']:.1f}%")
            report.append(f"  Gap to Benchmark:    {measure_data['gap_to_benchmark']:+.1f} pts")
            report.append(f"  Percentile Score:    {measure_data['percentile_score']:.1f} / 100")
            report.append(f"  Rating Impact:       {measure_data['impact_classification']}")

        report.append("")
        report.append("=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)

        return "\n".join(report)

    def to_json(self) -> Dict:
        """Export results as JSON."""
        if self.composite_score is None:
            self.calculate_composite_score()
        if self.star_rating is None:
            self.calculate_star_rating()

        return {
            'metadata': {
                'agency_name': self.agency_name,
                'generated_at': datetime.now().isoformat(),
            },
            'results': {
                'composite_quality_score': self.composite_score,
                'star_rating': self.star_rating,
            },
            'measures': {
                measure: {
                    'agency_performance': self.performance.get(measure),
                    'benchmark': self.STAR_RATING_MEASURES[measure]['benchmark'],
                    'percentile_score': self.percentile_scores.get(measure),
                }
                for measure in self.STAR_RATING_MEASURES.keys()
            },
        }


def main():
    """Main entry point for command-line usage."""

    parser = argparse.ArgumentParser(description='CMS Star Rating Estimator')
    parser.add_argument('--agency', type=str, default='Sunrise Home Health',
                       help='Agency name')
    parser.add_argument('--ambulation', type=float, default=48.0,
                       help='Improvement in Ambulation %')
    parser.add_argument('--bathing', type=float, default=62.0,
                       help='Improvement in Bathing %')
    parser.add_argument('--transferring', type=float, default=65.0,
                       help='Improvement in Transferring %')
    parser.add_argument('--toileting', type=float, default=60.0,
                       help='Improvement in Toileting %')
    parser.add_argument('--hospitalization', type=float, default=24.0,
                       help='Acute Care Hospitalization %')
    parser.add_argument('--ed-use', type=float, default=10.0,
                       help='ED Use %')
    parser.add_argument('--timely', type=float, default=92.0,
                       help='Timely Initiation %')
    parser.add_argument('--json-output', type=str, default=None,
                       help='Save JSON to file')

    args = parser.parse_args()

    # Initialize estimator
    estimator = StarRatingEstimator(args.agency)

    # Set performance
    estimator.set_all_performance({
        'improvement_in_ambulation': args.ambulation,
        'improvement_in_bathing': args.bathing,
        'improvement_in_transferring': args.transferring,
        'improvement_in_toileting': args.toileting,
        'acute_care_hospitalization': args.hospitalization,
        'ed_utilization': args.ed_use,
        'timely_initiation': args.timely,
    })

    # Calculate
    estimator.calculate_composite_score()
    estimator.calculate_star_rating()

    # Print report
    print(estimator.generate_report())

    # Save JSON
    if args.json_output:
        with open(args.json_output, 'w') as f:
            json.dump(estimator.to_json(), f, indent=2)
        print(f"\nJSON results saved to: {args.json_output}")


if __name__ == '__main__':
    main()
