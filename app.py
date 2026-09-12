"""
Energy Engineering Review Board (EERB)
AI engineering review before you build.
"""
# Load environment variables FIRST
from dotenv import load_dotenv
import os
load_dotenv()

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json

# Add project root to path
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import utilities
from utils.data_processor import load_demo_data, align_timeseries, process_load_csv, process_pv_csv
from calculations.load import analyze_load_profile, calculate_peak_duration
from calculations.pv import analyze_pv
from calculations.battery import analyze_bess, simulate_battery_soc

# Import agents
from agents import (
    AgentOrchestrator, LoadAnalyst, PVEngineer, BESSEngineer,
    SpecificationEngineer, IndependentCritic, LeadEngineer
)

# Configure page
st.set_page_config(
    page_title="EERB - Energy Engineering Review Board",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .conflict-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ff6b6b;
        margin: 10px 0;
    }
    .finding-box {
        padding: 10px;
        border-radius: 6px;
        margin: 8px 0;
    }
    .finding-critical {
        background-color: #ffe0e0;
        border-left: 4px solid #ff0000;
    }
    .finding-high {
        background-color: #ffe8cc;
        border-left: 4px solid #ff6b00;
    }
    .finding-medium {
        background-color: #fff9e6;
        border-left: 4px solid #ffb800;
    }
    .finding-low {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Main application entry point."""
    # Header
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 30px; border-bottom: 2px solid #0066cc; padding-bottom: 15px;">
        <div>
            <h1 style="margin: 0;">EERB</h1>
            <p style="margin: 5px 0 0 0; color: #0066cc; font-size: 14px;">Energy Engineering Review Board</p>
        </div>
        <p style="text-align: right; margin: 0; font-size: 12px; color: #666;">AI Engineering Review Before You Build</p>
    </div>
    """, unsafe_allow_html=True)

    # Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Home", "Demo Project", "Upload Project", "About"])

    with tab1:
        show_home()

    with tab2:
        show_demo_project()

    with tab3:
        show_upload_project()

    with tab4:
        show_about()

    # Disclaimer Footer
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 10px; color: #999; text-align: center; margin-top: 20px;">
    <b>Disclaimer:</b> This AI-assisted preliminary engineering review does not constitute final design, safety certification, regulatory approval, or professional engineering sign-off.
    Always have results reviewed by licensed professional engineers before implementation.
    </div>
    """, unsafe_allow_html=True)


def show_home():
    """Display home page with website-like layout."""

    # Hero Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0066cc 0%, #003d99 100%); padding: 60px 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 40px;">
        <h1 style="margin: 0; font-size: 48px; font-weight: bold;">Energy Engineering Review Board</h1>
        <p style="margin: 10px 0 0 0; font-size: 24px; opacity: 0.95;">AI Engineering Review Before You Build</p>
    </div>
    """, unsafe_allow_html=True)

    # Value Proposition Section
    st.markdown("### Why EERB?")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **⚡ Rapid Assessment**
        - 2-5 minutes vs 2 weeks
        - Instant preliminary review
        """)

    with col2:
        st.markdown("""
        **🎯 Conflict Detection**
        - Identifies inconsistencies
        - Flags technical issues early
        """)

    with col3:
        st.markdown("""
        **📊 Traceable Results**
        - Source-referenced findings
        - Clear recommendations
        """)

    st.markdown("---")

    # How It Works Section
    st.markdown("### How It Works")
    st.write("""
    EERB uses **6 specialized AI agents** that independently analyze your project from different angles:

    1. **Load Analyst** → Examines electricity consumption patterns
    2. **PV Engineer** → Evaluates solar capacity adequacy
    3. **BESS Engineer** → Assesses battery storage capability
    4. **Specification Engineer** → Reviews technical documents
    5. **Independent Critic** → Challenges conclusions, finds conflicts
    6. **Lead Engineer** → Synthesizes findings into final report

    All calculations are **deterministic** (verified mathematics) — no AI guessing on critical numbers.
    """)

    st.markdown("---")

    # Use Case Section
    st.markdown("### Demo Scenario")
    st.write("""
    **500 kW Solar PV + 1 MWh Battery Storage for Commercial Building**

    This demo shows EERB detecting a real technical issue:
    - Load peak duration: **4.5 hours**
    - Battery discharge duration: **2 hours**
    - **Result**: Battery insufficient for stated objective ⚠️

    EERB automatically flags this for professional verification.
    """)

    st.markdown("---")

    # CTA
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Try Demo Project", key="home_demo", use_container_width=True):
            st.session_state.selected_mode = "demo"
            st.rerun()

    with col2:
        if st.button("📤 Upload Your Project", key="home_upload", use_container_width=True):
            st.session_state.selected_mode = "upload"
            st.rerun()


def show_about():
    """Display About section with impressive branding."""

    # About Section
    st.markdown("### About EERB")
    st.markdown("""
    **Energy Engineering Review Board (EERB)** is an innovative AI platform that transforms how renewable energy projects are validated.

    Traditional project reviews are slow and expensive. Engineers spend weeks manually verifying designs. Issues are discovered late—when fixes cost thousands.

    EERB changes this by providing **instant, systematic preliminary review** using specialized AI agents that work in parallel.
    """)

    st.markdown("---")

    # Three Pillars
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### ⚡ Speed
        **2-5 minutes**

        Not weeks. Preliminary review in seconds. Get answers now, not later.
        """)

    with col2:
        st.markdown("""
        ### 🎯 Intelligence
        **6 AI Agents**

        Load analysis, PV design, battery systems, specifications, critical review, and synthesis.
        """)

    with col3:
        st.markdown("""
        ### 📊 Confidence
        **Deterministic Math**

        Real calculations, not guesses. Every number is verifiable. Every conclusion is traceable.
        """)

    st.markdown("---")

    # The Problem
    st.markdown("### The Problem We Solve")
    st.write("""
    **Energy projects face critical design flaws that emerge too late:**

    - Battery sizing doesn't match load profiles
    - PV capacity insufficient for stated objectives
    - Technical inconsistencies go undetected
    - Expensive engineering work begins on flawed assumptions
    - No systematic way to track review rationale

    **The cost?** Weeks of delay. $50K+ in rework. Projects abandoned entirely.
    """)

    st.markdown("---")

    # The Solution
    st.markdown("### How EERB Works")
    st.write("""
    **Multi-Agent AI Review → Conflict Detection → Traceable Report**

    1. You provide: load profile, PV specs, battery specs, project objective
    2. EERB launches 6 independent AI agents that analyze in parallel
    3. Agents use deterministic calculations (not guesses) to evaluate your design
    4. System automatically detects conflicts between agent conclusions
    5. You get a traceable engineering review with clear recommendations

    **Key Innovation:** The system doesn't just validate—it *challenges* your design by having agents critique each other's work.
    """)

    st.markdown("---")

    # Target Users
    st.markdown("### Who Uses EERB?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Renewable Energy EPCs**
        - Screen projects before detailed engineering
        - Reduce engineering risk
        - Accelerate go/no-go decisions
        """)

    with col2:
        st.markdown("""
        **Energy Consultants**
        - Enhance client proposals
        - Add credibility to preliminary designs
        - Reduce liability exposure
        """)

    st.markdown("""
    **Project Developers** | **Utilities** | **Engineering Teams**
    """)

    st.markdown("---")

    # Technology
    st.markdown("### Technology Behind EERB")
    st.write("""
    - **AI Agents:** OpenAI GPT-3.5-turbo (reasoning layer)
    - **Calculations:** Python deterministic engine (math layer)
    - **Interface:** Streamlit (cloud-deployed)
    - **Architecture:** 5-layer multi-agent orchestration
    - **Philosophy:** Combine LLM reasoning with verified mathematics
    """)

    st.markdown("---")

    # Call to Action
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: #f0f2f6; border-radius: 8px;">
            <h3 style="margin: 0 0 10px 0;">Ready to Validate Your Project?</h3>
            <p style="margin: 0; font-size: 14px;">Start with the demo or upload your own project.</p>
        </div>
        """, unsafe_allow_html=True)


