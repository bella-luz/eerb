# ROLE

Act as a senior product manager, AI architect, energy-systems engineer, Python architect, and hackathon technical lead.

You are designing a working prototype called:

# Energy Engineering Review Board (EERB)

Tagline:

**"AI engineering review before you build."**

The product must be realistic to build and demonstrate in a single hackathon weekend by a small mixed technical/nontechnical team.

Do NOT design an unrealistic enterprise system that cannot be implemented in 1–2 days.

The PRD must clearly distinguish the MVP from future features.

---

# 1. PRODUCT CONCEPT

Energy Engineering Review Board is a multi-agent AI system that reviews a proposed renewable-energy project BEFORE detailed engineering or implementation.

The user provides project requirements, technical documents/specifications, and optionally load/project data.

The system creates an AI engineering review board consisting of specialized agents.

The agents independently examine different aspects of the proposed project.

The system then:

1. extracts project information
2. identifies assumptions
3. performs deterministic engineering calculations
4. checks consistency between requirements and specifications
5. identifies missing information
6. identifies contradictions or potential risks
7. allows agents to challenge each other's conclusions
8. performs an independent critic review
9. produces a lead-engineer conclusion
10. generates a traceable preliminary engineering review report

The product is NOT intended to replace professional engineers, ETAP, HOMER, PVsyst, PVcase, OpenDSS, or detailed engineering studies.

It is an AI-assisted preliminary design-review and decision-support layer.

---

# 2. DIFFERENTIATION — CRITICAL

The hackathon already contains projects involving:

A. SolarGrid Advisor:
- Pakistani household electricity bills
- solar investment
- NEPRA/DISCO regulations
- solar savings
- household solar sizing
- bill extraction
- Urdu/English
- RAG over regulatory documents

B. Smart Grid Operational Assistance:
- renewable-grid operation
- power-system constraints
- operational scenarios
- corrective strategies
- operational decision support

C. Grid Guard AI:
- abnormal electricity consumption
- electrical fault investigation
- load/electrical information
- deterministic electrical calculations
- anomaly detection
- RAG
- multi-agent analysis
- engineering recommendations
- engineering assessment reports

Therefore EERB MUST NOT become:

- a household solar advisor
- a bill-analysis application
- a tariff advisor
- a real-time grid operator assistant
- an electrical fault-diagnosis platform
- an abnormal-consumption detector
- a generic energy chatbot
- a generic RAG chatbot

The core differentiation must remain:

**PROPOSED PROJECT → INDEPENDENT ENGINEERING REVIEW → CROSS-CHECK → CRITIQUE → DESIGN-REVIEW REPORT**

The central question EERB answers is:

> "Does this proposed energy project/design appear technically coherent based on the information provided, what assumptions or conflicts need attention, and what should an engineer verify before the project proceeds?"

---

# 3. PRIMARY MVP USE CASE

The MVP should focus on:

## PV + BESS preliminary design review

Example:

A commercial building proposes:

- 500 kW solar PV
- 1 MWh BESS
- 500 kW battery power
- commercial building load profile
- specified peak-shaving objective

The user uploads:

- project requirements
- load CSV
- optional PV/BESS technical specification documents

EERB reviews the proposal.

---

# 4. DEMONSTRATION SCENARIO

Create a compelling hackathon demonstration around:

## "Review a proposed 500 kW PV + 1 MWh BESS project."

The demo should intentionally contain at least one detectable issue or inconsistency.

Example:

Project requirement:
- reduce peak demand by approximately 30%

Load profile:
- peak lasts significantly longer than the assumed battery duration

Proposed BESS:
- 1 MWh
- 500 kW discharge

The system should calculate whether the battery can realistically support the stated objective under the simplified assumptions.

One agent may conclude:

> "The proposed battery appears adequate."

Another agent should identify:

> "The load peak duration is longer than the assumed discharge duration."

The critic should flag the disagreement.

The Lead Engineer should produce something such as:

> "The proposed configuration may be technically plausible, but the stated peak-shaving objective cannot be confidently validated from the current assumptions. Battery sizing should be reassessed using the actual peak-duration profile and tariff/demand requirements."

This disagreement is a core part of the demo.

---

# 5. DATA STRATEGY

