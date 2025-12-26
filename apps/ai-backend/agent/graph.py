import os
from typing import TypedDict, Annotated, Sequence
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv
from .prompts import get_system_prompt
from .tools import filter_candidates

# Load environment variables
load_dotenv()

# Define the state for our graph
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], lambda x, y: x + y]
    unique_keywords: list

class CandidateFilterAgent:
    def __init__(self, model_name: str = None):
        # Get configuration from environment
        self.model_name = model_name or os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        api_key = os.getenv("OLLAMA_API_KEY")
        
        # Configure the LLM with tools
        self.llm = ChatOllama(
            model=self.model_name,
            base_url=base_url,
            api_key=api_key,
            temperature=0
        ).bind_tools([filter_candidates])
        
        # Build the graph
        self.graph = self._build_graph()

    def _build_graph(self):
        builder = StateGraph(AgentState)
        
        # Define nodes
        builder.add_node("agent", self._call_model)
        builder.add_node("action", ToolNode([filter_candidates]))
        
        # Define edges
        builder.set_entry_point("agent")
        builder.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "action",
                "end": END
            }
        )
        builder.add_edge("action", "agent")
        
        return builder.compile()

    def _should_continue(self, state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "continue"
        print(f"DEBUG: _should_continue: Last message has no tool calls, ending.")
        return "end"

    async def _call_model(self, state: AgentState):
        messages = state["messages"]
        print(f"DEBUG: Calling model with {len(messages)} messages")
        print(f"DEBUG: Unique keywords for agent: {state['unique_keywords']}")
        # If the first message isn't a SystemMessage, add it
        if not any(isinstance(m, SystemMessage) for m in messages):
            system_prompt = get_system_prompt(state["unique_keywords"])
            print(f"DEBUG: Adding system prompt: {system_prompt[:100]}...")
            messages = [SystemMessage(content=system_prompt)] + list(messages)
            
        print(f"DEBUG: Invoking LLM...")
        try:
            response = await self.llm.ainvoke(messages)
            print(f"DEBUG: LLM Response received: {response.content[:50]}...")
            if response is None:
                print("DEBUG: LLM response is None!")
            return {"messages": [response]}
        except Exception as e:
            print(f"DEBUG: LLM Error: {e}")
            raise

    async def run(self, query: str, unique_keywords: list):
        print(f"DEBUG: Starting agent run with query: {query}")
        # Initialize state
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "unique_keywords": unique_keywords
        }
        
        # Run the graph
        print(f"DEBUG: Invoking graph.ainvoke...")
        try:
            result = await self.graph.ainvoke(initial_state)
            print(f"DEBUG: Graph invocation complete.")
            if result is None:
                print("DEBUG: Graph result is None!")
                return "Error: Agent returned no result."
            return result["messages"][-1].content
        except Exception as e:
            print(f"DEBUG: Graph Error: {e}")
            raise
