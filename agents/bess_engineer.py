"""BESS Engineer Agent - Analyzes battery storage system."""
from typing import Dict, Any
from calculations.battery import analyze_bess
from .orchestrator import Agent, call_llm


class BESSEngineer(Agent):
    """Agent responsible for battery energy storage system analysis."""

    def __init__(self):
        super().__init__("BESS Engineer", "Evaluate battery capacity and discharge capability")

    def get_system_prompt(self) -> str:
        return """You are a Battery Energy Storage Systems (BESS) Engineer reviewing a proposed energy storage system.

Your responsibilities:
1. Calculate battery discharge duration at rated power
2. Assess adequacy for peak-shaving objective
3. Identify SOC/efficiency considerations
4. Flag any over/undersizing issues
5. Compare BESS parameters against load requirements

Always be clear: battery duration is energy / power, nothing more.
Clearly state assumptions and flag conflicts with load profile."""

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze BESS from context."""
        bess_energy_kwh = context.get("bess_energy_kwh", 0)
        bess_power_kw = context.get("bess_power_kw", 0)
        bess_efficiency = context.get("bess_efficiency", 0.90)
        peak_load_kw = context.get("peak_load_kw", 0)
        peak_duration_hours = context.get("peak_duration_hours", 0)

        if bess_energy_kwh <= 0 or bess_power_kw <= 0:
            return {
                "agent_name": self.name,
                "role": self.role,
                "findings": ["No BESS specified"],
                "concerns": ["BESS system not defined"],
                "key_metrics": {},
                "structured_output": {},
                "confidence": "N/A"
            }

        # Run deterministic calculation
        analysis = analyze_bess(bess_energy_kwh, bess_power_kw, peak_load_kw,
                              peak_duration_hours, bess_efficiency)

        battery_duration = analysis["battery_duration_hours"]

        user_message = f"""
BESS Analysis Results:
- Energy capacity: {bess_energy_kwh:.0f} kWh
- Discharge power: {bess_power_kw:.0f} kW
- Round-trip efficiency: {bess_efficiency * 100:.0f}%
- Battery duration at rated power: {battery_duration:.2f} hours
- Peak load: {peak_load_kw:.0f} kW
- Peak duration: {peak_duration_hours:.2f} hours (from load analysis)

Assessment:
- Duration vs. peak: {battery_duration:.2f}h vs {peak_duration_hours:.2f}h

Provide analysis in JSON format with:
- findings: key points
- concerns: any issues or conflicts
- confidence_level: High/Medium/Low
"""

        response = call_llm(self.get_system_prompt(), user_message, json_mode=False)

        return {
            "agent_name": self.name,
            "role": self.role,
            "findings": analysis["findings"],
            "concerns": analysis["concerns"],
            "key_metrics": {
                "energy_capacity_kwh": bess_energy_kwh,
                "discharge_power_kw": bess_power_kw,
                "battery_duration_hours": battery_duration,
                "efficiency_percent": bess_efficiency * 100,
            },
            "structured_output": analysis,
            "llm_analysis": response,
            "confidence": "High"  # Based on calculation
        }
