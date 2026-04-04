#!/usr/bin/env python3
"""
HHVBP (Home Health Value-Based Purchasing) Financial Model
Author: Enzo Health Outcomes Analyst Agent
Date: April 4, 2026

This module implements a comprehensive HHVBP payment adjustment calculator
that computes Total Performance Score (TPS) based on agency performance across
10 HHVBP quality measures, and translates that score into a Medicare payment
adjustment (ranging from -8% to +8%).

The model follows the CY 2026 HHVBP methodology including:
- Achievement scoring (performance vs. achievement threshold)
- Benchmark scoring (bonus points if at/above national benchmark)
- Weighted measure aggregation
- Linear payment adjustment interpolation
- Sensitivity analysis capabilities

HHVBP Context:
The HHVBP program rewards home health agencies for high-quality patient care
using a mixed set of outcome and utilization measures. Agencies with TPS of 50
receive no payment adjustment; those above 50 receive bonuses; those below 50
face penalties. The payment adjustment ranges from -8% to +8% based on TPS.

Measure Weights (CY 2026):
- Improvement in Ambulation: 4.0%
- Improvement in Bathing: 4.0%
- Improvement in Dyspnea: 4.0%
- Improvement in Pain Interfering with Activity: 4.0%
- Improvement in Medication Management: 4.0%
- Discharge to Community: 4.0%
- Acute Care Hospitalization (inverse): 5.5%
- ED Use Without Hospitalization (inverse): 5.5%
- OASIS-based Care Transitions: 3.0%
- HHCAHPS Composite Measures (4 composites): ~8% total

Total: 100%

Scoring Methodology:
1. For each measure, calculate how far the agency's performance is from
   the achievement threshold (typically 10-20 points below benchmark)
2. If agency >= achievement threshold: score = 1 point per percentage point improvement
3. If agency >= benchmark: add bonus points (up to 10 bonus points)
4. Apply measure weight to get weighted score contribution
5. Sum all weighted contributions to get Total Performance Score (TPS)
6. Map TPS (0-100) to payment adjustment (-8% to +8%)
"""

import json
import argparse
import sys
from datetime import datetime
from typing import Dict, List, Tuple


