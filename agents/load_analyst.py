"""Load Analyst Agent - Analyzes load profiles."""
from typing import Dict, Any
import pandas as pd
from calculations.load import analyze_load_profile
from .orchestrator import Agent, call_llm


class LoadAnalyst(Agent):
    """Agent responsible for load profile analysis."""

    def __init__(self):
        super().__init__("Load Analyst", "Inspect load profile and calculate key metrics")

    def get_system_prompt(self) -> str:
        return """You are a Load Analysis Engineer reviewing a commercial building's electrical load profile.

Your job is to:
1. Understand the load characteristics (peak, average, variability)
2. Identify the peak period duration
3. Assess whether the load profile supports the project objective
4. Flag any concerns or unusual patterns
5. Make findings clear and actionable

Base your analysis on the numerical calculations provided, not speculation.
If data is missing, say so explicitly.
Do not hallucinate numbers."""

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze load profile from context."""
        # Extract load data and calculations
        load_kw = context.get("load_series")
        load_stats = context.get("load_statistics", {})
        peak_duration = context.get("peak_duration_hours", 0)

        if load_kw is None:
            return {
                "agent_name": self.name,
                "role": self.role,
                "error": "No load data provided",
                "findings": [],
                "concerns": [],
                "key_metrics": {},
                "structured_output": {}
            }

        # Run deterministic calculations
        analysis = analyze_load_profile(load_kw)

        # Prepare message for LLM
        user_message = f"""
Load Profile Analysis Results:
- Peak demand: {analysis['peak_demand_kw']:.1f} kW
- Average demand: {analysis['average_demand_kw']:.1f} kW
- Daily energy: {analysis['daily_energy_kwh']:.1f} kWh
- Peak duration (at ≥90% of peak): {analysis['peak_duration_hours']:.2f} hours
- Load range: {analysis['load_range_kw'][0]:.1f}–{analysis['load_range_kw'][1]:.1f} kW

Project Objective: {context.get('project_objective', 'Unknown')}

Provide a brief analysis in JSON format with:
- summary: key findings from the load profile
- peak_characteristics: description of peak behavior
- concerns: any issues detected
- confidence_level: High/Medium/Low
"""

        response = call_llm(self.get_system_prompt(), user_message, json_mode=False)

        return {
            "agent_name": self.name,
            "role": self.role,
            "findings": analysis["findings"],
            "concerns": [],
            "key_metrics": {
                "peak_demand_kw": analysis["peak_demand_kw"],
                "average_demand_kw": analysis["average_demand_kw"],
                "daily_energy_kwh": analysis["daily_energy_kwh"],
                "peak_duration_hours": analysis["peak_duration_hours"],
            },
            "structured_output": analysis,
            "llm_analysis": response,
            "confidence": "High"  # Based on data, not LLM
        }
