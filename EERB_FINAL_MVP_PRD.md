# Energy Engineering Review Board (EERB)
## Final MVP PRD — Hackathon Edition

**Tagline:** "AI engineering review before you build."

**Deadline:** Sunday, 13 Sep 2026, 11:59 PM PKT  
**Team:** 2 active members  
**Deliverables:** GitHub repo | Streamlit deployment | PRD | Slides | Video

---

## 1. EXECUTIVE SUMMARY

EERB is a multi-agent AI system that provides **preliminary technical review** of proposed renewable-energy projects (PV + BESS) BEFORE detailed engineering or implementation.

**Core Value:** Identify technical inconsistencies, missing information, and design conflicts in project proposals early—reducing wasted engineering effort.

**NOT:** A professional engineering certification, safety approval, or replacement for HOMER/PVsyst/ETAP.

**IS:** An AI-assisted decision-support layer for preliminary design review.

---

## 2. PROBLEM

Energy project teams often discover technical inconsistencies **after expensive engineering work begins**:
- Battery sizing doesn't match load profile
- PV capacity doesn't support stated objectives
- Load data assumptions conflict with tariff requirements
- Missing specifications make design verification impossible

**Current workflow:** Manual review by senior engineer → slow, expensive, bottleneck.

**EERB solution:** AI agents review in parallel, identify conflicts, flag missing info, produce traceable report.

---

## 3. TARGET USERS

1. **Renewable EPC teams** – preliminary design review before detailed engineering
2. **Energy consultants** – assist project vetting
3. **Project developers** – early-stage technical validation
4. **Energy engineering students** – learn engineering review methodology

---

## 4. MVP SCOPE

### ✅ MUST HAVE

- [ ] Streamlit web UI
- [ ] Two input modes: Demo Project + Upload Project
- [ ] Load data processing (CSV: timestamp, load_kw)
- [ ] User input for PV & BESS specs
- [ ] 6 AI agents with structured outputs:
  - Lead Engineer (orchestrator)
  - Load Analyst
  - PV Engineer
  - BESS Engineer
  - Specification Engineer (document review)
  - Independent Critic
- [ ] Deterministic calculation engine:
  - Peak load, average load, daily energy
  - PV energy contribution
  - Battery SOC simulation
  - Peak shaving calculation
- [ ] Simple RAG (PDF text extraction + keyword search, no semantic search for MVP)
- [ ] Results dashboard:
  - 4 charts (load profile, PV vs load, battery SOC, peak before/after)
  - KPI cards
- [ ] Engineering findings with severity levels (Critical/High/Medium/Low)
- [ ] Conflict detection ("Battery duration insufficient for peak-shaving objective")
- [ ] Final review report (downloadable)
- [ ] GitHub repo with clear structure
- [ ] Streamlit Cloud deployment
- [ ] Presentation slides
- [ ] Demo scenario with intentional technical issue

### ❌ NOT IN MVP

- Authentication / user accounts
- Database storage
- Real-time IoT / grid control
- Advanced PDF parsing
- Semantic RAG
- Mobile optimization
- Production security hardening
- Payment / subscription
- Multi-tenant support

---

## 5. USER WORKFLOW

### Mode A: Demo Project (One Click)
1. Click **"Load Demo Project"**
2. System populates: 500 kW PV, 1 MWh BESS, commercial load profile
3. Click **"Run Engineering Review"**
4. See agents work in real-time
5. View results dashboard + findings
6. Download report

### Mode B: Upload Project
1. Enter project info (name, type, location, objective)
2. Upload load CSV
3. Enter PV specs (capacity kW, optional CSV, optional spec PDF)
4. Enter BESS specs (energy kWh, power kW, efficiency, SOC range)
5. Upload optional spec PDFs
6. Click **"Run Engineering Review"**
7. View results + download report

---

## 6. DATA STRATEGY

### Demo Data (Bundled)
- **Load profile:** 1-week commercial building, 15-min intervals, 100–500 kW peak
- **PV profile:** Synthetic, clear day profile, 7.5-hour peak window
- **Specs:** Text files (not real PDFs to avoid licensing issues)

### Public Datasets (For Future)
- UCI ElectricityLoadDiagrams20112014 (if user uploads)
- NREL PVWatts data (if user provides location)
- For MVP: Use bundled demo data only

### Data Not Included
- Proprietary customer data
- Licensed PDFs (use demo specs instead)
- Real tariff/regulatory data (user can upload)

---

## 7. AGENT ARCHITECTURE

