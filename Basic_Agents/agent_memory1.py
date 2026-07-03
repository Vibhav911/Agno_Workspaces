import streamlit as st
from agno.agent import Agent
from agno.models.groq import Groq
from agno.knowledge.embedder.huggingface import HuggingfaceCustomEmbedder
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.lancedb import LanceDb, SearchType
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

# Initialize the agent
agent = Agent(
    model=Groq(id="openai/gpt-oss-120b"),
    description="You are a Thai cuisine expert!",
    instructions=[
        "Search your knowledge base for Thai recipes.",
        "If the question is better suited for the web, search the web to fill in gaps.",
        "Prefer the information in your knowledge base over the web results."
    ],
    knowledge=Knowledge(
        vector_db=LanceDb(
            table_name="recipes",
            uri="tmp/lancedb",
            search_type=SearchType.hybrid,
            embedder=HuggingfaceCustomEmbedder(),
        ),
    ),
    tools=[DuckDuckGoTools()],
    markdown=True,
)

if not os.path.exists("tmp/lancedb"):
    agent.knowledge.insert(
        url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
        reader = PDFReader()
    )

# Streamlit Interface
st.title("🥘 Thai Cuisine Expert")
st.write("Ask me anything about Thai cuisine! From recipes to history, I've got you covered.")

# User Input
user_input = st.text_input("Enter your question:")

# Display Response
if user_input:
    with st.spinner("Thinking..."):
        response = agent.run(user_input)
        st.markdown(response.content)