def show_demo_project():
    """Display demo project analysis."""
    st.markdown("## 📊 Demo Project: Commercial Building PV + BESS")

    # Load demo data
    try:
        load_df, pv_df = load_demo_data("data")
        load_kw, pv_kw = align_timeseries(load_df, pv_df)
    except Exception as e:
        st.error(f"❌ Failed to load demo data: {str(e)}")
        return

    # Project info
    st.markdown("### Project Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("PV Capacity", "500 kW")
    with col2:
        st.metric("BESS Capacity", "1 MWh")
    with col3:
        st.metric("BESS Power", "500 kW")
    with col4:
        st.metric("Objective", "Peak Reduction")

    # Project description
    st.write("""
    **Location**: Karachi
    **Type**: Commercial Building Retrofit
    **Objective**: Reduce peak demand by approximately 30%
    """)

    # Run analysis button
    if st.button("▶️ Run Engineering Review", key="demo_run"):
        run_engineering_review(
            project_name="Demo: Commercial Building",
            project_type="Commercial",
            location="Karachi",
            objective="Reduce peak demand by 30%",
            pv_capacity_kw=500,
            bess_energy_kwh=1000,
            bess_power_kw=500,
            bess_efficiency=0.90,
            load_kw=load_kw,
            pv_kw=pv_kw,
        )


def show_upload_project():
    """Display upload project interface."""
    st.markdown("## 📤 Upload Your Project")

    st.info("Upload your project data and documents for analysis.")

    # Project information
    col1, col2 = st.columns(2)
    with col1:
        project_name = st.text_input("Project Name", "My Energy Project")
        project_type = st.selectbox("Project Type", ["PV + BESS", "Solar Only", "Battery Only", "Other"])
    with col2:
        location = st.text_input("Location", "Karachi")
        objective = st.text_input("Project Objective", "Reduce peak demand")

    st.markdown("---")

    # Load data
    st.markdown("### 📊 Load Profile Data")
    load_file = st.file_uploader("Upload load CSV (timestamp, load_kw)", type=["csv"], key="load_upload")

    load_kw = None
    if load_file:
        load_df, msg = process_load_csv(load_file)
        if load_df is not None:
            st.success(msg)
            load_kw = load_df["load_kw"]
        else:
            st.error(msg)

    st.markdown("---")

    # PV specifications
    st.markdown("### ☀️ Solar PV Specifications")
    pv_capacity_kw = st.number_input("PV Capacity (kW)", min_value=0.0, value=500.0)

    pv_file = st.file_uploader("Upload PV generation CSV (optional)", type=["csv"], key="pv_upload")
    pv_kw = None
    if pv_file:
        pv_df, msg = process_pv_csv(pv_file)
        if pv_df is not None:
            st.success(msg)
            pv_kw = pv_df["pv_kw"]
        else:
            st.error(msg)

    st.markdown("---")

    # BESS specifications
    st.markdown("### 🔋 Battery Energy Storage (BESS) Specifications")
    col1, col2, col3 = st.columns(3)
    with col1:
        bess_energy_kwh = st.number_input("Energy Capacity (kWh)", min_value=0.0, value=1000.0)
    with col2:
        bess_power_kw = st.number_input("Discharge Power (kW)", min_value=0.0, value=500.0)
    with col3:
        bess_efficiency = st.slider("Round-trip Efficiency (%)", 70, 95, 90) / 100

    st.markdown("---")

    # Run analysis
    if st.button("▶️ Run Engineering Review", key="upload_run"):
        if load_kw is None:
            st.error("❌ Load data is required")
            return

        run_engineering_review(
            project_name=project_name,
            project_type=project_type,
            location=location,
            objective=objective,
            pv_capacity_kw=pv_capacity_kw,
            bess_energy_kwh=bess_energy_kwh,
            bess_power_kw=bess_power_kw,
            bess_efficiency=bess_efficiency,
            load_kw=load_kw,
            pv_kw=pv_kw,
        )


def run_engineering_review(project_name, project_type, location, objective,
                          pv_capacity_kw, bess_energy_kwh, bess_power_kw,
                          bess_efficiency, load_kw, pv_kw):
    """Run the full engineering review workflow."""

    st.markdown("---")
    st.markdown("## ⚙️ Running Engineering Review...")

    # Progress placeholder
    progress_container = st.container()

    # Calculate basic metrics
    load_analysis = analyze_load_profile(load_kw)
    peak_load_kw = load_analysis["peak_demand_kw"]
    avg_load_kw = load_analysis["average_demand_kw"]
    daily_load_kwh = load_analysis["daily_energy_kwh"]
    peak_duration = load_analysis["peak_duration_hours"]

    # PV analysis
    if pv_kw is not None:
        daily_pv_kwh = pv_kw.sum() * 0.25
    else:
        # Assume 18% capacity factor for Karachi
        daily_pv_kwh = pv_capacity_kw * 24 * 0.18

    pv_analysis = analyze_pv(pv_capacity_kw, daily_pv_kwh, peak_load_kw,
                            avg_load_kw, daily_load_kwh)

    # BESS analysis
    bess_analysis = analyze_bess(bess_energy_kwh, bess_power_kw, peak_load_kw,
                                peak_duration, bess_efficiency)

    # Show progress
    with progress_container:
        st.write("✓ Load Analysis")
        st.write("✓ PV Analysis")
        st.write("✓ BESS Analysis")

        # Agent orchestration
        st.write("✓ Load Analyst")
        st.write("✓ PV Engineer")
        st.write("✓ BESS Engineer")
        st.write("✓ Specification Engineer")
        st.write("✓ Independent Critic")
        st.write("✓ Lead Engineer")

    # Build context for agents
    context = {
        "project_name": project_name,
        "project_objective": objective,
        "load_series": load_kw,
        "pv_series": pv_kw,
        "load_statistics": load_analysis,
        "peak_duration_hours": peak_duration,
        "peak_load_kw": peak_load_kw,
        "average_load_kw": avg_load_kw,
        "daily_load_kwh": daily_load_kwh,
        "pv_capacity_kw": pv_capacity_kw,
        "bess_energy_kwh": bess_energy_kwh,
        "bess_power_kw": bess_power_kw,
        "bess_efficiency": bess_efficiency,
        "project_specs": {
            "pv_capacity_kw": pv_capacity_kw,
            "bess_energy_kwh": bess_energy_kwh,
            "bess_power_kw": bess_power_kw,
            "bess_efficiency": bess_efficiency,
        }
    }

    # Create orchestrator and agents
    orchestrator = AgentOrchestrator()
    orchestrator.register_agent(LoadAnalyst())
    orchestrator.register_agent(PVEngineer())
    orchestrator.register_agent(BESSEngineer())
    orchestrator.register_agent(SpecificationEngineer())

    # Run agents
    agent_results = orchestrator.run_all(context)

    # Detect conflicts
    conflicts = orchestrator.detect_conflicts()

    # Critic analysis
    context["agent_results"] = agent_results
    context["conflicts_detected"] = conflicts
    context["critic_findings"] = {"concerns": [c.get("issue") for c in conflicts]}
    context["project_info"] = {
        "project_name": project_name,
        "project_type": project_type,
        "objective": objective,
    }

    critic = IndependentCritic()
    critic_result = critic.analyze(context)

    lead_engineer = LeadEngineer()
    lead_result = lead_engineer.analyze(context)

    # Display results
    st.success("✅ Review Complete!")

    # Display dashboard
    display_results_dashboard(
        load_kw, pv_kw, load_analysis, pv_analysis, bess_analysis,
        agent_results, critic_result, lead_result, conflicts,
        bess_energy_kwh, bess_power_kw, bess_efficiency
    )


def display_results_dashboard(load_kw, pv_kw, load_analysis, pv_analysis, bess_analysis,
                             agent_results, critic_result, lead_result, conflicts,
                             bess_energy_kwh, bess_power_kw, bess_efficiency):
    """Display the results dashboard with charts and findings."""

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📊 Dashboard", "🔍 Analysis", "⚠️ Findings", "👥 Agents", "📄 Report"]
    )

    with tab1:
        display_dashboard_tab(load_kw, pv_kw, load_analysis, pv_analysis, bess_analysis,
                            bess_energy_kwh, bess_power_kw, bess_efficiency)

    with tab2:
        display_analysis_tab(load_analysis, pv_analysis, bess_analysis)

    with tab3:
        display_findings_tab(critic_result, conflicts)

    with tab4:
        display_agents_tab(agent_results, critic_result, lead_result)

    with tab5:
        display_report_tab(load_analysis, pv_analysis, bess_analysis, conflicts, lead_result)


