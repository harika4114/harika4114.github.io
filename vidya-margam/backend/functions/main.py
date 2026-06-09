import functions_framework
import os
import json
from google.cloud import translate_v2
from google.cloud import discoveryengine_v1
import google.generativeai as genai
from typing import Dict, List

# Initialize clients
translate_client = translate_v2.Client()
discovery_client = discoveryengine_v1.SearchServiceClient()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Configuration
PROJECT_ID = os.getenv("PROJECT_ID")
DATASTORE_ID = os.getenv("DATASTORE_ID")
LOCATION = os.getenv("REGION", "us-central1")


def translate_text(text: str, target_language: str = "en") -> str:
    """Translate text using Google Translate API."""
    try:
        result = translate_client.translate_text(
            text, target_language=target_language
        )
        return result["translatedText"]
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def search_documents(query: str) -> List[str]:
    """Search for relevant documents using Vertex AI Search."""
    try:
        search_request = discoveryengine_v1.SearchRequest(
            serving_config=f"projects/{PROJECT_ID}/locations/{LOCATION}/dataStores/{DATASTORE_ID}/servingConfigs/default_search:search",
            query=query,
            page_size=5,
        )
        response = discovery_client.search(search_request)

        sources = []
        for result in response.results:
            if hasattr(result.document, "title"):
                sources.append(result.document.title)
        return sources
    except Exception as e:
        print(f"Search error: {e}")
        return []


def generate_answer(question: str, sources: List[str]) -> str:
    """Generate answer using Gemini with Search grounding."""
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")

        # Build context from sources
        context = "\n".join([f"- {source}" for source in sources])
        prompt = f"""Based on the following educational materials:
{context}

Please answer this question in a clear, educational manner:
{question}

Provide a comprehensive answer that cites the source materials when relevant."""

        response = model.generate_content(prompt, stream=False)
        return response.text
    except Exception as e:
        print(f"Generation error: {e}")
        return "Unable to generate response. Please try again."


@functions_framework.http
def handle_request(request):
    """HTTP Cloud Function to handle Vidya Margam requests."""
    # Handle CORS
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
        return ("", 204, headers)

    try:
        # Parse request
        request_json = request.get_json()
        question = request_json.get("question", "")
        user_language = request_json.get("language", "te")
        user_id = request_json.get("userId", "anonymous")

        if not question:
            return {"error": "No question provided"}, 400

        # Step 1: Translate question to English for processing
        english_question = (
            translate_text(question, "en") if user_language != "en" else question
        )

        # Step 2: Search for relevant documents
        sources = search_documents(english_question)

        # Step 3: Generate answer using Gemini
        english_answer = generate_answer(english_question, sources)

        # Step 4: Translate answer back to user's language
        response_text = (
            translate_text(english_answer, user_language)
            if user_language != "en"
            else english_answer
        )

        # Build response
        response = {
            "answer": response_text,
            "sources": sources,
            "language": user_language,
            "userId": user_id,
        }

        # Add CORS headers
        headers = {"Access-Control-Allow-Origin": "*"}

        return (response, 200, headers)

    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}, 500
