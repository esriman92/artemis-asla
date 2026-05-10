import os
from typing import TypedDict, Annotated, List
from typing import Annotated
from operator import add
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END


# 1. Load Ground Control Credentials
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
memory = MemorySaver()


# 2. Define the "Clipboard" (The State)
# In NASA terms, this is our Telemetry Packet.
class AgentState(TypedDict):
    user_input: str
    messages: Annotated[List[str], add] # This keeps running a list of talk
    summary: str # The condensed history
    analysis: str
    log_entry: str
    steps: List[str]


# 3. Initialize the "Brain" (The LLM)
# We use 'Flash' for speed and low-Latency, critical for field ops.
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)


# 4. Define the Nodes (The Stations)

def analyzer_node(state: AgentState):
    """Analyze the astronaut's description for geological significance."""
    prompt = f"You are a NASA Geologist. Analyze this lunar observation: {state['user_input']}. Focus on mineral composition."
    response = llm.invoke(prompt)
    return {"analysis": response.content, "steps": state['steps'] + ["Analyzed Observation"]}


def summarizer_node(state: AgentState):
    """Condense the conversation history to save 'Payload Weight'."""
    # If the history is short, skip summarization
    if len(state['messages']) < 5:
        return {"steps": state['steps'] + ["Skipped Summary (Context Lean)"]}
    
    # The AI reviews the past messages and writes a brief summary
    prompt = f"Summarize the following mission progress into 2 sentences: {state['messages']}"
    summary_response = llm.invoke(prompt)

    # NASA Standard: We clear the message list to save tokens,
    # but keep the summary for the context!
    return {
        "summary": summary_response.context,
        "messages": [], # Resetting messages to keep the window clean
        "steps": state['steps'] + ["Generated Mission Summary"]
    }

def logger_node(state: AgentState):
    """Format the analysis into a formal NASA Mission Log."""
    prompt = f"Convert this analysis into a formal JSON-style mission log: {state['analysis']}"
    response = llm.invoke(prompt)
    return {"log_entry" : response.content, "steps": state['steps'] + ["Formatted Log"]}

# 5. Build the Graph (The Mission Flow)
workflow = StateGraph(AgentState)


# Add Our Stations
workflow.add_node("analyzer", analyzer_node)
workflow.add_node("summarizer", summarizer_node)
workflow.add_node("logger", logger_node)


# Connect the stations (The Flight Path) : Input -> Summarizer -> Analyze -> Log
workflow.set_entry_point("summarizer")
workflow.add_edge("summarizer", "analyzer")
workflow.add_edge("analyzer","logger")
workflow.add_edge("logger", END)


# Compile the Mission
asla_brain = workflow.compile(checkpointer=memory)