# Energy Engineering Review Board (EERB)

**"AI engineering review before you build."**

EERB is a multi-agent AI system that provides preliminary technical review of proposed renewable-energy projects (PV + BESS) before detailed engineering or implementation.

## 🎯 What is EERB?

EERB reviews your proposed energy projects using 6 specialized AI agents:
- **Load Analyst** – Analyzes electricity load profiles
- **PV Engineer** – Evaluates solar capacity
- **BESS Engineer** – Assesses battery storage adequacy
- **Specification Engineer** – Reviews technical documents
- **Independent Critic** – Challenges conclusions and identifies conflicts
- **Lead Engineer** – Synthesizes findings into final review

### Key Features

✅ **Deterministic Calculations** – No LLM hallucinations in critical math  
✅ **Conflict Detection** – Automatically flags inconsistencies  
✅ **Traceable Analysis** – Source-referenced findings  
✅ **Preliminary Report** – Clear, actionable recommendations  

---

## 🚀 Quick Start

### Installation

1. **Clone repo** (or download files)
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variable:**
   Create `.env` file with:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

4. **Run Streamlit:**
   ```bash
   streamlit run app.py
   ```

5. **Open browser:** http://localhost:8501

### Demo Project

Click "Demo Project" in the sidebar to see EERB in action with a pre-loaded 500 kW PV + 1 MWh BESS system.

### Upload Your Project

1. Go to "Upload Project"
2. Enter project details
3. Upload load CSV (columns: `timestamp`, `load_kw`)
4. Enter PV and BESS specs
5. Click "Run Engineering Review"

---

## 📊 Demo Scenario

The demo includes an **intentional technical conflict** to show how EERB detects issues:

**Project:** 500 kW PV + 1 MWh BESS for commercial building  
**Objective:** Reduce peak demand by 30%

**The Issue:**
- Load peak duration: **4.5 hours**
- Battery discharge duration: **2 hours** (at 500 kW)

**EERB Detection:**
- Load Analyst identifies 4.5-hour peak
- BESS Engineer calculates 2-hour duration
- Critic flags conflict
- Lead Engineer recommends verification

---

## 📋 Project Structure

```
eerb/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (LOCAL ONLY)
├── .gitignore               # Git ignore rules
│
├── data/
│   ├── demo_load.csv        # Demo load profile
│   └── demo_pv.csv          # Demo PV generation
│
├── calculations/            # Deterministic math engine
│   ├── load.py              # Load analysis
│   ├── pv.py                # PV calculations
│   └── battery.py           # Battery simulation
│
├── agents/                  # AI agents
│   ├── orchestrator.py      # Agent coordination
│   ├── load_analyst.py
│   ├── pv_engineer.py
│   ├── bess_engineer.py
│   ├── specification_engineer.py
│   ├── critic.py
│   └── lead_engineer.py
│
├── utils/                   # Utilities
│   ├── data_processor.py    # CSV processing
│   └── rag.py               # Document retrieval
│
└── schemas/                 # Data models
    └── models.py
```

---

## 🔧 Technology Stack

- **Streamlit** – Web UI
- **OpenAI API** – LLM agents (GPT-3.5-turbo)
- **Pandas & NumPy** – Data processing & calculations
- **Plotly** – Interactive charts
- **PyPDF2** – PDF text extraction
- **Pydantic** – Data validation

---

## 📐 How EERB Works

### 1. Data Input
- Load profile CSV
- PV capacity + generation profile
- BESS specs (energy, power, efficiency)
- Optional specification documents

### 2. Deterministic Calculations
```
Python functions execute:
- Peak load, average load, daily energy
- Battery duration (energy / power)
- SOC simulation
- Peak reduction estimate
```

### 3. Agent Analysis
```
Each agent independently:
- Examines assigned area
- Reports structured findings
- Identifies concerns
- Provides confidence level
```

### 4. Conflict Detection
```
System compares findings:
- Load peak duration vs. battery duration
- PV assumptions vs. load coverage
- Specification conflicts
- Missing information
```

### 5. Synthesis
```
Lead Engineer produces:
- Executive summary
- Key findings
- Critical conflicts
- Verification checklist
- Recommendations
```

---

## 📊 Input Data Format

### Load CSV
```csv
timestamp,load_kw
2026-09-08 00:00,85
2026-09-08 00:15,82
2026-09-08 00:30,80
...
```

### PV CSV (Optional)
```csv
timestamp,pv_kw
2026-09-08 00:00,0
2026-09-08 00:15,0
2026-09-08 06:00,5
...
```

---

## 🚢 Deployment to Streamlit Cloud

### 1. Push to GitHub
```bash
git add .
git commit -m "Initial EERB MVP"
git push origin main
```

### 2. Connect Streamlit Cloud
- Go to [streamlit.io/cloud](https://streamlit.io/cloud)
- Click "New app"
- Select GitHub repo and `app.py`

### 3. Add Secrets
In Streamlit Cloud dashboard → Secrets:
```
OPENAI_API_KEY = sk-...
```

### 4. Deploy
Click "Deploy" – app goes live in ~2 minutes

---

## 📝 Disclaimer

**This system provides an AI-assisted preliminary engineering review.**

It does NOT constitute:
- Final engineering design or certification
- Safety approval or testing
- Regulatory compliance guarantee


---

## 🔄 Agents Explained

### Load Analyst
Inspects load characteristics to understand project context.
- Peak demand, average load, daily energy
- Peak duration (how long peak lasts)
- Load variability analysis

### PV Engineer
Evaluates solar system adequacy.
- PV capacity vs. load
- Annual/daily energy generation
- Coverage ratio calculation
- Seasonal variation concerns

### BESS Engineer
Assesses battery storage system.
- **Duration = Energy / Power** (e.g., 1000 kWh / 500 kW = 2 hours)
- Peak-shaving capability
- SOC (State of Charge) constraints
- Efficiency losses

### Specification Engineer
Reviews technical documents and extracts specs.
- Equipment parameters
- Missing specifications
- Conflicting values
- Source tracking (RAG)

### Independent Critic
Challenges all conclusions.
- Identifies conflicts between agents
- Questions unsupported assumptions
- Flags missing information
- Assesses confidence levels

### Lead Engineer
Synthesizes all findings.
- Executive summary
- Overall design assessment
- Critical verification items
- Recommendations

---

## ⚡ Key Technologies

### Deterministic Calculation Engine
```python
# Example: Battery duration
duration_hours = energy_kwh / power_kw
# No LLM involved – pure math
```

### Conflict Detection
```python
if battery_duration < peak_duration:
    conflict = "Battery cannot support full peak"
```

### Simple RAG
- Extract text from PDFs
- Keyword-based search
- Source tracking
- No embeddings (for MVP simplicity)

---

## 🎓 Use Cases

- **Project developers** – Early-stage technical validation
- **Energy consultants** – Preliminary design review
- **EPC teams** – Pre-engineering feasibility check
- **Energy students** – Learning engineering review methodology
- **Procurement teams** – Vendor proposal evaluation

---

## 📧 Support

For issues or questions, contact the development team.

---

## 📜 License

This project is part of the Pak Angels HEC-NCAEC Generative & Agentic AI Training, Cohort 11 Mid-Term Hackathon.

---

**Built for the Pak Angels HEC-NCAEC Generative & Agentic AI Training, Cohort 11 Mid-Term Hackathon | Sep 2026****
