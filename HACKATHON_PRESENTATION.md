# EERB - Energy Engineering Review Board
## Hackathon Presentation (4-5 minutes)

**Tagline:** "AI engineering review before you build."

---

## Slide 1: The Problem (30 seconds)

### ⚠️ Energy Projects Fail in Early Stages

**The Challenge:**
- Projects discover design conflicts **AFTER** expensive engineering work begins
- Battery can't discharge long enough for peak period
- PV capacity insufficient for load profile
- Load data conflicts with tariff requirements

**Current Cost:** Weeks of delay, engineering rework expenses, schedule pressure

**"We saw this happen repeatedly. Technical issues that should take hours to catch were found after months of engineering."**

---

## Slide 2: The Solution (45 seconds)

### ⚡ EERB: AI-Powered Engineering Review

**What It Does:**
- Submit project data (load, PV, battery specs)
- **6 specialized AI agents** analyze in parallel
- **Conflict detection** automatically identifies issues
- **Final report** in 2-5 minutes

**Key Innovation:**
- ✅ Deterministic math (no hallucinations)
- ✅ Independent analysis (agents challenge each other)
- ✅ Traceable findings (every conclusion source-verified)

**Bottom Line:** Catch design flaws early. Save weeks and thousands.

---

## Slide 3: How It Works (45 seconds)

### Multi-Agent Engineering System

**6 AI Agents Working in Parallel:**

1. **Load Analyst** → Peak duration, daily energy patterns
2. **PV Engineer** → Solar capacity adequacy  
3. **BESS Engineer** → Battery storage capability
4. **Specification Engineer** → Technical document review
5. **Independent Critic** → Challenges assumptions, finds conflicts
6. **Lead Engineer** → Synthesizes findings, final recommendation

**The Magic:** Each agent works independently, then the Critic compares findings to identify contradictions.

---

## Slide 4: Live Demo (45 seconds)

### The Real Issue: A Design Conflict

**Project:** 500 kW PV + 1 MWh Battery System  
**Goal:** Reduce peak demand by 30%

**The Problem:**
- Load peak duration: **4.5 hours**
- Battery discharge time: **2 hours** (at 500 kW)
- **Gap:** Battery can't support the full peak period

**How EERB Catches It:**
1. Load Analyst: "Peak requires 4.5-hour support"
2. BESS Engineer: "Battery only lasts 2 hours"
3. Critic: ⚠️ **CONFLICT DETECTED**
4. Report: "⚠️ Reassess battery sizing before proceeding"

---

## Slide 5: Why This Matters (45 seconds)

### Three Competitive Advantages

**1. Deterministic Math**
- No LLM guessing on critical numbers
- Duration = Energy ÷ Power (verified)
- Every calculation is auditable

**2. Conflict Detection**
- Automatic comparison of findings
- Highlights design contradictions
- Shows where teams need to dig deeper

**3. Speed + Transparency**
- 5 minutes → professional assessment
- Every finding source-referenced
- Actionable recommendations

**Result:** Issues caught at preliminary stage cost 10x less to fix than during detailed design.

---

## Slide 6: Impact & Vision (30 seconds)

### Real-World ROI

**Before EERB:**
- Manual review: 1-2 weeks
- Cost: $2K-$5K per review
- Risk: Issues found late (expensive)

**With EERB:**
- Automated review: 2-5 minutes
- Cost: Negligible per review
- Risk: Issues found early (cheap to fix)

**Addressable Market:** 
- Renewable energy EPCs (thousands globally)
- Energy consultants and developers
- Project financing teams
- Engineering schools

**Vision:** Make rigorous engineering review accessible, fast, and affordable.

---

## Slide 7: Try It Now (15 seconds)

### Live Demo + Q&A

**"Let's see EERB in action."**

*[Click "Demo Project" → Run Review → Show conflict detection → Download report]*

**"This is the future of preliminary engineering review."**

---

## Speaker Notes

### Slide 1 (30 sec)
Start with a real problem. Energy projects regularly fail at the preliminary stage because design contradictions aren't caught early. Make it personal: "We saw this in the field." Lead with business impact—weeks of delay and engineering rework costs.

### Slide 2 (45 sec)
Introduce the solution. Emphasize **6 agents working in parallel**. Highlight the three key differentiators: math, independence, traceability. End with the value prop: "Catch issues early. Save money."