The application must NOT depend on private customer data for the hackathon.

Use publicly available data whenever possible.

Research and identify free, legally usable public datasets for:

1. electricity/load profiles
2. PV generation or solar resource data
3. public technical/reference information
4. optional building-energy data

For every dataset proposed, provide:

- dataset name
- URL
- provider
- license
- what fields it contains
- whether it can legally be used in a public hackathon demo
- approximate file size
- whether it should be downloaded and committed to GitHub
- whether it should instead be downloaded at runtime
- exact purpose in EERB

Prefer small subsets of large datasets.

Do not put huge datasets into GitHub unnecessarily.

If a required dataset is NOT freely available, explicitly say:

**"I cannot confirm that this dataset is freely available."**

Then provide a practical alternative:

- generate a clearly labelled synthetic dataset
- use a public dataset
- allow manual CSV upload
- provide a small demo CSV created from transparent assumptions

Never pretend synthetic data is real-world data.

---

# 6. HACKATHON DATA RECOMMENDATION

Evaluate the following public-data strategy:

### Primary load dataset

UCI ElectricityLoadDiagrams20112014.

Use a small subset representing one or a few consumers/buildings.

Convert the 15-minute values into the format required by the application.

Do not download/process the entire dataset during every application run.

Create a small demonstration CSV if appropriate.

### PV data

Evaluate free public solar-resource/PV-generation sources.

If live API access introduces reliability or API-key problems, use a small prepared public-data sample or a clearly labelled synthetic PV profile.

The application should still work if external data sources are unavailable.

### Technical documents

For the hackathon, provide a small controlled document set containing publicly available:

- battery specifications
- inverter specifications
- PV specifications
- general technical parameters

If actual manufacturer documents create copyright/licensing concerns, create a clearly labelled demonstration specification sheet based on publicly available technical parameters instead of redistributing copyrighted PDFs.

The PRD must distinguish:

**real public source**

from

**synthetic/demo data.**

---

# 7. USER INPUT

Design the MVP input around two modes.

## Mode A — Demo Project

One click:

**"Load Demo Project"**

This should populate a complete example project.

## Mode B — Upload Project

User can provide:

### Project information

- project name
- project type
- location
- project objective
- project description

### Load data

CSV upload.

Expected minimum columns:

- timestamp
- load_kw

### PV information

- PV capacity kW
- optional PV generation CSV
- optional technical specification document

### BESS information

- energy capacity kWh
- power rating kW
- round-trip efficiency
- minimum SOC
- maximum SOC
- initial SOC

### Optional documents

- project requirements PDF
- PV specification PDF
- inverter specification PDF
- BESS specification PDF

The application should work even when documents are not uploaded.

---

# 8. AGENT ARCHITECTURE

Do NOT create 15–20 agents.

Use approximately 5–6 meaningful agents.

Recommended architecture:

## Agent 1 — Lead Engineer

Responsibilities:

- understand project objective
- define review questions
- coordinate specialists
- synthesize final conclusion

The Lead Engineer should NOT perform engineering calculations itself.

---

## Agent 2 — Load Analyst

Responsibilities:

- inspect load profile
- calculate peak demand
- calculate average demand
- calculate daily energy
- identify peak duration
- identify important load characteristics
- evaluate whether load data supports project assumptions

---

## Agent 3 — PV Engineer

Responsibilities:

- inspect proposed PV capacity
- compare PV capacity with load
- evaluate simplified energy contribution
- identify missing PV assumptions
- inspect PV documentation
- flag inconsistent specifications

---

## Agent 4 — BESS Engineer

Responsibilities:

- inspect battery energy capacity
- inspect power capacity
- evaluate simplified duration
- evaluate SOC assumptions
- evaluate peak-shaving capability
- identify missing battery assumptions
- flag inconsistencies

---

## Agent 5 — Specification / Research Engineer

Responsibilities:

- inspect uploaded technical documents
- extract relevant specifications
- identify missing information
- compare stated project requirements against extracted specifications
- retrieve evidence from approved documents if RAG is implemented

---

## Agent 6 — Independent Critic

This agent is critical.

It should NOT simply summarize previous answers.

It should explicitly ask:

