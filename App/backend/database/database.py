from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY


# ==========================================================
# SUPABASE CONNECTION
# ==========================================================

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


print("Supabase connected successfully!")


# ==========================================================
# SAVE PREDICTION
# ==========================================================

def save_prediction(
    source,
    text_content,
    location,
    department_input,
    sentiment,
    sentiment_confidence,
    feedback_category,
    feedback_confidence,
    complaint_reason,
    complaint_confidence,
    predicted_department,
    department_confidence,
    priority,
    priority_confidence,
    emergency_detected,
    emergency_confidence,
    harmful_content_detected,
    harmful_content_confidence,
    recommended_action
):

    data = {

        "source": source,

        "text_content": text_content,

        "location": location,

        "department_input": department_input,

        # Module 1
        "sentiment": sentiment,

        "sentiment_confidence": sentiment_confidence,

        # Module 2
        "feedback_category": feedback_category,

        "feedback_confidence": feedback_confidence,

        # Module 3
        "complaint_reason": complaint_reason,

        "complaint_confidence": complaint_confidence,

        # Module 4
        "predicted_department": predicted_department,

        "department_confidence": department_confidence,

        # Module 5
        "priority": priority,

        "priority_confidence": priority_confidence,

        # Module 6
        "emergency_detected": emergency_detected,

        "emergency_confidence": emergency_confidence,

        # Module 7
        "harmful_content_detected": harmful_content_detected,

        "harmful_content_confidence": harmful_content_confidence,
        
        "recommended_action": recommended_action
    }

    response = (
        supabase
        .table("government_predictions")
        .insert(data)
        .execute()
    )

    return response
# ==========================================================
# MODULE 10: GOVERNMENT ACTION RECOMMENDATION
# ==========================================================

def get_recommended_action(
    complaint_reason,
    department,
    priority,
    complaint_text
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
                "recommended_action": (
                    "No government scheme is available."
                ),
                "description": None
            }

        # --------------------------------------------------
        # Build search text
        # --------------------------------------------------

        search_text = (
            f"{complaint_text} "
            f"{complaint_reason}"
        ).lower()

        # --------------------------------------------------
        # Remove common words
        # --------------------------------------------------

        stop_words = {
            "there",
            "this",
            "that",
            "with",
            "from",
            "have",
            "has",
            "been",
            "they",
            "them",
            "causing",
            "people",
            "road",
            "large",
            "very",
            "and",
            "the",
            "are",
            "for",
            "into",
            "which",
            "about",
            "under",
            "over"
        }

        words = [
            word.strip(".,!?;:()[]{}")
            for word in search_text.split()
        ]

        keywords = {
            word
            for word in words
            if len(word) >= 5
            and word not in stop_words
        }

        # --------------------------------------------------
        # Strong complaint-specific keywords
        # --------------------------------------------------

        complaint_keywords = {
            "pothole",
            "potholes",
            "road",
            "roads",
            "footpath",
            "footpaths",
            "infrastructure",
            "accident",
            "accidents"
        }

        relevant_keywords = (
            keywords.intersection(
                complaint_keywords
            )
        )

        best_scheme = None
        best_score = 0

        # --------------------------------------------------
        # Search schemes
        # --------------------------------------------------

        for scheme in schemes:

            scheme_text = " ".join([
                str(scheme.get("scheme_name") or ""),
                str(scheme.get("details") or ""),
                str(scheme.get("benefits") or ""),
                str(scheme.get("scheme_category") or ""),
                str(scheme.get("tags") or "")
            ]).lower()

            score = 0

            # Strong matching
            for keyword in relevant_keywords:

                if keyword in scheme_text:

                    score += 5

            # Complaint reason phrase matching
            reason_words = [
                word.strip(".,!?;:()[]{}").lower()
                for word in complaint_reason.split()
                if len(word) >= 5
                and word not in stop_words
            ]

            for word in reason_words:

                if word in scheme_text:

                    score += 2

            if score > best_score:

                best_score = score
                best_scheme = scheme

        # --------------------------------------------------
        # Minimum relevance threshold
        # --------------------------------------------------

        if best_scheme is None or best_score < 5:

            return {
                "scheme_name": None,

                "recommended_action": (
                "Refer the complaint to the responsible "
                "Urban Local Body for road inspection and repair. "
                "AMRUT may be reviewed where the issue falls "
                "within its eligible urban infrastructure components."
                ),

                "description": (
                    "No sufficiently relevant government "
                    "scheme was found in the scheme database."
                )
            }

        # --------------------------------------------------
        # Return relevant scheme
        # --------------------------------------------------

        return {

            "scheme_name": best_scheme.get(
                "scheme_name"
            ),

            "recommended_action": (
                "Review and consider the relevant "
                "government scheme."
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
                "Unable to retrieve government "
                "action recommendation."
            ),

            "description": None
        }