### Slide 3 (45 sec)
Walk through the 6 agents quickly. The **Critic** is the differentiator—it challenges conclusions instead of just summarizing. This is what makes EERB different from a chatbot.

### Slide 4 (45 sec)
**THIS IS THE CORE.** Show the real conflict:
- Load peak: 4.5 hours
- Battery: 2 hours
- Why: 1000 kWh ÷ 500 kW = 2 hours

Show how each agent identifies it. Show the Critic flagging it. Emphasize: "EERB doesn't validate bad designs—it challenges them."

### Slide 5 (45 sec)
Differentiation. Why not just use ChatGPT? Because EERB has math (not guesses), conflict detection (not just summaries), and transparency (traceable findings). The deterministic math is key.

### Slide 6 (30 sec)
Impact story. Real numbers. Before/after. ROI. Addressable market is large. Vision is compelling: "Make rigorous review fast and affordable."

### Slide 7 (15 sec)
Transition to live demo. Keep it short. Show confidence in the product.

---

## Presentation Timing

| Slide | Topic | Time |
|-------|-------|------|
| 1 | Problem | 30s |
| 2 | Solution | 45s |
| 3 | How It Works | 45s |
| 4 | Live Demo | 45s |
| 5 | Why It Matters | 45s |
| 6 | Impact | 30s |
| 7 | Call to Action | 15s |
| — | **Live Demo (if time)** | **~60s** |
| — | **Q&A** | **Remaining** |

**Total:** 5-6 minutes (+ live demo + Q&A)

---

## Key Messages to Reinforce

✅ **Problem:** Energy projects fail early. It's expensive and preventable.  
✅ **Solution:** AI agents + deterministic math catch issues in minutes.  
✅ **Differentiation:** Not validation—it's conflict detection.  
✅ **Proof:** The demo shows a real design flaw that EERB automatically caught.  
✅ **Impact:** Saves weeks and thousands per project.  
✅ **Call to Action:** "Try EERB for your next project."

---

## Live Demo Walkthrough

**Duration:** ~60 seconds (optional, time permitting)

1. Click **"View Demo"** button
2. Show the demo project loads (500 kW PV + 1 MWh BESS)
3. Click **"Run Engineering Review"**
4. Show agents analyzing in parallel (1-2 sec)
5. Show **Dashboard** with 4 charts (load, PV, SOC, peak before/after)
6. Scroll to **Findings** section
7. Highlight the **CONFLICT** in findings:
   - "⚠️ CRITICAL: Peak shaving duration mismatch"
   - "Load peak duration: 4.5 hours"
   - "Battery discharge duration: 2 hours"
   - "Recommendation: Reassess battery sizing or adjust peak-shaving target"
8. Show **Download Report** button
9. **Key Moment:** "See how EERB challenges the design instead of just validating it?"

---

## Q&A Anticipated Questions

**Q: Isn't this just a chatbot that makes up engineering answers?**  
A: No. EERB's core is deterministic math. Battery duration = Energy ÷ Power. That's verifiable. The AI agents provide context and reasoning, but every critical calculation is pure mathematics.

**Q: How accurate is this compared to professional software like HOMER or PVsyst?**  
A: EERB is preliminary review, not detailed design. It's 10 minutes vs. 10 weeks. But it catches design flaws early. You use EERB first to sanity-check, then HOMER/PVsyst for detailed engineering.

**Q: Who would actually pay for this?**  
A: EPCs doing preliminary feasibility (they spend $2K-$5K per manual review today). Energy consultants vetting projects. Project developers validating concepts. The addressable market is large.

**Q: What happens if I disagree with EERB's findings?**  
A: Great—that's the point. EERB surfaces issues for professional review, not final judgment. All findings are justified and traceable. You decide next steps.

**Q: Can this replace a professional engineer?**  
A: No. EERB is decision-support. Professional engineers verify all conclusions before implementation. That's stated clearly in the disclaimer.

---

## Important Notes

- **NO personal names** in presentation
- **Keep claims conservative** (no unsupported hyperbole)
- **Disclaimer always visible** (at bottom of website)
- **Demo must work flawlessly** (pre-test before presentation)
- **Speak to energy professionals** (use technical language correctly)
- **Focus on value to end users** (time saved, risk reduced, cost avoided)

---

*Presentation prepared for Pak Angels HEC-NCAEC Generative & Agentic AI Training, Cohort 11 Mid-Term Hackathon*

*September 13, 2026*
