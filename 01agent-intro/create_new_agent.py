"""
NEW 01: Create Microsoft Foundry Agent (Interactive Demo)

This is an INTERACTIVE demo where you can create a new agent in Microsoft Foundry
and chat with it in real-time.

to configure virtual environment execute the following commands in PowerShell:
python -m venv labenv
./labenv/scripts/Activate.ps1
pip install -r requirements.txt 

The agent is persistent and will be saved to Microsoft Foundry service.
"""

import asyncio
import os
from dotenv import load_dotenv

from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from azure.ai.projects.aio import AIProjectClient

# Load environment variables
load_dotenv('.env')

PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
MODEL_DEPLOYMENT = os.getenv("MODEL_DEPLOYMENT_NAME")


async def main():
    """Interactive demo: Create agent and chat."""
    
    print("\n" + "="*70)
    print("DEMO: Create Microsoft Foundry Agent (Interactive)")
    print("="*70)
    
    async with AzureCliCredential() as credential:
        # Create the agent in Azure AI Foundry
        async with AIProjectClient(
            endpoint=PROJECT_ENDPOINT,
            credential=credential
        ) as project_client:
            
            print("\n Creating new agent in Microsoft Foundry...")
            
            created_agent = await project_client.agents.create_agent(
                model=MODEL_DEPLOYMENT,
                name="STAgent_Interactive",
                instructions="You are a helpful AI assistant. Be concise and friendly."
            )
            
            print(f"Agent created successfully!")
            print(f"Agent ID: {created_agent.id}")
            
            # Now use the agent for chat
            async with ChatAgent(
                chat_client=AzureAIAgentClient(
                    agent_id=created_agent.id,
                    async_credential=credential,
                    project_endpoint=PROJECT_ENDPOINT,
                    model_deployment_name=MODEL_DEPLOYMENT,
                )
            ) as agent:
                
                print("Interactive Chat (Type 'quit' to exit)")
                                
                while True:
                    # Get user input
                    user_input = input("You: ")
                    
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        print("\n👋 Goodbye!")
                        break
                    
                    if not user_input.strip():
                        continue
                    
                    # Get response from agent
                    print("Agent: ", end="", flush=True)
                    async for chunk in agent.run_stream(user_input):
                        if chunk.text:
                            print(chunk.text, end="", flush=True)
                    print("\n")


if __name__ == "__main__":
    asyncio.run(main())
