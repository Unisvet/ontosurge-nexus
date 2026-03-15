# PART 2: System Architecture & Implementation Instructions

We build this using Python, FastAPI, and containerize it for scalable deployment. This architecture realizes the "Nexus Weaver" Core Directive established in Part 1. We utilize the Astral `uv` toolchain for fast, robust environment management. 

### Step 1: Initialize the Environment
Create your project directory and set up a Python virtual environment using `uv`. We add dependencies for HTTP routing, the Google Agent Development Kit (ADK), and Pydantic.

```bash
mkdir ontosurge-nexus && cd ontosurge-nexus
uv init
# Standard FastAPI + ADK Core + GenAI SDK
uv add fastapi uvicorn pydantic sse-starlette google-genai
# Install the Google Agent Development Kit
uv add google-adk
# Install dotenv to manage API keys securely
uv add python-dotenv
```

### Step 2: Multi-Agent Architecture (ADK)
Instead of a single monolithic script, the system is divided into specialized ADK Agents to match the Part 1 specification:

1.  **`main.py` (The Nexus Weaver)**: The root orchestrator. It uses a structured Pydantic schema (`SystemStateUpdate`) to mathematically calculate the `qnf_triggered` flag, `nai_dissonance_score`, and `impact_analysis` of a gravity inversion.
2.  **`character_creator.py` (Forge Pipeline)**: A sub-agent that instantiates new narrative entities with baseline causal and ethical adherence dials.
3.  **`environment_renderer.py` (Dynamic Topology)**: A sub-agent that dynamically reads the `impact_analysis` and alters the sensory physics of the location (e.g., floating rocks, inverted lighting) to match the new reality state.
4.  **`character_renderer.py` (Static Subconscious)**: A sub-agent that receives the `nai_dissonance_score` and generates the entity's direct internal monologue reacting to the flux.
5.  **`image_agent.py` (Visual Synthesizer)**: A tool-calling agent wrapped around `gemini-3.1-flash-image-preview` to generate a live, base64-encoded visual representation of the altered space.

### Step 3: Architect the Nexus Weaver (Backend API)
Create `main.py`. Here, we instantiate the generative ADK runners, define the Antigravity Skills as python tools (representing future MCP connections), and stream the generated realities directly to the Architect UI using Server-Sent Events (SSE). 

Critically, the architecture streams text from the environment and character agents sequentially, while *simultaneously* processing the visual image generation in a background `asyncio` thread to avoid blocking the narrative output.

*(Refer to the repository's `main.py` for the complete implementation of the FastAPI application and SSE generators.)*

### Step 4: Containerize and Deploy to Google Cloud Run
Cloud Run provides a secure, auto-scaling HTTPS endpoint perfect for robust deployments.

1. Create a `Dockerfile` optimized for `uv`:
```dockerfile
FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.4 /uv /bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
# Install dependencies into the system environment to avoid activating venvs in Docker
RUN uv pip install --system -r pyproject.toml

COPY . .
# Cloud Run expects traffic on port 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

2. Deploy via Google Cloud CLI:
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

gcloud run deploy ontosurge-nexus \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GEMINI_API_KEY=your_gemini_api_key_here"
```

## 🚀 Pro-Level Enhancements & Architecture Proposals (Antigravity Nexus)
Based on the ambitious **Ontosurge Core System Constitution** you drafted in Part 1, the following improvements are suggested for the current implementation:

### 1. Model Context Protocol (MCP) as the "MSP Servers"
Currently, the MCP skills (`query_notebooklm_msp`, `commit_github_msp_state`) in `main.py` are mock python functions. We should actively bridge these to actual **MCP Servers**. 
- Deploy the `@modelcontextprotocol/server-github` to genuinely commit Role Agent states back to a remote repository.
- Connect to Google NotebookLM MCP to anchor the `causal_adherence` baselines against a massive lore-bible PDF. 
- **Goal:** The Nexus Weaver dynamically maps external reality back into the prompt without hardcoded responses.

### 2. Persistent Ontological State (Database Integration)
"Quantum Narrative Fluctuations (QNF)" break causality. If causality breaks, the universe must remember it. The current ADK `InMemorySessionService` disappears on restart.
- **Proposal:** Build a custom ADK `SessionService` driver for `Google Cloud Firestore` or `PostgresDB`. 
- Before the agent renders reality, it fetches the `target_entity`'s *Accumulated Ontological History*. The state generated in the SSE stream gets saved to Firestore so that tomorrow's reality inversion is permanently impacted by today's gravity changes.

### 3. Deepening the NAI System
The `character_renderer` currently takes the `nai_dissonance_score` purely as visual context. 
- **Proposal:** Implement a feedback loop. If an entity's `nai_dissonance_score` stays over 0.8 for three consecutive inversions, permanently alter their baseline dials in the database via the QNF module, fundamentally shifting their archetype.

### 4. Advanced Parallel Streaming
The UI handles the new parallel `image_url` chunk excellently, but the generative text (`char_chunk` and `env_chunk`) are still streamed sequentially because ADK runners maintain conversation history.
- **Proposal:** Fully decouple the semantic streams. Stream the Environment render and the Character internal monologue in isolated `asyncio.create_task` wrappers so they print to the console simultaneously across two different visual columns, maximizing the feeling of real-time multi-agent chaos.