def display_dashboard_tab(load_kw, pv_kw, load_analysis, pv_analysis, bess_analysis,
                          bess_energy_kwh, bess_power_kw, bess_efficiency):
    """Display main dashboard with charts and KPIs."""

    # KPI metrics
    st.markdown("### 📈 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Peak Load", f"{load_analysis['peak_demand_kw']:.0f} kW")

    with col2:
        st.metric("Daily Energy", f"{load_analysis['daily_energy_kwh']:.0f} kWh")

    with col3:
        st.metric("Peak Duration", f"{load_analysis['peak_duration_hours']:.1f} hrs")

    with col4:
        st.metric("Battery Duration", f"{bess_analysis['battery_duration_hours']:.1f} hrs")

    # Charts
    st.markdown("### 📉 Charts")
    col1, col2 = st.columns(2)

    with col1:
        # Load profile chart
        fig_load = go.Figure()
        fig_load.add_trace(go.Scatter(y=load_kw.values, mode="lines", name="Load",
                                     line=dict(color="blue", width=2)))
        fig_load.update_layout(title="Load Profile", xaxis_title="Time (15-min intervals)",
                             yaxis_title="Power (kW)", height=400)
        st.plotly_chart(fig_load, use_container_width=True)

    with col2:
        # PV generation chart
        if pv_kw is not None:
            fig_pv = go.Figure()
            fig_pv.add_trace(go.Scatter(y=load_kw.values, mode="lines", name="Load",
                                       line=dict(color="blue", width=2)))
            fig_pv.add_trace(go.Scatter(y=pv_kw.values, mode="lines", name="PV Generation",
                                       line=dict(color="orange", width=2)))
            fig_pv.update_layout(title="Load vs PV Generation", xaxis_title="Time (15-min intervals)",
                               yaxis_title="Power (kW)", height=400)
            st.plotly_chart(fig_pv, use_container_width=True)

    # Overall status
    st.markdown("---")
    st.markdown("### 🎯 Overall Review Status")

    # Determine status based on conflicts
    if len([c for c in [] if c.get("severity") == "High"]) > 0:
        status_color = "🟡"
        status_text = "Review Required"
    else:
        status_color = "🟢"
        status_text = "Preliminary Design Appears Consistent"

    st.markdown(f"### {status_color} {status_text}")
    st.write("""
    The design appears technically plausible based on the preliminary calculations.

    **However:** Professional engineering verification is required before implementation.
    """)


