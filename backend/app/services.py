import os
import json
from openai import AsyncOpenAI
from .schemas import BrandAnalysisResponse
from dotenv import load_dotenv

load_dotenv()

# Point the client to your local Ollama server
client = AsyncOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("Groq_key")  #
)

SYSTEM_PROMPT_ANALYZE = """
You are an expert Brand Strategist and Analyst. Your job is to analyze provided text and distill it into a clear, structured Brand Voice profile. Analyze the user-provided text. Based ONLY on this text, you must identify the following attributes and return them in a JSON object with the exact keys: "BrandArchetype", "ToneAndVoice", "CoreValues", "TargetAudience", "Keywords".
- ToneAndVoice should be a list of 3-5 adjectives.
- CoreValues should be a list of 3-4 brand values.
- Keywords should be a list of 5-10 central nouns and verbs.
Your entire response must be ONLY the raw JSON object, starting with { and ending with }. Do not include any other text, explanations, or markdown formatting.
"""

GUIDE_GENERATOR_PROMPT = """
You are a Senior Copywriter and Brand Manager. Your task is to create a detailed Brand Voice & Tone Guide based on a strategic analysis. You will be given a JSON object containing a brand analysis. Your task is to generate a comprehensive, human-readable guide in Markdown format. The guide must be clear, actionable, and ready to be shared with a marketing team.

The guide must include these sections:

### Brand Personality
- **Our Archetype**: Explain the brand's archetype and what it means for the brand's communication style.
- **Our Voice Is...**: List the Tone & Voice adjectives.
- **Our Voice Is Not...**: List the opposite of the Tone & Voice adjectives.

### Core Messaging
- **Our Values**: List and briefly explain the core values.
- **Key Terms**: List the keywords that are central to our messaging.

### Writing Style Guide
- **Do**: Provide 3-4 practical writing tips based on the analysis. (e.g., 'Use active voice', 'Keep sentences short', 'Address the reader directly as "you"').
- **Don't**: Provide 3-4 things to avoid in writing. (e.g., 'Avoid corporate jargon', 'Don't be overly formal or robotic').
- **Example Snippet**: Write a 2-3 sentence example of copy that perfectly embodies this brand voice.

Respond with ONLY the raw Markdown text.
"""

CONTENT_GENERATOR_PROMPT = """
You are an AI Copywriter that is an expert in embodying a specific brand voice. You MUST strictly and exclusively adhere to the provided Brand Voice Guide. Do not deviate from it. Your task is to fulfill the user's request, ensuring every word you write aligns perfectly with the rules and personality defined in the guide.

You will be given the complete guide within the `<brand_guide>` tags and a user's request within the `<request>` tags.

Generate only the requested content. Do not add any conversational text, introductions, or explanations.
"""

async def analyze_brand(text: str) -> BrandAnalysisResponse:
    """ Analyzes the provided text using a local AI model to extract brand identity. """
    try:
        response = await client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_ANALYZE},
                {"role": "user", "content": f"Here is the brand text: {text}"}
            ],
            temperature=0.0,
            stop=None 
        )
        response_content = response.choices[0].message.content.strip()
        
        json_string = None
        json_start = response_content.find('{')
        
        if json_start != -1:
            json_end = response_content.rfind('}')
            if json_end == -1 or json_end < json_start:
                json_string = response_content[json_start:] + "}"
            else:
                json_string = response_content[json_start : json_end + 1]

        if json_string:
            try:
                analysis_json = json.loads(json_string)
                return BrandAnalysisResponse(**analysis_json)
            except json.JSONDecodeError:
                raise ValueError("Extracted text is not a valid JSON object.")
        else:
            raise ValueError("No valid JSON object found in the model's response.")
    except Exception as e:
        raise

async def generate_guide(analysis_data: dict) -> str:
    """ Generates a brand guide in Markdown format based on the analysis data. """
    try:
        response = await client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": GUIDE_GENERATOR_PROMPT},
                {"role": "user", "content": f"Here is the brand analysis JSON: {json.dumps(analysis_data)}"}
            ],
            temperature=0.5
        )
        guide_markdown = response.choices[0].message.content
        return guide_markdown.strip()
    except Exception as e:
        raise

async def generate_content(guide: str, request: str) -> str:
    """ Generates on-brand content based on a guide and a user request. """
    try:
        response = await client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": CONTENT_GENERATOR_PROMPT},
                {"role": "user", "content": f"<brand_guide>\n{guide}\n</brand_guide>\n\n<request>\n{request}\n</request>"}
            ],
            temperature=0.7 # Higher temperature for creative writing
        )
        content = response.choices[0].message.content
        return content.strip()
    except Exception as e:
        raise
