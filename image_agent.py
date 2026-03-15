import base64
from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool
from google.genai import types
from google import genai
from dotenv import load_dotenv

load_dotenv(override=True)

def generate_image(prompt: str) -> str:
    """Generates an image from a text prompt and returns the base64 encoded image string.
    
    Args:
        prompt: The descriptive text prompt for the image.
    """
    client = genai.Client()
    try:
        response = client.models.generate_content(
            model='gemini-3.1-flash-image-preview',
            contents=prompt,
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                b64 = base64.b64encode(part.inline_data.data).decode('utf-8')
                mime_type = part.inline_data.mime_type or "image/png"
                return f"data:{mime_type};base64,{b64}"
            
    except Exception as e:
        return f"Error generating image: {str(e)}"
    
    return "Error generating image: No image returned."

image_generation_tool = FunctionTool(func=generate_image)

image_agent = Agent(
    model='gemini-2.5-pro',
    name='image_creator_agent',
    instruction="""You are an AI assistant that generates images based on user descriptions.
    When a user asks for an image, you MUST use the `generate_image` tool to create it.
    Return ONLY the exact base64 image URL outputted by the tool.""",
    tools=[image_generation_tool],
    generate_content_config=types.GenerateContentConfig(temperature=0.7)
)
