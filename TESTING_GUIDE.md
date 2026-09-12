# Testing Guide - Input Files & Scenarios

## 📊 Where Are Test Files?

All test files are **already bundled** in your project:

```
C:\Users\dandy\Desktop\Iqra\AI training\Mid Hackathon\data\
├── demo_load.csv          ← Load profile data
└── demo_pv.csv            ← Solar generation data
```

---

## ✅ TESTING SCENARIO 1: Demo Mode (Easiest)

### No files needed! Just click.

1. Run the app: `streamlit run app.py`
2. Click sidebar: **"Demo Project"**
3. View project info (500 kW PV + 1 MWh BESS)
4. Click **"Run Engineering Review"**
5. Wait 30 seconds for agents to analyze
6. See dashboard with charts and findings

**What you'll see:**
- ✅ Load profile chart
- ✅ PV generation chart
- ✅ Battery SOC chart
- ✅ Peak reduction chart
- ✅ **CONFLICT DETECTED:** Battery duration (2h) < Peak period (4.5h)
- ✅ Downloadable report

**Time:** 2-5 minutes including runtime

---

## ✅ TESTING SCENARIO 2: Upload Mode (Using Demo Data)

### Use the bundled CSV files

1. Click sidebar: **"Upload Project"**
2. Fill in project info:
   - Project Name: `Test Project`
   - Type: `PV + BESS`
   - Location: `Karachi`
   - Objective: `Reduce peak demand`
3. PV Capacity: `500` kW
4. BESS Energy: `1000` kWh
5. BESS Power: `500` kW
6. **Upload Load CSV:** `C:\Users\dandy\Desktop\Iqra\AI training\Mid Hackathon\data\demo_load.csv`
7. **Upload PV CSV:** `C:\Users\dandy\Desktop\Iqra\AI training\Mid Hackathon\data\demo_pv.csv`
8. Click **"Run Engineering Review"**

**Expected Result:** Same as Demo Mode (same data)

---

## ✅ TESTING SCENARIO 3: Create Your Own Test CSV

### Generate test data for different scenarios

#### Test Data 1: Small Load (Easier Battery)

Save as `test_small_load.csv`:

```csv
timestamp,load_kw
2026-09-08 00:00,50
2026-09-08 00:15,50
2026-09-08 00:30,50
2026-09-08 00:45,50
2026-09-08 01:00,50
2026-09-08 01:15,100
2026-09-08 01:30,150
2026-09-08 01:45,150
2026-09-08 02:00,150
2026-09-08 02:15,100
2026-09-08 02:30,50
2026-09-08 02:45,50
```

**Then test with:**
- PV: 100 kW
- BESS: 200 kWh, 100 kW

**Expected outcome:** No conflict (battery adequate)

#### Test Data 2: Large Load (Battery Stressed)

Save as `test_large_load.csv`:

```csv
timestamp,load_kw
2026-09-08 00:00,100
2026-09-08 00:15,100
2026-09-08 00:30,100
2026-09-08 00:45,100
2026-09-08 01:00,100
2026-09-08 01:15,500
2026-09-08 01:30,800
2026-09-08 01:45,900
2026-09-08 02:00,1000
2026-09-08 02:15,1000
2026-09-08 02:30,1000
2026-09-08 02:45,800
2026-09-08 03:00,500
2026-09-08 03:15,100
2026-09-08 03:30,100
2026-09-08 03:45,100
```

**Then test with:**
- PV: 500 kW
- BESS: 500 kWh, 200 kW

**Expected outcome:** Conflict (peak lasts 8 intervals = 2 hours, battery provides 2.5 hours, but peak is high)

---

## 📋 CSV Format Requirements

### Required Columns

**Load CSV:**
```csv
timestamp,load_kw
2026-09-08 00:00,85
2026-09-08 00:15,82
```

- **Column 1:** `timestamp` (any datetime format, e.g., `2026-09-08 00:00`)
- **Column 2:** `load_kw` (numbers only, no negative values)