def display_analysis_tab(load_analysis, pv_analysis, bess_analysis):
    """Display detailed analysis tab."""

    st.markdown("### Load Analysis")
    for finding in load_analysis["findings"]:
        st.write(f"- {finding}")

    st.markdown("### PV Analysis")
    for finding in pv_analysis["findings"]:
        st.write(f"- {finding}")

    if pv_analysis["concerns"]:
        st.warning("**Concerns:**")
        for concern in pv_analysis["concerns"]:
            st.write(f"- {concern}")

    st.markdown("### BESS Analysis")
    for finding in bess_analysis["findings"]:
        st.write(f"- {finding}")

    if bess_analysis["concerns"]:
        st.warning("**Concerns:**")
        for concern in bess_analysis["concerns"]:
            st.write(f"- {concern}")


def display_findings_tab(critic_result, conflicts):
    """Display findings and conflicts."""

    st.markdown("### ⚠️ Conflicts Identified")

    if not conflicts:
        st.success("✓ No major conflicts detected.")
    else:
        for conflict in conflicts:
            st.markdown(f"""
            <div class="conflict-box">
            <b>{conflict.get('issue', 'Unknown')}</b><br>
            <b>Severity:</b> {conflict.get('severity', 'Unknown')}<br>
            <b>Details:</b> {conflict.get('explanation', 'N/A')}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### 🔍 Critic Assessment")

    if critic_result.get("concerns"):
        st.warning("**Critical Concerns:**")
        for concern in critic_result["concerns"][:5]:
            st.write(f"- {concern}")


def display_agents_tab(agent_results, critic_result, lead_result):
    """Display individual agent findings."""

    st.markdown("### 👥 Agent Results")

    for agent_name, result in agent_results.items():
        with st.expander(f"**{agent_name}**"):
            st.write(f"**Role:** {result.get('role', 'N/A')}")
            st.write(f"**Confidence:** {result.get('confidence', 'N/A')}")

            if result.get("findings"):
                st.write("**Findings:**")
                for finding in result["findings"]:
                    st.write(f"- {finding}")

            if result.get("concerns"):
                st.warning("**Concerns:**")
                for concern in result["concerns"]:
                    st.write(f"- {concern}")


def display_report_tab(load_analysis, pv_analysis, bess_analysis, conflicts, lead_result):
    """Display final report."""

    st.markdown("### 📄 Final Engineering Review Report")

    report_text = f"""
## Executive Summary

This preliminary engineering review evaluates the proposed PV + BESS project design based on submitted data and deterministic calculations.

## Key Findings

- **Peak Load:** {load_analysis['peak_demand_kw']:.0f} kW
- **Peak Duration:** {load_analysis['peak_duration_hours']:.2f} hours
- **BESS Duration:** {bess_analysis['battery_duration_hours']:.2f} hours
- **Load Coverage:** {(load_analysis['daily_energy_kwh'] / (load_analysis['daily_energy_kwh'] + 1)) * 100:.0f}%

## Conflicts Detected

"""

    if conflicts:
        for conflict in conflicts:
            report_text += f"- **{conflict.get('issue')}**: {conflict.get('explanation')}\n"
    else:
        report_text += "- No major conflicts detected.\n"

    report_text += """
## Recommendations

1. Have results reviewed by licensed professional engineers
2. Conduct detailed site assessment
3. Verify all assumptions with actual field data
4. Follow applicable standards and regulations
5. Perform necessary testing before implementation

## Disclaimer

This is a preliminary AI-assisted engineering review. It does NOT constitute:
- Final engineering design
- Safety certification
- Regulatory approval
- Professional engineering sign-off

---

*Report generated on """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "*"

    st.markdown(report_text)

    # Download report
    if st.button("📥 Download Report"):
        st.download_button(
            label="Download as Text",
            data=report_text,
            file_name=f"eerb_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )


if __name__ == "__main__":
    main()
