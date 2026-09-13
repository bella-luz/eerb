# EERB Hackathon Submission Guide
## Complete Instructions for Setup, Testing, and Presentation

---

## 📋 Quick Start (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment
Create a `.env` file in the project root:
```
OPENAI_API_KEY=sk-your-key-here
```

### 3. Run the App
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

### 4. Test the Demo
- Click the **"View Demo"** button
- Click **"Run Engineering Review"**
- Wait for agents to complete analysis (~30-60 seconds)
- Review the dashboard and findings
- Scroll down to see the conflict detection

---

## 🎯 What is EERB?

**EERB (Energy Engineering Review Board)** is a multi-agent AI system that provides preliminary engineering review of renewable energy projects (PV + BESS) **before** detailed engineering work begins.

**Key Innovation:**
- 6 specialized AI agents analyze projects in parallel
- Deterministic calculations (no LLM hallucinations in math)
- Automatic conflict detection between findings
- Traceable engineering report in minutes, not weeks

**Target Users:**
- Renewable energy EPCs
- Energy consultants
- Project developers
- Engineering students
- Energy professionals

---

## 🚀 For the Hackathon Presentation

### Pre-Presentation Checklist

**30 minutes before:**
- [ ] Test the app locally: `streamlit run app.py`
- [ ] Verify the demo loads successfully
- [ ] Run the engineering review once to ensure API works
- [ ] Check dashboard and findings display correctly
- [ ] Verify report can be downloaded
- [ ] Have presentation slides ready (HACKATHON_PRESENTATION.md)

**During Setup:**
- [ ] Have projector/screen ready
- [ ] Open Streamlit app in browser (full screen, zoom 100%)
- [ ] Have backup presentation slides visible
- [ ] Keep presentation notes handy

### Presentation Flow (4-5 minutes)

**Slides 1-3: Setup (2 minutes)**
- Problem: Energy projects fail at preliminary stage
- Solution: EERB's 6-agent system
- How it works: Multi-agent architecture

**Slides 4-5: Live Demo (1.5-2 minutes)**
- Show demo project loading
- Run engineering review
- Show conflict detection
- Highlight findings and recommendations

**Slides 6-7: Impact & Q&A (30-45 seconds)**
- Business case (ROI)
- Call to action
- Open for questions

### Live Demo (What Judges See)

1. **Load Home Tab**
   - Show professional hero section
   - Show three core advantages
   - Show multi-agent system overview

2. **Click "View Demo"**
   - Demonstrates load CSV processing
   - Shows 500 kW PV + 1 MWh BESS system
   - Displays clean interface

3. **Click "Run Engineering Review"**
   - Show agents working in parallel
   - Agents: Load Analyst, PV Engineer, BESS Engineer, Spec Engineer, Critic, Lead Engineer
   - Wait for completion (~30-60 seconds)

4. **Show Results Dashboard**
   - **KPI Cards:** Peak load, daily energy, battery duration, etc.
   - **Charts:** Load profile, PV generation, battery SOC, peak reduction estimate
   - Professional interactive Plotly visualizations

5. **Show Findings by Severity**
   - **CRITICAL findings:** Battery duration mismatch
   - **HIGH findings:** Peak shaving capability gap
   - **MEDIUM findings:** Design assumptions to verify
   - **LOW findings:** Additional considerations

6. **Highlight the Key Conflict**
   - Load Analyst: "Peak lasts 4.5 hours"
   - BESS Engineer: "Battery only lasts 2 hours at 500 kW"
   - Critic: ⚠️ **CONFLICT DETECTED** - "This mismatch must be addressed"
   - Lead Engineer: "Recommendation: Reassess battery sizing or peak-shaving strategy"

7. **Show Final Report**
   - Executive summary
   - Findings organized by severity
   - Verification checklist
   - Downloadable text report

### Key Talking Points During Demo

- **"Notice the conflict detection."** The system doesn't just validate designs—it challenges them.
- **"All calculations are deterministic."** Duration = Energy ÷ Power. No AI guessing on critical math.
- **"This whole review took minutes."** Manual engineering review takes weeks and costs thousands.
- **"Every finding is source-referenced."** Judges can see exactly where each conclusion comes from.
- **"This is preliminary review."** Professional engineers verify before implementation—that's stated in the disclaimer.

---

## 📊 Project Structure

