from google import genai
import json
import os
from dotenv import load_dotenv

load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def askAi(prompt):
    prmpt = f"""
You are a senior career consultant with deep experience guiding students and professionals in India.

Your job is to generate a structured career roadmap based on the user's query.

Return the response strictly as a valid JSON object that follows the schema below.
Do not include explanations, markdown, comments, or extra text.

JSON SCHEMA (MUST MATCH EXACTLY):

{{
  "greetings": "short friendly greeting",
  "roadmapTitle": "short and catchy roadmap title",
  "roadmapDesc": "2–3 line overview of the roadmap",
  "roadmapSteps": [
    {{
      "stepTitle": "short step title",
      "stepDesc": "clear and practical explanation",
      "stepEstimatedTime": "number of days"
    }}
  ],
  "resources": {{
    "books": [
      {{
        "bookTitle": "book title",
        "bookAuthor": "real author name",
        "bookDesc": "short practical description"
      }}
    ],
    "videos": [
      "valid YouTube URL",
      "valid YouTube URL"
    ]
  }},
  "lastWords": "short motivating closing line"
}}

Constraints:
- Output must be valid JSON.
- All fields must be present and non-empty.
- Estimated time must be in days only.
- Authors and YouTube links must be real.
- Tone should be simple, motivating, and friendly with subtle Indian context.

User Query:
{prompt}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config={
            "response_mime_type": "application/json"
        },
        contents=prmpt
    )

    try:
      return json.loads(response.text)
    except json.JSONDecodeError:
        print("RAW OUTPUT:", response.text)
        raise ValueError("AI returned invalid JSON")
