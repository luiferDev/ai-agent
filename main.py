from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from tools import search_tool, wiki_tool, save_tool
from dataclasses import dataclass
import json

load_dotenv()

@dataclass
class ResearchResponse:
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

llm = ChatOllama(
    model="granite4:350m", 
    base_url="http://localhost:11434",
    temperature=0.01
)

agent = create_agent(
    model=llm,
    tools=[search_tool, wiki_tool, save_tool],
    system_prompt="""You are a research assistant. Use the available tools to research the user's question. 
    After using tools, provide your final response in this exact JSON format:
    {
        "topic": "main topic of the research",
        "summary": "detailed summary of findings",
        "sources": ["list of sources used"],
        "tools_used": ["list of tools you used"]
    }"""
)
query = input("Enter your research question: ")
response = agent.invoke({"messages": [{"role": "user", "content": query }]})

# Obtener el último mensaje
last_message = response["messages"][-1].content

try:
    data = json.loads(last_message)
    research_response = ResearchResponse(
        topic=data["topic"],
        summary=data["summary"],
        sources=data["sources"],
        tools_used=data["tools_used"]
    )
    print(last_message)
except:
    print("Respuesta sin parsear:")
    print(last_message)