### Agent 1: Lead Engineer
**Role:** Orchestrator, final synthesizer
- Define review questions from project objective
- Coordinate specialists
- Produce final conclusions
- Ensure no unsupported claims
- Track confidence levels

**Output:**
```json
{
  "agent": "Lead Engineer",
  "review_questions": ["Is battery adequate?", "Does PV cover objectives?"],
  "coordination_notes": "Waiting for Load Analyst results...",
  "final_conclusion": "Design appears technically plausible with caveats...",
  "confidence": "Medium"
}
```

### Agent 2: Load Analyst
**Role:** Inspect load profile
- Peak demand (kW)
- Average demand (kW)
- Daily energy (kWh)
- Peak duration (hours)
- Load characteristics
- Validation of assumptions

**Output:**
```json
{
  "agent": "Load Analyst",
  "peak_demand_kw": 520,
  "average_demand_kw": 280,
  "daily_energy_kwh": 6720,
  "peak_duration_hours": 4.5,
  "findings": ["Peak lasts 4.5 hours", "Daytime load higher than night"],
  "confidence": "High"
}
```

### Agent 3: PV Engineer
**Role:** Inspect PV adequacy
- PV capacity vs load
- Estimated annual energy
- Self-consumption ratio
- Missing assumptions
- Spec document review

**Output:**
```json
{
  "agent": "PV Engineer",
  "pv_capacity_kw": 500,
  "estimated_daily_production_kwh": 3500,
  "daily_load_kwh": 6720,
  "pv_to_peak_ratio": 0.96,
  "findings": ["PV covers ~52% of daily load", "Assumes clear-day profile"],
  "concerns": ["Seasonal variation not provided"],
  "confidence": "Medium"
}
```

### Agent 4: BESS Engineer
**Role:** Inspect battery adequacy
- Energy capacity, power rating
- Discharge duration at rated power
- Peak-shaving capability
- SOC assumptions
- Efficiency impact

**Output:**
```json
{
  "agent": "BESS Engineer",
  "energy_capacity_kwh": 1000,
  "power_rating_kw": 500,
  "duration_at_rated_power_hours": 2.0,
  "peak_shaving_capability": "Can reduce peak by ~30% for 2 hours",
  "findings": ["Battery duration = 2 hours at 500 kW"],
  "concerns": ["Load peak is 4.5 hours; battery lasts 2 hours"],
  "confidence": "High"
}
```

### Agent 5: Specification Engineer
**Role:** Review documents, extract specs
- Equipment names, capacities
- Conflicting specifications
- Missing information
- Evidence sourcing (RAG)

**Output:**
```json
{
  "agent": "Specification Engineer",
  "extracted_specs": [
    {"equipment": "BESS", "energy_kwh": 1000, "power_kw": 500, "source": "spec_sheet.pdf"},
    {"equipment": "Inverter", "power_kw": 600, "efficiency": 0.95, "source": "spec_sheet.pdf"}
  ],
  "missing_info": ["Minimum SOC not specified", "Round-trip efficiency not provided"],
  "conflicts": [],
  "confidence": "High"
}
```

### Agent 6: Independent Critic
**Role:** Challenge conclusions, identify gaps
- Unsupported assumptions?
- Where do agents disagree?
- Calculations consistent?
- Confidence appropriate?
- Missing critical info?

**Output:**
```json
{
  "agent": "Critic",
  "conflicts_identified": [
    {
      "issue": "Battery Duration vs Peak Duration",
      "agent_1": "BESS Engineer says battery lasts 2 hours",
      "agent_2": "Load Analyst says peak lasts 4.5 hours",
      "severity": "High"
    }
  ],
  "unsupported_assumptions": ["Assumes constant discharge rate", "Ignores seasonal variation"],
  "missing_critical_info": ["Tariff demand charges", "Tariff peak-demand window"],
  "confidence_assessment": "Medium—battery adequacy cannot be confirmed without tariff details",
  "recommendation": "Reassess battery sizing using actual peak-demand window and tariff"
}
```

---

## 8. DETERMINISTIC CALCULATION ENGINE

All math is **Python functions**, not LLM hallucinations.

### Core Functions

```python
def calculate_load_statistics(load_kw_series) -> dict:
    # Returns: peak, average, daily_energy, peak_duration

def calculate_pv_energy(pv_capacity_kw, irradiance_profile) -> float:
    # Returns: estimated daily energy kWh

def simulate_battery_soc(
    load_profile, pv_generation, battery_capacity_kwh, 
    power_kw, efficiency, min_soc, max_soc
) -> dict:
    # Returns: SOC timeseries, peak_before, peak_after, peak_reduction

def calculate_battery_duration(energy_kwh, power_kw) -> float:
    # Returns: duration hours at rated power

def calculate_peak_shaving(load_peak_kw, battery_power_kw) -> float:
    # Returns: peak reduction percentage
```

