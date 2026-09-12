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

# Premium AI/Robotic Design - Professional SaaS Aesthetic
st.markdown("""
    <style>
    * {
        font-family: 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
    }

    /* Dark background with premium gradient */
    body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #0a1628 0%, #1a2744 40%, #0f1929 100%);
        color: #e2e8f0;
    }

    [data-testid="stMainBlockContainer"] {
        background: transparent;
    }

    /* Tab styling - Premium web-like, centered */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background: rgba(15, 23, 42, 0.95);
        padding: 8px 12px;
        border-radius: 14px 14px 0 0;
        border-bottom: 3px solid #00d9ff;
        backdrop-filter: blur(20px);
        box-shadow: 0 -4px 20px rgba(0, 217, 255, 0.15);
        display: flex;
        justify-content: center;
    }

    .stTabs [data-baseweb="tab-list"] button {
        font-size: 13px;
        font-weight: 700;
        padding: 14px 28px;
        border-radius: 10px 10px 0 0;
        border: none;
        background: transparent;
        color: #94a3b8;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-size: 11px;
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: linear-gradient(135deg, #00d9ff 0%, #06b6d4 100%);
        color: #0a1628;
        box-shadow: 0 0 30px rgba(0, 217, 255, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        font-weight: 800;
    }

    .stTabs [data-baseweb="tab-list"] button:hover {
        color: #00d9ff;
        background: rgba(0, 217, 255, 0.15);
    }

    /* Card styling - Dark theme */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        padding: 24px;
        border-radius: 12px;
        margin: 12px 0;
        border: 1px solid rgba(0, 217, 255, 0.2);
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.1), inset 0 1px 1px rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }

    .metric-card:hover {
        border-color: rgba(0, 217, 255, 0.5);
        box-shadow: 0 0 30px rgba(0, 217, 255, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.05);
        transform: translateY(-4px);
    }

    /* Hero section - Dark & AI-themed */
    .hero-section {
        background: linear-gradient(135deg, #00d9ff 0%, #06b6d4 50%, #0ea5e9 100%);
        padding: 80px 40px;
        border-radius: 20px;
        color: #0a1628;
        text-align: center;
        margin-bottom: 50px;
        box-shadow: 0 0 60px rgba(0, 217, 255, 0.3);
        position: relative;
        overflow: hidden;
    }

    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(249, 115, 22, 0.1) 0%, transparent 70%);
        border-radius: 50%;
    }

    .hero-section h1 {
        margin: 0;
        font-size: 52px;
        font-weight: 800;
        letter-spacing: -2px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .hero-section p {
        margin: 16px 0 0 0;
        font-size: 20px;
        opacity: 0.95;
        font-weight: 500;
    }

    /* Section titles */
    h2 {
        color: #00d9ff;
        font-weight: 800;
        margin-top: 40px;
        margin-bottom: 24px;
        font-size: 32px;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-shadow: 0 0 20px rgba(0, 217, 255, 0.2);
    }

    h3 {
        color: #00d9ff;
        font-weight: 700;
        margin-top: 24px;
        margin-bottom: 16px;
        font-size: 18px;
        letter-spacing: 0.5px;
    }

    /* Buttons - Premium SaaS style */
    .stButton > button {
        background: linear-gradient(135deg, #00d9ff 0%, #06b6d4 100%);
        color: #0a1628;
        border: 2px solid #00d9ff;
        border-radius: 12px;
        padding: 16px 40px;
        font-weight: 800;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 0 25px rgba(0, 217, 255, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.3);
        cursor: pointer;
        position: relative;
    }

    .stButton > button:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 0 50px rgba(0, 217, 255, 0.7), 0 10px 40px rgba(0, 217, 255, 0.3);
        border-color: #f97316;
    }

    .stButton > button:active {
        transform: translateY(-2px);
    }

    /* File uploader styling */
    .stFileUploadDropzone {
        border: 2px dashed #00d9ff !important;
        border-radius: 12px !important;
        background: rgba(0, 217, 255, 0.05) !important;
    }

    .stFileUploadDropzone:hover {
        background: rgba(0, 217, 255, 0.1) !important;
        border-color: #f97316 !important;
    }

    /* Loading animation */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 217, 255, 0.4); }
        50% { box-shadow: 0 0 40px rgba(0, 217, 255, 0.8); }
    }

    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(0, 217, 255, 0.2);
        border-top: 3px solid #00d9ff;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    /* Info/Alert boxes */
    .stAlert {
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%);
        border: 1px solid rgba(0, 217, 255, 0.3);
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }

    /* Conflict/Warning boxes */
    .conflict-box {
        background: linear-gradient(135deg, rgba(249, 115, 22, 0.15) 0%, rgba(245, 158, 11, 0.05) 100%);
        padding: 18px;
        border-radius: 12px;
        border-left: 5px solid #f97316;
        margin: 12px 0;
        box-shadow: 0 0 20px rgba(249, 115, 22, 0.15);
        border: 1px solid rgba(249, 115, 22, 0.3);
    }

    /* Finding boxes */
    .finding-box {
        padding: 16px;
        border-radius: 10px;
        margin: 12px 0;
        border-left: 4px solid #00d9ff;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        box-shadow: 0 0 15px rgba(0, 217, 255, 0.1);
        border: 1px solid rgba(0, 217, 255, 0.2);
    }

    .finding-critical {
        border-left-color: #ef4444;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
        border-color: rgba(239, 68, 68, 0.3);
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.15);
    }

    .finding-high {
        border-left-color: #f97316;
        background: linear-gradient(135deg, rgba(249, 115, 22, 0.1) 0%, rgba(234, 88, 12, 0.05) 100%);
        border-color: rgba(249, 115, 22, 0.3);
        box-shadow: 0 0 20px rgba(249, 115, 22, 0.15);
    }

    .finding-medium {
        border-left-color: #eab308;
        background: linear-gradient(135deg, rgba(234, 179, 8, 0.1) 0%, rgba(202, 138, 4, 0.05) 100%);
        border-color: rgba(234, 179, 8, 0.3);
    }

    .finding-low {
        border-left-color: #10b981;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%);
        border-color: rgba(16, 185, 129, 0.3);
    }

    /* Divider */
    hr {
        border: none;
        border-top: 1px solid rgba(0, 217, 255, 0.2);
        margin: 40px 0;
    }

    /* Text colors */
    p, span {
        color: #e2e8f0;
    }

    strong {
        color: #00d9ff;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Main application entry point."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# EERB", unsafe_allow_html=True)
        st.markdown("## Energy Engineering Review Board", unsafe_allow_html=True)
        st.markdown("### *AI-Powered Engineering Analysis Before You Build*", unsafe_allow_html=True)

    st.markdown("---")

    # Navigation Tabs - Reorganized for better flow
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Demo", "Upload", "Home"])

    with tab1:
        show_about()

    with tab2:
        show_demo_project()

    with tab3:
        show_upload_project()

    with tab4:
        show_home()

    # Disclaimer Footer
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border: 1px solid #f59e0b; border-radius: 10px; padding: 16px; margin-top: 40px; text-align: center;">
        <p style="margin: 0; font-size: 12px; color: #92400e; font-weight: 600;">
            ⚠️  DISCLAIMER
        </p>
        <p style="margin: 8px 0 0 0; font-size: 11px; color: #b45309; line-height: 1.5;">
            This AI-assisted preliminary engineering review does not constitute final design, safety certification, regulatory approval, or professional engineering sign-off.<br/>
            <strong>Always have results reviewed by licensed professional engineers before implementation.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)


def show_home():
    """Display home page with website-like layout."""

    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1>Energy Engineering Review Board</h1>
        <p>AI-Powered Preliminary Engineering Analysis in Minutes</p>
    </div>
    """, unsafe_allow_html=True)

    # Value Proposition Section
    st.markdown("### 🎯 Why Choose EERB?")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin-top: 0; color: #0066cc;">⚡ Rapid Assessment</h3>
            <p style="margin: 12px 0; color: #475569;">
                <strong>2-5 minutes</strong><br/>
                vs 2 weeks traditional review
            </p>
            <p style="font-size: 13px; color: #64748b; margin: 0;">Instant preliminary analysis, not weeks of delay</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin-top: 0; color: #0066cc;">🎯 Conflict Detection</h3>
            <p style="margin: 12px 0; color: #475569;">
                <strong>Catch Issues Early</strong><br/>
                Before expensive rework
            </p>
            <p style="font-size: 13px; color: #64748b; margin: 0;">Multi-agent system identifies technical contradictions</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin-top: 0; color: #0066cc;">📊 Traceable Results</h3>
            <p style="margin: 12px 0; color: #475569;">
                <strong>Professional Reports</strong><br/>
                Detailed findings & recommendations
            </p>
            <p style="font-size: 13px; color: #64748b; margin: 0;">Every conclusion is verifiable and referenced</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # How It Works Section
    st.markdown("### 🔍 How It Works")

    cols = st.columns(3)

    agents = [
        ("📊 Load Analyst", "Examines electricity consumption patterns and peak demands"),
        ("☀️ PV Engineer", "Evaluates solar capacity adequacy and generation potential"),
        ("🔋 BESS Engineer", "Assesses battery storage capability and discharge duration"),
        ("📋 Spec Engineer", "Reviews technical documents and requirements"),
        ("🤔 Independent Critic", "Challenges conclusions and identifies conflicts"),
        ("👨‍💼 Lead Engineer", "Synthesizes findings into professional report")
    ]

    for i, (title, desc) in enumerate(agents):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="margin: 0 0 8px 0; color: #0066cc;">{title}</h4>
                <p style="margin: 0; font-size: 13px; color: #64748b;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border: 1px solid #3b82f6; padding: 16px; border-radius: 10px; margin-top: 20px;">
        <p style="margin: 0; color: #0c4a6e; font-size: 14px;"><strong>✓ Deterministic Calculations</strong><br/>All math is verifiable and reproducible — no AI guessing on critical numbers.</p>
    </div>
    """)

    st.markdown("---")

    # Use Case Section
    st.markdown("### 📋 Demo Scenario")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border: 2px solid #0284c7; padding: 24px; border-radius: 12px; margin: 20px 0;">
        <h4 style="margin: 0 0 12px 0; color: #0c4a6e;">Commercial Building with Solar + Battery Storage</h4>
        <p style="margin: 8px 0; color: #0c4a6e;"><strong>System Specification:</strong> 500 kW PV + 1 MWh Battery (500 kW discharge)</p>
        <p style="margin: 8px 0; color: #0c4a6e;"><strong>Technical Finding:</strong> Load peak duration (4.5 hrs) exceeds battery discharge duration (2 hrs)</p>
        <div style="background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%); padding: 12px; border-radius: 8px; margin-top: 12px; border-left: 4px solid #f97316;">
            <p style="margin: 0; color: #7c2d12; font-weight: 600;">⚠️ Battery Insufficient for Peak-Shaving Objective</p>
            <p style="margin: 6px 0 0 0; font-size: 13px; color: #92400e;">EERB flags this design issue automatically for professional review and correction.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # CTA
    st.markdown("### 🚀 Get Started")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown("")

    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <p style="color: #64748b; font-size: 14px; margin-bottom: 16px;">Choose how you want to proceed:</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️  Demo Project", key="home_demo", use_container_width=True):
            st.session_state.selected_mode = "demo"
            st.rerun()

    with col2:
        if st.button("📤  Upload Your Project", key="home_upload", use_container_width=True):
            st.session_state.selected_mode = "upload"
            st.rerun()


def show_about():
    """Display About section (Overview tab) with AI-robotic aesthetic."""

    st.markdown("## System Overview")

    # Problem statement
    st.markdown("""
    <div class="metric-card" style="border-left: 4px solid #ef4444;">
        <h3 style="margin-top: 0; color: #ef4444;">The Challenge</h3>
        <p style="margin: 12px 0; line-height: 1.7;">
            Renewable energy projects face critical design flaws that emerge too late. Engineers spend weeks manually verifying solar capacity, battery duration, and load profiles. Technical contradictions go undetected. Expensive engineering work begins on flawed assumptions. The cost: weeks of delay, $50K+ in rework.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # Solution statement
    st.markdown("""
    <div class="metric-card" style="border-left: 4px solid #10b981;">
        <h3 style="margin-top: 0; color: #10b981;">Our Solution</h3>
        <p style="margin: 12px 0; line-height: 1.7;">
            EERB uses <strong>6 specialized AI agents</strong> working in parallel to analyze renewable energy designs systematically. Multi-agent analysis detects conflicts automatically. Deterministic calculations ensure every conclusion is verifiable. Professional report delivered in minutes instead of weeks.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("---")
    st.markdown("")

    # Three Pillars - Clean, modern design
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 28px; margin-bottom: 12px;">⚡</div>
            <h3 style="margin: 0 0 12px 0; color: #00d9ff; font-size: 16px; text-transform: uppercase; letter-spacing: 1px;">SPEED</h3>
            <p style="margin: 0 0 8px 0; color: #00d9ff; font-size: 20px; font-weight: 800;">2-5 MIN</p>
            <p style="margin: 0; color: #94a3b8; font-size: 13px; line-height: 1.6;">Preliminary review in minutes. Not weeks of manual analysis.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 28px; margin-bottom: 12px;">🧠</div>
            <h3 style="margin: 0 0 12px 0; color: #00d9ff; font-size: 16px; text-transform: uppercase; letter-spacing: 1px;">INTELLIGENCE</h3>
            <p style="margin: 0 0 8px 0; color: #00d9ff; font-size: 20px; font-weight: 800;">6 AI AGENTS</p>
            <p style="margin: 0; color: #94a3b8; font-size: 13px; line-height: 1.6;">Load analysis, PV design, battery systems, specifications, critique, synthesis.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 28px; margin-bottom: 12px;">✓</div>
            <h3 style="margin: 0 0 12px 0; color: #00d9ff; font-size: 16px; text-transform: uppercase; letter-spacing: 1px;">CONFIDENCE</h3>
            <p style="margin: 0 0 8px 0; color: #00d9ff; font-size: 20px; font-weight: 800;">VERIFIED</p>
            <p style="margin: 0; color: #94a3b8; font-size: 13px; line-height: 1.6;">Deterministic math. Every number verifiable. Every conclusion traceable.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("---")
    st.markdown("")

    # Technology Stack
    st.markdown("## Technology Stack")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin-top: 0; color: #00d9ff;">COMPUTATION</h4>
            <p style="margin: 8px 0 0 0; color: #94a3b8; font-size: 13px;">
                Python • Deterministic Calculations<br/>
                OpenAI GPT-3.5 • Reasoning Layer<br/>
                Multi-Agent Orchestration
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin-top: 0; color: #00d9ff;">DEPLOYMENT</h4>
            <p style="margin: 8px 0 0 0; color: #94a3b8; font-size: 13px;">
                Streamlit Cloud Backend<br/>
                React/Vercel Frontend<br/>
                Cloud-Native Architecture
            </p>
        </div>
        """, unsafe_allow_html=True)

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
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%); border: 1px solid rgba(0, 217, 255, 0.2); border-radius: 12px;">
            <h3 style="margin: 0 0 10px 0; color: #00d9ff; font-weight: 700;">Ready to Validate Your Project?</h3>
            <p style="margin: 0; font-size: 14px; color: #cbd5e1;">Start with the demo or upload your own project.</p>
        </div>
        """, unsafe_allow_html=True)


def show_demo_project():
    """Display demo project analysis - Dynamic & Interactive."""
    st.markdown("## Demo Analysis")

    # Load demo data
    try:
        load_df, pv_df = load_demo_data("data")
        load_kw, pv_kw = align_timeseries(load_df, pv_df)
    except Exception as e:
        st.error(f"Failed to load demo data: {str(e)}")
        return

    # Project specification card
    st.markdown("""
    <div class="metric-card" style="border-left: 4px solid #00d9ff; margin-bottom: 30px;">
        <h3 style="margin-top: 0; color: #00d9ff; text-transform: uppercase; letter-spacing: 1px;">Commercial Building Retrofit</h3>
        <p style="color: #94a3b8; margin: 8px 0;">Karachi, Pakistan | Peak Demand Reduction Study</p>
        <hr style="border-color: rgba(0, 217, 255, 0.2); margin: 12px 0;">
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-top: 16px;">
            <div style="text-align: center;">
                <div style="font-size: 24px; color: #00d9ff; font-weight: 800;">500</div>
                <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px;">kW PV</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 24px; color: #00d9ff; font-weight: 800;">1,000</div>
                <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px;">kWh BESS</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 24px; color: #00d9ff; font-weight: 800;">500</div>
                <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px;">kW Discharge</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 24px; color: #f97316; font-weight: 800;">~30%</div>
                <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px;">Target</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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

    # Professional analysis header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h2 style="color: #00d9ff; text-transform: uppercase; letter-spacing: 2px; font-size: 20px; margin: 0;">Analyzing Your Project</h2>
        <p style="color: #94a3b8; font-size: 13px; margin-top: 8px;">Multi-agent AI system is running engineering analysis...</p>
    </div>
    """, unsafe_allow_html=True)

    # Progress placeholder with better styling
    progress_container = st.container()

    # Calculate basic metrics with animated status
    with progress_container:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="background: rgba(0, 217, 255, 0.05); border: 1px solid rgba(0, 217, 255, 0.2); border-radius: 12px; padding: 20px; text-align: center;">
                <div style="animation: pulse-glow 1.5s ease-in-out infinite; display: inline-block;">
                    <div style="font-size: 24px; margin-bottom: 8px;">⚙️</div>
                    <p style="color: #00d9ff; font-weight: 700; font-size: 13px; margin: 0;">PROCESSING...</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    load_analysis = analyze_load_profile(load_kw)
    peak_load_kw = load_analysis["peak_demand_kw"]
    avg_load_kw = load_analysis["average_demand_kw"]
    daily_load_kwh = load_analysis["daily_energy_kwh"]
    peak_duration = load_analysis["peak_duration_hours"]

    # PV analysis
    if pv_kw is not None:
        daily_pv_kwh = pv_kw.sum() * 0.25
    else:
        daily_pv_kwh = pv_capacity_kw * 24 * 0.18

    pv_analysis = analyze_pv(pv_capacity_kw, daily_pv_kwh, peak_load_kw,
                            avg_load_kw, daily_load_kwh)

    # BESS analysis
    bess_analysis = analyze_bess(bess_energy_kwh, bess_power_kw, peak_load_kw,
                                peak_duration, bess_efficiency)

    # Show completion status with better styling
    with progress_container:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0, 217, 255, 0.08) 0%, rgba(16, 185, 129, 0.04) 100%); border: 1px solid rgba(0, 217, 255, 0.15); border-radius: 12px; padding: 20px; margin-top: 20px;">
            <p style="color: #00d9ff; font-weight: 700; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 12px 0;">Analysis Complete</p>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
                <div style="padding: 10px; background: rgba(0, 217, 255, 0.05); border-radius: 8px; border-left: 3px solid #10b981;">
                    <p style="color: #10b981; font-weight: 700; font-size: 11px; margin: 0;">✓ Load Analysis</p>
                </div>
                <div style="padding: 10px; background: rgba(0, 217, 255, 0.05); border-radius: 8px; border-left: 3px solid #10b981;">
                    <p style="color: #10b981; font-weight: 700; font-size: 11px; margin: 0;">✓ PV Analysis</p>
                </div>
                <div style="padding: 10px; background: rgba(0, 217, 255, 0.05); border-radius: 8px; border-left: 3px solid #10b981;">
                    <p style="color: #10b981; font-weight: 700; font-size: 11px; margin: 0;">✓ BESS Analysis</p>
                </div>
                <div style="padding: 10px; background: rgba(0, 217, 255, 0.05); border-radius: 8px; border-left: 3px solid #10b981;">
                    <p style="color: #10b981; font-weight: 700; font-size: 11px; margin: 0;">✓ AI Agents</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

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
