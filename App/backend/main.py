from fastapi import FastAPI
from datetime import datetime
import traceback

from database.schemas import SocialMediaInput

from database.database import (
    save_prediction,
    get_recommended_action
)

from predict import (
    predict_sentiment,
    predict_feedback_category,
    predict_complaint_reason,
    predict_department,
    predict_priority,
    predict_emergency,
    predict_harmful_content,
    predict_trend_forecast,
    predict_anomaly,
)


# ==========================================================
# FASTAPI APPLICATION
# ==========================================================

app = FastAPI(
    title="Government Social Media Analytics API",
    description="Government Social Media Analytics and Decision Support System",
    version="1.0"
)


# ==========================================================
# HOME API
# ==========================================================

@app.get("/")
def home():

    return {
        "message": "Government Social Media Analytics API is running"
    }


# ==========================================================
# PREDICTION API
# ==========================================================

@app.post("/predict")
def predict(data: SocialMediaInput):

    try:

        # ==================================================
        # INPUT
        # ==================================================

        text = data.post_text

        if not text or not text.strip():

            raise ValueError(
                "Post text cannot be empty."
            )


        # ==================================================
        # MODULE 1: SENTIMENT
        # ==================================================

        print("\n========== MODULE 1 ==========")

        sentiment_result = predict_sentiment(
            text
        )

        print(
            "Sentiment:",
            sentiment_result
        )

        sentiment = sentiment_result.get(
            "sentiment",
            "Unknown"
        )


        # ==================================================
        # MODULE 2: FEEDBACK CATEGORY
        # ==================================================

        print("\n========== MODULE 2 ==========")

        feedback_result = predict_feedback_category(
            text
        )

        print(
            "Feedback Category:",
            feedback_result
        )


        # ==================================================
        # MODULE 3: COMPLAINT REASON
        # ==================================================

        print("\n========== MODULE 3 ==========")

        complaint_result = predict_complaint_reason(
            text
        )

        print(
            "Complaint Reason:",
            complaint_result
        )

        complaint_reason = complaint_result.get(
            "complaint_reason",
            ""
        )


        # ==================================================
        # MODULE 4: DEPARTMENT
        # ==================================================

        print("\n========== MODULE 4 ==========")

        department_result = predict_department(
            text
        )

        print(
            "Department:",
            department_result
        )

        predicted_department = department_result.get(
            "department",
            ""
        )


        # ==================================================
        # MODULE 5: PRIORITY
        # ==================================================

        print("\n========== MODULE 5 ==========")

        now = datetime.now()

        sentiment_confidence = (
            sentiment_result.get(
                "confidence"
            ) or 0.0
        )

        priority_result = predict_priority(

            interaction_summary=text,

            channel=data.platform,

            department=predicted_department,

            scheme_name="",

            state=data.location or "",

            language="English",

            sentiment_label=sentiment,

            weekday=now.strftime("%A"),

            sentiment_score=float(
                sentiment_confidence
            ),

            resolution_time_hrs=0.0,

            reopen_count=0,

            escalated=0,

            satisfaction_rating=0.0,

            cost_to_resolve_inr=0.0,

            complexity_index=0.0,

            year=now.year,

            month=now.month,

            day=now.day,

            hour=now.hour,

            summary_length=len(text)
        )

        print(
            "Priority:",
            priority_result
        )

        priority = priority_result.get(
            "priority",
            "Medium"
        )


        # ==================================================
        # MODULE 6: EMERGENCY
        # ==================================================

        print("\n========== MODULE 6 ==========")

        emergency_result = predict_emergency(
            text
        )

        print(
            "Emergency:",
            emergency_result
        )


        # ==================================================
        # MODULE 7: HARMFUL CONTENT
        # ==================================================

        print("\n========== MODULE 7 ==========")

        harmful_result = predict_harmful_content(
            text
        )

        print(
            "Harmful Content:",
            harmful_result
        )


        # ==================================================
        # MODULE 10: GOVERNMENT ACTION
        # ==================================================

        print("\n========== MODULE 10 ==========")

        recommended_action = get_recommended_action(

            complaint_reason,

            predicted_department,

            priority,

            text

        )

        print(
            "Recommended Action:",
            recommended_action
        )


        # ==================================================
        # SAVE RESULT TO SUPABASE
        # ==================================================

        print(
            "\n========== SAVING TO SUPABASE =========="
        )
        print("About to save prediction...")
        
        save_prediction(

            source=data.platform,

            text_content=data.post_text,

            location=data.location,

            department_input=data.department,

            sentiment=sentiment_result.get(
                "sentiment"
            ),

            sentiment_confidence=sentiment_result.get(
                "confidence"
            ),

            feedback_category=feedback_result.get(
                "feedback_category"
            ),

            feedback_confidence=feedback_result.get(
                "confidence"
            ),

            complaint_reason=complaint_result.get(
                "complaint_reason"
            ),

            complaint_confidence=complaint_result.get(
                "confidence"
            ),

            predicted_department=department_result.get(
                "department"
            ),

            department_confidence=department_result.get(
                "confidence"
            ),

            priority=priority_result.get(
                "priority"
            ),

            priority_confidence=priority_result.get(
                "confidence"
            ),

            emergency_detected=(
                emergency_result.get(
                    "emergency"
                ) == "Yes"
            ),

            emergency_confidence=emergency_result.get(
                "confidence"
            ),

            harmful_content_detected=(
                harmful_result.get(
                    "harmful_content"
                ) != "NOT"
            ),

            harmful_content_confidence=harmful_result.get(
                "confidence"
            ),
            
            recommended_action=recommended_action

        )

        print(
            "Prediction saved to Supabase!"
        )


        # ==================================================
        # FINAL RESPONSE
        # ==================================================

        return {

            "platform": data.platform,

            "post_text": data.post_text,

            "location": data.location,

            "sentiment": sentiment_result,

            "feedback_category": feedback_result,

            "complaint_reason": complaint_result,

            "department": department_result,

            "priority": priority_result,

            "emergency": emergency_result,

            "harmful_content": harmful_result,

            "recommended_action": recommended_action

        }


    except Exception as e:

        traceback.print_exc()

        return {
            "error": str(e)
        }


# ==========================================================
# MODULE 8: TREND FORECAST API
# ==========================================================

@app.get("/trend-forecast")
def trend_forecast(
    periods: int = 12
):

    try:

        result = predict_trend_forecast(
            periods
        )

        return result

    except Exception as e:

        traceback.print_exc()

        return {
            "error": str(e)
        }


# ==========================================================
# MODULE 9: ANOMALY DETECTION API
# ==========================================================

@app.get("/anomaly")
def anomaly_detection(

    actual_complaints: float,

    lag_1: float,

    lag_2: float,

    lag_3: float,

    rolling_mean_3: float,

    rolling_std_3: float,

    pct_change: float

):

    try:

        result = predict_anomaly(

            actual_complaints,

            lag_1,

            lag_2,

            lag_3,

            rolling_mean_3,

            rolling_std_3,

            pct_change

        )

        return result

    except Exception as e:

        traceback.print_exc()

        return {
            "error": str(e)
        }