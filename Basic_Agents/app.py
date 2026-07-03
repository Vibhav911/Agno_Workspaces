from agno.agent import Agent
from agno.models.groq import Groq
import os
from dotenv import load_dotenv
from agno.tools.duckduckgo import DuckDuckGoTools

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")



agent = Agent(
     model=Groq(id="llama-3.3-70b-versatile"),
     description="You are an assistant. Please reply to the user's queries. Use only DuckDuckGo for web searches.",
     tools=[DuckDuckGoTools()],
     markdown=True
)

agent.print_response("Tell me about the latest sports news", stream=True)