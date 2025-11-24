"""
NEW 02: Use Existing Microsoft Foundry Agent (Interactive Demo)

to configure virtual environment execute the following commands in PowerShell:
python -m venv labenv
./labenv/scripts/Activate.ps1
pip install -r requirements.txt 

This demo connects to an EXISTING agent in Microsoft Foundry.
You'll need to update the .env file with your agent ID.
"""

import asyncio
import os
from dotenv import load_dotenv

from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

# Load environment variables
load_dotenv('.env')

PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
AGENT_ID = os.getenv("AZURE_AI_AGENT_ID")


async def main():
    """Interactive demo: Connect to existing agent."""
    
    print("DEMO: Connect to Existing Azure AI Foundry Agent")
        
    print(f"\n Connecting to agent: {AGENT_ID}")
    
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(
                async_credential=credential,
                project_endpoint=PROJECT_ENDPOINT,
                agent_id=AGENT_ID
            )
        ) as agent
    ):
        print("Connected successfully!")
        
        print("Interactive Chat (Type 'quit' to exit)")        
        
        while True:
            # Get user input
            user_input = input("You: ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not user_input.strip():
                continue
            
            # Get streaming response
            print("Agent: ", end="", flush=True)
            async for chunk in agent.run_stream(user_input):
                if chunk.text:
                    print(chunk.text, end="", flush=True)
            print("\n")


if __name__ == "__main__":
    asyncio.run(main())
