# 🚀 Artemis Surface Log Agent (ASLA)

**ASLA** is a deterministic, fault-tolerant Agentic AI system designed for simulated deep-space geological analysis. It bridges the gap between unstructured human input and structured mission data using a cyclic state machine architecture.

## 🧠 System Architecture
Unlike standard linear chatbots, ASLA is built on a **Directed Cyclic Graph (LangGraph)**:
* **Cognitive Engine:** Google Gemini 2.5 Flash (via Langchain).
* **State Management:** Implementations of MemorySaver for context retention across disrupted sessions.
* **Sensory Tools:** ReAct-based tool binding for zero-hallucination querying of external mineralogy databases.
* **Infrastructure:** Dockerized and deployed serverless via Google Cloud Run.

## 🛠️ Key Features
1. **Tool Precedence:** The architecture forces the LLM to prioritize explicit tool output (`FeTiO3`) over latent training data, minimizing hallucinations.
2. **Context Compression:** A Summarization Node automatically compresses rolling memory buffers to prevent Context Window Overflows during long missions.
3. **Structured Outputs:** Uses strict validation to convert conversational analysis into database-ready JSON arrays.

## 🚀 How to Run Locally
1. Clone the repository.
2. Copy `.env.example` to `.env` and add your Google Gemini API key.
3. Run `pip install -r requirements.txt`.
4. Launch the cockpit: `streamlit run main.py`.


***This is First Cognitive Assistant Built for Space Exploration for Mineralogy and Geology with Autonomous Logger for Data Analysis and Modeling (Commit: May 10th, 2026, Sunday).***
