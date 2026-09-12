"""Specification Engineer Agent - Reviews technical documents."""
from typing import Dict, Any
from utils.rag import SimpleRAG, extract_specifications_from_text
from .orchestrator import Agent, call_llm


class SpecificationEngineer(Agent):
    """Agent responsible for document review and specification extraction."""

    def __init__(self):
        super().__init__("Specification Engineer", "Extract and validate equipment specifications from documents")
        self.rag = SimpleRAG()

    def add_document(self, content: str, name: str):
        """Add a document to the RAG system."""
        self.rag.add_text(content, name)

    def get_system_prompt(self) -> str:
        return """You are a Specification Review Engineer examining technical equipment specifications.

Your responsibilities:
1. Extract key equipment parameters (capacity, efficiency, limits)
2. Identify missing critical information
3. Detect conflicting specifications
4. Verify specifications match project requirements
5. Source evidence from documents

Never invent specifications. If something is not in the documents, say so explicitly.
Flag any ambiguities or contradictions clearly."""

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze specifications from documents and project info."""
        project_specs = context.get("project_specs", {})
        doc_list = self.rag.get_document_list()

        findings = []
        concerns = []

        # Extract specs from documents
        all_specs = {}
        for doc_name in doc_list:
            content = self.rag.get_document_content(doc_name)
            specs = extract_specifications_from_text(content)
            all_specs[doc_name] = specs

        # Prepare LLM message
        doc_summary = f"Documents available: {len(doc_list)}\n"
        for doc in doc_list:
            doc_summary += f"  - {doc}\n"

        project_summary = f"""
Project Specifications:
- PV Capacity: {project_specs.get('pv_capacity_kw', 'Not specified')} kW
- BESS Energy: {project_specs.get('bess_energy_kwh', 'Not specified')} kWh
- BESS Power: {project_specs.get('bess_power_kw', 'Not specified')} kW
- BESS Efficiency: {project_specs.get('bess_efficiency', 'Not specified')}

{doc_summary}
"""

        user_message = f"""
{project_summary}

Based on the extracted specifications, assess:
1. Are project specs supported by documents?
2. Are there conflicting specifications?
3. What critical information is missing?

Provide analysis in JSON format.
"""

        response = call_llm(self.get_system_prompt(), user_message, json_mode=False)

        if doc_list:
            findings.append(f"Reviewed {len(doc_list)} documents")
        else:
            concerns.append("No specification documents uploaded")

        return {
            "agent_name": self.name,
            "role": self.role,
            "findings": findings,
            "concerns": concerns,
            "key_metrics": {
                "documents_reviewed": len(doc_list),
            },
            "structured_output": {
                "documents": doc_list,
                "extracted_specs": all_specs,
            },
            "llm_analysis": response,
            "confidence": "High" if doc_list else "Low"
        }
