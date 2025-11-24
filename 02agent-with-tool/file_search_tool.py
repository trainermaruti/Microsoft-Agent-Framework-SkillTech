"""
NEW 03: File Search Tool (Interactive Demo)

to configure virtual environment execute the following commands in PowerShell:
python -m venv labenv
./labenv/scripts/Activate.ps1
pip install -r requirements.txt 

This demo shows how to use the built-in File Search Tool with Microsoft Foundry.
The agent can search through uploaded documents in a vector store.

NOTE: You need to create a vector store and upload files first in Microsoft Foundry.
"""

import asyncio
import os
from dotenv import load_dotenv

from agent_framework import ChatAgent, HostedFileSearchTool, HostedVectorStoreContent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

# Load environment variables
load_dotenv('.env')

PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
MODEL_DEPLOYMENT = os.getenv("MODEL_DEPLOYMENT_NAME")

# IMPORTANT: Replace with your actual vector store ID from Microsoft Foundry
# You can create a vector store in the Azure AI Foundry portal and upload files
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID", "assistant-1bXV9VQkG63EuptpBxZWP4")


async def main():
    """Interactive demo: Agent with File Search Tool."""
    
    print("\n" + "="*70)
    print("🔍 DEMO: File Search Tool")
    print("="*70)
    
    if VECTOR_STORE_ID == "YOUR_VECTOR_STORE_ID_HERE":
        print("\n⚠️  WARNING: Please set VECTOR_STORE_ID in .env file")
        print("   1. Go to Azure AI Foundry portal")
        print("   2. Create a Vector Store")
        print("   3. Upload documents (PDF, TXT, DOCX)")
        print("   4. Copy the Vector Store ID")
        print("   5. Add VECTOR_STORE_ID=your_id to .env01")
        print("\n   For demo purposes, we'll create an agent anyway,")
        print("   but file search won't work without a vector store.\n")
    
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(
                async_credential=credential,
                project_endpoint=PROJECT_ENDPOINT,
                model_deployment_name=MODEL_DEPLOYMENT,
            ),
            instructions="You are a document search assistant. Use the file search tool to find information in uploaded documents.",
            name="FileSearchAgent",
            tools=[
                HostedFileSearchTool(
                    inputs=[
                        HostedVectorStoreContent(vector_store_id=VECTOR_STORE_ID)
                    ],
                    max_results=5
                )
            ]
        ) as agent
    ):
        print("\n Agent created with File Search Tool")
        print("💡 TIP: Ask questions about documents in your vector store")
        
        print("\n" + "="*70)
        print("💬 Interactive Chat (Type 'quit' to exit)")
        print("="*70 + "\n")
        
        while True:
            user_input = input("You: ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not user_input.strip():
                continue
            
            print("Agent: ", end="", flush=True)
            async for chunk in agent.run_stream(user_input):
                if chunk.text:
                    print(chunk.text, end="", flush=True)
            print("\n")


if __name__ == "__main__":
    asyncio.run(main())
