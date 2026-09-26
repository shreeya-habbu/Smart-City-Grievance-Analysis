import os

from google import genai

from rag.rag_engine import build_rag_context


API_KEY = os.getenv("Smart_city_API_Key")
MODEL_NAME = "gemini-3.6-flash"

client = None

if API_KEY:
    client = genai.Client(
        api_key=API_KEY
    )


def is_configured():
    return client is not None


def analyze_with_gemini(grievance_text):

    if not is_configured():
        return None

    # --------------------------------------------------------
    # RAG RETRIEVAL
    # --------------------------------------------------------

    rag_context = build_rag_context(
        grievance_text,
        top_k=3
    )

    # --------------------------------------------------------
    # GEMINI PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are an AI assistant for a Smart City Grievance Analysis System.

Analyze the citizen grievance using the retrieved civic
knowledge provided below.

IMPORTANT:
- Use the retrieved information only as supporting context.
- The citizen's actual grievance text is the primary
  source for classification.
- Retrieved knowledge is supporting context only.
- Do not invent facts.
- Do not claim that retrieved information is an official
  decision or government order.
- The final classification is an AI-assisted recommendation
  and should be reviewed by an authorized human administrator.

Return a concise analysis containing:

1. Category
2. Priority
3. Severity
4. Summary
5. Reason

Use these categories:

- Roads & Transport
- Water & Sanitation
- Electricity & Lighting
- Public Safety
- Environment
- Public Services

IMPORTANT CATEGORY RULES:

- Garbage, waste, trash, litter, dumping, dustbins,
  garbage collection, solid waste and waste disposal
  MUST be classified as Environment.

- Water supply, water leakage, pipeline problems,
  sewage, sewer and drainage problems should be
  classified as Water & Sanitation.

- Road, pothole, traffic, footpath, parking and
  public transport problems should be classified as
  Roads & Transport.

Do not classify a garbage or waste complaint as
Water & Sanitation just because sanitation-related
information appears in the retrieved context.

Priority must be one of:

- Critical
- High
- Medium
- Low

Severity must be one of:

- Critical
- High
- Medium
- Low

------------------------------------------------------------
RETRIEVED CIVIC KNOWLEDGE
------------------------------------------------------------

{rag_context}

------------------------------------------------------------
CITIZEN GRIEVANCE
------------------------------------------------------------

{grievance_text}

------------------------------------------------------------

Keep the response concise and factual.
Do not invent information that is not present in the
grievance or retrieved context.
"""

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except Exception as error:

        print(
            "Gemini API error:",
            error
        )

        return None