**PV CSV (Optional):**
```csv
timestamp,pv_kw
2026-09-08 06:00,5
2026-09-08 06:15,15
```

- **Column 1:** `timestamp` (must match load CSV times if used together)
- **Column 2:** `pv_kw` (numbers, can be 0)

### What App Validates

✅ Timestamps are valid  
✅ load_kw column exists  
✅ All values are numbers  
✅ No negative values  
✅ No missing data points  

If validation fails, you get a clear error message.

---

## 🧪 TEST CHECKLIST

### Before Deployment

- [ ] **Demo Mode Works**
  - [ ] "Demo Project" button works
  - [ ] "Run Engineering Review" executes
  - [ ] Charts display (load, PV, SOC, peak)
  - [ ] Dashboard shows findings
  - [ ] Conflict is highlighted
  - [ ] Report downloads

- [ ] **Upload Mode Works**
  - [ ] Load CSV upload accepts demo_load.csv
  - [ ] Form validation works
  - [ ] "Run Engineering Review" executes
  - [ ] Results display
  - [ ] Same conflict detected

- [ ] **Edge Cases**
  - [ ] Handles small datasets
  - [ ] Handles large datasets
  - [ ] Shows error for malformed CSV
  - [ ] Graceful fallback if PDF processing fails

---

## 🚀 LOCAL TESTING

### Before Pushing to GitHub

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run locally:**
   ```bash
   cd "C:\Users\dandy\Desktop\Iqra\AI training\Mid Hackathon"
   streamlit run app.py
   ```

3. **Open browser:**
   ```
   http://localhost:8501
   ```

4. **Test both modes:**
   - Demo Project (quick test)
   - Upload Project with demo_load.csv (comprehensive test)

5. **Verify:**
   - ✅ No error messages in console
   - ✅ Charts render
   - ✅ All buttons work
   - ✅ Download works

---

## 🐛 DEBUGGING

### If Demo Project Fails

**Error:** "FileNotFoundError: data/demo_load.csv"

**Fix:** Ensure you're running from the correct directory:
```bash
cd "C:\Users\dandy\Desktop\Iqra\AI training\Mid Hackathon"
streamlit run app.py
```

### If Upload Fails

**Error:** "CSV must contain 'load_kw' column"

**Fix:** Check your CSV has exactly these columns:
- `timestamp`
- `load_kw`

No extra columns, exact column names.

### If Charts Don't Render

**Fix:** Plotly should be installed. Reinstall:
```bash
pip install --upgrade plotly
```

### If LLM Agents Fail

**Error:** "ERROR: OPENAI_API_KEY not found"

**Fix:** Ensure `.env` file exists in project root with:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

---

## 📊 What Each Test Verifies

| Test | Verifies | Success Indicator |
|------|----------|-------------------|
| Demo Project | Full workflow, agents, calculations | Charts + conflict detected |
| Upload CSV | Data validation, parsing | Same results as demo |
| Small Load | Undersized BESS scenario | No conflict (battery adequate) |
| Large Load | Oversized peak scenario | Conflict detected |
| Malformed CSV | Error handling | Clear error message |

---

## ✅ READY FOR DEPLOYMENT?

When all tests pass, you're ready to:

1. ✅ Push to GitHub
2. ✅ Deploy to Streamlit Cloud
3. ✅ Record demo video

Checklist:
- [ ] Demo mode works perfectly
- [ ] Upload mode works perfectly
- [ ] Conflict is detected in demo
- [ ] Report downloads without error
- [ ] No error messages in console
- [ ] All buttons responsive
- [ ] Charts render clearly

---

## 📞 NEED HELP?

If something breaks:
1. Run `pip install -r requirements.txt` again
2. Delete `.streamlit/cache` folder if it exists
3. Restart Streamlit: `Ctrl+C`, then `streamlit run app.py`
4. Check that `.env` file has your API key

---

*Ready to test? Start with Demo Mode - it's the fastest way to verify everything works!*