- What assumptions are unsupported?
- Where do agents disagree?
- Are calculations consistent?
- Is any conclusion too confident?
- What important information is missing?
- Could the proposed configuration fail to meet the stated objective?

The Critic produces:

- conflicts
- concerns
- unsupported assumptions
- missing information
- confidence assessment

The Lead Engineer then synthesizes the final result.

---

# 9. AGENT COMMUNICATION

Design the architecture so agents do NOT blindly pass natural-language messages around.

Use structured JSON-like outputs internally.

Example:

{
  "agent": "BESS Engineer",
  "finding": "Battery duration may be insufficient",
  "severity": "medium",
  "evidence": "...",
  "calculation": "...",
  "confidence": 0.82,
  "requires_verification": true
}

The final Lead Engineer should receive structured findings from all agents.

Define schemas for:

- Finding
- Calculation
- Assumption
- Conflict
- MissingInformation
- Recommendation
- AgentResult
- FinalReview

---

# 10. DETERMINISTIC ENGINEERING CALCULATION ENGINE

CRITICAL RULE:

The LLM must NOT perform important engineering mathematics itself.

Implement calculations as deterministic Python functions.

Recommended functions:

calculate_load_statistics()

calculate_peak_demand()

calculate_average_load()

calculate_daily_energy()

calculate_peak_duration()

calculate_pv_energy()

calculate_energy_balance()

simulate_battery_soc()

calculate_battery_duration()

calculate_peak_shaving()

calculate_self_consumption()

calculate_basic_project_metrics()

Each function should:

- accept structured numeric input
- return structured numeric output
- be independently testable
- contain no LLM calls

The LLM should decide WHICH calculation is relevant.

Python performs the calculation.

The LLM interprets the result.

Architecture:

LLM:
"What should be checked?"

↓

Python calculation engine:
"Here are the numerical results."

↓

LLM:
"What do these results mean for the project?"

---

# 11. BATTERY SIMULATION

Design a simple transparent battery SOC simulation.

Inputs:

- load profile
- PV generation profile
- battery capacity
- battery power
- efficiency
- min SOC
- max SOC
- initial SOC

Implement a simple operating strategy suitable for the MVP.

Example:

1. PV serves load first.
2. Excess PV charges battery.
3. Battery may discharge during defined peak periods.
4. Battery respects:
   - power limit
   - energy limit
   - SOC limits
   - efficiency

Clearly state that this is a simplified preliminary simulation and NOT a full dispatch optimization engine.

Output:

- SOC over time
- battery charging energy
- battery discharging energy
- peak before battery
- peak after battery
- peak reduction
- energy curtailed if relevant
- solar self-consumption if relevant

---

# 12. RAG

Do not make RAG the primary innovation.

Use RAG only where document evidence is useful.

For MVP, keep the document corpus small.

Possible sources:

- uploaded project documents
- uploaded specifications
- approved public technical references

The system should show:

- source document
- relevant section/page where possible
- finding supported by source

Do not allow the model to invent citations.

If evidence is unavailable, say:

**"No supporting source was found in the provided document set."**

---

# 13. DOCUMENT INTELLIGENCE

The MVP should support PDF upload if feasible.

Extract:

- equipment names
- capacities
- voltage
- power
- energy capacity
- efficiency
- operating limits
- warranty/cycle information where available
- project requirements
- assumptions

Represent extracted information as structured data.

Example:

{
  "equipment": "BESS",
  "energy_capacity_kwh": 1000,
  "power_kw": 500,
  "efficiency": 0.90,
  "source": "battery_spec.pdf",
  "page": 4
}

The system must distinguish:

- extracted fact
- calculated value
- AI interpretation
- assumption

---

# 14. CONFLICT DETECTION

This is one of the core differentiating features.

Create a mechanism to compare agent findings.

Example:

Load Analyst:

"Peak period requires approximately 3 hours of support."

BESS Engineer:

"1 MWh battery provides approximately 2 hours at 500 kW."

Critic:

"Battery duration is shorter than the identified peak-support requirement."

This should become:

### ⚠️ Engineering Conflict

and appear prominently in the UI.

---

# 15. CONFIDENCE SYSTEM

Every major conclusion should have:

- High
- Medium
- Low

confidence.

Confidence should be based on factors such as:

