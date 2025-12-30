import os
from dotenv import load_dotenv
from langchain_classic.agents import create_tool_calling_agent, Agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient
from mailer import send_email

load_dotenv()

google_key = os.getenv("GOOGLE_API_KEY")
tavily_key = os.getenv("TAVILY_API_KEY")
print(f"Key loaded: {google_key is not None}")

client = TavilyClient(tavily_key)

@tool
def get_gold_price() -> str:
    """Useful for searching current gold spot prices in International and Shanghai markets."""
    print(" 查询金价 (Au99.99 & XAU)...")
    response = client.search(
        query="current spot gold price USD oz AND 上海黄金交易所 Au99.99 最新价格 人民币/克",
        search_depth="advanced",
        max_results=5
    )
    raw_prices = [r['content'] for r in response.get("results", [])]
    return "\n---\n".join(raw_prices)

@tool
def get_silver_price() -> str:
    """Useful for searching current silver spot prices in International and Shanghai markets."""
    print(" 查询银价 (Ag(T+D) & XAG)...")
    response = client.search(
        query="current spot silver price USD oz AND 上海黄金交易所 Ag(T+D) 白银最新价格 人民币/千克",
        search_depth="advanced",
        max_results=5
    )
    raw_prices = [r['content'] for r in response.get("results", [])]
    return "\n---\n".join(raw_prices)

@tool
def get_news()->str:
    """Useful for searching significant International Politics or financial news impact in International and Shanghai markets."""
    response = client.search(
        query="significant international politics or financial news that impacts precious metal prices",
        search_depth="advanced",
        max_results=10
    )
    raw_news = []
    for result in response.get('results',[]):
        raw_news.append(result['content'])

    # Splice them into one string
    news = "\n---\n".join(raw_news)
    return news

tools = [get_gold_price, get_silver_price, get_news]

# Initialize the models
llm = ChatGoogleGenerativeAI(
    model = "gemini-2.0-flash",
    temperature = 0,
    google_api_key = os.getenv("GOOGLE_API_KEY"),
    max_output_tokens = 1500,
    request_timeout = 60

)

# Define prompt
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful financial assistant. You have access to tools to obtain the prices of gold, silver, and news. "
     "Please analyze the trend based on the data you find. "
     "Give me a systematic and objective analysis. "

     "KNOWLEDGE BASE: "
     "1. 'Au99.99' refers to the standard spot gold price at Shanghai Gold Exchange (SGE). "
     "2. 'Ag(T+D)' refers to the standard silver price at SGE. "

     "IMPORTANT: Please write the final analysis report in Simplified Chinese (简体中文). "
     "STRICT OUTPUT RULE: Do NOT include any conversational filler. Start directly with the Markdown title."
     ),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print("---Start Running Agent---")
result = agent_executor.invoke({
    "input": "Search for current gold spot and silver spot prices in USD and CNY, and relevant financial news. "
             "Analyze how the news affects the prices. "
             "Please generate a comprehensive report in Chinese."
})

analysis_content = result["output"]

print("\n--- Analysis Generated ---\n")
print(analysis_content)

print("\n--- Sending Email ---\n")
send_email(content=analysis_content, subject="【每日行情】金银价趋势分析简报")
