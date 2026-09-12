"""PV Engineer Agent - Analyzes PV adequacy."""
from typing import Dict, Any
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculations.pv import analyze_pv
from .orchestrator import Agent, call_llm


class PVEngineer(Agent):
    """Agent responsible for PV system analysis."""

    def __init__(self):
        super().__init__("PV Engineer", "Evaluate PV capacity and generation adequacy")

    def get_system_prompt(self) -> str:
        return """You are a Solar PV Engineer reviewing a proposed photovoltaic system.

Your responsibilities:
1. Assess PV capacity relative to peak and average load
2. Evaluate estimated energy generation
3. Identify missing PV assumptions (seasonal variation, tilt, azimuth)
4. Compare PV to BESS strategy alignment
5. Flag practical concerns

Base conclusions on calculations, not assumptions.
Clearly state what information is missing."""

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze PV system from context."""
        pv_capacity_kw = context.get("pv_capacity_kw", 0)
        pv_kw = context.get("pv_series")
        peak_load_kw = context.get("peak_load_kw", 0)
        avg_load_kw = context.get("average_load_kw", 0)
        daily_load_kwh = context.get("daily_load_kwh", 0)

        if pv_capacity_kw <= 0:
            return {
                "agent_name": self.name,
                "role": self.role,
                "findings": ["No PV capacity specified"],
                "concerns": ["PV system not defined"],
                "key_metrics": {},
                "structured_output": {},
                "confidence": "N/A"
            }

        # Calculate PV generation
        daily_pv_kwh = 0
        if pv_kw is not None:
            daily_pv_kwh = pv_kw.sum() * 0.25  # 15-min intervals

        analysis = analyze_pv(pv_capacity_kw, daily_pv_kwh, peak_load_kw,
                            avg_load_kw, daily_load_kwh)

        user_message = f"""
PV System Analysis:
- PV Capacity: {pv_capacity_kw:.0f} kW
- Estimated daily generation: {daily_pv_kwh:.0f} kWh (from provided profile)
- Peak load: {peak_load_kw:.0f} kW
- Average load: {avg_load_kw:.0f} kW
- Daily load: {daily_load_kwh:.0f} kWh
- PV-to-peak ratio: {analysis['pv_to_peak_ratio']:.2f}
- Load coverage: {analysis['load_coverage_percent']:.0f}%

Provide assessment in JSON format with:
- findings: key observations
- concerns: any issues
- confidence_level: High/Medium/Low
"""

        response = call_llm(self.get_system_prompt(), user_message, json_mode=False)

        return {
            "agent_name": self.name,
            "role": self.role,
            "findings": analysis["findings"],
            "concerns": analysis["concerns"],
            "key_metrics": {
                "pv_capacity_kw": pv_capacity_kw,
                "daily_generation_kwh": daily_pv_kwh,
                "pv_to_peak_ratio": analysis["pv_to_peak_ratio"],
                "load_coverage_percent": analysis["load_coverage_percent"],
            },
            "structured_output": analysis,
            "llm_analysis": response,
            "confidence": "High"
        }
