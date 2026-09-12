"""Independent Critic Agent - Challenges conclusions and identifies conflicts."""
from typing import Dict, Any, List
from .orchestrator import Agent, call_llm


class IndependentCritic(Agent):
    """Agent responsible for critical review of all findings."""

    def __init__(self):
        super().__init__("Independent Critic", "Challenge conclusions and identify conflicts")

    def get_system_prompt(self) -> str:
        return """You are an Independent Engineering Critic reviewing a complex project analysis.

Your role is NOT to summarize. Your role is to:
1. Identify conflicts between agents
2. Question unsupported assumptions
3. Find missing critical information
4. Assess confidence levels realistically
5. Spot red flags or contradictions
6. Challenge overconfident conclusions

Be specific about conflicts, not vague.
Make clear recommendations for verification.
Never accept an answer just because an "expert" said it."""

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Critique all other agent findings."""
        agent_results = context.get("agent_results", {})
        conflicts_detected = context.get("conflicts_detected", [])

        # Extract key numbers for conflict checking
        user_message = self._build_critique_prompt(agent_results, conflicts_detected)

        response = call_llm(self.get_system_prompt(), user_message, json_mode=False)

        findings = []
        concerns = []

        # Add detected conflicts to findings
        for conflict in conflicts_detected:
            concerns.append(f"CONFLICT: {conflict.get('issue', 'Unknown')}")

        # Add unsupported assumptions
        assumptions = self._extract_unsupported_assumptions(agent_results)
        for assumption in assumptions:
            findings.append(f"Unsupported assumption: {assumption}")

        # Add missing information
        missing = self._extract_missing_info(agent_results)
        for info in missing:
            concerns.append(f"Missing: {info}")

        return {
            "agent_name": self.name,
            "role": self.role,
            "findings": findings,
            "concerns": concerns,
            "key_metrics": {
                "conflicts_identified": len(conflicts_detected),
                "unsupported_assumptions": len(assumptions),
                "missing_info_items": len(missing),
            },
            "structured_output": {
                "conflicts": conflicts_detected,
                "unsupported_assumptions": assumptions,
                "missing_info": missing,
            },
            "llm_analysis": response,
            "confidence": "High"
        }

    def _build_critique_prompt(self, agent_results: Dict, conflicts: List) -> str:
        """Build comprehensive critique prompt."""
        prompt = "Agent Findings Summary:\n\n"

        for agent_name, result in agent_results.items():
            prompt += f"## {agent_name}\n"
            prompt += f"Findings: {', '.join(result.get('findings', []))}\n"
            prompt += f"Concerns: {', '.join(result.get('concerns', []))}\n"
            prompt += f"Confidence: {result.get('confidence', 'Unknown')}\n\n"

        prompt += "\n## Detected Conflicts:\n"
        for conflict in conflicts:
            prompt += f"- {conflict.get('issue')}: {conflict.get('agent_1')} vs {conflict.get('agent_2')}\n"

        prompt += """
As the Independent Critic, analyze:
1. Do the numerical findings contradict each other?
2. Are there unsupported leaps in reasoning?
3. What critical data is missing?
4. Are conclusions appropriately qualified?
5. What verification is absolutely necessary before proceeding?
"""
        return prompt

    def _extract_unsupported_assumptions(self, agent_results: Dict) -> List[str]:
        """Extract unsupported assumptions from results."""
        assumptions = []
        for agent_name, result in agent_results.items():
            if "concerns" in result:
                for concern in result["concerns"]:
                    if "assume" in concern.lower() or "not" in concern.lower():
                        assumptions.append(concern)
        return assumptions[:5]  # Top 5

    def _extract_missing_info(self, agent_results: Dict) -> List[str]:
        """Extract missing information from results."""
        missing = []
        for agent_name, result in agent_results.items():
            if "concerns" in result:
                for concern in result["concerns"]:
                    if "missing" in concern.lower() or "not provided" in concern.lower():
                        missing.append(concern)
        return missing[:5]  # Top 5
