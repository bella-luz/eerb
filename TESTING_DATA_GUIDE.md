# EERB Testing Data Guide

## Demo Files Ready to Use ✅

Two realistic CSV files have been created for testing:

### 1. **Load Profile** (`data/demo_load_realistic.csv`)
- **48 hours** of commercial building electricity consumption
- **15-minute intervals** (96 data points)
- **Realistic pattern:**
  - Nighttime baseline: 50-85 kW
  - Early morning ramp: 06:00-09:00
  - Daytime peak: 270-325 kW (09:00-18:00)
  - Evening decline: 18:00-22:00
  - Midnight baseline: 75-85 kW

### 2. **PV Generation** (`data/demo_pv_realistic.csv`)
- **48 hours** of solar panel generation (500 kW capacity assumed)
- **Same 15-minute intervals**
- **Realistic solar pattern:**
  - Night: 0 kW (18:00-06:00)
  - Sunrise ramp: 06:00-09:00
  - Peak generation: 375 kW (10:00-14:00, ~75% of capacity)
  - Afternoon decline: 14:00-18:00
  - Sunset: <5 kW

---

## How to Use in Demo Video

### **Step 1: Upload Load Data**
In Streamlit "Upload" tab:
- Click "Upload load CSV"
- Select: `data/demo_load_realistic.csv`
- System validates: ✓ "Load data processed successfully"

### **Step 2: Configure System Specs**
- **PV Capacity:** 500 kW (pre-filled)
- **BESS Energy:** 1000 kWh
- **BESS Power:** 500 kW discharge
- **BESS Efficiency:** 90%

### **Step 3: Upload PV Data (Optional)**
- Click "Upload PV generation CSV"
- Select: `data/demo_pv_realistic.csv`
- System validates PV data

### **Step 4: Run Analysis**
- Click "Run Engineering Review"
- System performs:
  - Load analysis
  - PV evaluation
  - Battery assessment
  - AI agent analysis
  - Conflict detection
  - Report generation

---

## What EERB Will Find

With these datasets and 500 kW PV + 1 MWh battery:

✅ **Peak Load:** ~325 kW (13:00-18:00)  
✅ **Peak Duration:** ~5 hours (09:00-14:00)  
✅ **Daily Energy:** ~4,200 kWh  
✅ **Daily PV Generation:** ~2,500 kWh (est.)  
✅ **Battery Duration:** 2 hours (1000 kWh ÷ 500 kW)

**⚠️ Expected Conflict:**
- Load peak duration (5 hrs) > Battery discharge duration (2 hrs)
- Battery insufficient for stated peak-shaving objective
- AI system will flag this automatically

---

## File Locations

```
Mid Hackathon/
├── data/
│   ├── demo_load_realistic.csv       ← Use this for demo
│   ├── demo_pv_realistic.csv         ← Use this for demo
│   ├── demo_load.csv                 (old demo file)
│   └── demo_pv.csv                   (old demo file)
```

---

## Testing Checklist for Demo Video

- [ ] Navigate to Streamlit app
- [ ] Click "Upload" tab
- [ ] Upload load profile CSV
- [ ] Upload PV generation CSV
- [ ] Fill system specs (500 kW, 1000 kWh, 500 kW)
- [ ] Click "Run Engineering Review"
- [ ] Show analysis results
- [ ] Show conflict detection (Battery insufficient warning)
- [ ] Show agents' findings
- [ ] Show professional report

---

## Tips for Demo Video

1. **Clear audio:** Explain what EERB is analyzing
2. **Show real data:** Point out the load profile pattern
3. **Show the conflict:** Highlight when EERB detects the mismatch
4. **Show the value:** "EERB caught this issue in 2 minutes instead of 2 weeks"
5. **Professional tone:** "Multi-agent AI analysis identifies technical contradictions"

---

**Ready to record! Good luck with your demo! 🎬**
