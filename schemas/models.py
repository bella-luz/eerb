"""Data models for EERB agent outputs."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class Finding(BaseModel):
    """A single finding from an agent."""
    issue: str
    severity: str  # Critical, High, Medium, Low
    evidence: str
    confidence: str  # High, Medium, Low
    requires_verification: bool = False


class AgentResult(BaseModel):
    """Result from a single agent."""
    agent_name: str
    role: str
    findings: List[str]
    concerns: List[str]
    key_metrics: Dict[str, Any]
    structured_output: Dict[str, Any]
    confidence: str  # High, Medium, Low


class Conflict(BaseModel):
    """A detected conflict between agents."""
    issue_title: str
    agent_1_name: str
    agent_1_statement: str
    agent_2_name: str
    agent_2_statement: str
    severity: str  # High, Medium, Low
    explanation: str


class MissingInformation(BaseModel):
    """Missing data that affects analysis."""
    item: str
    impact: str
    severity: str


class Recommendation(BaseModel):
    """A recommendation from the system."""
    action: str
    rationale: str
    priority: str  # High, Medium, Low


class CriticFinding(BaseModel):
    """Finding from the Independent Critic agent."""
    conflicts: List[Conflict]
    unsupported_assumptions: List[str]
    missing_critical_info: List[MissingInformation]
    confidence_assessment: str
    recommendations: List[Recommendation]


class FinalReview(BaseModel):
    """Final review synthesis from Lead Engineer."""
    executive_summary: str
    overall_status: str  # Preliminary Design Appears Consistent, Review Required, Significant Issues
    key_findings: List[str]
    recommendations: List[str]
    confidence_level: str
    items_requiring_verification: List[str]
    disclaimer: str


class ProjectInput(BaseModel):
    """User-provided project information."""
    project_name: str
    project_type: str
    location: str
    objective: str
    pv_capacity_kw: float
    bess_energy_kwh: float
    bess_power_kw: float
    bess_efficiency: float = 0.90
    bess_min_soc: float = 0.10
    bess_max_soc: float = 0.95
    load_csv_path: Optional[str] = None
    pv_csv_path: Optional[str] = None
    documents: List[str] = []


class ReviewOutput(BaseModel):
    """Complete review output."""
    project_input: ProjectInput
    agent_results: Dict[str, AgentResult]
    conflicts: List[Conflict]
    missing_info: List[MissingInformation]
    critic_findings: CriticFinding
    final_review: FinalReview
    calculations: Dict[str, Any]