**Architecture:**
```
LLM: "What should we check?"
  ↓
Python: "Here are the calculations"
  ↓
LLM: "What do these numbers mean?"
```

---

## 9. RAG ARCHITECTURE (Lightweight)

### What We'll Do
1. User uploads PDF spec sheets
2. Extract **text only** (PyPDF2 or pdfplumber)
3. Store text in simple dictionary/list
4. When agent asks "Find battery efficiency in spec", use **keyword search**
5. Return matching text + source

### What We Won't Do
- Semantic embeddings / FAISS (too complex for MVP)
- Fine-grained document parsing
- Citation confidence scoring

### RAG Output
```json
{
  "query": "battery efficiency",
  "result": "Round-trip efficiency 90%",
  "source": "battery_spec.pdf",
  "page": null,
  "confidence": "Medium"
}
```

---

## 10. CONFLICT DETECTION

**Automatic comparison of agent findings:**

```
Load Analyst: "Peak period = 4.5 hours"
BESS Engineer: "Battery duration = 2 hours"
  ↓
Critic: "⚠️ CONFLICT: Battery cannot support full peak-shaving objective"
  ↓
Lead Engineer: "Reassess battery sizing"
```

**Display in UI:** Highlighted warning card with severity level.

---

## 11. STREAMLIT UI STRUCTURE

### Sidebar
- 🏠 **Home**
- 📋 **Demo Project** (one click)
- 📤 **Upload Project** (3-step form)
- ⚙️ **Settings**
- 📖 **Help & Disclaimer**

### Main Page - Demo Project Flow

**Step 1: Project Overview**
```
Project Name: Commercial Building PV+BESS Retrofit
Location: Karachi
Objective: Peak demand reduction by 30%
```

**Step 2: Loaded Data**
- Load profile: 7 days, 500 kW peak
- PV: 500 kW capacity
- BESS: 1 MWh, 500 kW power

**Step 3: Start Review**
```
[RUN ENGINEERING REVIEW] ← Large button
```

### Review Execution (Real-time Progress)
```
✓ Lead Engineer — Defining review scope
✓ Load Analyst — Analyzing load profile
✓ PV Engineer — Evaluating PV capacity
✓ BESS Engineer — Checking battery specs
✓ Specification Engineer — Reviewing documents
✓ Independent Critic — Challenging conclusions
✓ Lead Engineer — Synthesizing final report
```

### Results Dashboard

**Charts (4):**
1. Load profile (line chart, kW over time)
2. PV generation vs load (overlaid lines)
3. Battery SOC (line chart, %)
4. Peak demand before/after (bar chart)

**KPI Cards:**
- Peak Load: 520 kW
- Daily Energy: 6,720 kWh
- PV Capacity: 500 kW
- BESS Capacity: 1 MWh
- Battery Duration: 2 hours
- Peak Reduction: 30%

**Overall Status:**
```
🟡 REVIEW REQUIRED

Design appears technically plausible, but battery duration 
is insufficient for stated peak-shaving objective.
```

### Findings Section

**Critical Issues** (0)
**High Priority** (1)
- ⚠️ **Battery Duration Inadequate**
  - Issue: Battery provides 2 hours at rated power, peak lasts 4.5 hours
  - Severity: High
  - Confidence: High
  - Recommendation: Reassess battery sizing using actual peak window

**Medium Priority** (2)
**Low Priority** (1)

### Agent Details (Expandable)
Click each agent to see structured findings as JSON/table.

### Actions
- [📥 Download Report]
- [📊 Download CSV Data]
- [🔄 New Review]

---

## 12. FINAL REPORT SECTIONS

1. **Executive Summary** (1 paragraph)
2. **Project Description** (name, type, location, objective)
3. **Disclaimer** ("This is preliminary review, not professional engineering certification")
4. **Input Data Summary**
5. **Key Assumptions**
6. **Load Analysis Results**
7. **PV Analysis Results**
8. **BESS Analysis Results**
9. **Deterministic Calculations**
10. **Agent Findings** (all agents)
11. **Engineering Conflicts** (if any)
12. **Missing Information**
13. **Risks**
14. **Recommendations**
15. **Confidence Assessment**
16. **Items Requiring Professional Verification**

---

## 13. TECHNOLOGY STACK