- data completeness
- calculation availability
- source availability
- agent agreement
- unsupported assumptions

Do NOT present fake mathematical confidence probabilities unless there is a justified methodology.

Prefer:

**Confidence: Medium**

Reason:

> "Load data is available, but tariff requirements and detailed inverter operating limits were not provided."

---

# 16. FINAL REPORT

Generate a structured preliminary engineering review.

Sections:

1. Executive Summary
2. Project Description
3. Input Data
4. Extracted Specifications
5. Key Assumptions
6. Load Analysis
7. PV Analysis
8. BESS Analysis
9. Deterministic Calculation Results
10. Agent Findings
11. Engineering Conflicts
12. Missing Information
13. Risks
14. Recommendations
15. Confidence
16. Items Requiring Professional Verification

The report must clearly state:

> "This system provides an AI-assisted preliminary engineering review. It does not constitute final engineering design, certification, grid approval, safety approval, or professional engineering sign-off."

Never say:

"This system confirms the project is safe."

Instead use:

"No major issue was identified within the parameters and calculations evaluated; professional engineering validation is required."

---

# 17. STREAMLIT UI

Build the MVP in Streamlit.

Suggested layout:

## Sidebar

- New Project
- Demo Project
- Upload Project
- Settings

## Main page

### Step 1 — Project

Project name
Project type
Objective
Location

### Step 2 — Data

Load CSV
PV information
BESS information
Documents

### Step 3 — Start Review

Large button:

**Run Engineering Review**

Then show an animated/progressive review.

Example:

✓ Project Planner  
✓ Load Analyst  
✓ PV Engineer  
✓ BESS Engineer  
✓ Specification Engineer  
⚠ Independent Critic  
✓ Lead Engineer

Do not fake real-time processing if the agents are not actually executing sequentially. Use genuine workflow states.

---

# 18. RESULTS DASHBOARD

Show four primary charts:

1. Load profile
2. PV generation vs load
3. Battery SOC
4. Peak demand before vs after battery

Show KPI cards:

- Peak load
- Daily energy
- PV capacity
- BESS capacity
- Battery duration
- Estimated peak reduction

Then show:

### Overall Review

Green / Yellow / Red style status.

But do NOT represent this as a safety certification.

Use labels such as:

- Preliminary Design Appears Consistent
- Review Required
- Significant Issues Identified

---

# 19. FINDINGS UI

Create cards for:

### Critical
### High
### Medium
### Low

Each finding should show:

- issue
- source
- calculation
- affected component
- recommendation
- confidence

Example:

**Medium — Battery Duration**

The proposed BESS provides approximately 2 hours at its rated discharge power, while the analyzed peak-support period is longer.

Recommendation:

Reassess BESS energy capacity using the actual demand profile and project objective.

---

# 20. AGENT BOARD UI

Create a visually compelling engineering-board interface.

Example:

┌──────────────────────────────┐
│ ENERGY ENGINEERING BOARD     │
├──────────────────────────────┤
│ ✓ Lead Engineer              │
│ ✓ Load Analyst               │
│ ✓ PV Engineer                │
│ ✓ BESS Engineer              │
│ ✓ Specification Engineer     │
│ ⚠ Independent Critic         │
│ ✓ Final Review               │
└──────────────────────────────┘

Allow the user to expand each agent and see its structured findings.

---

# 21. ARCHITECTURE

Design a clean architecture suitable for a weekend MVP.

Recommended:

Streamlit UI

↓

Application / orchestration layer

↓

Agent layer

- Lead Engineer
- Load Analyst
- PV Engineer
- BESS Engineer
- Specification Engineer
- Critic

↓

Tool layer

- deterministic calculations
- PDF extraction
- CSV processing
- RAG retrieval
- evidence extraction

↓

Data layer

- demo CSV
- uploaded files
- small local document corpus
- optional vector index

↓

LLM provider

Use an OpenAI-compatible interface where possible so the model provider can be swapped.

Do not tightly couple the application to one model.

---

# 22. TECHNOLOGY STACK

Recommend the simplest stack that can realistically be deployed on Streamlit Community Cloud.

Preferred:

Python

Streamlit

Pandas

NumPy

Plotly

PyPDF/PyMuPDF or another lightweight PDF extraction library

