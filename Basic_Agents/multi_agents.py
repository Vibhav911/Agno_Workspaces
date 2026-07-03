from agno.agent import Agent
from agno.team import Team
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
import os
from dotenv import load_dotenv


load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


web_agent = Agent(
     name="Web Agent",
     role="Search the web for information",
     model=Groq(id="openai/gpt-oss-120b"),
     tools=[DuckDuckGoTools()],
     instructions="Always include sources. Use only Duckduckgo Tool to search for web",
     markdown=True
)


finance_agent = Agent(
     name="Finance Agent",
     role="Get financial data",
     model=Groq(id="openai/gpt-oss-120b"),
     tools=[YFinanceTools(enable_stock_price=True ,enable_company_info=True, enable_analyst_recommendations=True)],
     instructions="Use tables to display data",
     markdown=True
)


agent_team = Team(
     members=[web_agent, finance_agent],
     model=Groq(id="openai/gpt-oss-120b"),
     instructions=["Always include sources", "Use tables to display data"],
     markdown=True
)


agent_team.print_response("What's the market outlook and finance performance of AI semiconductor companies ? like NVDA", stream=True)