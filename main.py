import os
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from google.adk.agents.llm_agent import Agent
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

from character_creator import character_creator_agent
from environment_renderer import environment_agent
from character_renderer import character_agent
from space_around import space_around_agent
from image_agent import generate_image

load_dotenv(override=True)

app = FastAPI(title="Ontosurge Nexus - Architect's Console API")

# Mount the static directory to serve the frontend UI
app.mount("/console", StaticFiles(directory="static", html=True), name="static")

# --- 1. ANTIGRAVITY SKILLS (Model Context Protocol / MSP Connectors) ---

def query_notebooklm_msp(query: str) -> str:
    """Queries the NotebookLM Mission Support Protocol (MSP) for DOS rules and baseline weights."""
    print(f"[Antigravity Skill] Querying Context for: {query}")
    return f"Data: Entity '{query}' baseline requires strict causal adherence (Weight: 1.0)."

def commit_github_msp_state(entity_id: str, new_state: str) -> str:
    """Commits a reality-altering state change to the GitHub MSP Server to update Role Agent logic."""
    print(f"[Antigravity Skill] Committing new reality state for {entity_id} to repository.")
    return f"Success: Committed ontological inversion for {entity_id}."

def modulate_ontological_dial(dial_name: str, new_weight: float) -> str:
    """Modulates the ontological weight of a specific narrative dial (0.0 to 1.0)."""
    print(f"[Antigravity Skill] Modulating {dial_name} to {new_weight}")
    return f"Success: {dial_name} shifted to {new_weight}."

# --- 2. AGENT INITIALIZATION & SCHEMA ENFORCEMENT ---

# Define the strict Schema requested in Part 1 to force the mathematical output
class SystemStateUpdate(BaseModel):
    target_entity: str = Field(description="The entity whose reality is being inverted.")
    dials_adjusted: list[str] = Field(description="List of strings describing the dial adjustments (e.g., 'causal_adherence: 0.2').")
    qnf_triggered: bool = Field(description="True if an ontological weight dropped below 0.3.")
    nai_dissonance_score: float = Field(description="Cognitive dissonance score for Subordinate agents (0.0-1.0)")
    impact_analysis: str = Field(description="Logical Meta-Physics calculation of the warped causality.")
    # reality_render removed because sub-agents handle this now

# Load the First Prompt (System Constitution from Part 1)
try:
    with open("instructions.md", "r") as f:
        SYSTEM_PROMPT = f.read()
except FileNotFoundError:
    SYSTEM_PROMPT = "You are the Ontosurge Core (the Nexus Weaver)..." # Fallback

# Initialize the ROOT ADK Agent (Nexus Weaver)
root_agent = Agent(
    model='gemini-2.5-pro',
    name='nexus_weaver',
    description="The main orchestrator.",
    instruction=SYSTEM_PROMPT,
    tools=[query_notebooklm_msp, commit_github_msp_state, modulate_ontological_dial],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.9 # Higher temp enables better "Quantum Narrative Fluctuations"
    ),
    sub_agents=[character_creator_agent, environment_agent, character_agent, space_around_agent]
)

session_service = InMemorySessionService()
runner_root = Runner(app_name="ontosurge_root", agent=root_agent, session_service=session_service, auto_create_session=True)

# Initialize the Subordinate Agents related Runners
runner_creator = Runner(app_name="ontosurge_creator", agent=character_creator_agent, session_service=session_service, auto_create_session=True)
runner_env = Runner(app_name="ontosurge_env", agent=environment_agent, session_service=session_service, auto_create_session=True)
runner_char = Runner(app_name="ontosurge_char", agent=character_agent, session_service=session_service, auto_create_session=True)
runner_space = Runner(app_name="ontosurge_space", agent=space_around_agent, session_service=session_service, auto_create_session=True)

# --- 3. FASTAPI ENDPOINTS ---

class ArchitectCommand(BaseModel):
    target_entity: str
    action: str
    dial_adjustments: dict # e.g., {"causal_adherence": 0.2, "ethical_flux": 0.9}

class CreateEntityRequest(BaseModel):
    description: str

class VisualizeRequest(BaseModel):
    environment_text: str

@app.post("/api/v1/generate_entity")
async def generate_entity(req: CreateEntityRequest):
    import uuid
    message = types.Content(role="user", parts=[types.Part.from_text(text=f"Generate a character matching: {req.description}")])
    agen = runner_creator.run_async(user_id="arch", session_id=str(uuid.uuid4()), new_message=message)
    full_resp = ""
    async for event in agen:
        if getattr(event, 'content', None) and getattr(event.content, 'parts', None):
            for part in event.content.parts:
                if getattr(part, 'text', None):
                    full_resp += part.text
    try:
        # Strip potential markdown formatting if model didn't listen
        clean_json = full_resp.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json[7:-3]
        return json.loads(clean_json)
    except Exception as e:
        return {"error": "Failed to parse generator output", "raw": full_resp}

