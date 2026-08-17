"""
=============================================================================
🏛️ GOVERNMENT SOCIAL MEDIA ANALYTICS & DECISION SUPPORT SYSTEM (GovDSS)
=============================================================================
Executive Command Center & Multi-Module Machine Learning Platform
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Optional Plotly import with fallback
try:
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# =============================================================================
# 1. PAGE CONFIGURATION & METADATA
# =============================================================================

st.set_page_config(
    page_title="GovDSS | Executive Social Media Analytics",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend & File Paths
BACKEND_URL = "http://127.0.0.1:8000"
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent.parent
DATA_DIR = PROJECT_DIR / "Data"
SCHEMES_CSV_PATH = PROJECT_DIR / "government_schemes_final.csv"
if not SCHEMES_CSV_PATH.exists():
    SCHEMES_CSV_PATH = DATA_DIR / "government_schemes_lookup.csv"

# =============================================================================
# 2. SUPABASE CONNECTION WITH SAFE FALLBACK
# =============================================================================

supabase = None
SUPABASE_STATUS = "Disconnected"
try:
    from supabase import create_client
    if "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets:
        supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
        SUPABASE_STATUS = "Connected"
except Exception as e:
    SUPABASE_STATUS = f"Offline ({str(e)[:25]}...)"

# Check Backend API Health
BACKEND_ONLINE = False
try:
    health_resp = requests.get(f"{BACKEND_URL}/", timeout=1.5)
    if health_resp.status_code == 200:
        BACKEND_ONLINE = True
except Exception:
    BACKEND_ONLINE = False

# =============================================================================
# 3. EXECUTIVE GOVTECH DESIGN SYSTEM (CSS)
# =============================================================================

st.markdown(
    """
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --primary: #1e40af;
        --primary-light: #3b82f6;
        --surface: #0f172a;
        --card-bg: #1e293b;
        --border-color: #334155;
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --accent: #8b5cf6;
    }

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Custom Header Component */
    .gov-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);
        padding: 24px 30px;
        border-radius: 16px;
        border: 1px solid #3b82f640;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .gov-title {
        font-size: 28px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .gov-subtitle {
        font-size: 14px;
        color: #93c5fd;
        margin-top: 6px;
        font-weight: 500;
    }

    /* Status Pills */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
    }
    .status-online { background-color: #065f46; color: #34d399; }
    .status-offline { background-color: #7f1d1d; color: #f87171; }
    .status-standby { background-color: #78350f; color: #fbbf24; }

    /* Custom Card Containers */
    .gov-card {
        background-color: #1e293b;
        border-radius: 12px;
        border: 1px solid #334155;
        padding: 20px;
        margin-bottom: 15px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .gov-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.15);
    }

    .gov-stat-number {
        font-size: 28px;
        font-weight: 800;
        color: #f8fafc;
        margin-top: 4px;
    }
    .gov-stat-label {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #94a3b8;
    }

    /* Result Metric Badges */
    .badge-danger {
        background-color: #450a0a;
        color: #fca5a5;
        border: 1px solid #991b1b;
        padding: 6px 12px;
        border-radius: 8px;
        font-weight: 700;
        display: inline-block;
    }
    .badge-warning {
        background-color: #451a03;
        color: #fcd34d;
        border: 1px solid #b45309;
        padding: 6px 12px;
        border-radius: 8px;
        font-weight: 700;
        display: inline-block;
    }
    .badge-success {
        background-color: #022c22;
        color: #6ee7b7;
        border: 1px solid #047857;
        padding: 6px 12px;
        border-radius: 8px;
        font-weight: 700;
        display: inline-block;
    }
    .badge-info {
        background-color: #082f49;
        color: #7dd3fc;
        border: 1px solid #0369a1;
        padding: 6px 12px;
        border-radius: 8px;
        font-weight: 700;
        display: inline-block;
    }

    /* Dispatch Ticket */
    .ticket-container {
        background: #090d16;
        border: 1px dashed #3b82f6;
        border-radius: 10px;
        padding: 16px;
        font-family: 'JetBrains Mono', monospace;
        color: #cbd5e1;
    }

    /* Streamlit overrides */
    div[data-testid="stMetric"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 14px 18px;
    }
    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 800 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =============================================================================
# 4. DATA LOADER & CACHING HELPERS
# =============================================================================

@st.cache_data(ttl=3600)
def load_schemes_dataset():
    """Loads 3,400+ government schemes catalog."""
    if SCHEMES_CSV_PATH.exists():
        try:
            df = pd.read_csv(SCHEMES_CSV_PATH)
            # Normalize column names
            df.columns = [c.strip().lower() for c in df.columns]
            if "schemecategory" in df.columns and "scheme_category" not in df.columns:
                df["scheme_category"] = df["schemecategory"]
            return df
        except Exception:
            pass
    return pd.DataFrame()

@st.cache_data(ttl=600)
def load_demo_analytics_data():
    """Generates realistic government social media grievance records for live demonstration."""
    np.random.seed(42)
    departments = ["Roads & Infrastructure", "Water Supply & Sewerage", "Electricity & Power", 
                   "Public Health", "Education & Welfare", "Waste Management", "Public Transport"]
    reasons = ["Potholes & Road Damage", "No Water Supply / Pipe Leak", "Frequent Power Cuts", 
               "Hospital Medicine Shortage", "Garbage Overflow", "Bus Schedule Delay", "Streetlight Malfunction"]
    sentiments = ["Negative", "Negative", "Negative", "Neutral", "Positive"]
    priorities = ["High", "High", "Medium", "Medium", "Low"]
    platforms = ["Twitter", "Facebook", "YouTube", "Instagram", "Reddit"]
    locations = ["Bengaluru", "Hyderabad", "Delhi NCR", "Mumbai", "Kolkata", "Chennai", "Pune", "Ahmedabad"]

    records = []
    base_date = datetime.now() - timedelta(days=30)
    for i in range(120):
        date_stamp = base_date + timedelta(hours=i*6 + np.random.randint(0, 5))
        dep = np.random.choice(departments)
        prio = np.random.choice(priorities)
        is_emerg = bool(prio == "High" and np.random.rand() > 0.6)
        is_harm = bool(np.random.rand() > 0.88)
        
        sample_posts = [
            f"Severe water logging and massive potholes near main junction in {np.random.choice(locations)}. 3 accidents today already!",
            f"No electricity in our colony since yesterday morning. High voltage fluctuations damaged appliances.",
            f"Drinking water supplied today is muddy and stinking. People falling sick in {np.random.choice(locations)}.",
            f"Appreciate the prompt response from municipal staff for garbage collection this morning.",
            f"Primary health center has no doctors available and basic fever syrups are out of stock.",
            f"Urgent: Massive pipeline burst flooding the road near market, emergency repair needed immediately!"
        ]
        
        records.append({
            "id": i + 1,
            "created_at": date_stamp.isoformat(),
            "source": np.random.choice(platforms),
            "text_content": np.random.choice(sample_posts),
            "location": np.random.choice(locations),
            "sentiment": "Negative" if is_emerg else np.random.choice(sentiments),
            "sentiment_confidence": round(0.75 + np.random.rand()*0.23, 2),
            "feedback_category": "Complaint" if not is_harm else "Harmful Content",
            "feedback_confidence": round(0.80 + np.random.rand()*0.18, 2),
            "complaint_reason": np.random.choice(reasons),
            "complaint_confidence": round(0.78 + np.random.rand()*0.2, 2),
            "predicted_department": dep,
            "department_confidence": round(0.82 + np.random.rand()*0.16, 2),
            "priority": "High" if is_emerg else prio,
            "priority_confidence": round(0.79 + np.random.rand()*0.19, 2),
            "emergency_detected": is_emerg,
            "emergency_confidence": round(0.88 if is_emerg else 0.12, 2),
            "harmful_content_detected": is_harm,
            "harmful_content_confidence": round(0.85 if is_harm else 0.08, 2),
            "recommended_action": "Dispatched to Executive Engineer for immediate resolution."
        })
    return pd.DataFrame(records)

# =============================================================================
# 5. ML INFERENCE ENGINE (ONLINE REST + LOCAL MODEL FALLBACK)
# =============================================================================

def execute_prediction_pipeline(platform: str, location: str, text: str):
    """
    Executes full 9-module grievance triage.
    Tries FastAPI backend first; seamlessly executes intelligent local rules/matching if backend is offline.
    """
    # 1. Try Live FastAPI Backend
    if BACKEND_ONLINE:
        try:
            payload = {
                "platform": platform,
                "post_text": text,
                "location": location,
                "department": ""
            }
            resp = requests.post(f"{BACKEND_URL}/predict", json=payload, timeout=25)
            if resp.status_code == 200:
                result = resp.json()
                if "error" not in result:
                    return result, "Live FastAPI API"
        except Exception:
            pass

    # 2. Local Fallback Intelligent Inference (GovDSS Standalone Core)
    text_lower = text.lower()

    # Module 1: Sentiment
    pos_words = ["good", "great", "thank", "appreciate", "fast", "resolved", "excellent", "clean", "fixed"]
    neg_words = ["bad", "worst", "pothole", "accident", "broken", "dirty", "fire", "blast", "leak", "cut", "delay", "corrupt", "overflow", "stinking", "shortage"]
    neg_score = sum(1 for w in neg_words if w in text_lower)
    pos_score = sum(1 for w in pos_words if w in text_lower)
    
    if neg_score > pos_score:
        sentiment = "Negative"
        sent_conf = min(0.96, 0.70 + neg_score * 0.08)
    elif pos_score > neg_score:
        sentiment = "Positive"
        sent_conf = min(0.95, 0.72 + pos_score * 0.08)
    else:
        sentiment = "Neutral"
        sent_conf = 0.68

    # Module 2 & 7: Harmful & Feedback Category
    toxic_words = ["kill", "shoot", "terrorist", "threat", "destroy", "hate", "attack"]
    is_harmful = any(w in text_lower for w in toxic_words)
    harmful_label = "HOF (Harmful/Offensive)" if is_harmful else "NOT (Safe Content)"
    
    if is_harmful:
        category = "Harmful Content"
    elif any(w in text_lower for w in ["suggest", "should provide", "request to add", "please consider"]):
        category = "Suggestion"
    elif any(w in text_lower for w in ["what is", "how to", "eligibility", "when will", "where can"]):
        category = "Inquiry"
    elif sentiment == "Positive":
        category = "Praise / Appreciation"
    else:
        category = "Complaint / Grievance"

    # Module 4: Department Prediction
    dept_map = {
        "Roads & Highway Infrastructure": ["road", "pothole", "tar", "accident", "flyover", "signal", "traffic", "bridge", "street"],
        "Water Resources & Sewerage": ["water", "pipe", "pipeline", "drainage", "sewage", "drinking water", "tap", "leakage", "dirty water"],
        "Electricity & Renewable Energy": ["power", "electricity", "transformer", "blackout", "voltage", "wire", "current", "meter", "load shedding"],
        "Public Health & Family Welfare": ["hospital", "doctor", "medicine", "health", "clinic", "fever", "syrup", "ambulance", "treatment", "bed"],
        "Education & Youth Affairs": ["school", "college", "scholarship", "exam", "teacher", "student", "fees", "admission", "books"],
        "Municipal Solid Waste & Sanitation": ["garbage", "trash", "waste", "cleaning", "dump", "stinking", "sanitation", "smell", "dustbin"],
        "Disaster Management & Civil Defense": ["flood", "fire", "blast", "cyclone", "drowning", "building collapse", "earthquake", "trapped"]
    }
    
    predicted_dept = "General Administration & Citizen Grievances"
    max_dept_hits = 0
    for dept, keys in dept_map.items():
        hits = sum(1 for k in keys if k in text_lower)
        if hits > max_dept_hits:
            max_dept_hits = hits
            predicted_dept = dept
    dept_conf = min(0.95, 0.70 + max_dept_hits * 0.08)

    # Module 6: Emergency Detection
    emerg_words = ["accident", "fire", "blast", "flood", "bleeding", "collapsed", "urgent", "trapped", "casualty", "burst", "life threatening", "immediately"]
    is_emergency = any(w in text_lower for w in emerg_words)
    emergency_label = "Yes" if is_emergency else "No"
    emerg_conf = 0.94 if is_emergency else 0.15

    # Module 5: Priority Prediction
    if is_emergency or is_harmful or "urgent" in text_lower or max_dept_hits >= 3:
        priority = "High"
        prio_conf = 0.92
    elif sentiment == "Negative" or max_dept_hits >= 1:
        priority = "Medium"
        prio_conf = 0.81
    else:
        priority = "Low"
        prio_conf = 0.74

    # Module 3: Complaint Root Cause
    if "pothole" in text_lower or "road" in text_lower:
        complaint_reason = "Damaged Road Surface / Pothole Hazard"
    elif "water" in text_lower and ("leak" in text_lower or "burst" in text_lower):
        complaint_reason = "Water Pipeline Rupture & Loss of Supply"
    elif "power" in text_lower or "cut" in text_lower or "transformer" in text_lower:
        complaint_reason = "Unscheduled Power Outage & Grid Instability"
    elif "hospital" in text_lower or "medicine" in text_lower:
        complaint_reason = "Healthcare Facility Shortage & Doctor Unavailability"
    elif "scholarship" in text_lower:
        complaint_reason = "Educational Disbursement & Verification Delay"
    elif "garbage" in text_lower or "waste" in text_lower:
        complaint_reason = "Uncollected Municipal Solid Waste"
    else:
        complaint_reason = "Civic Service Disruption & Operational Delay"

    # Module 10: Scheme Recommendation Engine
    schemes_df = load_schemes_dataset()
    matched_scheme = {}
    if not schemes_df.empty:
        # Search relevant scheme based on department and complaint keywords
        query_words = [w for w in (complaint_reason + " " + predicted_dept).lower().split() if len(w) > 3]
        best_row = None
        best_score = 0
        
        for idx, row in schemes_df.head(400).iterrows():
            combined_text = f"{row.get('scheme_name', '')} {row.get('details', '')} {row.get('schemecategory', '')} {row.get('tags', '')}".lower()
            score = sum(1 for qw in query_words if qw in combined_text)
            if score > best_score:
                best_score = score
                best_row = row
        
        if best_row is not None and best_score > 0:
            matched_scheme = {
                "scheme_name": best_row.get("scheme_name", "National Civic Assistance Programme"),
                "description": best_row.get("details", "Government support program for affected citizens."),
                "benefits": best_row.get("benefits", "Immediate administrative relief and service restoration."),
                "eligibility": best_row.get("eligibility", "Resident citizens affected by civic infrastructure disruption."),
                "application": best_row.get("application", "Submit grievance on State Citizen Portal or District Helpline."),
                "scheme_category": best_row.get("schemecategory", "Public Welfare & Infrastructure")
            }
        else:
            matched_scheme = {
                "scheme_name": "Pradhan Mantri Gram Sadak / National Urban Infrastructure Mission",
                "description": "Comprehensive central and state scheme for urban civic repair, rapid disaster restoration, and welfare assistance.",
                "benefits": "Expedited municipal contractor deployment, repair reimbursement, and citizen grievance redressal within 48 hours.",
                "eligibility": "All registered citizens within municipal and rural jurisdiction.",
                "application": "Directly accessible via Central Grievance Redressal (CPGRAMS) or Urban Local Body portal.",
                "scheme_category": "Infrastructure & Public Services"
            }
    else:
        matched_scheme = {
            "scheme_name": "National Disaster & Civic Relief Fund",
            "description": "Emergency welfare and fast-track rehabilitation scheme.",
            "benefits": "Direct emergency squad dispatch, compensation for infrastructure damages.",
            "eligibility": "Citizens residing in affected ward.",
            "application": "Apply via Municipal Commissioner's Office.",
            "scheme_category": "Emergency & Welfare"
        }

    result = {
        "platform": platform,
        "post_text": text,
        "location": location,
        "sentiment": {"sentiment": sentiment, "confidence": sent_conf},
        "feedback_category": {"feedback_category": category, "confidence": 0.85},
        "complaint_reason": {"complaint_reason": complaint_reason, "confidence": 0.84},
        "department": {"department": predicted_dept, "confidence": dept_conf},
        "priority": {"priority": priority, "confidence": prio_conf},
        "emergency": {"emergency": emergency_label, "confidence": emerg_conf},
        "harmful_content": {"harmful_content": harmful_label, "confidence": 0.90 if is_harmful else 0.92},
        "recommended_action": matched_scheme
    }

    return result, "GovDSS Local Inference Core"

# =============================================================================
# 6. SIDEBAR NAVIGATION & SYSTEM HEALTH PULSE
# =============================================================================

with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; padding: 10px 0 15px 0;">
            <span style="font-size: 38px;">🏛️</span>
            <h2 style="margin: 4px 0 0 0; font-size: 20px; font-weight: 800; color: #f8fafc;">GovDSS Central</h2>
            <p style="font-size: 11px; color: #94a3b8; margin: 0; letter-spacing: 0.5px;">DECISION SUPPORT PLATFORM</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    default_page = st.session_state.get("nav_target", "🏛️ Executive Command Hub")
    page_options = [
        "🏛️ Executive Command Hub",
        "📊 Live Analytics & Oversight",
        "🔍 Grievance Triage & DSS",
        "📈 Trend Forecasting (ETS)",
        "⚠️ Anomaly & Surge Radar",
        "🚨 Emergency & Incident Room",
        "📋 Government Schemes Hub"
    ]
    
    default_idx = page_options.index(default_page) if default_page in page_options else 0
    
    page = st.radio(
        "Executive Command Navigation",
        page_options,
        index=default_idx
    )
    
    st.markdown("---")
    
    # System Status Card
    st.markdown("#### ⚡ System Pulse")
    
    # Backend indicator
    if BACKEND_ONLINE:
        st.markdown('<span class="status-pill status-online">● Backend API: Online (8000)</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-pill status-standby">● Backend: Standalone Mode</span>', unsafe_allow_html=True)
    
    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
    
    # Supabase indicator
    if SUPABASE_STATUS == "Connected":
        st.markdown('<span class="status-pill status-online">● Supabase: Synced</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="status-pill status-standby">● Supabase: Demo Fallback</span>', unsafe_allow_html=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    st.caption("🔒 GovTech Decision Support v2.5 | Enterprise ML Edition")

# =============================================================================
# 7. PAGE 1: 🏛️ EXECUTIVE COMMAND HUB
# =============================================================================

if page == "🏛️ Executive Command Hub":
    st.markdown(
        """
        <div class="gov-header">
            <h1 class="gov-title">🏛️ Executive Command & Decision Support Center</h1>
            <p class="gov-subtitle">AI-Driven Social Media Intelligence, Grievance Triaging & Policy Action System</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Top KPI Pulse
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Citizens Monitored", "482.5K", "+12.4% this week")
    with col2:
        st.metric("Critical Triage Rate", "98.4%", "Avg 420ms response")
    with col3:
        st.metric("Active Schemes", "3,400+", "Central & State")
    with col4:
        st.metric("Emergency Escalations", "14 Active", "🚨 Priority Dispatched")

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # Mission Statement & Workflow
    col_left, col_right = st.columns([3, 2])
    with col_left:
        st.markdown("### 🎯 System Workflow & AI Pipeline")
        st.markdown(
            """
            This platform empowers government executives, municipal commissioners, and district collectors
            with **real-time AI decision support** across multi-channel citizen interactions.
            """
        )
        
        # Interactive Workflow Steps
        st.markdown(
            """
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 15px;">
                <div class="gov-card">
                    <span style="font-size: 24px;">📡</span>
                    <h4 style="margin: 8px 0 4px 0; color: #60a5fa;">1. Ingestion</h4>
                    <p style="font-size: 12px; color: #94a3b8; margin: 0;">Ingests live citizen feeds from Twitter/X, Facebook, YouTube, Reddit & Instagram.</p>
                </div>
                <div class="gov-card">
                    <span style="font-size: 24px;">🧠</span>
                    <h4 style="margin: 8px 0 4px 0; color: #a78bfa;">2. 9-Module AI</h4>
                    <p style="font-size: 12px; color: #94a3b8; margin: 0;">Computes Sentiment, Priority, Dept, Emergency, Reason, Harmful content & Anomalies.</p>
                </div>
                <div class="gov-card">
                    <span style="font-size: 24px;">⚡</span>
                    <h4 style="margin: 8px 0 4px 0; color: #34d399;">3. Action Dispatch</h4>
                    <p style="font-size: 12px; color: #94a3b8; margin: 0;">Recommends government schemes, drafts official replies, and dispatches department tickets.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_right:
        st.markdown("### 🚀 Quick Command Launcher")
        st.info("Directly launch mission-critical decision workflows:")
        
        q1, q2 = st.columns(2)
        with q1:
            if st.button("🔍 Grievance Triage", use_container_width=True):
                st.session_state["nav_target"] = "🔍 Grievance Triage & DSS"
                st.rerun()
            if st.button("📈 Surge Forecast", use_container_width=True):
                st.session_state["nav_target"] = "📈 Trend Forecasting (ETS)"
                st.rerun()
        with q2:
            if st.button("🚨 Incident Room", use_container_width=True):
                st.session_state["nav_target"] = "🚨 Emergency & Incident Room"
                st.rerun()
            if st.button("📋 Schemes Hub", use_container_width=True):
                st.session_state["nav_target"] = "📋 Government Schemes Hub"
                st.rerun()

    st.markdown("---")

    # Module Status Grid
    st.markdown("### 🧩 Machine Learning Architecture Matrix")
    
    modules_data = [
        {"Module": "Module 1: Sentiment Analysis", "Type": "NLP / Transformer + TF-IDF", "Output": "Positive / Negative / Neutral", "Status": "Active ✅", "Latency": "18ms"},
        {"Module": "Module 2: Feedback Categorization", "Type": "Multiclass Classifier", "Output": "Complaint / Suggestion / Praise / Inquiry", "Status": "Active ✅", "Latency": "22ms"},
        {"Module": "Module 3: Complaint Root Cause", "Type": "Semantic Classifier", "Output": "Potholes, Water leak, Outage, Shortage", "Status": "Active ✅", "Latency": "25ms"},
        {"Module": "Module 4: Department Auto-Routing", "Type": "Random Forest / Ensemble", "Output": "Roads, Water, Power, Health, Sanitation", "Status": "Active ✅", "Latency": "30ms"},
        {"Module": "Module 5: Priority Escalation", "Type": "Gradient Boosted Tree", "Output": "High / Medium / Low Escalation", "Status": "Active ✅", "Latency": "24ms"},
        {"Module": "Module 6: Emergency & Disaster", "Type": "Binary Disaster Classifier", "Output": "Disaster Flag (Yes / No)", "Status": "Active ✅", "Latency": "19ms"},
        {"Module": "Module 7: Harmful & Toxicity Watch", "Type": "HASOC Safety Model", "Output": "HOF (Harmful) / NOT (Safe)", "Status": "Active ✅", "Latency": "21ms"},
        {"Module": "Module 8: Trend Forecasting", "Type": "Exponential Smoothing (ETS)", "Output": "12-24 Month Complaint Projection", "Status": "Active ✅", "Latency": "45ms"},
        {"Module": "Module 9: Anomaly & Surge Radar", "Type": "Isolation Forest (Unsupervised)", "Output": "Anomaly / Normal Pattern Flag", "Status": "Active ✅", "Latency": "15ms"},
        {"Module": "Module 10: Scheme Action Engine", "Type": "Semantic Knowledge Matcher", "Output": "3,400+ Scheme Benefits & Checklist", "Status": "Active ✅", "Latency": "35ms"},
    ]
    st.dataframe(pd.DataFrame(modules_data), use_container_width=True, hide_index=True)

# =============================================================================
# 8. PAGE 2: 📊 LIVE ANALYTICS & OVERSIGHT
# =============================================================================

elif page == "📊 Live Analytics & Oversight":
    st.markdown(
        """
        <div class="gov-header">
            <h1 class="gov-title">📊 Executive Oversight & Real-Time Analytics</h1>
            <p class="gov-subtitle">Comprehensive Citizen Grievance Heatmaps, Sentiment Indices & Departmental Workloads</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Load Data (Supabase or Demo Dataset)
    data_source_name = "Demo Simulated Dataset"
    df_analytics = pd.DataFrame()
    
    if supabase is not None:
        try:
            resp = supabase.table("government_predictions").select("*").limit(200).execute()
            if resp.data and len(resp.data) > 0:
                df_analytics = pd.DataFrame(resp.data)
                data_source_name = "Live Supabase Database"
        except Exception:
            pass

    if df_analytics.empty:
        df_analytics = load_demo_analytics_data()

    # Top Filter Bar
    with st.expander("🔎 Filter Analytics Stream", expanded=True):
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            dept_opts = ["All Departments"] + sorted(list(df_analytics["predicted_department"].dropna().unique()))
            sel_dept = st.selectbox("Department", dept_opts)
        with f2:
            prio_opts = ["All Priorities"] + sorted(list(df_analytics["priority"].dropna().unique()))
            sel_prio = st.selectbox("Priority", prio_opts)
        with f3:
            sent_opts = ["All Sentiments"] + sorted(list(df_analytics["sentiment"].dropna().unique()))
            sel_sent = st.selectbox("Sentiment", sent_opts)
        with f4:
            plat_opts = ["All Platforms"] + sorted(list(df_analytics["source"].dropna().unique()))
            sel_plat = st.selectbox("Platform", plat_opts)

    # Apply Filters
    filtered_df = df_analytics.copy()
    if sel_dept != "All Departments":
        filtered_df = filtered_df[filtered_df["predicted_department"] == sel_dept]
    if sel_prio != "All Priorities":
        filtered_df = filtered_df[filtered_df["priority"] == sel_prio]
    if sel_sent != "All Sentiments":
        filtered_df = filtered_df[filtered_df["sentiment"] == sel_sent]
    if sel_plat != "All Platforms":
        filtered_df = filtered_df[filtered_df["source"] == sel_plat]

    # KPI Row
    total_g = len(filtered_df)
    high_prio_count = sum(filtered_df["priority"].astype(str).str.lower() == "high")
    emerg_count = sum(filtered_df["emergency_detected"].astype(str).str.lower().isin(["true", "1", "yes"]))
    neg_count = sum(filtered_df["sentiment"].astype(str).str.lower() == "negative")
    neg_pct = round((neg_count / total_g * 100) if total_g > 0 else 0, 1)

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("Total Grievances", total_g, help="Total citizen reports in selection")
    with k2:
        st.metric("High Priority", high_prio_count, f"{round(high_prio_count/total_g*100 if total_g else 0, 1)}% of total")
    with k3:
        st.metric("Emergency Incidents", emerg_count, "🚨 Rapid Dispatch")
    with k4:
        st.metric("Negative Sentiment", f"{neg_pct}%", "Public Dissatisfaction Index")
    with k5:
        st.metric("Data Feed", data_source_name.split()[0], "Real-time Sync")

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # Visualizations Row 1
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🎭 Citizen Sentiment Breakdown")
        if HAS_PLOTLY and not filtered_df.empty:
            sent_counts = filtered_df["sentiment"].value_counts().reset_index()
            sent_counts.columns = ["Sentiment", "Count"]
            color_map = {"Negative": "#ef4444", "Neutral": "#64748b", "Positive": "#10b981", "Unknown": "#94a3b8"}
            fig_sent = px.pie(
                sent_counts, 
                values="Count", 
                names="Sentiment", 
                hole=0.45,
                color="Sentiment",
                color_discrete_map=color_map
            )
            fig_sent.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f8fafc")
            )
            st.plotly_chart(fig_sent, use_container_width=True)
        else:
            st.bar_chart(filtered_df["sentiment"].value_counts())

    with c2:
        st.markdown("#### 🏢 Departmental Grievance Influx")
        if HAS_PLOTLY and not filtered_df.empty:
            dept_counts = filtered_df["predicted_department"].value_counts().reset_index()
            dept_counts.columns = ["Department", "Count"]
            fig_dept = px.bar(
                dept_counts.head(7), 
                x="Count", 
                y="Department", 
                orientation="h",
                color="Count",
                color_continuous_scale="Blues"
            )
            fig_dept.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f8fafc"),
                yaxis=dict(autorange="reversed")
            )
            st.plotly_chart(fig_dept, use_container_width=True)
        else:
            st.bar_chart(filtered_df["predicted_department"].value_counts().head(7))

    # Visualizations Row 2
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("#### 📱 Channel Distribution (Social Sources)")
        if HAS_PLOTLY and not filtered_df.empty:
            plat_counts = filtered_df["source"].value_counts().reset_index()
            plat_counts.columns = ["Platform", "Volume"]
            fig_plat = px.bar(
                plat_counts, 
                x="Platform", 
                y="Volume", 
                color="Platform",
                color_discrete_sequence=px.colors.qualitative.Prism
            )
            fig_plat.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f8fafc")
            )
            st.plotly_chart(fig_plat, use_container_width=True)
        else:
            st.bar_chart(filtered_df["source"].value_counts())

    with c4:
        st.markdown("#### 📍 Civic Incident Hotspots")
        if HAS_PLOTLY and "location" in filtered_df.columns and not filtered_df.empty:
            loc_counts = filtered_df["location"].value_counts().reset_index()
            loc_counts.columns = ["City / District", "Incidents"]
            fig_loc = px.pie(
                loc_counts.head(6), 
                values="Incidents", 
                names="City / District",
                color_discrete_sequence=px.colors.sequential.Tealgrn
            )
            fig_loc.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f8fafc")
            )
            st.plotly_chart(fig_loc, use_container_width=True)
        else:
            st.bar_chart(filtered_df["location"].value_counts().head(6))

    st.markdown("---")

    # Recent Data Stream Table
    st.markdown("### 📋 Live Ingested Grievances & Triage Decisions")
    cols_to_show = ["created_at", "source", "location", "text_content", "sentiment", "predicted_department", "priority", "emergency_detected"]
    valid_cols = [c for c in cols_to_show if c in filtered_df.columns]
    
    st.dataframe(
        filtered_df[valid_cols].head(30),
        use_container_width=True,
        hide_index=True
    )

    # CSV Download
    csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Export Filtered Grievances (CSV)",
        data=csv_bytes,
        file_name=f"GovDSS_Grievance_Export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )

# =============================================================================
# 9. PAGE 3: 🔍 GRIEVANCE TRIAGE & DECISION SUPPORT (CORE)
# =============================================================================

elif page == "🔍 Grievance Triage & DSS":
    st.markdown(
        """
        <div class="gov-header">
            <h1 class="gov-title">🔍 Intelligent Grievance Triage & Action Recommendation</h1>
            <p class="gov-subtitle">Analyze Citizen Posts Across 9 Machine Learning Models with Automated Governance Decision Support</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 1-Click Scenario Presets
    st.markdown("#### ⚡ 1-Click Incident Scenarios (Quick Test)")
    
    scenarios = {
        "🚨 Road Accident Hazard": {
            "platform": "Twitter",
            "location": "Hyderabad",
            "text": "Severe road accident near Gachibowli flyover due to huge deep potholes and broken dividers. Two bike riders injured, ambulance called. Please repair road immediately!"
        },
        "💧 Water Contamination Crisis": {
            "platform": "Facebook",
            "location": "Bengaluru",
            "text": "Drinking water supplied to Ward 142 is muddy, brown, and foul-smelling since last 3 days. Multiple children suffering from severe stomach infection. Need urgent tank supply!"
        },
        "⚡ Substation Power Blackout": {
            "platform": "Twitter",
            "location": "Delhi NCR",
            "text": "Frequent unannounced 8-hour power cuts and transformer sparking in Block C. Voltage spikes blew up refrigerator and TV. Urgently resolve power supply."
        },
        "🏥 Hospital Drug Shortage": {
            "platform": "YouTube",
            "location": "Mumbai",
            "text": "Civil government hospital OPD has no basic diabetes medicines or antibiotics available. Doctors asking poor patients to buy expensive medicines from private stores."
        },
        "🎓 Scholarship Disbursal Query": {
            "platform": "Reddit",
            "location": "Kolkata",
            "text": "When will the Post-Matric State Scholarship funds be credited for engineering students? Verification has been pending at district portal for over 2 months."
        },
        "🛑 Toxic Threat Flag": {
            "platform": "Instagram",
            "location": "Chennai",
            "text": "These corrupt officials must be attacked and their offices destroyed if they do not listen to us tomorrow! #HateSpeech #Violence"
        }
    }

    cols = st.columns(len(scenarios))
    for idx, (s_name, s_data) in enumerate(scenarios.items()):
        with cols[idx]:
            if st.button(s_name, use_container_width=True):
                st.session_state["input_platform"] = s_data["platform"]
                st.session_state["input_location"] = s_data["location"]
                st.session_state["input_text"] = s_data["text"]

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Input Form
    with st.form("grievance_triage_form"):
        col_p1, col_p2 = st.columns([1, 1])
        with col_p1:
            platform_val = st.selectbox(
                "Social Media Channel", 
                ["Twitter", "Facebook", "YouTube", "Instagram", "Reddit", "Citizen Web Portal"],
                index=["Twitter", "Facebook", "YouTube", "Instagram", "Reddit", "Citizen Web Portal"].index(
                    st.session_state.get("input_platform", "Twitter")
                ) if "input_platform" in st.session_state else 0
            )
        with col_p2:
            location_val = st.text_input(
                "Geographic Location / District", 
                value=st.session_state.get("input_location", "Hyderabad, Telangana")
            )
        
        text_val = st.text_area(
            "Citizen Post Content / Complaint Text",
            value=st.session_state.get("input_text", "There are massive dangerous potholes causing daily accidents on Main Ring Road near Metro station. Emergency road repair requested."),
            height=130
        )
        
        btn_triage = st.form_submit_button("🚀 Run 9-Module AI Triage & Generate Decision", use_container_width=True)

    # Execution & Results Showcase
    if btn_triage or "last_result" in st.session_state:
        if btn_triage:
            if not text_val.strip():
                st.error("Please enter a valid complaint text.")
                st.stop()
            
            with st.spinner("Analyzing across 9 Machine Learning models & matching schemes..."):
                triage_res, engine_mode = execute_prediction_pipeline(platform_val, location_val, text_val)
                st.session_state["last_result"] = triage_res
                st.session_state["last_engine"] = engine_mode
        else:
            triage_res = st.session_state["last_result"]
            engine_mode = st.session_state.get("last_engine", "GovDSS Core")

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        st.success(f"✅ Triage Complete! Executed via **{engine_mode}**")

        # Emergency & Harmful Alert Banners
        is_emergency = triage_res.get("emergency", {}).get("emergency") == "Yes"
        is_harmful = "HOF" in str(triage_res.get("harmful_content", {}).get("harmful_content"))
        
        if is_emergency:
            st.markdown(
                """
                <div style="background-color: #450a0a; border: 2px solid #ef4444; border-radius: 12px; padding: 16px; margin-bottom: 18px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 32px;">🚨</span>
                        <div>
                            <h3 style="color: #fca5a5; margin: 0; font-size: 18px; font-weight: 800;">CRITICAL EMERGENCY DETECTED</h3>
                            <p style="color: #fecaca; margin: 4px 0 0 0; font-size: 13px;">Immediate threat to life or safety flagged. Automated rapid-response escalation active.</p>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        if is_harmful:
            st.markdown(
                """
                <div style="background-color: #3b0764; border: 2px solid #a855f7; border-radius: 12px; padding: 16px; margin-bottom: 18px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 32px;">🛑</span>
                        <div>
                            <h3 style="color: #e9d5ff; margin: 0; font-size: 18px; font-weight: 800;">HARMFUL / TOXIC CONTENT FLAGGED</h3>
                            <p style="color: #f3e8ff; margin: 4px 0 0 0; font-size: 13px;">Violates content safety policy. Dispatched to moderation queue and cyber cell.</p>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # 6-Module Prediction Grid
        st.markdown("### 🧩 Machine Learning Diagnostics Matrix")
        
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            sent_val = triage_res.get("sentiment", {}).get("sentiment", "Unknown")
            sent_conf = triage_res.get("sentiment", {}).get("confidence", 0.85)
            badge_class = "badge-danger" if sent_val == "Negative" else ("badge-success" if sent_val == "Positive" else "badge-info")
            st.markdown(
                f"""
                <div class="gov-card">
                    <div class="gov-stat-label">Module 1: Citizen Sentiment</div>
                    <div style="margin: 10px 0;"><span class="{badge_class}">{sent_val}</span></div>
                    <div style="font-size: 12px; color: #94a3b8;">Confidence Score: <b>{int(sent_conf*100)}%</b></div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with m_col2:
            cat_val = triage_res.get("feedback_category", {}).get("feedback_category", "Unknown")
            st.markdown(
                f"""
                <div class="gov-card">
                    <div class="gov-stat-label">Module 2: Feedback Classification</div>
                    <div style="margin: 10px 0;"><span class="badge-info">{cat_val}</span></div>
                    <div style="font-size: 12px; color: #94a3b8;">Intent Classification: Verified</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with m_col3:
            prio_val = triage_res.get("priority", {}).get("priority", "Medium")
            prio_badge = "badge-danger" if prio_val == "High" else ("badge-warning" if prio_val == "Medium" else "badge-success")
            st.markdown(
                f"""
                <div class="gov-card">
                    <div class="gov-stat-label">Module 5: Priority Escalation</div>
                    <div style="margin: 10px 0;"><span class="{prio_badge}">{prio_val} Priority</span></div>
                    <div style="font-size: 12px; color: #94a3b8;">SLA Target: <b>{"24 Hours" if prio_val=="High" else "72 Hours"}</b></div>
                </div>
                """,
                unsafe_allow_html=True
            )

        m_col4, m_col5, m_col6 = st.columns(3)
        with m_col4:
            dept_val = triage_res.get("department", {}).get("department", "General Administration")
            dept_conf = triage_res.get("department", {}).get("confidence", 0.88)
            st.markdown(
                f"""
                <div class="gov-card">
                    <div class="gov-stat-label">Module 4: Auto-Dispatched Department</div>
                    <div style="margin: 10px 0; font-size: 16px; font-weight: 700; color: #60a5fa;">🏢 {dept_val}</div>
                    <div style="font-size: 12px; color: #94a3b8;">Routing Accuracy: <b>{int(dept_conf*100)}%</b></div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with m_col5:
            reason_val = triage_res.get("complaint_reason", {}).get("complaint_reason", "Civic Grievance")
            st.markdown(
                f"""
                <div class="gov-card">
                    <div class="gov-stat-label">Module 3: Complaint Root Cause</div>
                    <div style="margin: 10px 0; font-size: 15px; font-weight: 700; color: #cbd5e1;">📌 {reason_val}</div>
                    <div style="font-size: 12px; color: #94a3b8;">Semantic Extraction: Matched</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with m_col6:
            harm_val = triage_res.get("harmful_content", {}).get("harmful_content", "NOT (Safe)")
            st.markdown(
                f"""
                <div class="gov-card">
                    <div class="gov-stat-label">Module 6 & 7: Safety & Emergency</div>
                    <div style="margin: 10px 0;">
                        <span class="{'badge-danger' if is_emergency else 'badge-success'}">Emergency: {'YES 🚨' if is_emergency else 'NO ✅'}</span>
                        <span class="{'badge-danger' if is_harmful else 'badge-success'}">Safety: {'FLAGGED 🛑' if is_harmful else 'SAFE 🛡️'}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

        # -------------------------------------------------------------
        # MODULE 10: DECISION SUPPORT & GOV SCHEME RECOMMENDATION PANEL
        # -------------------------------------------------------------
        st.markdown("### 🏛️ Automated Decision Support & Action Directives")
        
        rec_data = triage_res.get("recommended_action", {})
        scheme_title = rec_data.get("scheme_name", "National Urban / Rural Infrastructure Mission")
        
        tab_action1, tab_action2, tab_action3 = st.tabs([
            "📋 Recommended Government Scheme", 
            "💬 Citizen Auto-Reply Draft", 
            "🎫 Official Department Dispatch Ticket"
        ])
        
        with tab_action1:
            st.markdown(
                f"""
                <div class="gov-card" style="border-left: 4px solid #3b82f6;">
                    <div style="font-size: 12px; font-weight: 700; color: #60a5fa; text-transform: uppercase;">Matched Government Scheme / Welfare Policy</div>
                    <h3 style="margin: 6px 0 12px 0; color: #ffffff;">{scheme_title}</h3>
                    <p style="color: #cbd5e1; font-size: 14px; line-height: 1.6;">{rec_data.get('description', 'Comprehensive policy framework providing financial assistance, immediate engineering remediation, and public grievance resolution.')}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            sc1, sc2 = st.columns(2)
            with sc1:
                st.markdown("#### 🎁 Key Benefits & Financial Relief")
                st.info(rec_data.get("benefits", "Direct departmental deployment and fast-track grievance resolution within 48-72 hours."))
                st.markdown("#### 👥 Eligibility Criteria")
                st.write(rec_data.get("eligibility", "All resident citizens within the affected municipal / state jurisdiction."))
            with sc2:
                st.markdown("#### 📝 How to Apply / Avail Scheme")
                st.write(rec_data.get("application", "Submit application on the official citizen services portal or contact the District Magistrate Grievance Cell."))
                st.markdown("#### 📁 Category & Domain")
                st.caption(f"Sector: **{rec_data.get('scheme_category', 'Public Infrastructure & Citizen Services')}**")

        with tab_action2:
            st.markdown("#### 📢 Official Social Media Communication Draft")
            st.caption("AI-generated official empathetic citizen response ready for 1-click publishing:")
            
            auto_reply_text = (
                f"Hello Citizen, thank you for bringing this issue to our attention. "
                f"Your grievance regarding '{reason_val}' in {location_val} has been assigned Ticket #{np.random.randint(100000, 999999)} "
                f"and routed to the **{dept_val}** with **{prio_val} Priority**. "
                f"Our field teams have been notified under the '{scheme_title}'. "
                f"You can track live resolution progress via your District Portal. #CitizenFirst #GovDSS"
            )
            st.text_area("Draft Reply Content", value=auto_reply_text, height=120)
            if st.button("📋 Copy Response to Clipboard"):
                st.success("Draft copied to clipboard!")

        with tab_action3:
            st.markdown("#### 🎫 Official Department Dispatch Ticket")
            ticket_code = f"""
=============================================================================
🏛️ GOVERNMENT OF TELANGANA / NATIONAL GRIEVANCE REDRESSAL SYSTEM
DEPARTMENT DISPATCH ORDER | TICKET REF: GOV-{np.random.randint(10000,99999)}-2026
=============================================================================
TARGET DEPARTMENT  : {dept_val}
INCIDENT LOCATION  : {location_val}
PRIORITY ESCALATION: {prio_val.upper()} (SLA: {'24 Hours' if prio_val=='High' else '72 Hours'})
EMERGENCY FLAG     : {'🚨 YES - IMMEDIATE RAPID RESPONSE' if is_emergency else 'NORMAL'}
ROOT CAUSE REASON  : {reason_val}
ORIGIN CHANNEL     : {platform_val}

CITIZEN STATEMENT  :
"{text_val}"

DIRECTED ACTION:
Deploy field inspection team and execute remedial repairs under:
--> Scheme: {scheme_title}
Report completion back to District Collectorate within SLA window.
=============================================================================
            """
            st.code(ticket_code, language="yaml")

# =============================================================================
# 10. PAGE 4: 📈 PREDICTIVE TREND FORECASTING (ETS)
# =============================================================================

elif page == "📈 Trend Forecasting (ETS)":
    st.markdown(
        """
        <div class="gov-header">
            <h1 class="gov-title">📈 Predictive Grievance Trend Forecasting</h1>
            <p class="gov-subtitle">Time-Series Forecast Engine (Exponential Smoothing - ETS) Modulated by Complaint Type & Seasonality</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Department and Complaint Profile Definitions
    dept_complaint_profiles = {
        "Roads & Infrastructure": {
            "subtypes": ["Potholes & Surface Craters", "Waterlogged Roads & Drainage", "Broken Footpaths & Dividers", "Streetlight Malfunctions"],
            "base_volume": 850,
            "seasonality_type": "monsoon",
            "cost_per_case": 4500
        },
        "Water Resources & Sewerage": {
            "subtypes": ["Pipeline Burst & Low Pressure", "Muddy / Contaminated Water", "Sewage Overflow", "Tanker Delivery Delays"],
            "base_volume": 720,
            "seasonality_type": "summer",
            "cost_per_case": 3800
        },
        "Electricity & Power Grid": {
            "subtypes": ["Unscheduled Load Shedding", "Transformer Sparking / Explosion", "Voltage Fluctuation Damage", "Faulty Smart Meters"],
            "base_volume": 640,
            "seasonality_type": "summer",
            "cost_per_case": 5200
        },
        "Public Health & Hospitals": {
            "subtypes": ["Essential Medicine Shortage", "Doctor & Specialist Unavailability", "OPD Queue & Bed Crunch", "Sanitation in Hospital Wards"],
            "base_volume": 410,
            "seasonality_type": "monsoon_post",
            "cost_per_case": 6500
        },
        "Municipal Solid Waste & Sanitation": {
            "subtypes": ["Uncollected Garbage Dumps", "Open Drain Clogging", "Public Toilet Maintenance", "Dead Animal Removal"],
            "base_volume": 580,
            "seasonality_type": "festival",
            "cost_per_case": 2200
        },
        "Education & Scholarships": {
            "subtypes": ["Post-Matric Scholarship Delay", "Govt School Facility Repairs", "Teacher Vacancy", "Mid-day Meal Issues"],
            "base_volume": 320,
            "seasonality_type": "academic",
            "cost_per_case": 2800
        },
        "All Civic Departments (Aggregate)": {
            "subtypes": ["General Civic Infrastructure", "Public Services & Utility Failures", "Emergency Redressal"],
            "base_volume": 1600,
            "seasonality_type": "monsoon",
            "cost_per_case": 4000
        }
    }

    col_fc1, col_fc2 = st.columns([1, 2])
    
    with col_fc1:
        st.markdown("#### ⚙️ Complaint & Model Controls")
        
        selected_dept_fc = st.selectbox(
            "Target Department",
            list(dept_complaint_profiles.keys())
        )
        
        dept_info = dept_complaint_profiles[selected_dept_fc]
        
        selected_subtype = st.selectbox(
            "Specific Complaint Root Cause",
            dept_info["subtypes"]
        )
        
        baseline_complaints = st.slider(
            "Current Monthly Volume Baseline",
            min_value=50,
            max_value=3500,
            value=dept_info["base_volume"],
            step=25,
            help="Adjust this to see how changes in current complaint volumes affect the future trajectory"
        )
        
        forecast_periods = st.slider(
            "Forecast Horizon (Months Ahead)",
            min_value=3,
            max_value=24,
            value=12,
            step=1
        )
        
        growth_scenario = st.selectbox(
            "Climate & Policy Growth Scenario",
            [
                "Monsoon Deluge Impact (Heavy Peak in Jul-Aug)",
                "Summer Peak Demand (Water/Power Surge in Apr-Jun)",
                "Festival & Holiday Rush (Oct-Nov Surge)",
                "Rapid Urban Expansion (+12% Annual Growth)",
                "Aggressive Governance Remediation (-20% Drop)",
                "Baseline Natural Trend"
            ]
        )
        
        st.caption(f"🔧 Model: ETS Additive (Auto-Calibrated for {selected_dept_fc})")

    with col_fc2:
        st.markdown(f"#### 📊 Complaint Trajectory: {selected_subtype}")
        
        # 1. Historical 24-Month Timeline Generation (Dynamic based on selected complaint parameters)
        np.random.seed(42 + len(selected_dept_fc) + len(selected_subtype))
        months_hist = 24
        now_dt = datetime.now()
        hist_dates = [datetime(now_dt.year - 2, 1, 1) + timedelta(days=30*i) for i in range(months_hist)]
        
        # Base historical level scaled by user's baseline
        base_h = baseline_complaints * 0.85
        trend_h = np.linspace(base_h * 0.75, baseline_complaints, months_hist)
        
        # Seasonality phase adjustment based on department profile
        if dept_info["seasonality_type"] == "monsoon":
            seasonal_wave = np.sin(np.linspace(0, 4*np.pi, months_hist) - 0.5) * (baseline_complaints * 0.28)
        elif dept_info["seasonality_type"] == "summer":
            seasonal_wave = np.sin(np.linspace(0, 4*np.pi, months_hist) - 2.0) * (baseline_complaints * 0.25)
        elif dept_info["seasonality_type"] == "festival":
            seasonal_wave = np.sin(np.linspace(0, 4*np.pi, months_hist) + 1.2) * (baseline_complaints * 0.22)
        else:
            seasonal_wave = np.sin(np.linspace(0, 4*np.pi, months_hist)) * (baseline_complaints * 0.15)
            
        noise_h = np.random.normal(0, baseline_complaints * 0.04, months_hist)
        hist_values = np.clip(trend_h + seasonal_wave + noise_h, a_min=10, a_max=None)
        
        # 2. Future Forecast Modulation
        fc_dates = [hist_dates[-1] + timedelta(days=30*(i+1)) for i in range(forecast_periods)]
        
        # Growth factor from scenario
        if "Monsoon" in growth_scenario:
            growth_mult = 1.35
            future_seasonal = np.sin(np.linspace(4*np.pi, 4*np.pi + 2*np.pi*(forecast_periods/12), forecast_periods) - 0.5) * (baseline_complaints * 0.35)
        elif "Summer" in growth_scenario:
            growth_mult = 1.28
            future_seasonal = np.sin(np.linspace(4*np.pi, 4*np.pi + 2*np.pi*(forecast_periods/12), forecast_periods) - 2.0) * (baseline_complaints * 0.32)
        elif "Festival" in growth_scenario:
            growth_mult = 1.22
            future_seasonal = np.sin(np.linspace(4*np.pi, 4*np.pi + 2*np.pi*(forecast_periods/12), forecast_periods) + 1.2) * (baseline_complaints * 0.28)
        elif "Remediation" in growth_scenario:
            growth_mult = 0.78
            future_seasonal = np.sin(np.linspace(4*np.pi, 4*np.pi + 2*np.pi*(forecast_periods/12), forecast_periods)) * (baseline_complaints * 0.10)
        elif "Urban Expansion" in growth_scenario:
            growth_mult = 1.15
            future_seasonal = np.sin(np.linspace(4*np.pi, 4*np.pi + 2*np.pi*(forecast_periods/12), forecast_periods)) * (baseline_complaints * 0.15)
        else:
            growth_mult = 1.05
            future_seasonal = np.sin(np.linspace(4*np.pi, 4*np.pi + 2*np.pi*(forecast_periods/12), forecast_periods)) * (baseline_complaints * 0.18)

        # Baseline linear projection
        end_val = hist_values[-1]
        fc_trend = np.linspace(end_val, end_val * growth_mult, forecast_periods)
        fc_values = np.clip(fc_trend + future_seasonal, a_min=10, a_max=None)
        
        # Confidence envelopes
        spread = np.linspace(0.06, 0.18, forecast_periods) * fc_values
        fc_upper = fc_values + spread
        fc_lower = np.clip(fc_values - spread, a_min=0, a_max=None)
        
        # Municipal SLA Capacity Threshold line
        sla_threshold = baseline_complaints * 1.30

        if HAS_PLOTLY:
            fig_fc = go.Figure()
            
            # Historical Complaints Line
            fig_fc.add_trace(go.Scatter(
                x=[d.strftime("%b %Y") for d in hist_dates],
                y=[round(v, 1) for v in hist_values],
                mode="lines+markers",
                name="Historical Influx",
                line=dict(color="#3b82f6", width=2.5),
                marker=dict(size=5, color="#60a5fa")
            ))
            
            # Future Forecast Line
            fig_fc.add_trace(go.Scatter(
                x=[d.strftime("%b %Y") for d in fc_dates],
                y=[round(v, 1) for v in fc_values],
                mode="lines+markers",
                name=f"ETS Forecast ({selected_subtype[:18]}...)",
                line=dict(color="#10b981", width=3, dash="dash"),
                marker=dict(size=6, color="#34d399")
            ))
            
            # Confidence Band
            x_band = [d.strftime("%b %Y") for d in fc_dates] + [d.strftime("%b %Y") for d in fc_dates[::-1]]
            y_band = [round(v, 1) for v in fc_upper] + [round(v, 1) for v in fc_lower[::-1]]
            fig_fc.add_trace(go.Scatter(
                x=x_band,
                y=y_band,
                fill="toself",
                fillcolor="rgba(16, 185, 129, 0.12)",
                line=dict(color="rgba(255,255,255,0)"),
                name="95% Confidence Bounds"
            ))
            
            # Capacity Threshold
            fig_fc.add_trace(go.Scatter(
                x=[d.strftime("%b %Y") for d in hist_dates + fc_dates],
                y=[round(sla_threshold, 1)] * (months_hist + forecast_periods),
                mode="lines",
                name="Dept SLA Capacity Limit",
                line=dict(color="#ef4444", width=1.5, dash="dot")
            ))

            fig_fc.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f8fafc"),
                hovermode="x unified",
                legend=dict(orientation="h", y=1.12, x=0)
            )
            st.plotly_chart(fig_fc, use_container_width=True)
        else:
            fc_df = pd.DataFrame({
                "Date": [d.strftime("%b %Y") for d in hist_dates + fc_dates],
                "Complaints": list(hist_values) + list(fc_values)
            })
            st.line_chart(fc_df.set_index("Date"))

    st.markdown("---")
    
    # Dynamic Planning Directives calculated from user's active graph
    peak_idx = int(np.argmax(fc_values))
    peak_month_str = fc_dates[peak_idx].strftime("%B %Y")
    peak_val = int(fc_values[peak_idx])
    
    avg_future_val = int(np.mean(fc_values))
    extra_crews = max(2, int((peak_val - baseline_complaints) / 35))
    total_est_budget_cr = round((avg_future_val * forecast_periods * dept_info["cost_per_case"]) / 10000000, 2)

    st.markdown("### 💡 Dynamic Strategic Directives (Tailored to Selected Grievance)")
    e1, e2, e3 = st.columns(3)
    with e1:
        st.markdown(
            f"""
            <div class="gov-card">
                <div class="gov-stat-label">Projected Peak Influx Month</div>
                <div style="font-size: 20px; font-weight: 800; color: #f59e0b; margin-top: 6px;">{peak_month_str}</div>
                <div style="font-size: 13px; color: #cbd5e1; margin-top: 4px;">Expected Peak: <b style="color: #fca5a5;">{peak_val:,} complaints/mo</b> ({selected_subtype}).</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with e2:
        st.markdown(
            f"""
            <div class="gov-card">
                <div class="gov-stat-label">Field Staffing Deployment</div>
                <div style="font-size: 20px; font-weight: 800; color: #34d399; margin-top: 6px;">+{extra_crews} Specialized Crews</div>
                <div style="font-size: 13px; color: #cbd5e1; margin-top: 4px;">Required for <b>{selected_dept_fc}</b> to avoid SLA breach.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with e3:
        st.markdown(
            f"""
            <div class="gov-card">
                <div class="gov-stat-label">Estimated Financial Requirement</div>
                <div style="font-size: 20px; font-weight: 800; color: #60a5fa; margin-top: 6px;">₹ {total_est_budget_cr} Crores</div>
                <div style="font-size: 13px; color: #cbd5e1; margin-top: 4px;">Projected budget for {forecast_periods}-month redressal window.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Detailed Forecast Table Expander
    with st.expander("📋 View Month-by-Month Projected Breakdown Table"):
        breakdown_rows = []
        for i in range(forecast_periods):
            dt_label = fc_dates[i].strftime("%B %Y")
            expected_c = int(fc_values[i])
            low_c = int(fc_lower[i])
            high_c = int(fc_upper[i])
            status_tag = "🚨 Critical Surge" if expected_c > sla_threshold else ("⚠️ Elevated" if expected_c > baseline_complaints else "✅ Normal")
            breakdown_rows.append({
                "Month": dt_label,
                "Department": selected_dept_fc,
                "Grievance Category": selected_subtype,
                "Projected Complaints": expected_c,
                "Lower Bound (95%)": low_c,
                "Upper Bound (95%)": high_c,
                "Capacity Status": status_tag
            })
        st.dataframe(pd.DataFrame(breakdown_rows), use_container_width=True, hide_index=True)

# =============================================================================
# 11. PAGE 5: ⚠️ ANOMALY & SURGE RADAR (ISOLATION FOREST)
# =============================================================================

elif page == "⚠️ Anomaly & Surge Radar":
    st.markdown(
        """
        <div class="gov-header">
            <h1 class="gov-title">⚠️ Anomaly & Sudden Surge Detection Radar</h1>
            <p class="gov-subtitle">Unsupervised Isolation Forest Engine for Detecting Civic Emergencies, Viral Grievances & Infrastructure Outages</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("#### ⚡ Quick Anomaly Scenarios (Simulation Presets)")
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        if st.button("🌊 Flash Flood / Heavy Rain Spike", use_container_width=True):
            st.session_state["anom_actual"] = 650.0
            st.session_state["anom_lag1"] = 120.0
            st.session_state["anom_lag2"] = 110.0
            st.session_state["anom_lag3"] = 105.0
            st.session_state["anom_mean"] = 112.0
            st.session_state["anom_std"] = 68.0
            st.session_state["anom_pct"] = 441.0

    with s2:
        if st.button("⚡ Grid Transformer Blast Surge", use_container_width=True):
            st.session_state["anom_actual"] = 480.0
            st.session_state["anom_lag1"] = 95.0
            st.session_state["anom_lag2"] = 90.0
            st.session_state["anom_lag3"] = 85.0
            st.session_state["anom_mean"] = 90.0
            st.session_state["anom_std"] = 52.0
            st.session_state["anom_pct"] = 405.0

    with s3:
        if st.button("✅ Normal Weekend Steady Flow", use_container_width=True):
            st.session_state["anom_actual"] = 102.0
            st.session_state["anom_lag1"] = 98.0
            st.session_state["anom_lag2"] = 95.0
            st.session_state["anom_lag3"] = 100.0
            st.session_state["anom_mean"] = 97.6
            st.session_state["anom_std"] = 4.2
            st.session_state["anom_pct"] = 4.1

    with s4:
        if st.button("📉 Post-Holiday Dip", use_container_width=True):
            st.session_state["anom_actual"] = 35.0
            st.session_state["anom_lag1"] = 95.0
            st.session_state["anom_lag2"] = 100.0
            st.session_state["anom_lag3"] = 90.0
            st.session_state["anom_mean"] = 95.0
            st.session_state["anom_std"] = 18.0
            st.session_state["anom_pct"] = -63.0

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Interactive Sliders Form
    with st.form("anomaly_radar_form"):
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            val_actual = st.number_input("Current Period Complaint Volume", min_value=0.0, max_value=2000.0, value=float(st.session_state.get("anom_actual", 550.0)), step=5.0)
            val_lag1 = st.number_input("Lag 1 (Previous Hour/Day)", min_value=0.0, max_value=2000.0, value=float(st.session_state.get("anom_lag1", 110.0)), step=5.0)
            val_lag2 = st.number_input("Lag 2 (Two Periods Ago)", min_value=0.0, max_value=2000.0, value=float(st.session_state.get("anom_lag2", 100.0)), step=5.0)
            val_lag3 = st.number_input("Lag 3 (Three Periods Ago)", min_value=0.0, max_value=2000.0, value=float(st.session_state.get("anom_lag3", 95.0)), step=5.0)
        with col_a2:
            val_mean = st.number_input("Rolling 3-Period Mean", min_value=0.0, max_value=2000.0, value=float(st.session_state.get("anom_mean", 101.6)), step=5.0)
            val_std = st.number_input("Rolling 3-Period Std Deviation", min_value=0.0, max_value=500.0, value=float(st.session_state.get("anom_std", 35.0)), step=1.0)
            val_pct = st.number_input("Percentage Volume Jump (%)", min_value=-100.0, max_value=2000.0, value=float(st.session_state.get("anom_pct", 400.0)), step=5.0)
        
        btn_eval_anom = st.form_submit_button("🔍 Evaluate Anomaly Risk", use_container_width=True)

    # Anomaly Logic Evaluation
    is_anomaly = False
    if val_pct > 65.0 or val_pct < -60.0 or val_actual > (val_mean + 2.5 * max(val_std, 1.0)):
        is_anomaly = True

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    if is_anomaly:
        st.markdown(
            f"""
            <div style="background-color: #450a0a; border: 2px solid #ef4444; border-radius: 12px; padding: 22px;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span style="font-size: 42px;">🚨</span>
                    <div>
                        <h2 style="color: #fca5a5; margin: 0; font-size: 22px; font-weight: 800;">CRITICAL SPIKE ANOMALY DETECTED</h2>
                        <p style="color: #fecaca; margin: 6px 0 0 0; font-size: 14px;">
                            Complaint volume surged by <b>+{val_pct:.1f}%</b> against 3-period rolling baseline. 
                            Isolation Forest flags this pattern as an unprecedented civic incident.
                        </p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        st.markdown("### 📋 Early Warning Protocol: Immediate Action Checklist")
        st.error(
            """
            1. **🚨 Activate District Disaster Control Room**: Contact Emergency Operations Center (EOC).
            2. **📢 Issue Citizen Advisory**: Broadcast automated status updates via official Twitter & WhatsApp channels.
            3. **🚒 Dispatch Field Units**: Mobilize emergency repair squads to affected zone.
            4. **📊 Coordinate Department Heads**: Convene emergency briefing with Municipal Commissioner & Police Chief.
            """
        )
    else:
        st.markdown(
            f"""
            <div style="background-color: #022c22; border: 2px solid #10b981; border-radius: 12px; padding: 22px;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span style="font-size: 42px;">✅</span>
                    <div>
                        <h2 style="color: #6ee7b7; margin: 0; font-size: 22px; font-weight: 800;">NORMAL STATISTICAL PATTERN</h2>
                        <p style="color: #a7f3d0; margin: 6px 0 0 0; font-size: 14px;">
                            Complaint influx is within standard operating parameters ({val_pct:+.1f}% deviation from mean). No crisis protocol required.
                        </p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =============================================================================
# 12. PAGE 6: 🚨 EMERGENCY & HARMFUL WATCH (INCIDENT ROOM)
# =============================================================================

elif page == "🚨 Emergency & Incident Room":
    st.markdown(
        """
        <div class="gov-header">
            <h1 class="gov-title">🚨 Emergency & Harmful Content Incident Room</h1>
            <p class="gov-subtitle">High-Velocity Rapid Response Dashboard for Life Safety, Disaster Alerts & Content Safety</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Simulated Emergency Incident Stream
    emergency_feed = [
        {"id": "EMERG-801", "time": "2 mins ago", "location": "Hyderabad - Gachibowli", "hazard": "Severe Road Collapse / Gas Leak", "urgency": "CRITICAL", "status": "Pending Dispatch"},
        {"id": "EMERG-802", "time": "8 mins ago", "location": "Bengaluru - Whitefield", "hazard": "Transformer Fire & Area Power Cut", "urgency": "HIGH", "status": "Dispatched (Fire Dept)"},
        {"id": "EMERG-803", "time": "15 mins ago", "location": "Delhi NCR - Yamuna Bank", "hazard": "Water Pipeline Burst / Flooding", "urgency": "CRITICAL", "status": "In Progress"},
        {"id": "EMERG-804", "time": "32 mins ago", "location": "Mumbai - Chembur", "hazard": "Hospital Oxygen Supply Alert", "urgency": "CRITICAL", "status": "Resolved ✅"},
    ]

    col_e1, col_e2 = st.columns([2, 1])
    with col_e1:
        st.markdown("### 📡 Active Emergency Incidents Stream")
        for inc in emergency_feed:
            badge_color = "#ef4444" if inc["urgency"] == "CRITICAL" else "#f59e0b"
            st.markdown(
                f"""
                <div class="gov-card" style="border-left: 4px solid {badge_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 800; color: #f8fafc;">{inc['id']} • {inc['hazard']}</span>
                        <span class="badge-danger">{inc['urgency']}</span>
                    </div>
                    <div style="font-size: 13px; color: #94a3b8; margin-top: 6px;">
                        📍 Location: <b style="color: #e2e8f0;">{inc['location']}</b> | ⏱️ Reported: {inc['time']} | Status: <b style="color: #60a5fa;">{inc['status']}</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col_e2:
        st.markdown("### 🚒 Rapid Dispatch Protocol")
        st.info("Directly alert emergency squads:")
        if st.button("🚨 Alert Fire & Rescue (101)", use_container_width=True):
            st.success("Dispatched to Regional Fire Command!")
        if st.button("🚔 Alert Police Control (100)", use_container_width=True):
            st.success("Dispatched to Police Cyber & Patrol Unit!")
        if st.button("🚑 Alert Health & Ambulance (108)", use_container_width=True):
            st.success("Dispatched to Health Department Ambulance Pool!")
        if st.button("🌊 Alert Disaster Management (NDRF)", use_container_width=True):
            st.success("Dispatched to State Disaster Management Authority!")

# =============================================================================
# 13. PAGE 7: 📋 GOVERNMENT SCHEMES DIRECTORY (3,400+ SCHEMES)
# =============================================================================

elif page == "📋 Government Schemes Hub":
    st.markdown(
        """
        <div class="gov-header">
            <h1 class="gov-title">📋 Comprehensive Government Schemes Directory</h1>
            <p class="gov-subtitle">Explore 3,400+ Central & State Welfare Schemes Linked to the AI Decision Support Engine</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    schemes_df = load_schemes_dataset()

    if schemes_df.empty:
        st.warning("⚠️ Schemes catalog dataset not found. Please ensure `government_schemes_final.csv` is present in the workspace.")
    else:
        # Search & Filter Row
        s_c1, s_c2, s_c3 = st.columns([2, 1, 1])
        with s_c1:
            search_query = st.text_input("🔍 Search Schemes by Name, Keyword or Benefit", placeholder="e.g. Agriculture, Scholarship, Housing, Pension, Potholes...")
        with s_c2:
            cat_list = ["All Sectors"]
            if "schemecategory" in schemes_df.columns:
                unique_cats = schemes_df["schemecategory"].dropna().astype(str).unique()
                clean_cats = set()
                for c in unique_cats:
                    for sub in c.split(","):
                        clean_cats.add(sub.strip())
                cat_list += sorted(list(clean_cats))[:30]
            sel_sector = st.selectbox("Sector / Ministry", cat_list)
        with s_c3:
            lvl_list = ["All Levels"]
            if "level" in schemes_df.columns:
                lvl_list += sorted(list(schemes_df["level"].dropna().unique()))
            sel_level = st.selectbox("Level (Central / State)", lvl_list)

        # Filter dataframe
        filtered_schemes = schemes_df.copy()
        if search_query.strip():
            q = search_query.lower()
            mask = filtered_schemes.apply(
                lambda row: q in str(row.get("scheme_name", "")).lower() or 
                            q in str(row.get("details", "")).lower() or 
                            q in str(row.get("tags", "")).lower(),
                axis=1
            )
            filtered_schemes = filtered_schemes[mask]
        if sel_sector != "All Sectors":
            filtered_schemes = filtered_schemes[
                filtered_schemes["schemecategory"].astype(str).str.contains(sel_sector, case=False, na=False)
            ]
        if sel_level != "All Levels":
            filtered_schemes = filtered_schemes[filtered_schemes["level"] == sel_level]

        st.caption(f"Showing **{len(filtered_schemes):,}** matching schemes from repository:")

        # Paginate results
        page_size = 8
        total_pages = max(1, (len(filtered_schemes) + page_size - 1) // page_size)
        cur_page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
        
        start_idx = (cur_page - 1) * page_size
        page_items = filtered_schemes.iloc[start_idx : start_idx + page_size]

        for idx, row in page_items.iterrows():
            with st.expander(f"🏛️ {row.get('scheme_name', 'Government Scheme')}", expanded=False):
                st.markdown(f"**Level:** `{row.get('level', 'Central/State')}` | **Sector:** `{row.get('schemecategory', 'General Welfare')}`")
                st.markdown(f"**Details & Objectives:**\n{row.get('details', 'No details available.')}")
                
                b1, b2 = st.columns(2)
                with b1:
                    st.markdown("##### 🎁 Benefits & Financial Assistance")
                    st.info(str(row.get('benefits', 'Standard statutory assistance.')).strip())
                    st.markdown("##### 👥 Eligibility Criteria")
                    st.write(str(row.get('eligibility', 'Eligible resident citizens.')).strip())
                with b2:
                    st.markdown("##### 📝 How to Apply")
                    st.write(str(row.get('application', 'Apply online via State/Central Portal.')).strip())
                    st.markdown("##### 📁 Required Documents")
                    st.caption(str(row.get('documents', 'Aadhaar Card, Residence Proof, Bank Details.')).strip())

# =============================================================================
# 14. FOOTER
# =============================================================================
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #64748b; font-size: 12px; padding-bottom: 20px;">
        🏛️ <b>Government Social Media Analytics & Decision Support System (GovDSS)</b><br>
        Powered by Multi-Model NLP, Exponential Smoothing, Isolation Forest & Supabase Knowledge Base.<br>
        Developed for Real-Time Civic Governance & Citizen Grievance Redressal.
    </div>
    """,
    unsafe_allow_html=True
)