class HHVBPModel:
    """Complete HHVBP financial model calculator."""

    # ========== HHVBP CONSTANTS (CY 2026) ==========

    # Benchmark values (National Averages for CY 2026)
    BENCHMARKS = {
        'improvement_in_ambulation': 53.2,
        'improvement_in_bathing': 67.1,
        'improvement_in_dyspnea': 57.9,
        'improvement_in_pain': 42.5,
        'improvement_in_medication_management': 38.1,
        'discharge_to_community': 61.8,
        'acute_care_hospitalization': 14.7,  # inverse: lower is better
        'ed_use_without_hospitalization': 8.2,  # inverse: lower is better
        'timely_initiation_of_care': 96.3,
        'hhcahps_communication': 72.0,
    }

    # Achievement Thresholds (10-20 points below benchmark for most measures)
    ACHIEVEMENT_THRESHOLDS = {
        'improvement_in_ambulation': 45.0,  # 8.2 below benchmark
        'improvement_in_bathing': 58.0,      # 9.1 below benchmark
        'improvement_in_dyspnea': 50.0,      # 7.9 below benchmark
        'improvement_in_pain': 35.0,         # 7.5 below benchmark
        'improvement_in_medication_management': 30.0,  # 8.1 below benchmark
        'discharge_to_community': 53.0,      # 8.8 below benchmark
        'acute_care_hospitalization': 22.0,  # inverse: HIGHER threshold (lower performance acceptable)
        'ed_use_without_hospitalization': 12.0,  # inverse: HIGHER threshold
        'timely_initiation_of_care': 90.0,   # 6.3 below benchmark
        'hhcahps_communication': 65.0,       # 7 below benchmark
    }

    # Measure Weights (CY 2026 - sum = 1.0)
    WEIGHTS = {
        'improvement_in_ambulation': 0.04,
        'improvement_in_bathing': 0.04,
        'improvement_in_dyspnea': 0.04,
        'improvement_in_pain': 0.04,
        'improvement_in_medication_management': 0.04,
        'discharge_to_community': 0.04,
        'acute_care_hospitalization': 0.055,
        'ed_use_without_hospitalization': 0.055,
        'timely_initiation_of_care': 0.03,
        'hhcahps_communication': 0.08,
    }

    # Maximum bonus points per measure (achieved when at/above benchmark)
    MAX_BONUS_POINTS = 10

    # Payment adjustment range
    MIN_PAYMENT_ADJUSTMENT = -0.08  # -8%
    MAX_PAYMENT_ADJUSTMENT = 0.08   # +8%

    # TPS breakeven point: where payment adjustment = 0%
    BREAKEVEN_TPS = 50.0

    def __init__(self, annual_revenue: float):
        """
        Initialize the HHVBP model for an agency.

        Args:
            annual_revenue: Annual Medicare revenue in dollars
        """
        self.annual_revenue = annual_revenue
        self.performance = {}  # Will store agency performance metrics
        self.scores = {}       # Will store calculated scores
        self.tps = None        # Total Performance Score
        self.payment_adjustment_pct = None
        self.payment_adjustment_dollars = None

    def set_performance(self, measure_name: str, agency_rate: float) -> None:
        """
        Set agency performance for a specific HHVBP measure.

        Args:
            measure_name: Name of the measure (must match keys in BENCHMARKS)
            agency_rate: Agency's performance rate as a percentage (0-100)
        """
        if measure_name not in self.BENCHMARKS:
            raise ValueError(f"Unknown measure: {measure_name}")
        self.performance[measure_name] = agency_rate

    def set_all_performance(self, performance_dict: Dict[str, float]) -> None:
        """
        Set all agency performance metrics at once.

        Args:
            performance_dict: Dictionary of measure_name -> agency_rate
        """
        for measure_name, rate in performance_dict.items():
            self.set_performance(measure_name, rate)

    def calculate_measure_score(self, measure_name: str) -> Tuple[float, float, float]:
        """
        Calculate achievement score + benchmark bonus for a single measure.

        Scoring Logic:
        1. Achievement Score (0-10 points):
           - If agency < achievement threshold: score = 0
           - If achievement threshold <= agency < benchmark:
             score = (agency - achievement_threshold) / (benchmark - achievement_threshold) * 10
           - If agency >= benchmark: score = 10

        2. Benchmark Bonus (0-10 points):
           - If agency >= benchmark: bonus = min(10, (agency - benchmark))
           - Otherwise: bonus = 0

        3. For INVERSE measures (hospitalization, ED use):
           - Logic is reversed: lower is better
           - Achievement threshold is HIGHER than benchmark
           - If agency > threshold: score = 0
           - If benchmark < agency <= threshold:
             score = (threshold - agency) / (threshold - benchmark) * 10
           - If agency <= benchmark: score = 10 + bonus

        Returns:
            Tuple of (achievement_score, benchmark_bonus, total_measure_score)
        """
        agency_rate = self.performance.get(measure_name)
        if agency_rate is None:
            raise ValueError(f"Performance data not provided for {measure_name}")

        benchmark = self.BENCHMARKS[measure_name]
        threshold = self.ACHIEVEMENT_THRESHOLDS[measure_name]

        # Identify inverse measures (where lower performance is better)
        inverse_measures = [
            'acute_care_hospitalization',
            'ed_use_without_hospitalization'
        ]

        if measure_name in inverse_measures:
            # INVERSE MEASURE: lower is better
            # threshold > benchmark (e.g., threshold=22%, benchmark=14.7%)

            if agency_rate > threshold:
                # Below threshold: poor performance
                achievement_score = 0.0
            elif benchmark <= agency_rate <= threshold:
                # Between benchmark and threshold: partial credit
                achievement_score = ((threshold - agency_rate) /
                                   (threshold - benchmark)) * 10
            else:  # agency_rate < benchmark
                # At or above benchmark: full achievement
                achievement_score = 10.0

            # Bonus: only if at or above benchmark
            if agency_rate <= benchmark:
                bonus = min(10.0, (benchmark - agency_rate))
            else:
                bonus = 0.0
        else:
            # NORMAL MEASURE: higher is better
            # threshold < benchmark (e.g., threshold=45%, benchmark=53.2%)

            if agency_rate < threshold:
                # Below threshold: no achievement
                achievement_score = 0.0
            elif threshold <= agency_rate < benchmark:
                # Between threshold and benchmark: partial credit
                achievement_score = ((agency_rate - threshold) /
                                   (benchmark - threshold)) * 10
            else:  # agency_rate >= benchmark
                # At or above benchmark: full achievement
                achievement_score = 10.0

            # Bonus: only if at or above benchmark
            if agency_rate >= benchmark:
                bonus = min(10.0, (agency_rate - benchmark))
            else:
                bonus = 0.0

        total_score = achievement_score + bonus
        return achievement_score, bonus, total_score

    def calculate_tps(self) -> float:
        """
        Calculate Total Performance Score (TPS) using weighted achievement and bonus scores.

        TPS = Sum(measure_weight * (achievement_score + benchmark_bonus)) / 20 * 100

        The denominator of 20 is used because each measure can have a max of 20 points
        (10 achievement + 10 bonus), and we want TPS to be on a 0-100 scale.

        Returns:
            Total Performance Score (0-100)
        """
        total_weighted_points = 0.0

        for measure_name in self.BENCHMARKS.keys():
            if measure_name not in self.performance:
                raise ValueError(f"Missing performance data for {measure_name}")

            _, _, measure_score = self.calculate_measure_score(measure_name)
            weight = self.WEIGHTS[measure_name]

            # Weighted contribution: (score out of 20) * weight * 100
            weighted_contribution = (measure_score / 20.0) * weight * 100
            total_weighted_points += weighted_contribution

            self.scores[measure_name] = {
                'agency_performance': self.performance[measure_name],
                'benchmark': self.BENCHMARKS[measure_name],
                'threshold': self.ACHIEVEMENT_THRESHOLDS[measure_name],
                'achievement_score': self.calculate_measure_score(measure_name)[0],
                'bonus_score': self.calculate_measure_score(measure_name)[1],
                'total_measure_score': measure_score,
                'weight': weight,
                'weighted_points': weighted_contribution,
            }

        self.tps = total_weighted_points
        return self.tps

    def calculate_payment_adjustment(self) -> Tuple[float, float]:
        """
        Map Total Performance Score (TPS) to payment adjustment percentage.

        Linear Interpolation Logic:
        - TPS = 100: payment adjustment = +8.0%
        - TPS = 50: payment adjustment = 0% (breakeven)
        - TPS = 0: payment adjustment = -8.0%

        Formula:
        adjustment% = ((TPS - 50) / 50) * 8%

        Returns:
            Tuple of (payment_adjustment_pct, payment_adjustment_dollars)
        """
        if self.tps is None:
            self.calculate_tps()

        # Linear interpolation: maps TPS 0-100 to adjustment -8% to +8%
        adjustment_pct = ((self.tps - self.BREAKEVEN_TPS) / self.BREAKEVEN_TPS) * 0.08

        # Clamp to min/max range
        adjustment_pct = max(self.MIN_PAYMENT_ADJUSTMENT,
                            min(self.MAX_PAYMENT_ADJUSTMENT, adjustment_pct))

        adjustment_dollars = self.annual_revenue * adjustment_pct

        self.payment_adjustment_pct = adjustment_pct
        self.payment_adjustment_dollars = adjustment_dollars

        return adjustment_pct, adjustment_dollars

    def sensitivity_analysis(self, measure_name: str,
                            improvement_points: float) -> Dict:
        """
        Run sensitivity analysis: what happens if a single measure improves by N points?

        Args:
            measure_name: Name of the measure to improve
            improvement_points: How many percentage points to improve (e.g., 5 for +5%)

        Returns:
            Dictionary with baseline and improved TPS/adjustment
        """
        # Baseline calculation
        baseline_tps = self.tps or self.calculate_tps()
        baseline_adj_pct, baseline_adj_dollars = (
            self.payment_adjustment_pct,
            self.payment_adjustment_dollars
        ) or self.calculate_payment_adjustment()

        # Create a copy and improve the measure
        original_performance = self.performance[measure_name]
        self.performance[measure_name] += improvement_points

        # Recalculate scores (reset cached scores for this measure)
        if measure_name in self.scores:
            del self.scores[measure_name]

        improved_tps = self.calculate_tps()
        improved_adj_pct, improved_adj_dollars = self.calculate_payment_adjustment()

        # Restore original performance
        self.performance[measure_name] = original_performance

        return {
            'measure': measure_name,
            'baseline_performance': original_performance,
            'improved_performance': original_performance + improvement_points,
            'improvement_points': improvement_points,
            'baseline_tps': baseline_tps,
            'improved_tps': improved_tps,
            'tps_impact': improved_tps - baseline_tps,
            'baseline_adjustment_pct': baseline_adj_pct,
            'improved_adjustment_pct': improved_adj_pct,
            'adjustment_pct_impact': improved_adj_pct - baseline_adj_pct,
            'baseline_adjustment_dollars': baseline_adj_dollars,
            'improved_adjustment_dollars': improved_adj_dollars,
            'adjustment_dollars_impact': improved_adj_dollars - baseline_adj_dollars,
        }

    def get_scenario_analysis(self, scenario_type: str) -> Dict:
        """
        Generate a specific scenario (best case, worst case, etc).

        Args:
            scenario_type: 'best_case', 'worst_case', or 'break_even'

        Returns:
            Dictionary with scenario performance and results
        """
        original_performance = dict(self.performance)

        if scenario_type == 'best_case':
            # All measures at benchmark
            for measure in self.BENCHMARKS.keys():
                self.performance[measure] = self.BENCHMARKS[measure]

        elif scenario_type == 'worst_case':
            # All measures 10 points below benchmark
            for measure in self.BENCHMARKS.keys():
                self.performance[measure] = self.BENCHMARKS[measure] - 10

        # Reset cached calculations
        self.tps = None
        self.payment_adjustment_pct = None
        self.payment_adjustment_dollars = None
        self.scores = {}

        tps = self.calculate_tps()
        adj_pct, adj_dollars = self.calculate_payment_adjustment()

        result = {
            'scenario': scenario_type,
            'performance': dict(self.performance),
            'tps': tps,
            'payment_adjustment_pct': adj_pct,
            'payment_adjustment_dollars': adj_dollars,
        }

        # Restore original
        self.performance = original_performance
        self.tps = None
        self.payment_adjustment_pct = None
        self.payment_adjustment_dollars = None
        self.scores = {}

        return result

    def generate_report(self) -> str:
        """
        Generate a comprehensive text report of the HHVBP analysis.

        Returns:
            Formatted report string
        """
        if self.tps is None:
            self.calculate_tps()
        if self.payment_adjustment_pct is None:
            self.calculate_payment_adjustment()

        report = []
        report.append("=" * 80)
        report.append("HHVBP FINANCIAL MODEL ANALYSIS REPORT")
        report.append(f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}")
        report.append("=" * 80)
        report.append("")

        # Executive Summary
        report.append("EXECUTIVE SUMMARY")
        report.append("-" * 80)
        report.append(f"Annual Medicare Revenue:           ${self.annual_revenue:,.2f}")
        report.append(f"Total Performance Score (TPS):     {self.tps:.1f} / 100")
        report.append(f"Payment Adjustment:                {self.payment_adjustment_pct*100:+.2f}%")
        report.append(f"Dollar Impact (Annual):            ${self.payment_adjustment_dollars:+,.2f}")
        report.append("")

        # Interpretation
        if self.tps >= 75:
            interpretation = "EXCELLENT - Performing well above national averages"
        elif self.tps >= 60:
            interpretation = "GOOD - Performing above national averages"
        elif self.tps >= 50:
            interpretation = "ACCEPTABLE - Performing near national averages"
        else:
            interpretation = "NEEDS IMPROVEMENT - Performing below national averages"

        report.append(f"Assessment: {interpretation}")
        report.append("")

        # Measure-by-Measure Breakdown
        report.append("MEASURE-BY-MEASURE PERFORMANCE ANALYSIS")
        report.append("-" * 80)

        for measure_name in sorted(self.scores.keys()):
            score_data = self.scores[measure_name]
            report.append(f"\n{measure_name.replace('_', ' ').title()}")
            report.append(f"  Agency Performance:    {score_data['agency_performance']:.1f}%")
            report.append(f"  Achievement Threshold: {score_data['threshold']:.1f}%")
            report.append(f"  National Benchmark:    {score_data['benchmark']:.1f}%")
            report.append(f"  Achievement Score:     {score_data['achievement_score']:.1f} / 10")
            report.append(f"  Benchmark Bonus:       {score_data['bonus_score']:.1f} / 10")
            report.append(f"  Measure Score:         {score_data['total_measure_score']:.1f} / 20")
            report.append(f"  Weight:                {score_data['weight']*100:.1f}%")
            report.append(f"  Weighted Points:       {score_data['weighted_points']:.2f}")

        report.append("")
        report.append("")
        report.append("=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)

        return "\n".join(report)

    def to_json(self) -> Dict:
        """
        Export results as a JSON-serializable dictionary.

        Returns:
            Dictionary suitable for JSON serialization
        """
        if self.tps is None:
            self.calculate_tps()
        if self.payment_adjustment_pct is None:
            self.calculate_payment_adjustment()

        return {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'annual_revenue': self.annual_revenue,
            },
            'summary': {
                'total_performance_score': self.tps,
                'payment_adjustment_pct': self.payment_adjustment_pct,
                'payment_adjustment_dollars': self.payment_adjustment_dollars,
            },
            'performance': self.performance,
            'benchmarks': self.BENCHMARKS,
            'thresholds': self.ACHIEVEMENT_THRESHOLDS,
            'measure_scores': {k: v for k, v in self.scores.items()},
        }


