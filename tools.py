from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from datetime import datetime

@tool
def save_text_to_file(data):
    """Saves structured research data to a text file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"
    
    with open("research_output.txt", "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to research_output.txt"

@tool
def web_search(query):
    """Search the web for information using DuckDuckGo"""
    search = DuckDuckGoSearchRun()
    return search.run(query)

@tool
def wikipedia_search(query):
    """Search Wikipedia for information"""
    from langchain_community.tools import WikipediaQueryRun
    api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
    wiki = WikipediaQueryRun(api_wrapper=api_wrapper)
    return wiki.run(query)

save_tool = save_text_to_file
search_tool = web_search
wiki_tool = wikipedia_search
