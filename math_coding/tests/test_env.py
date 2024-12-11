import os
from promptflow.client import PFClient

def test_env_variables():
    # Initialize PFClient
    pf = PFClient()
    
    # List all connections
    print("\nListing all connections:")
    try:
        connections = pf.connections.list()
        for conn in connections:
            print(f"Connection name: {conn.name}")
            print(f"Connection type: {conn.type}")
            print(f"Connection configs: {conn.configs}")
            print("---")
    except Exception as e:
        print("Error listing connections:", str(e))
    
    print("\nChecking environment variables:")
    print("AZURE_OPENAI_API_KEY:", bool(os.getenv("AZURE_OPENAI_API_KEY")))
    print("AZURE_OPENAI_ENDPOINT:", os.getenv("AZURE_OPENAI_ENDPOINT"))
    
    # Test connection to Azure OpenAI
    from openai import AzureOpenAI
    
    print("\nTesting Azure OpenAI connection:")
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2023-07-01-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    
    # Try a simple completion
    try:
        response = client.chat.completions.create(
            model="gpt-35-turbo",  # Using the deployment name from your flow.dag.yaml
            messages=[{"role": "user", "content": "Hello!"}]
        )
        print("Connection successful!")
    except Exception as e:
        print("Connection failed:", str(e))

if __name__ == "__main__":
    test_env_variables() 