@app.post("/api/v1/manipulate_reality")
async def manipulate_reality(cmd: ArchitectCommand):
    user_prompt = f"""
    ARCHITECT COMMAND: {cmd.action}
    TARGET ENTITY: {cmd.target_entity}
    ONTOLOGICAL DIALS: {cmd.dial_adjustments}
    Execute Gravitational Inversion, utilize MSP tools to verify and commit, and output the system state.
    
    IMPORTANT: You MUST return strictly RAW JSON. Do NOT wrap it in ```json blocks. It MUST match the exact following schema:
    {{
      "target_entity": "string",
      "qnf_triggered": true/false,
      "nai_dissonance_score": float,
      "impact_analysis": "string"
    }}
    """
    
    message = types.Content(
        role="user", 
        parts=[types.Part.from_text(text=user_prompt)]
    )
    
    async def event_stream():
        import uuid
        session_id = str(uuid.uuid4())
        
        # 1. RUN ROOT AGENT (System State Math)
        root_agen = runner_root.run_async(user_id="architect", session_id=session_id, new_message=message)
        
        full_root_json = ""
        async for event in root_agen:
            if getattr(event, 'content', None) and getattr(event.content, 'parts', None):
                for part in event.content.parts:
                    if getattr(part, 'text', None):
                        full_root_json += part.text
        
        root_data = {}
        try:
            clean_json = full_root_json.strip()
            if clean_json.startswith("```json"):
                clean_json = clean_json[7:-3]
            elif clean_json.startswith("```"):
                clean_json = clean_json[3:-3]
            root_data = json.loads(clean_json)
            yield f"data: {json.dumps({'type': 'root_update', 'data': root_data})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'data': f'Failed to parse root logic: {str(e)} | Raw: {full_root_json}'})}\n\n"
            return

        # 2. RUN ENVIRONMENT AGENT (Dynamic Surroundings)
        yield f"data: {json.dumps({'type': 'env_chunk', 'data': '\n\n===[ ENVIRONMENT RENDER ]===\n'})}\n\n"
        env_prompt = f"TARGET ENTITY: {cmd.target_entity}\nIMPACT ANALYSIS: {root_data.get('impact_analysis', '')}"
        env_msg = types.Content(role="user", parts=[types.Part.from_text(text=env_prompt)])
        env_agen = runner_env.run_async(user_id="architect", session_id=session_id, new_message=env_msg)
        
        env_full_text = ""
        async for event in env_agen:
            if getattr(event, 'content', None) and getattr(event.content, 'parts', None):
                for part in event.content.parts:
                    if getattr(part, 'text', None):
                        env_full_text += part.text
                        yield f"data: {json.dumps({'type': 'env_chunk', 'data': part.text})}\n\n"

        import asyncio
        async def generate_image_bg():
            # Run generate_image directly via thread to avoid blocking and token limits
            img_prompt = f"Based on the following environment render, extract a concise visual prompt and generate a vivid image of the space. Render: {env_full_text}"
            img_result = await asyncio.to_thread(generate_image, img_prompt)
            return img_result.strip() if img_result else ""

        # Spawn the background task before starting the char_agen stream
        img_task = asyncio.create_task(generate_image_bg())

        # 3. RUN CHARACTER AGENT (Static Subconscious)
        yield f"data: {json.dumps({'type': 'char_chunk', 'data': '\\n\\n===[ ENTITY SUBCONSCIOUS ]===\\n'})}\n\n"
        char_prompt = f"TARGET ENTITY: {cmd.target_entity}\nIMPACT ANALYSIS: {root_data.get('impact_analysis', '')}\nNAI DISSONANCE: {root_data.get('nai_dissonance_score', 0)}"
        char_msg = types.Content(role="user", parts=[types.Part.from_text(text=char_prompt)])
        char_agen = runner_char.run_async(user_id="architect", session_id=session_id, new_message=char_msg)
        
        async for event in char_agen:
            if getattr(event, 'content', None) and getattr(event.content, 'parts', None):
                for part in event.content.parts:
                    if getattr(part, 'text', None):
                        yield f"data: {json.dumps({'type': 'char_chunk', 'data': part.text})}\n\n"

        # 4. Await and yield the image result
        try:
            img_url = await img_task
            import re
            
            # Clean up potential markdown formatting from LLM response
            if img_url.startswith("```"):
                lines = img_url.split("\n")
                if len(lines) >= 3:
                     img_url = "".join(lines[1:-1])
                     
            match = re.search(r'(data:image/[^;]+;base64,[A-Za-z0-9+/=]+)', img_url)
            if match:
                img_url = match.group(1)
                
            yield f"data: {json.dumps({'type': 'image_url', 'data': img_url})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'data': f'Background image generation failed: {str(e)}'})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.post("/api/v1/visualize_space")
async def visualize_space(req: VisualizeRequest):
    import uuid
    import asyncio
    from image_agent import generate_image
    
    session_id = str(uuid.uuid4())
    message = types.Content(role="user", parts=[types.Part.from_text(text=f"Extract visual prompt from this environment render:\n{req.environment_text}")])
    
    agen = runner_space.run_async(user_id="architect", session_id=session_id, new_message=message)
    img_prompt = ""
    async for event in agen:
        if getattr(event, 'content', None) and getattr(event.content, 'parts', None):
            for part in event.content.parts:
                if getattr(part, 'text', None):
                    img_prompt += part.text
                    
    img_prompt = img_prompt.strip()
    
    # Now generate the image directly using the image_agent
    try:
        img_result = await asyncio.to_thread(generate_image, img_prompt)
        import re
        
        # Clean up potential markdown formatting from LLM response
        if img_result.startswith("```"):
            lines = img_result.split("\n")
            if len(lines) >= 3:
                 img_result = "".join(lines[1:-1])
                 
        match = re.search(r'(data:image/[^;]+;base64,[A-Za-z0-9+/=]+)', img_result)
        if match:
             return {"image_url": match.group(1), "prompt_used": img_prompt}
             
    except Exception as e:
        return {"error": str(e)}
        
    return {"error": "Image generation failed."}
