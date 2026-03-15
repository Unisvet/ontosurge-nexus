# 🌌 The Ontosurge Nexus (TON)

***The Narrative Meta-Physics Engine powered by Google Gemini ADK***

[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![Google ADK](https://img.shields.io/badge/Agent_Development_Kit-Framework-orange.svg)](https://ai.google.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135+-green.svg)](https://fastapi.tiangolo.com/)

---

## 📖 The Core Philosophy: Gravitational Inversion

The Ontosurge Nexus is more than a generative text application; it is a **Narrative Meta-Physics Engine**. Built upon the core concept of **Gravitational Inversion (Antigravity)**, TON allows the "Architect" (User) to dynamically alter the fundamental "rules of existence" within a story.

Instead of writing a plot, you manipulate the *ontological weight* of specific entities. What happens to a fiercely loyal Paladin when you reduce their "Ethical Consistency" dial to 10%? What happens to the geometry of their surrounding world when "Causal Adherence" breaks down? 

This system uses a meticulously orchestrated ensemble of multi-turn AI Agents to continuously calculate precisely how reality bends in response to your mathematical interventions.

---

## 🧠 Multi-Agent Architecture

This project abandons the monolithic "chatbot" design in favor of a deeply specialized ecosystem of agents driven by the **Google Agent Development Kit (ADK)** and `gemini-2.5-pro`.

1. **The Nexus Weaver (`main.py`)**: The brutal, logical orchestrator. Forces mathematical JSON schemas to calculate exactly how heavily an inversion shatters reality ("Quantum Narrative Fluctuations").
2. **The Forge Pipeline (`character_creator.py`)**: A sub-agent that instantiates new narrative entities with baseline psychological and causal weights.
3. **The Static Subconscious (`character_renderer.py`)**: Trapped inside the entity's mind, this agent receives the cognitive dissonance scores and outputs the hero's increasingly panicked internal monologue as the rules of their reality shift.
4. **The Dynamic Topology (`environment_renderer.py`)**: Processes the mathematical "Impact Analysis" to rip apart the sensory physics of the surrounding location (e.g., rivers flowing backwards, floating architecture).
5. **The Visual Synthesizer (`image_agent.py`)**: Uses `gemini-3.1-flash-image-preview` in a parallel processing thread to manifest a high-fidelity image of the broken, localized reality based directly on the Environment Agent's descriptions.

---

## ⚡ Real-Time Streaming (SSE)

The Ontosurge Console is built for immersion. Utilizing Server-Sent Events (SSE), the application streams the descent into madness *live*. As the Nexus Weaver shatters causality, you watch the Environment and the Entity's Subconscious render simultaneously on the screen while the Visual Synthesizer paints the paradoxical outcome in the background.

---

## 🚀 Quickstart & Installation

The Nexus is built upon [uv](https://docs.astral.sh/uv/), an extremely fast Python package and project manager.

### 1. Clone & Configure
```bash
git clone https://github.com/Unisvet/ontosurge-nexus.git
cd ontosurge-nexus
```

Create a `.env` file in the root directory and add your Google Gemini API key:
```ini
GEMINI_API_KEY="YourKeyHere..."
```

### 2. Ignite the Core
Use `uv` to automatically install the environment, lock the dependencies, and launch the asynchronous FastAPI server:
```bash
uv run fastapi dev main.py
```

Open your browser to [http://localhost:8000](http://localhost:8000).

---

## ☁️ Deployment (Google Cloud Run)

The Ontosurge system is fully containerized for production on Google Cloud Run. 

1. Ensure the `gcloud` CLI is installed and authenticated.
2. Deploy directly from source:
```bash
gcloud run deploy ontosurge-nexus \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GEMINI_API_KEY=your_key_here"
```

## 🔮 Future Horizon (Pro-Level Enhancements)
*   **MCP Server Integrations**: Replacing local mocked skills with true Model Context Protocol (MCP) integrations so the Nexus Weaver can commit state changes to GitHub repositories or query lore bibles via NotebookLM dynamically.
*   **Persistent Firestore Ontologies**: Creating a custom ADK `SessionService` backed by Google Firestore so that Gravity Inversions become permanent, shaping the universe forever across future sessions.
