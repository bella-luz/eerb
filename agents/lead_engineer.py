"""Lead Engineer Agent - Synthesizes all findings into final review."""
from typing import Dict, Any
from .orchestrator import Agent, call_llm


class LeadEngineer(Agent):
    """Agent responsible for synthesizing all findings into final review."""

    def __init__(self):
        super().__init__("Lead Engineer", "Synthesize all findings into final engineering review")

    def get_system_prompt(self) -> str:
        return """You are the Lead Engineering Review Officer synthesizing a comprehensive technical review.

Your role:
1. Synthesize all specialist findings
2. Produce a clear overall assessment
3. Identify the TOP 3-5 items requiring professional verification
4. State confidence level realistically
5. Give actionable next steps

Format:
- Be concise but complete
- Use clear language, avoid jargon
- Distinguish facts from interpretations
- Make clear recommendations

Remember: This is a PRELIMINARY review, not final engineering sign-off."""

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize all findings into final review."""
        agent_results = context.get("agent_results", {})
        conflicts = context.get("conflicts_detected", [])
        critic_findings = context.get("critic_findings", {})
        project_info = context.get("project_info", {})

        user_message = self._build_synthesis_prompt(
            agent_results, conflicts, critic_findings, project_info
        )

        response = call_llm(self.get_system_prompt(), user_message, json_mode=False)

        # Determine overall status
        overall_status = self._determine_status(conflicts, critic_findings)

        return {
            "agent_name": self.name,
            "role": self.role,
            "findings": self._extract_key_findings(agent_results),
            "concerns": self._extract_critical_concerns(conflicts, critic_findings),
            "key_metrics": {
                "overall_status": overall_status,
                "conflicts_found": len(conflicts),
            },
            "structured_output": {
                "overall_status": overall_status,
                "llm_synthesis": response,
            },
            "llm_analysis": response,
            "confidence": "Medium" if len(conflicts) > 0 else "High"
        }

    def _build_synthesis_prompt(self, agent_results: Dict, conflicts: List,
                               critic_findings: Dict, project_info: Dict) -> str:
        """Build comprehensive synthesis prompt."""
        prompt = f"""
PROJECT INFORMATION:
- Name: {project_info.get('project_name', 'Unknown')}
- Type: {project_info.get('project_type', 'Unknown')}
- Objective: {project_info.get('objective', 'Unknown')}

AGENT SUMMARY:
"""
        for agent_name, result in agent_results.items():
            metrics = result.get("key_metrics", {})
            findings = result.get("findings", [])
            prompt += f"\n{agent_name}:\n"
            for finding in findings[:2]:  # Top 2 findings
                prompt += f"  - {finding}\n"

        if conflicts:
            prompt += "\nCRITICAL CONFLICTS IDENTIFIED:\n"
            for conflict in conflicts:
                prompt += f"  - {conflict.get('issue', 'Unknown')}\n"
                prompt += f"    {conflict.get('explanation', '')}\n"

        prompt += """
SYNTHESIS TASK:
Based on the above findings, provide:
1. Executive summary (1-2 sentences)
2. Overall design assessment
3. Top 3-5 items requiring professional verification
4. Confidence level and rationale
5. Recommended next steps

Remember: This is preliminary review only.
"""
        return prompt

    def _determine_status(self, conflicts: List, critic_findings: Dict) -> str:
        """Determine overall review status."""
        if len(conflicts) == 0 and len(critic_findings.get("concerns", [])) < 3:
            return "Preliminary Design Appears Consistent"
        elif len(conflicts) < 3:
            return "Review Required"
        else:
            return "Significant Issues Identified"

    def _extract_key_findings(self, agent_results: Dict) -> List[str]:
        """Extract top findings from all agents."""
        findings = []
        for agent_name, result in agent_results.items():
            agent_findings = result.get("findings", [])
            if agent_findings:
                findings.append(agent_findings[0])  # Top finding
        return findings

    def _extract_critical_concerns(self, conflicts: List, critic_findings: Dict) -> List[str]:
        """Extract critical concerns."""
        concerns = []
        for conflict in conflicts:
            concerns.append(f"CONFLICT: {conflict.get('issue', 'Unknown')}")
        for concern in critic_findings.get("concerns", [])[:3]:
            concerns.append(concern)
        return concerns
