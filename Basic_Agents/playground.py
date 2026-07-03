from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.db.sqlite import SqliteDb
from agno.os import AgentOS
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

agent_storage = "tmp/agents.db"

web_agent = Agent(
     model=Groq(id="openai/gpt-oss-120b"),
     tools=[DuckDuckGoTools()],
     instructions=["Always include sources"],

     # Store an agent session in sqlite database
     db = SqliteDb(db_file=agent_storage, knowledge_table="web_agent"),

     # Add date and time to the instruction
     add_datetime_to_context=True,

     # Add the history of conversation to the messages
     add_history_to_context=True,

     # Number of history responses to add to the messages
     num_history_messages=3,

     markdown=True
)

finance_agent = Agent(
     name="finance Agent",
     model=Groq(id="openai/gpt-oss-120b"),
     tools=[YFinanceTools(enable_stock_price=True ,enable_company_info=True, enable_analyst_recommendations=True)],
     instructions= ["Always use tables to display data"],
     db = SqliteDb(db_file=agent_storage, knowledge_table= "finance_agent"),
     add_datetime_to_context=True,
     add_history_to_context=True,
          num_history_messages=3,
     markdown=True
)

app = AgentOS(agents=[web_agent, finance_agent]).get_app()