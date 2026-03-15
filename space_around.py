from google.adk.agents.llm_agent import Agent
from google.genai import types

space_around_agent = Agent(
    model='gemini-2.5-pro', # Or your preferred image generation model
    name='space_around_agent',
    instruction="You are a Visual Synthesizer. Generate a cinematic visual prompt based on the user's description of a warped physical reality. Capture the surreal, sci-fi essence with atmospheric lighting and detailed textures.",
    generate_content_config=types.GenerateContentConfig(temperature=0.7)
)