LLM API

Optional lightweight vector search:

FAISS or Chroma

Do NOT introduce unnecessary infrastructure such as:

- Kubernetes
- Docker unless necessary
- Redis
- PostgreSQL
- microservices
- complex cloud infrastructure
- authentication
- message queues

The hackathon MVP should preferably run as one Streamlit application.

---

# 23. AGENT FRAMEWORK

Evaluate whether LangGraph is actually necessary.

Compare:

A. Plain Python orchestration
B. LangChain
C. LangGraph

Choose the simplest architecture that provides genuine multi-agent orchestration.

If LangGraph materially improves:

- agent state
- branching
- retries
- structured workflow
- critic loop

then use it.

Otherwise use clean Python orchestration.

Do not add a framework merely to make the architecture sound more advanced.

---

# 24. MODEL REQUIREMENTS

The system must use an LLM for:

- planning
- agent reasoning
- document interpretation
- engineering explanation
- conflict analysis
- final synthesis

The LLM must NOT be responsible for:

- core numerical calculations
- battery SOC arithmetic
- load statistics
- deterministic engineering equations

---

# 25. API KEY SECURITY

Never hardcode API keys.

For local development:

.env

For Streamlit deployment:

Streamlit secrets.

The repository must never contain:

- API keys
- passwords
- tokens
- private credentials

---

# 26. GITHUB STRUCTURE

Design the repository around something like:

eerb/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── demo_load.csv
│   └── demo_pv.csv
│
├── documents/
│   └── demo_specs/
│
├── agents/
│   ├── lead_engineer.py
│   ├── load_analyst.py
│   ├── pv_engineer.py
│   ├── bess_engineer.py
│   ├── specification_engineer.py
│   └── critic.py
│
├── calculations/
│   ├── load.py
│   ├── pv.py
│   ├── battery.py
│   └── metrics.py
│
├── retrieval/
│   └── rag.py
│
├── document_processing/
│   └── pdf_parser.py
│
├── schemas/
│   └── models.py
│
└── utils/
    └── helpers.py

However, simplify this structure if it would slow down the hackathon.

The final recommendation must prioritize working software over architectural purity.

---

# 27. TESTING

Define test scenarios.

At minimum:

### Scenario 1 — Normal

PV+BESS appears broadly consistent.

### Scenario 2 — Oversized/undersized battery

The system should detect the issue.

### Scenario 3 — Missing information

The system should explicitly report insufficient information instead of hallucinating.

### Scenario 4 — Conflicting specification

Two project documents contain inconsistent values.

The system should identify the conflict.

### Scenario 5 — Poor-quality CSV

The system should provide a useful validation error.

---

# 28. HACKATHON DEMO SCRIPT

Design a 3–5 minute demonstration.

Recommended sequence:

1. Introduce EERB.
2. Load Demo Project.
3. Show proposed 500 kW PV + 1 MWh BESS project.
4. Upload/show project documents.
5. Click "Run Engineering Review."
6. Show agents working.
7. Show deterministic calculations.
8. Show agent disagreement.
9. Show critic identifying the issue.
10. Show Lead Engineer conclusion.
11. Show final engineering report.
12. Show one-click download.

The most important moment should be:

**The AI does not simply answer the user. It challenges the proposed design.**

---

# 29. FUTURE ROADMAP

Do not implement these during the weekend, but design the architecture so they can be added later.

Phase 2:

- EV charging projects
- microgrid projects
- wind projects
- energy-efficiency projects

Phase 3:

- vendor proposal comparison
- EPC bid comparison
- automated technical compliance matrices

Phase 4:

- deeper document intelligence
- tender/RFP analysis
- equipment datasheet comparison

Phase 5:

- trusted engineering knowledge base
- standards and regulations
- organization-specific engineering rules

Phase 6:

- scenario comparison
- PV/BESS sizing alternatives
- optimization

Phase 7:

- integration with engineering software such as:
  - HOMER
  - PVsyst
  - OpenDSS
  - pandapower
  - PyPSA

Phase 8:

- enterprise project management
- audit trail
- role-based access
- approval workflows

---

# 30. BUSINESS MODEL

Do NOT invent market prices as facts.

Create a business-model hypothesis.