- **Python 3.10+**
- **Streamlit** (UI + deployment)
- **Pandas** (data processing)
- **NumPy** (calculations)
- **Plotly** (charts)
- **PyPDF2 or pdfplumber** (PDF text extraction)
- **OpenAI API** (LLM agents)
- **python-dotenv** (environment variables)
- **Requests** (API calls)

**No:** Kubernetes, Docker, Redis, PostgreSQL, authentication, message queues.

---

## 14. GITHUB REPOSITORY STRUCTURE

```
eerb/
├── .env (LOCAL ONLY - NOT in GitHub)
├── .gitignore
├── README.md
├── requirements.txt
├── app.py (Main Streamlit app)
│
├── data/
│   ├── demo_load.csv
│   ├── demo_pv.csv
│   └── README_DATA.md
│
├── agents/
│   ├── __init__.py
│   ├── lead_engineer.py
│   ├── load_analyst.py
│   ├── pv_engineer.py
│   ├── bess_engineer.py
│   ├── specification_engineer.py
│   └── critic.py
│
├── calculations/
│   ├── __init__.py
│   ├── load.py
│   ├── pv.py
│   ├── battery.py
│   └── metrics.py
│
├── utils/
│   ├── __init__.py
│   ├── pdf_parser.py
│   ├── rag.py
│   ├── data_processor.py
│   └── helpers.py
│
├── schemas/
│   ├── __init__.py
│   └── models.py
│
├── docs/
│   ├── DEPLOYMENT.md
│   ├── ARCHITECTURE.md
│   └── API_SCHEMA.md
│
└── tests/
    ├── test_calculations.py
    ├── test_agents.py
    └── test_rag.py
```

---

## 15. DEMO SCENARIO (Intentional Issue)

**Project:** 500 kW PV + 1 MWh BESS Commercial Building Retrofit

**Stated Objective:** Reduce peak demand by 30%

**Load Profile:** Commercial building, 7-day average
- Peak: 520 kW
- Peak duration: **4.5 hours** (1 PM – 5:30 PM)
- Average load: 280 kW
- Daily energy: 6,720 kWh

**PV Proposed:** 500 kW
- Annual capacity factor: ~18% (Karachi average)
- Covers ~52% of daily load

**BESS Proposed:** 1 MWh, 500 kW power
- Round-trip efficiency: 90%
- Discharge duration: **2 hours** (at 500 kW)
- Charge during off-peak, discharge during peak

**THE ISSUE:** 
Battery discharge duration (2 hours) < peak support period (4.5 hours)

**What EERB Should Detect:**
- Load Analyst: "Peak lasts 4.5 hours"
- BESS Engineer: "Battery lasts 2 hours"
- Critic: "CONFLICT: Battery cannot meet stated objective"
- Lead Engineer: "Battery sizing requires reassessment"

**Result:** 🟡 REVIEW REQUIRED (not a failure, but flagged for verification)

---

## 16. HACKATHON DEMO SCRIPT (4–5 min)

1. **Intro (30 sec)**
   - "This is EERB—AI engineering review before you build"
   - Show problem: missed issues delay projects, cost time/money

2. **Load Demo Project (30 sec)**
   - Click "Demo Project"
   - Show: 500 kW PV + 1 MWh BESS for commercial building

3. **Run Review (1 min)**
   - Click "Run Engineering Review"
   - Show progress: agents working in parallel
   - Highlight the **conflict detection** moment

4. **Results Dashboard (1.5 min)**
   - Show 4 charts
   - Show KPI cards
   - Show overall status

5. **Findings & Conflict (1 min)**
   - Highlight HIGH priority: "Battery Duration Inadequate"
   - Show it came from Critic's challenge
   - Show the recommendation

6. **Download Report (30 sec)**
   - Click "Download Report"
   - Explain: traceable, source-referenced, ready for professional engineer

7. **Close (30 sec)**
   - "EERB identifies issues before expensive engineering. It's not certification—it's a smart thinking partner."

---

## 17. TESTING SCENARIOS

### Scenario 1: Normal Project
- PV + BESS appear consistent
- Expected result: 🟢 Preliminary Design Appears Consistent

### Scenario 2: Undersized Battery
- BESS too small for peak-shaving objective
- Expected result: 🟡 Review Required (conflict flagged)

### Scenario 3: Missing Data
- No load CSV provided
- Expected result: 🔴 Insufficient Information (app halts gracefully)

### Scenario 4: Invalid CSV
- Malformed timestamps, missing columns
- Expected result: 🔴 Data Validation Error (clear message)

### Scenario 5: Conflicting Specs
- Two PDFs say different battery efficiency
- Expected result: 🟡 Review Required (conflict noted)

---

