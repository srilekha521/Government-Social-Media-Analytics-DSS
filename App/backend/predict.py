from pathlib import Path
import joblib


# ==========================================================
# MODEL PATH
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
PICKLES_DIR = BASE_DIR.parent / "Pickles"


# ==========================================================
# HELPER FUNCTION
# ==========================================================

def load_pickle(filename):
    path = PICKLES_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Model file not found: {path}"
        )

    return joblib.load(path)


# ==========================================================
# LOAD SENTIMENT MODEL
# ==========================================================

sentiment_model = load_pickle(
    "01_sentiment_model.pkl"
)


# ==========================================================
# LOAD FEEDBACK CATEGORY ARTIFACTS
# ==========================================================

feedback_category_model = load_pickle(
    "feedback_category_model.pkl"
)

feedback_label_encoder = load_pickle(
    "feedback_label_encoder.pkl"
)

feedback_tfidf_vectorizer = load_pickle(
    "feedback_tfidf_vectorizer.pkl"
)


# ==========================================================
# LOAD COMPLAINT REASON ARTIFACTS
# ==========================================================

complaint_reason_model = load_pickle(
    "complaint_reason_model.pkl"
)

complaint_tfidf_vectorizer = load_pickle(
    "complaint_tfidf_vectorizer.pkl"
)


# ==========================================================
# LOAD DEPARTMENT ARTIFACTS
# ==========================================================
# ==========================================================
# MODULE 4: DEPARTMENT MODEL
# ==========================================================

department_model = load_pickle(
    "department_model1.pkl"
)

department_labels = load_pickle(
    "department_labels.pkl"
)

# ==========================================================
# LOAD EMERGENCY MODEL
# ==========================================================

emergency_model = load_pickle(
    "emergency_model.pkl"
)

emergency_vectorizer = load_pickle(
    "emergency_vectorizer.pkl"
)


# ==========================================================
# LOAD HARMFUL CONTENT ARTIFACTS
# ==========================================================

harmful_content_model = load_pickle(
    "harmful_content_model.pkl"
)

harmful_label_encoder = load_pickle(
    "harmful_label_encoder.pkl"
)


# ==========================================================
# LOAD ANOMALY DETECTION ARTIFACTS
# ==========================================================

anomaly_isolation_forest_model = load_pickle(
    "anomaly_isolation_forest_model.pkl"
)


# ==========================================================
# LOAD TREND FORECASTING MODEL
# ==========================================================

trend_ets_model = load_pickle(
    "trend_ets_model.pkl"
)


print("All available models loaded successfully!")
# ==========================================================
# MODULE 1: SENTIMENT PREDICTION
# ==========================================================

def predict_sentiment(text):

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    prediction = sentiment_model.predict([text])

    confidence = None

    if hasattr(sentiment_model, "predict_proba"):
        probabilities = sentiment_model.predict_proba([text])[0]
        confidence = float(max(probabilities))

    return {
        "sentiment": str(prediction[0]),
        "confidence": confidence
    }

# ==========================================================
# MODULE 2: FEEDBACK CATEGORY PREDICTION
# ==========================================================

def predict_feedback_category(text):

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    # Convert text into TF-IDF features
    text_vector = feedback_tfidf_vectorizer.transform([text])

    # Predict encoded category
    prediction = feedback_category_model.predict(text_vector)

    # Convert encoded value back to category name
    category = feedback_label_encoder.inverse_transform(prediction)[0]

    # Get confidence
    confidence = None

    if hasattr(feedback_category_model, "predict_proba"):
        probabilities = feedback_category_model.predict_proba(text_vector)[0]
        confidence = float(max(probabilities))

    return {
        "feedback_category": str(category),
        "confidence": confidence
    }
# ==========================================================
# MODULE 3: COMPLAINT REASON PREDICTION
# ==========================================================

def predict_complaint_reason(text):

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    # Convert text into TF-IDF features
    text_vector = complaint_tfidf_vectorizer.transform([text])

    # Predict complaint reason
    prediction = complaint_reason_model.predict(text_vector)

    return {
        "complaint_reason": str(prediction[0])
    }

    
# ==========================================================
# MODULE 4: DEPARTMENT MODEL
# ==========================================================

department_model = load_pickle(
    "department_model1.pkl"
)

department_labels = load_pickle(
    "department_labels.pkl"
)


# ==========================================================
# MODULE 4: DEPARTMENT PREDICTION
# ==========================================================

def predict_department(text):

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    prediction = department_model.predict(
        [text]
    )[0]

    # ------------------------------------------------------
    # The new model directly returns the department name
    # Example: "Municipal Corporation"
    # ------------------------------------------------------

    department = str(prediction)

    return {
        "department": department,
        "confidence": None
    }
    
# ==========================================================
# MODULE 5: LOAD PRIORITY MODEL
# ==========================================================

