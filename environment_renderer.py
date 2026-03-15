from google.adk.agents.llm_agent import Agent
from google.genai import types

environment_agent = Agent(
    model='gemini-2.5-pro',
    name='environment_renderer',
    instruction="You are the Environment Renderer. Based on the target entity and Impact Analysis, vividly describe the physical surroundings and space around them after a Reality Inversion. Do not describe the character's thoughts, only the environment. Return creative narrative text.",
    generate_content_config=types.GenerateContentConfig(temperature=0.9)
)