Potential customers:

- renewable EPCs
- energy engineering consultants
- electrical engineering companies
- project developers
- industrial energy teams
- procurement teams

Potential value proposition:

Reduce time spent on preliminary technical review and identify missing information or inconsistencies before expensive engineering work proceeds.

Possible future pricing model:

- individual engineer subscription
- team subscription
- per-project review
- enterprise license

Clearly label all prices as:

**Hypothetical pricing — requires customer validation.**

---

# 31. COMPETITIVE POSITIONING

Compare EERB against:

- SolarGrid Advisor
- Smart Grid Operational Assistance
- Grid Guard AI
- generic AI chatbots
- engineering simulation software

Create a feature comparison table.

The central differentiator must be:

**Pre-project independent engineering review.**

---

# 32. SECURITY AND SAFETY

The application must:

- never claim professional certification
- never claim safety approval
- never claim regulatory approval
- clearly distinguish assumptions from facts
- clearly identify missing information
- show sources where possible
- avoid unsupported engineering conclusions

Include an explicit disclaimer.

---

# 33. WEEKEND MVP LIMITS

The PRD MUST identify features that are deliberately excluded.

Exclude from MVP:

- authentication
- payment
- database
- multi-tenant architecture
- real-time IoT
- real-time grid control
- automatic control
- full protection coordination
- detailed power-flow simulation
- advanced optimization
- full standards compliance
- mobile application
- production-grade enterprise security
- large-scale document ingestion

---

# 34. IMPLEMENTATION PLAN

Create a detailed 2-day implementation plan.

Day 1 morning:

- project setup
- Streamlit UI
- demo dataset
- CSV processing
- deterministic calculation engine

Day 1 afternoon:

- Load Analyst
- PV Engineer
- BESS Engineer
- basic orchestration

Day 1 evening:

- Specification Engineer
- Critic
- Lead Engineer

Day 2 morning:

- document extraction
- conflict detection
- charts
- results dashboard

Day 2 afternoon:

- report generation
- testing
- UI polish
- GitHub deployment

Day 2 evening:

- demo rehearsal
- bug fixing
- fallback mode

---

# 35. FAILURE/FALLBACK DESIGN

This is critical for a hackathon.

The application must still demonstrate the core product if:

- an LLM API fails
- an external data source fails
- a PDF cannot be parsed
- a user uploads malformed data

Create a demo/fallback mode.

The demo must be able to run using:

- bundled demo CSV
- bundled demo specifications
- deterministic calculations
- available LLM API

External APIs should not be required for the core demo unless absolutely necessary.

---

# 36. PRD OUTPUT FORMAT

Produce the final PRD with these sections:

1. Executive Summary
2. Problem
3. Target Users
4. User Personas
5. Product Vision
6. Differentiation
7. User Stories
8. MVP Scope
9. Non-MVP Scope
10. User Workflow
11. Data Strategy
12. Public Dataset Research
13. Data Acquisition Instructions
14. Agent Architecture
15. Agent Responsibilities
16. Agent Communication Schema
17. Deterministic Calculation Engine
18. RAG Architecture
19. Document Processing
20. Conflict Detection
21. Confidence System
22. Streamlit UI
23. System Architecture
24. Repository Structure
25. Technology Stack
26. LLM/API Strategy
27. Security
28. Testing
29. Demo Scenario
30. Hackathon Demo Script
31. Deployment Architecture
32. GitHub Structure
33. Two-Day Implementation Plan
34. Failure/Fallback Plan
35. Future Roadmap
36. Business Model
37. Competitive Analysis
38. Risks
39. Success Metrics
40. Final MVP Definition

For every feature, explicitly label:

**MUST HAVE**

**SHOULD HAVE**

or

**FUTURE**

Do not over-engineer the MVP.

At the end provide:

### FINAL MVP IN ONE SENTENCE

### FINAL ARCHITECTURE DIAGRAM

### EXACT FILE STRUCTURE

### EXACT DATA NEEDED

### EXACT HACKATHON DEMO FLOW

### TOP 10 IMPLEMENTATION RISKS

### WHAT NOT TO BUILD

The final PRD must be implementation-ready enough that another AI coding assistant can use it to generate the application step-by-step.