```
eerb/
├── app.py                           # Main Streamlit application (1342 lines)
├── requirements.txt                 # Python dependencies
├── .env                            # Environment variables (LOCAL ONLY)
├── .gitignore                      # Git configuration
│
├── data/
│   ├── demo_load.csv              # Load profile (commercial building)
│   ├── demo_load_realistic.csv     # Alternative realistic load
│   ├── demo_pv.csv                # PV generation profile
│   └── demo_pv_realistic.csv       # Alternative realistic PV
│
├── calculations/                   # Deterministic math engine
│   ├── load.py                    # Load analysis functions
│   ├── pv.py                      # PV calculations
│   └── battery.py                 # Battery simulation
│
├── agents/                         # AI multi-agent system
│   ├── orchestrator.py            # Coordinates all agents
│   ├── load_analyst.py            # Analyzes load profiles
│   ├── pv_engineer.py             # Evaluates PV systems
│   ├── bess_engineer.py           # Assesses battery systems
│   ├── specification_engineer.py   # Reviews technical docs
│   ├── critic.py                  # Identifies conflicts
│   └── lead_engineer.py           # Synthesizes findings
│
├── utils/                          # Utility functions
│   ├── data_processor.py          # CSV processing
│   └── rag.py                     # Document retrieval
│
├── schemas/                        # Data models
│   └── models.py                  # Pydantic models
│
└── Documentation/
    ├── README.md                  # Project overview
    ├── HACKATHON_PRESENTATION.md  # 7-slide presentation (4-5 min)
    ├── HACKATHON_GUIDE.md         # This file
    ├── TESTING_GUIDE.md           # Detailed testing procedures
    └── DEPLOYMENT_GUIDE.md        # Cloud deployment instructions
```

---

## 🧪 Testing Checklist

### Unit Tests (Pre-Presentation)

**Load Analysis:**
- Peak detection works correctly
- Peak duration calculation is accurate
- Load variability analysis produces reasonable values

**PV Analysis:**
- Solar generation calculated correctly
- Annual/daily energy generation produces realistic numbers
- Coverage ratio calculation works

**Battery Analysis:**
- Duration = Energy / Power formula correct
- SOC (State of Charge) simulation produces sensible curves
- Peak-shaving estimate is reasonable

### Integration Tests

**Data Processing:**
- CSV import works with required columns (timestamp, load_kw)
- Optional PV CSV imports correctly
- Data alignment handles different timestamp frequencies

**Agent Orchestration:**
- All 6 agents initialize successfully
- Agent analysis completes without errors
- Conflict detection identifies the design issue
- Lead engineer synthesizes findings correctly

**UI/UX Testing:**
- Tabs load without errors
- Demo project loads automatically
- Upload form accepts CSV files
- Results display renders correctly
- Download report button works
- All styling displays correctly (dark theme)

### Manual Testing Workflow

1. **Test the Demo Project**
   ```
   - Open app at http://localhost:8501
   - Click "View Demo"
   - Click "Run Engineering Review"
   - Wait for agents to complete
   - Verify all results appear
   - Check that conflict is identified
   - Test download report button
   ```

2. **Test Upload Workflow**
   ```
   - Click "Upload Project"
   - Enter project details
   - Upload demo CSV files from /data folder
   - Click "Run Engineering Review"
   - Verify results match demo results
   ```

3. **Verify Professional Design**
   ```
   - Check dark theme renders correctly
   - Verify all text is centered and professional
   - Check that color scheme is consistent
   - Ensure emoji icons display correctly
   - Verify no layout breaks on different screen sizes
   ```

4. **Test Error Handling**
   ```
   - Try uploading wrong file format
   - Try with missing required fields
   - Try with invalid API key
   - Verify error messages are user-friendly
   ```

---

## 🎨 Professional Styling Features

The app uses a **professional enterprise design system** with:

- **Dark Theme:** Neutral corporate background (slate blue accents)
- **Centered Layout:** All text center-aligned for professional look
- **Responsive Typography:** Large, readable fonts with proper hierarchy
- **Smooth Animations:** Hover effects, transitions
- **Professional Colors:**
  - Primary: Slate Blue (#4682B4)
  - Background: Dark Navy (#0F1419)
  - Accent: Cyan (#00D9FF)
  - Success: Green (#10B981)
  - Warning: Orange (#F97316)
  - Error: Red (#EF4444)

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'openai'"
**Solution:** Install requirements: `pip install -r requirements.txt`

### Issue: "OpenAI API key not found"
**Solution:** Create `.env` file with `OPENAI_API_KEY=sk-...`

### Issue: "Streamlit cloud deployment fails"
**Solution:** Add `OPENAI_API_KEY` to Streamlit Cloud secrets, not to `.env`

### Issue: "App runs but demo project doesn't load"
**Solution:** Check that `data/` folder exists with CSV files

### Issue: "Agents hang or timeout"
**Solution:** 
- Check OpenAI API rate limits
- Verify network connection
- Check that API key is valid
- Increase timeout in agent orchestrator if needed

### Issue: "CSV upload fails"
**Solution:** Ensure CSV has required columns: `timestamp` and `load_kw`

---

## 📱 Responsive Design

The app is designed for:
- **Desktop** (optimal): 1400+ px width
- **Laptop:** Full-width tabs and visualizations
- **Mobile:** Stacked layout, touch-friendly buttons

Note: For presentation, use a laptop/desktop screen with 1080p or higher resolution.

---

## 🚢 Deployment Options

### Option 1: Local Development
```bash
streamlit run app.py
```
Open `http://localhost:8501`

### Option 2: Streamlit Cloud (Free)
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Select repo and `app.py`
5. Add `OPENAI_API_KEY` to Secrets
6. Click Deploy

### Option 3: Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

```bash
docker build -t eerb .
docker run -p 8501:8501 -e OPENAI_API_KEY=sk-... eerb
```

---

## 📊 Performance Expectations

| Operation | Expected Time | Notes |
|-----------|---------------|-------|
| App startup | 2-3 seconds | Streamlit initialization |
| Demo project load | <1 second | Pre-loaded data |
| Engineering review | 30-60 seconds | 6 agents analyzing in parallel |
| Results display | <1 second | Immediate render |
| Report generation | <1 second | Markdown compilation |

---

## 🎓 Learning Resources

**For judges/evaluators:**
- **README.md** - Project overview and concepts
- **PRESENTATION_SLIDES.md** - Detailed slide notes (for reference)
- **HACKATHON_PRESENTATION.md** - Condensed 7-slide presentation
- **TESTING_GUIDE.md** - Test procedures and expected results
- **DEPLOYMENT_GUIDE.md** - Cloud deployment instructions

**For users:**
- **In-app Overview tab** - System architecture and agents
- **In-app Home tab** - Value proposition and use cases
- **In-app disclaimer** - Legal and scope limitations

---

## 💡 Key Differentiators to Emphasize

1. **Deterministic Math:** Battery duration = Energy ÷ Power (verifiable)
2. **Multi-Agent Architecture:** 6 specialized agents challenge each other
3. **Conflict Detection:** System identifies contradictions, not just summaries
4. **Speed:** 2-5 minutes vs. 1-2 weeks for manual review
5. **Traceability:** Every finding source-referenced and justified

---

## ⚖️ Disclaimer (Always Visible in App)

**EERB provides an AI-assisted preliminary engineering review.**

It does NOT constitute:
- ❌ Final engineering design
- ❌ Safety certification  
- ❌ Regulatory approval
- ❌ Professional engineering sign-off

**Licensed professional engineers must verify all conclusions before implementation.**

---

## 🏆 Hackathon Evaluation Criteria

**What judges are looking for:**
- ✅ **Problem Understanding:** Is the problem real and important?
- ✅ **Solution Design:** Is the approach sound and innovative?
- ✅ **Technical Execution:** Does the code work correctly?
- ✅ **Presentation:** Is the pitch clear and compelling?
- ✅ **Demo:** Does it work live without errors?
- ✅ **Value Proposition:** Why would someone use this?
- ✅ **Business Model:** Is there a path to market?

**EERB Strengths:**
- ✅ Solves real engineering problem
- ✅ Multi-agent architecture is innovative
- ✅ Deterministic math prevents hallucinations
- ✅ Conflict detection is unique feature
- ✅ Professional UI/UX
- ✅ Works reliably in demo
- ✅ Clear market (renewable energy industry)
- ✅ Revenue model (subscription, per-project, enterprise)

---

## 📞 Support

If issues arise during presentation:

1. **App won't start:** Restart Streamlit, check Python environment
2. **Demo hangs:** Check OpenAI API quota, verify internet connection
3. **Display issues:** Refresh browser, clear cache
4. **Data missing:** Verify `/data` folder has CSV files

**Fallback:** Have presentation slides ready to present without live demo if needed.

---

## 🎉 Final Notes

- **Start early:** Test everything 30+ minutes before presentation
- **Have a backup:** Screenshots of working demo on phone
- **Know your talking points:** Practice the narrative before presenting
- **Engage judges:** Ask questions, invite feedback
- **Be honest:** Acknowledge limitations and MVP status
- **Show enthusiasm:** Believe in the product and its potential

**"This is the future of preliminary engineering review."**

---

*Last Updated: September 13, 2026*  
*For Pak Angels HEC-NCAEC Generative & Agentic AI Training, Cohort 11 Mid-Term Hackathon*
