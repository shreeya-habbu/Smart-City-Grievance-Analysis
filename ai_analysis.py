import re


# ============================================================
# SMART CITY AI GRIEVANCE ANALYSIS
# ============================================================

CATEGORIES = {

    "Roads & Transport": [
        "road", "pothole", "traffic", "signal", "street",
        "footpath", "sidewalk", "bus", "parking",
        "vehicle", "bridge", "transport"
    ],

    "Water & Sanitation": [
        "water", "water supply", "leakage", "pipeline",
        "sewage", "drainage", "drain", "toilet",
        "sewer", "contamination", "dirty water",
        "water shortage"
    ],

    "Electricity & Lighting": [
        "electricity", "power", "electric", "light",
        "streetlight", "lamp", "transformer",
        "wire", "current", "blackout"
    ],

    "Public Safety": [
        "crime", "unsafe", "danger", "accident",
        "fire", "police", "emergency", "theft",
        "harassment", "open manhole"
    ],

    "Environment": [
        "garbage", "waste", "trash", "litter",
        "dumping", "dustbin", "garbage collection",
        "waste disposal", "solid waste", "overflowing bin",
        "pollution", "smoke", "air pollution",
        "noise pollution", "noise", "tree", "trees",
        "environment", "plastic", "dust"
    ],

    "Public Services": [
        "hospital", "health", "school", "park",
        "public service", "municipality",
        "government", "service"
    ]
}


# ============================================================
# PRIORITY KEYWORDS
# ============================================================

CRITICAL_KEYWORDS = [
    "emergency",
    "fire",
    "life threatening",
    "life-threatening",
    "accident",
    "major accident",
    "gas leak",
    "electrical fire"
]

HIGH_KEYWORDS = [
    "danger",
    "dangerous",
    "unsafe",
    "severe",
    "urgent",
    "flood",
    "major leakage",
    "broken electric wire",
    "open manhole"
]

MEDIUM_KEYWORDS = [
    "leak",
    "pothole",
    "garbage",
    "waste",
    "street light",
    "drain",
    "noise",
    "pollution"
]


# ============================================================
# TEXT PREPROCESSING
# ============================================================

def clean_text(text):

    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s-]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# CATEGORY CLASSIFICATION
# ============================================================

def classify_category(text):

    text = clean_text(text)

    # --------------------------------------------------------
    # Strong Environment / Waste indicators
    # --------------------------------------------------------

    environment_priority_terms = [
        "garbage",
        "waste",
        "trash",
        "litter",
        "dumping",
        "dustbin",
        "garbage collection",
        "waste disposal",
        "solid waste",
        "overflowing bin"
    ]

    for keyword in environment_priority_terms:

        if keyword in text:
            return "Environment"

    # --------------------------------------------------------
    # Strong Water indicators
    # --------------------------------------------------------

    water_priority_terms = [
        "water supply",
        "water shortage",
        "dirty water",
        "water contamination",
        "pipeline leakage",
        "sewage",
        "sewer",
        "drainage"
    ]

    for keyword in water_priority_terms:

        if keyword in text:
            return "Water & Sanitation"

    # --------------------------------------------------------
    # Normal category scoring
    # --------------------------------------------------------

    scores = {}

    for category, keywords in CATEGORIES.items():

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += 1

        scores[category] = score

    best_category = max(
        scores,
        key=scores.get
    )

    if scores[best_category] == 0:
        return "Other"

    return best_category


# ============================================================
# PRIORITY DETECTION
# ============================================================

def detect_priority(text):

    text = clean_text(text)

    for keyword in CRITICAL_KEYWORDS:

        if keyword in text:
            return "Critical"

    for keyword in HIGH_KEYWORDS:

        if keyword in text:
            return "High"

    for keyword in MEDIUM_KEYWORDS:

        if keyword in text:
            return "Medium"

    return "Low"


# ============================================================
# SEVERITY ANALYSIS
# ============================================================

def detect_severity(text):

    text = clean_text(text)

    critical_count = sum(
        1
        for keyword in CRITICAL_KEYWORDS
        if keyword in text
    )

    high_count = sum(
        1
        for keyword in HIGH_KEYWORDS
        if keyword in text
    )

    if critical_count >= 1:
        return "Critical"

    if high_count >= 1:
        return "High"

    if len(text.split()) > 20:
        return "Medium"

    return "Low"


# ============================================================
# AI SUMMARY
# ============================================================

def generate_summary(
    title,
    description,
    category,
    priority
):

    if priority == "Critical":

        action = (
            "Immediate attention is recommended."
        )

    elif priority == "High":

        action = (
            "The grievance should be reviewed on priority."
        )

    elif priority == "Medium":

        action = (
            "The grievance should be reviewed "
            "through the normal service workflow."
        )

    else:

        action = (
            "The grievance can be handled "
            "through the regular service process."
        )

    return (
        f"The grievance concerns {category.lower()}. "
        f"AI analysis assigned a {priority.lower()} priority. "
        f"{action}"
    )


# ============================================================
# AI REASON
# ============================================================

def generate_reason(
    text,
    category,
    priority,
    severity
):

    reasons = []

    reasons.append(
        f"Relevant civic category detected: {category}."
    )

    reasons.append(
        f"Priority level identified as {priority}."
    )

    reasons.append(
        f"Severity level estimated as {severity}."
    )

    return " ".join(reasons)


# ============================================================
# COMPLETE AI ANALYSIS
# ============================================================

def analyze_grievance(
    title,
    description
):

    combined_text = (
        f"{title} {description}"
    )

    category = classify_category(
        combined_text
    )

    priority = detect_priority(
        combined_text
    )

    severity = detect_severity(
        combined_text
    )

    summary = generate_summary(
        title,
        description,
        category,
        priority
    )

    reason = generate_reason(
        combined_text,
        category,
        priority,
        severity
    )

    return {
        "category": category,
        "priority": priority,
        "severity": severity,
        "summary": summary,
        "reason": reason
    }


# ============================================================
# TEST AI ENGINE
# ============================================================

if __name__ == "__main__":

    test_cases = [

        (
            "Garbage piling up",
            "Garbage and waste have been accumulating "
            "near a residential area."
        ),

        (
            "Water leakage",
            "A water pipeline is leaking continuously."
        ),

        (
            "Road pothole",
            "A large pothole is present on the main road."
        )
    ]

    print("\nAI GRIEVANCE ANALYSIS")
    print("-" * 40)

    for title, description in test_cases:

        result = analyze_grievance(
            title,
            description
        )

        print("\nComplaint:", title)
        print("Category:", result["category"])
        print("Priority:", result["priority"])
        print("Severity:", result["severity"])