## 18. DEPLOYMENT TO STREAMLIT CLOUD

### Steps
1. Push code to GitHub (bella-luz/eerb)
2. Go to Streamlit Cloud dashboard
3. Connect GitHub repo
4. Add secrets:
   - `OPENAI_API_KEY = sk-...`
5. Deploy
6. Get public URL

**Expected deployment time:** ~3–5 minutes

---

## 19. PRESENTATION SLIDES (Google Slides or PDF)

1. **Title Slide**
   - "Energy Engineering Review Board (EERB)"
   - "AI engineering review before you build"

2. **Problem**
   - Missed technical issues delay projects
   - Current: manual senior-engineer review (slow, bottleneck)

3. **Solution**
   - Multi-agent AI review in parallel
   - Deterministic math + LLM reasoning
   - Identifies conflicts, flags missing info

4. **Demo Project**
   - 500 kW PV + 1 MWh BESS
   - Commercial load profile
   - Intentional battery-sizing issue

5. **Key Features**
   - 6 specialized agents
   - Real-time conflict detection
   - Traceable report
   - No hallucinations (deterministic math)

6. **Results Example**
   - Show dashboard with charts
   - Show findings card highlighting conflict
   - Show it caught the battery-duration issue

7. **Target Users**
   - EPCs, consultants, developers, energy teams

8. **Future Roadmap**
   - EV charging, microgrids, wind
   - Vendor comparison
   - Standards compliance

9. **Q&A**

---

## 20. IMPLEMENTATION PRIORITY (Strict Order)

### Phase 1 (Calculations + Data) — 3 hours
- [ ] Load calculation functions (peak, average, daily energy, duration)
- [ ] PV calculation functions
- [ ] Battery SOC simulation engine
- [ ] Create demo CSV files
- [ ] Test calculations with demo data

### Phase 2 (Agents) — 4 hours
- [ ] Agent schema (JSON output structure)
- [ ] Lead Engineer agent
- [ ] Load Analyst agent
- [ ] PV Engineer agent
- [ ] BESS Engineer agent
- [ ] Specification Engineer agent (simple)
- [ ] Critic agent
- [ ] Agent orchestration (sequential call)

### Phase 3 (UI + Integration) — 3 hours
- [ ] Streamlit basic layout
- [ ] Demo Project mode (load bundled data)
- [ ] Upload Project mode (3-step form)
- [ ] Run button + progress display
- [ ] Results dashboard (charts + KPIs)

### Phase 4 (Polish + Report) — 2 hours
- [ ] Findings cards UI
- [ ] Conflict detection display
- [ ] Report generation + download
- [ ] Styling/theme
- [ ] Error handling

### Phase 5 (Testing + Deployment) — 1 hour
- [ ] Local testing with demo data
- [ ] Fix bugs
- [ ] Push to GitHub
- [ ] Deploy to Streamlit Cloud
- [ ] Verify live deployment

### Phase 6 (Documentation + Slides) — 1 hour
- [ ] README
- [ ] DEPLOYMENT.md
- [ ] Presentation slides
- [ ] Demo video script

---

## 21. SUCCESS CRITERIA

✅ App loads without errors on Streamlit Cloud  
✅ Demo Project runs end-to-end in <60 seconds  
✅ Agents produce structured output (not hallucinations)  
✅ Conflict detection works (battery-duration issue is flagged)  
✅ Charts render correctly  
✅ Report is downloadable + readable  
✅ Code is in GitHub with .gitignore (no API keys exposed)  
✅ Presentation slides are clear and concise  
✅ Disclaimer is visible and clear  

---

## 22. WHAT NOT TO BUILD

❌ Authentication  
❌ Database  
❌ Semantic RAG/embeddings  
❌ Mobile UI  
❌ Real-time optimization  
❌ Multiple projects in one session  
❌ User accounts  
❌ Payment integration  
❌ Kubernetes/Docker  
❌ Production-grade security  

---

## FINAL MVP IN ONE SENTENCE

**EERB is a Streamlit app with 6 AI agents that identifies technical inconsistencies in proposed PV+BESS projects by running deterministic calculations, comparing results, and flagging conflicts in a traceable report—all in 2 days, no database.**

---

## SUBMISSION CHECKLIST

- [ ] GitHub repo (code + README)
- [ ] Streamlit Cloud deployment (working link)
- [ ] PRD document (this file)
- [ ] Presentation slides (PDF or Google Slides link)
- [ ] Demo video (4–5 min, recorded locally or YouTube)
- [ ] All links submitted by Sunday 11:59 PM PKT

---

**Ready to build. Let's go.** 🚀