def main():
    """Main entry point for command-line usage."""

    parser = argparse.ArgumentParser(
        description='HHVBP Financial Model Calculator'
    )
    parser.add_argument('--revenue', type=float, default=500000,
                       help='Annual Medicare revenue (default: $500,000)')
    parser.add_argument('--ambulation', type=float, default=48.0,
                       help='Improvement in Ambulation % (default: 48.0)')
    parser.add_argument('--bathing', type=float, default=62.0,
                       help='Improvement in Bathing % (default: 62.0)')
    parser.add_argument('--dyspnea', type=float, default=54.0,
                       help='Improvement in Dyspnea % (default: 54.0)')
    parser.add_argument('--pain', type=float, default=38.0,
                       help='Improvement in Pain % (default: 38.0)')
    parser.add_argument('--medication', type=float, default=41.0,
                       help='Improvement in Medication Management % (default: 41.0)')
    parser.add_argument('--discharge', type=float, default=52.0,
                       help='Discharge to Community % (default: 52.0)')
    parser.add_argument('--hospitalization', type=float, default=24.0,
                       help='Acute Care Hospitalization % (default: 24.0)')
    parser.add_argument('--ed-use', type=float, default=10.0,
                       help='ED Use Without Hospitalization % (default: 10.0)')
    parser.add_argument('--timely-initiation', type=float, default=92.0,
                       help='Timely Initiation of Care % (default: 92.0)')
    parser.add_argument('--hhcahps', type=float, default=70.0,
                       help='HHCAHPS Communication Composite % (default: 70.0)')
    parser.add_argument('--json-output', type=str, default=None,
                       help='Save JSON results to file')

    args = parser.parse_args()

    # Initialize model
    model = HHVBPModel(args.revenue)

    # Set performance (using Sunrise Home Health default data)
    model.set_all_performance({
        'improvement_in_ambulation': args.ambulation,
        'improvement_in_bathing': args.bathing,
        'improvement_in_dyspnea': args.dyspnea,
        'improvement_in_pain': args.pain,
        'improvement_in_medication_management': args.medication,
        'discharge_to_community': args.discharge,
        'acute_care_hospitalization': args.hospitalization,
        'ed_use_without_hospitalization': args.ed_use,
        'timely_initiation_of_care': args.timely_initiation,
        'hhcahps_communication': args.hhcahps,
    })

    # Calculate metrics
    model.calculate_tps()
    model.calculate_payment_adjustment()

    # Print report
    print(model.generate_report())

    # Save JSON if requested
    if args.json_output:
        with open(args.json_output, 'w') as f:
            json.dump(model.to_json(), f, indent=2)
        print(f"\nJSON results saved to: {args.json_output}")


if __name__ == '__main__':
    main()
