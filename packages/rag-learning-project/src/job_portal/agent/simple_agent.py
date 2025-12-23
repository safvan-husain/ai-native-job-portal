"""
Enhanced chat agent using Ollama Cloud with tool support.
"""

import os
from typing import Optional, Iterator, Annotated, TypedDict
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode
from .prompts import get_system_prompt_with_tools
from .tools import (
    search_jobs, get_company_details, compare_companies,
    search_candidates, get_candidate_details, compare_candidates
)

# Load environment variables
load_dotenv()


# Extended state for job portal
class JobPortalState(MessagesState):
    """Extended state with job portal specific fields."""
    user_type: Optional[str] = None
    search_results: list = []
    selected_items: list = []
    comparison_mode: bool = False


class SimpleAgent:
    """
    Enhanced conversational agent using Ollama Cloud with tool support.
    Intelligently uses tools based on user type and conversation context.
    """
    
    def __init__(
        self,
        user_type: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize the enhanced agent with tools.
        
        Args:
            user_type: Either 'job_seeker' or 'company'
            model: Ollama model name (defaults to env var)
            base_url: Ollama API base URL (defaults to env var)
            api_key: Ollama API key (defaults to env var)
        """
        self.user_type = user_type
        
        # Get configuration from env or parameters
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "https://ollama.com")
        self.api_key = api_key or os.getenv("OLLAMA_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "OLLAMA_API_KEY not found. Please set it in .env file or pass as parameter."
            )
        
        # Get tools based on user type
        self.tools = self._get_tools_for_user_type(user_type)
        
        # Initialize Ollama client with tools
        self.llm = ChatOllama(
            model=self.model,
            base_url=self.base_url,
            api_key=self.api_key,
            temperature=0.7,
        ).bind_tools(self.tools)
        
        # Initialize memory
        self.memory = MemorySaver()
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _get_tools_for_user_type(self, user_type: Optional[str]) -> list:
        """Get appropriate tools based on user type."""
        if user_type == "job_seeker":
            return [search_jobs, get_company_details, compare_companies]
        elif user_type == "company":
            return [search_candidates, get_candidate_details, compare_candidates]
        else:
            # If user type not set, provide all tools
            return [
                search_jobs, get_company_details, compare_companies,
                search_candidates, get_candidate_details, compare_candidates
            ]
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph conversation graph with tool support."""
        
        # Define the chatbot function
        def chatbot(state: JobPortalState):
            """Process messages and generate response with tool support."""
            # Get system prompt based on user type
            system_prompt = get_system_prompt_with_tools(self.user_type)
            
            # Prepend system message if not already there
            messages = state["messages"]
            if not messages or not isinstance(messages[0], SystemMessage):
                messages = [SystemMessage(content=system_prompt)] + messages
            
            # Get response from LLM (may include tool calls)
            response = self.llm.invoke(messages)
            
            return {"messages": [response]}
        
        # Define routing logic
        def should_continue(state: JobPortalState):
            """Determine if we should continue to tools or end."""
            messages = state["messages"]
            last_message = messages[-1]
            
            # If the LLM makes a tool call, route to tools
            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                return "tools"
            # Otherwise, end the conversation turn
            return END
        
        # Create tool node
        tool_node = ToolNode(self.tools)
        
        # Create graph with extended state
        graph_builder = StateGraph(JobPortalState)
        
        # Add nodes
        graph_builder.add_node("chatbot", chatbot)
        graph_builder.add_node("tools", tool_node)
        
        # Add edges
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_conditional_edges(
            "chatbot",
            should_continue,
            ["tools", END]
        )
        graph_builder.add_edge("tools", "chatbot")
        
        # Compile with memory
        return graph_builder.compile(checkpointer=self.memory)
    
    def chat(
        self,
        message: str,
        thread_id: str = "default"
    ) -> str:
        """
        Send a message and get a response.
        
        Args:
            message: User message
            thread_id: Conversation thread ID (for memory)
            
        Returns:
            Agent response as string
        """
        config = {"configurable": {"thread_id": thread_id}}
        
        # Invoke the graph
        result = self.graph.invoke(
            {"messages": [HumanMessage(content=message)]},
            config=config
        )
        
        # Extract the last message (agent's response)
        return result["messages"][-1].content
    
    def stream_chat(
        self,
        message: str,
        thread_id: str = "default"
    ) -> Iterator[str]:
        """
        Send a message and stream the response.
        
        Args:
            message: User message
            thread_id: Conversation thread ID (for memory)
            
        Yields:
            Chunks of the agent's response
        """
        config = {"configurable": {"thread_id": thread_id}}
        
        # Stream the graph
        for event in self.graph.stream(
            {"messages": [HumanMessage(content=message)]},
            config=config,
            stream_mode="values"
        ):
            # Get the last message in the event
            if event.get("messages"):
                last_message = event["messages"][-1]
                if isinstance(last_message, AIMessage):
                    yield last_message.content
    
    def set_user_type(self, user_type: str):
        """
        Update the user type and rebuild the graph with appropriate tools.
        
        Args:
            user_type: Either 'job_seeker' or 'company'
        """
        self.user_type = user_type
        self.tools = self._get_tools_for_user_type(user_type)
        self.llm = ChatOllama(
            model=self.model,
            base_url=self.base_url,
            api_key=self.api_key,
            temperature=0.7,
        ).bind_tools(self.tools)
        self.graph = self._build_graph()
    
    def get_conversation_history(self, thread_id: str = "default") -> list:
        """
        Get the conversation history for a thread.
        
        Args:
            thread_id: Conversation thread ID
            
        Returns:
            List of messages
        """
        config = {"configurable": {"thread_id": thread_id}}
        state = self.graph.get_state(config)
        return state.values.get("messages", [])


# Convenience function for quick testing
def test_agent():
    """Test the agent with a simple conversation."""
    print("Testing Simple Agent...")
    print("-" * 50)
    
    # Create agent
    agent = SimpleAgent(user_type="job_seeker")
    
    # Test conversation
    messages = [
        "Hi, I'm looking for a job",
        "I'm a Python developer with 5 years of experience",
        "What did I just tell you about my experience?"
    ]
    
    for msg in messages:
        print(f"\nUser: {msg}")
        response = agent.chat(msg, thread_id="test")
        print(f"Agent: {response}")
    
    print("\n" + "-" * 50)
    print("Test complete!")


if __name__ == "__main__":
    test_agent()
