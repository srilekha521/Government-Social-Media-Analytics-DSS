import streamlit as st
import requests
import pandas as pd


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Government Social Media Analytics",
    page_icon="🏛️",
    layout="wide"
)


# ==========================================================
# BACKEND URL
# ==========================================================

BACKEND_URL = "http://127.0.0.1:8000"


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 32px;
        font-weight: 700;
    }

    .subtitle {
        font-size: 16px;
        margin-bottom: 25px;
    }

    .metric-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        text-align: center;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("🏛️ Government Analytics")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Overview",
        "🔍 Prediction",
        "📈 Trends",
        "⚠️ Anomalies",
        "📋 Government Schemes"
    ]
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Government Social Media Analytics & Decision Support System"
)


# ==========================================================
# HOME
# ==========================================================

if page == "🏠 Home":

    st.markdown(
        '<div class="main-title">'
        '🏛️ Government Social Media Analytics'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        ### Social Media Analytics & Decision Support System

        This platform analyzes citizen feedback from social media
        and provides government departments with actionable insights.
        """
    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            """
            ### 🔍 Prediction

            Analyze citizen complaints and predict:

            - Sentiment
            - Feedback category
            - Complaint reason
            - Department
            - Priority
            """
        )

    with col2:

        st.success(
            """
            ### 📊 Analytics

            Understand:

            - Complaint trends
            - Department performance
            - Priority distribution
            - Social media patterns
            """
        )

    with col3:

        st.warning(
            """
            ### 🏛️ Decision Support

            Recommend relevant government schemes
            based on citizen complaints.
            """
        )

    st.markdown("---")

    st.subheader("System Workflow")

    st.write(
        """
        Social Media Post
        ↓
        Machine Learning Models
        ↓
        Complaint Analysis
        ↓
        Department & Priority
        ↓
        Government Scheme Recommendation
        ↓
        Decision Support
        """
    )


# ==========================================================
# OVERVIEW
# ==========================================================

elif page == "📊 Overview":

    st.title("📊 Overview")

    st.write(
        "Overview dashboard will display analytics from stored predictions."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Complaints",
            "—"
        )

    with col2:
        st.metric(
            "High Priority",
            "—"
        )

    with col3:
        st.metric(
            "Emergency Cases",
            "—"
        )

    with col4:
        st.metric(
            "Departments",
            "—"
        )

    st.info(
        "Supabase analytics connection will be added next."
    )


# ==========================================================
# PREDICTION
# ==========================================================

elif page == "🔍 Prediction":

    st.title("🔍 Citizen Complaint Prediction")

    st.write(
        "Enter a citizen complaint to analyze it using the ML backend."
    )

    st.markdown("---")

    platform = st.selectbox(
        "Social Media Platform",
        [
            "YouTube",
            "Twitter",
            "Facebook",
            "Instagram",
            "Reddit"
        ]
    )

    location = st.text_input(
        "Location",
        placeholder="Example: Hyderabad"
    )

    complaint = st.text_area(
        "Citizen Complaint",
        placeholder=(
            "Example: There are large potholes on the road "
            "causing accidents. Please repair the road immediately."
        ),
        height=150
    )

    if st.button(
        "🔍 Analyze Complaint",
        use_container_width=True
    ):

        if not complaint.strip():

            st.error(
                "Please enter a complaint."
            )

        else:

            payload = {

                "platform": platform,

                "post_text": complaint,

                "location": location,

                "department": ""

            }

            try:

                with st.spinner(
                    "Analyzing complaint..."
                ):

                    response = requests.post(

                        f"{BACKEND_URL}/predict",

                        json=payload,

                        timeout=120

                    )

                if response.status_code == 200:

                    result = response.json()

                    if "error" in result:

                        st.error(
                            result["error"]
                        )

                    else:

                        st.success(
                            "Complaint analyzed successfully!"
                        )

                        st.markdown("---")

                        # ----------------------------------
                        # RESULTS
                        # ----------------------------------

                        st.subheader(
                            "Prediction Results"
                        )

                        col1, col2, col3 = st.columns(3)

                        with col1:

                            st.metric(
                                "Sentiment",
                                result[
                                    "sentiment"
                                ].get(
                                    "sentiment",
                                    "Unknown"
                                )
                            )

                        with col2:

                            st.metric(
                                "Feedback",
                                result[
                                    "feedback_category"
                                ].get(
                                    "feedback_category",
                                    "Unknown"
                                )
                            )

                        with col3:

                            st.metric(
                                "Priority",
                                result[
                                    "priority"
                                ].get(
                                    "priority",
                                    "Unknown"
                                )
                            )

                        col1, col2, col3 = st.columns(3)

                        with col1:

                            st.metric(
                                "Department",
                                result[
                                    "department"
                                ].get(
                                    "department",
                                    "Unknown"
                                )
                            )

                        with col2:

                            st.metric(
                                "Emergency",
                                result[
                                    "emergency"
                                ].get(
                                    "emergency",
                                    "Unknown"
                                )
                            )

                        with col3:

                            st.metric(
                                "Harmful Content",
                                result[
                                    "harmful_content"
                                ].get(
                                    "harmful_content",
                                    "Unknown"
                                )
                            )

                        # ----------------------------------
                        # COMPLAINT REASON
                        # ----------------------------------

                        st.markdown("---")

                        st.subheader(
                            "📌 Complaint Reason"
                        )

                        st.info(
                            result[
                                "complaint_reason"
                            ].get(
                                "complaint_reason",
                                "Not available"
                            )
                        )

                        # ----------------------------------
                        # GOVERNMENT RECOMMENDATION
                        # ----------------------------------

                        st.markdown("---")

                        st.subheader(
                            "🏛️ Government Recommendation"
                        )

                        recommendation = result.get(
                            "recommended_action",
                            {}
                        )

                        scheme_name = recommendation.get(
                            "scheme_name"
                        )

                        if scheme_name:

                            st.success(
                                f"Recommended Scheme: {scheme_name}"
                            )

                            st.write(
                                recommendation.get(
                                    "description",
                                    ""
                                )
                            )

                            with st.expander(
                                "View Scheme Details"
                            ):

                                st.write(
                                    "**Benefits**"
                                )

                                st.write(
                                    recommendation.get(
                                        "benefits",
                                        "Not available"
                                    )
                                )

                                st.write(
                                    "**Eligibility**"
                                )

                                st.write(
                                    recommendation.get(
                                        "eligibility",
                                        "Not available"
                                    )
                                )

                                st.write(
                                    "**Application**"
                                )

                                st.write(
                                    recommendation.get(
                                        "application",
                                        "Not available"
                                    )
                                )

                        else:

                            st.warning(
                                recommendation.get(
                                    "recommended_action",
                                    "No recommendation available."
                                )
                            )

                        # ----------------------------------
                        # RAW RESULT
                        # ----------------------------------

                        with st.expander(
                            "View Complete API Response"
                        ):

                            st.json(result)

                else:

                    st.error(
                        f"Backend error: {response.status_code}"
                    )

                    st.code(
                        response.text
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    """
                    ❌ Cannot connect to the FastAPI backend.

                    Make sure the backend is running:

                    uvicorn main:app --reload
                    """
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The backend took too long to respond."
                )

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )


# ==========================================================
# TRENDS
# ==========================================================

elif page == "📈 Trends":

    st.title("📈 Complaint Trends")

    st.info(
        "Trend forecasting API will be connected here."
    )

    periods = st.slider(
        "Forecast Periods",
        min_value=1,
        max_value=24,
        value=12
    )

    if st.button(
        "Generate Forecast"
    ):

        try:

            response = requests.get(
                f"{BACKEND_URL}/trend-forecast",
                params={
                    "periods": periods
                },
                timeout=120
            )

            if response.status_code == 200:

                result = response.json()

                if "error" in result:

                    st.error(
                        result["error"]
                    )

                else:

                    st.success(
                        "Forecast generated successfully."
                    )

                    st.json(result)

            else:

                st.error(
                    f"Backend error: {response.status_code}"
                )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )


# ==========================================================
# ANOMALIES
# ==========================================================

elif page == "⚠️ Anomalies":

    st.title("⚠️ Anomaly Detection")

    st.write(
        "Enter complaint statistics to detect unusual activity."
    )

    actual = st.number_input(
        "Actual Complaints",
        min_value=0.0,
        value=100.0
    )

    lag1 = st.number_input(
        "Previous Period Complaints",
        min_value=0.0,
        value=90.0
    )

    lag2 = st.number_input(
        "Two Periods Ago",
        min_value=0.0,
        value=85.0
    )

    lag3 = st.number_input(
        "Three Periods Ago",
        min_value=0.0,
        value=80.0
    )

    rolling_mean = st.number_input(
        "Rolling Mean",
        min_value=0.0,
        value=85.0
    )

    rolling_std = st.number_input(
        "Rolling Standard Deviation",
        min_value=0.0,
        value=10.0
    )

    pct_change = st.number_input(
        "Percentage Change",
        value=15.0
    )

    if st.button(
        "Detect Anomaly"
    ):

        try:

            response = requests.get(

                f"{BACKEND_URL}/anomaly",

                params={

                    "actual_complaints": actual,

                    "lag_1": lag1,

                    "lag_2": lag2,

                    "lag_3": lag3,

                    "rolling_mean_3": rolling_mean,

                    "rolling_std_3": rolling_std,

                    "pct_change": pct_change

                },

                timeout=120

            )

            if response.status_code == 200:

                result = response.json()

                if "error" in result:

                    st.error(
                        result["error"]
                    )

                else:

                    st.success(
                        "Anomaly analysis completed."
                    )

                    st.json(result)

            else:

                st.error(
                    f"Backend error: {response.status_code}"
                )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )


# ==========================================================
# GOVERNMENT SCHEMES
# ==========================================================

elif page == "📋 Government Schemes":

    st.title("📋 Government Schemes")

    st.write(
        """
        Government schemes used by the recommendation engine
        will be displayed here.
        """
    )

    st.info(
        "Supabase government_schemes_lookup connection will be added next."
    )