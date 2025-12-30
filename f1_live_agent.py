import os
import time
from google.genai.errors import ClientError
from google import genai
from google.genai import types
from duckduckgo_search import DDGS
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_KEY")
client = genai.Client(api_key=api_key)

def search_internet(query: str):
    print(f"\n🔎 Searching for: '{query}'...")
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))
    return results

chat = client.chats.create(
    model="gemini-flash-latest",
    config=types.GenerateContentConfig(
        tools=[search_internet],
        response_modalities=["TEXT"],
        system_instruction="You're an F1 expert. Use the search_internet to find current information about races, standings, and news"
    )
)

print("🏎️ F1 Live Agent is online. (Type 'exit' or 'quit' to quit)")
print('-'*50)

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    try:
        response = chat.send_message(user_input)
        if response.text:
            print(f"Agent: {response.text}")
        else:
            print("Agent: No response. Somthing might have gone wrong with the tool output")

    except ClientError as e:
        print(f"\n ⚠️ Limit reached! Cooling down for 30 seconds")
        time.sleep(35)
        print("Ready to go again! \n")