priority_model = load_pickle(
    "DepartmentPriorityModel.pkl"
)
def predict_priority(
    interaction_summary,
    channel,
    department,
    scheme_name,
    state,
    language,
    sentiment_label,
    weekday,
    sentiment_score,
    resolution_time_hrs,
    reopen_count,
    escalated,
    satisfaction_rating,
    cost_to_resolve_inr,
    complexity_index,
    year,
    month,
    day,
    hour,
    summary_length
):

    import pandas as pd

    input_data = {
        "interaction_summary": [interaction_summary],
        "channel": [channel],
        "department": [department],
        "scheme_name": [scheme_name],
        "state": [state],
        "language": [language],
        "sentiment_label": [sentiment_label],
        "Weekday": [weekday],
        "sentiment_score": [sentiment_score],
        "resolution_time_hrs": [resolution_time_hrs],
        "reopen_count": [reopen_count],
        "escalated": [escalated],
        "satisfaction_rating": [satisfaction_rating],
        "cost_to_resolve_inr": [cost_to_resolve_inr],
        "complexity_index": [complexity_index],
        "Year": [year],
        "Month": [month],
        "Day": [day],
        "Hour": [hour],
        "Summary_Length": [summary_length]
    }

    input_df = pd.DataFrame(input_data)

    prediction = priority_model.predict(input_df)[0]

    # Convert numeric priority to categorical label
    priority_mapping = {
        0: "Low",
        1: "High",
        2: "Medium"
    }

    priority = priority_mapping.get(
        int(prediction),
        str(prediction)
    )

    return {
        "priority": priority
    }
# ==========================================================
# LOAD EMERGENCY MODEL
# ==========================================================

emergency_model = load_pickle(
    "emergency_model.pkl"
)

emergency_vectorizer = load_pickle(
    "emergency_vectorizer.pkl"
)
# ==========================================================
# MODULE 6: EMERGENCY DETECTION
# ==========================================================

def predict_emergency(text):

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    text_vector = emergency_vectorizer.transform([text])

    prediction = emergency_model.predict(text_vector)[0]

    emergency = "Yes" if prediction == 1 else "No"

    return {
        "emergency": emergency
    }
# ==========================================================
# MODULE 7: HARMFUL CONTENT DETECTION
# ==========================================================

def predict_harmful_content(text):

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    prediction = harmful_content_model.predict([text])

    # Convert encoded label to original category
    harmful_content = harmful_label_encoder.inverse_transform(
        prediction
    )[0]

    return {
        "harmful_content": str(harmful_content)
    }

# ==========================================================
# LOAD MODULE 8: TREND FORECASTING MODEL
# ==========================================================

trend_ets_model = load_pickle(
    "trend_ets_model.pkl"
)
# ==========================================================
# MODULE 8: TREND FORECASTING
# ==========================================================

def predict_trend_forecast(periods=12):

    if periods <= 0:
        raise ValueError("Periods must be greater than zero.")

    # Generate future forecast
    forecast = trend_ets_model.forecast(periods)

    # Prevent negative complaint counts
    forecast = forecast.clip(lower=0)

    return {
        "forecast": [
            round(float(value), 2)
            for value in forecast
        ]
    }
# ==========================================================
# MODULE 9: ANOMALY DETECTION
# ==========================================================

def predict_anomaly(
    actual_complaints,
    lag_1,
    lag_2,
    lag_3,
    rolling_mean_3,
    rolling_std_3,
    pct_change
):

    # Create input using the EXACT feature order
    # used during model training.

    input_data = [[
        actual_complaints,
        lag_1,
        lag_2,
        lag_3,
        rolling_mean_3,
        rolling_std_3,
        pct_change
    ]]

    # Predict anomaly
    prediction = anomaly_isolation_forest_model.predict(
        input_data
    )[0]

    # Isolation Forest:
    #  1  = Normal
    # -1  = Anomaly

    if prediction == -1:
        anomaly = "Anomaly"
    else:
        anomaly = "Normal"

    return {
        "anomaly": anomaly
    }
# ==========================================================
# MODULE 10: GOVERNMENT ACTION RECOMMENDATION
# ==========================================================

def get_recommended_action(
    complaint_reason,
    department,
    priority
):

    try:

        response = (
            supabase
            .table("government_schemes_lookup")
            .select(
                "scheme_name, details, benefits, eligibility, "
                "application, documents, level, scheme_category, tags"
            )
            .execute()
        )

        schemes = response.data or []

        if not schemes:

            return {
                "scheme_name": None,
                "recommended_action": "No government scheme found.",
                "description": None
            }

        search_text = (
            f"{complaint_reason} "
            f"{department} "
            f"{priority}"
        ).lower()

        best_scheme = None
        best_score = 0

        for scheme in schemes:

            scheme_text = " ".join([
                str(scheme.get("scheme_name") or ""),
                str(scheme.get("details") or ""),
                str(scheme.get("benefits") or ""),
                str(scheme.get("scheme_category") or ""),
                str(scheme.get("tags") or "")
            ]).lower()

            keywords = [
                word
                for word in search_text.split()
                if len(word) > 3
            ]

            score = sum(
                1
                for keyword in keywords
                if keyword in scheme_text
            )

            if score > best_score:

                best_score = score
                best_scheme = scheme

        if best_scheme is None or best_score == 0:

            return {
                "scheme_name": None,
                "recommended_action": (
                    "No closely matching government scheme found."
                ),
                "description": None
            }

        return {
            "scheme_name": best_scheme.get(
                "scheme_name"
            ),

            "recommended_action": (
                "Review and consider the relevant government scheme."
            ),

            "description": best_scheme.get(
                "details"
            ),

            "benefits": best_scheme.get(
                "benefits"
            ),

            "eligibility": best_scheme.get(
                "eligibility"
            ),

            "application": best_scheme.get(
                "application"
            ),

            "source_level": best_scheme.get(
                "level"
            ),

            "scheme_category": best_scheme.get(
                "scheme_category"
            )
        }

    except Exception as e:

        print(
            "Module 10 error:",
            str(e)
        )

        return {
            "scheme_name": None,
            "recommended_action": (
                "Unable to retrieve government scheme."
            ),
            "description": None
        }