from google.adk.agents.llm_agent import Agent
from google.genai import types

character_creator_agent = Agent(
    model='gemini-2.5-pro',
    name='character_creator',
    instruction="You are the Entity Forge. Generate a new character entity based on a short description. Return raw JSON: {\"name\": \"...\", \"background\": \"...\", \"baseline_causal_adherence\": 0.8, \"baseline_ethical_consistency\": 0.8}",
    generate_content_config=types.GenerateContentConfig(temperature=0.7)
)
