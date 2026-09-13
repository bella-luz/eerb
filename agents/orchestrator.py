"""Agent orchestration and coordination."""
import json
from typing import Dict, List, Any
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def call_llm(system_prompt: str, user_message: str, json_mode: bool = False) -> str:
    """
    Call OpenAI API with structured prompts.

    Args:
        system_prompt: System instructions for the agent
        user_message: The actual question/task
        json_mode: If True, request JSON output

    Returns:
        The LLM response as a string
    """
    try:
        kwargs = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 1500,
        }

        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content

    except Exception as e:
        return f"ERROR: {str(e)}"


def parse_json_response(response: str) -> Dict[str, Any]:
    """Safely parse JSON from LLM response."""
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        # Try to extract JSON from response
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        return {"raw_response": response, "parse_error": True}


class Agent:
    """Base agent class."""

    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def get_system_prompt(self) -> str:
        """Override in subclass."""
        raise NotImplementedError

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Override in subclass."""
        raise NotImplementedError


class AgentOrchestrator:
    """Orchestrates multiple agents."""

    def __init__(self):
        self.agents = {}
        self.results = {}
        self.conflicts = []

    def register_agent(self, agent: Agent):
        """Register an agent."""
        self.agents[agent.name] = agent

    def run_all(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run all agents sequentially and collect results."""
        results = {}

        for agent_name, agent in self.agents.items():
            try:
                result = agent.analyze(context)
                results[agent_name] = result
            except Exception as e:
                results[agent_name] = {
                    "error": str(e),
                    "findings": [],
                    "concerns": []
                }

        self.results = results
        return results

    def detect_conflicts(self) -> List[Dict[str, Any]]:
        """Detect conflicts between agent findings."""
        conflicts = []

        # Example conflict detection logic
        # This would be customized based on agent outputs
        results = self.results

        if "Load Analyst" in results and "BESS Engineer" in results:
            load_result = results["Load Analyst"]
            bess_result = results["BESS Engineer"]

            # Extract key metrics
            peak_duration = load_result.get("key_metrics", {}).get("peak_duration_hours", 0)
            battery_duration = bess_result.get("key_metrics", {}).get("battery_duration_hours", 0)

            if peak_duration > 0 and battery_duration > 0:
                if battery_duration < peak_duration:
                    gap = peak_duration - battery_duration
                    conflicts.append({
                        "issue": "Battery Duration Insufficient for Peak Load",
                        "agent_1": "Load Analyst",
                        "agent_1_statement": f"Peak duration: {peak_duration:.2f} hours",
                        "agent_2": "BESS Engineer",
                        "agent_2_statement": f"Battery duration: {battery_duration:.2f} hours",
                        "severity": "High",
                        "explanation": f"Battery can discharge for {battery_duration:.2f} hours, but peak demand lasts {peak_duration:.2f} hours. "
                                     f"Gap: {gap:.2f} hours of unmet demand. Battery cannot support full peak-shaving objective."
                    })

        self.conflicts = conflicts
        return conflicts

    def summarize(self) -> Dict[str, Any]:
        """Summarize all agent results."""
        return {
            "total_agents": len(self.agents),
            "completed_agents": len([r for r in self.results.values() if "error" not in r]),
            "results": self.results,
            "conflicts_detected": len(self.conflicts),
            "conflicts": self.conflicts
        }
