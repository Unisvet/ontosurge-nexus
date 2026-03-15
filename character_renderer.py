from google.adk.agents.llm_agent import Agent
from google.genai import types

character_agent = Agent(
    model='gemini-2.5-pro',
    name='character_renderer',
    instruction="You are the Character Subconscious. Given the Impact Analysis and NAI dissonance score, describe the Target Entity's internal monologue and physical reaction. Return creative narrative text.",
    generate_content_config=types.GenerateContentConfig(temperature=0.9)
)
