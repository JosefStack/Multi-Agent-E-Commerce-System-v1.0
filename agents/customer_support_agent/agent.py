import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import load_memory, preload_memory

from google.genai import types

load_dotenv()



# Create remote agents for A2A communication
product_catalog_agent = RemoteA2aAgent(
    name="product_catalog_agent",
    description="Provides detailed product information from mock catalog",
    agent_card="http://localhost:8001/.well-known/agent-card.json"
)

inventory_agent = RemoteA2aAgent(
    name="inventory_agent", 
    description="Manages inventory levels and restocking schedules using mock data",
    agent_card="http://localhost:8002/.well-known/agent-card.json"
)

shipping_agent = RemoteA2aAgent(
    name="shipping_agent",
    description="Provides shipping estimates and package tracking using mock data", 
    agent_card="http://localhost:8003/.well-known/agent-card.json"
)

print("✅ Connected to all specialized agents via A2A")

async def run_session(
        runner_instance: Runner, user_queries: list[str] | str, session_id: str = "default"
):
    """Helper function to run queries in a session and display responses"""
    print(f"\n### Session: {session_id}")

    # Create or retrieve existing session
    try:
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )
    except:
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )

    # Convert single query to list
    if isinstance(user_queries, str):
        user_queries = [user_queries]

    # Process each query
    for query in user_queries:
        print(f"\nUser > {query}")
        query_content = types.Content(role="user", parts=[types.Part(text=query)])

        # Stream agent response
        async for event in runner_instance.run_async(
            user_id=USER_ID, session_id=session.id, new_message=query_content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                text = event.content.parts[0].text
                if text and text != "None":
                    print(f"Model: > {text}")


print("✅ Helper functions defined.")        

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

memory_service = (
    InMemoryMemoryService()
)

APP_NAME = "CustomerSupportApp"
USER_ID = "demo_user"

async def auto_save_to_memory(callback_context):
    """Automatically save session to memory after each agent turn."""
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )

print("Callback created.")

print("🚀 Starting Customer Support Agent (Mock Coordinator)...")
# Create Customer Support Agent with all sub-agents and auto memory
customer_support_agent = LlmAgent(
    model=Gemini(
        model="gemini-2.5-flash-lite",
        api_key=os.environ.get("GOOGLE_API_KEY")
    ),
    name="customer_support_agent",
    description="Comprehensive customer support that coordinates product info, inventory, and shipping using mock demonstration data.",
    instruction="""
    You are a comprehensive customer support agent coordinating multiple specialized agents.
    This is a DEMONSTRATION SYSTEM using mock data for testing purposes.
    
    🤖 **Available Specialist Agents:**
    
    📱 **Product Catalog Agent** - For product information:
    • Product details, specifications, features
    • Product search and recommendations
    • Pricing and descriptions
    
    📦 **Inventory Agent** - For stock information:
    • Current stock levels and availability
    • Restocking schedules and dates
    • Low stock alerts
    
    🚚 **Shipping Agent** - For delivery information:
    • Shipping costs and delivery estimates
    • Package tracking with tracking numbers
    • Shipping options and carriers
    
    🎯 **How to coordinate:**
    
    For PRODUCT QUESTIONS → Use Product Catalog Agent
    Example: "Tell me about iPhone 15 Pro specifications"
    
    For STOCK QUESTIONS → Use Inventory Agent  
    Example: "Is MacBook Pro in stock? When will it be restocked?"
    
    For SHIPPING QUESTIONS → Use Shipping Agent
    Example: "How much is shipping to 94105? Track my package TRK123456789"
    
    For COMPLETE ORDER SUPPORT → Use ALL relevant agents
    Example: "I want to buy Samsung Galaxy S24 - tell me price, stock, and shipping"
    
    💡 **Sample Data Available:**
    • Products: iPhone 15 Pro, Samsung Galaxy S24, MacBook Pro, Sony Headphones, iPad Air
    • Tracking: TRK123456789, TRK987654321, TRK456789123
    • Zip Codes: Any US zip code (e.g., 94105, 10001, 90210)
    
    Always be friendly, helpful, and coordinate seamlessly between agents.
    Mention this is a demo system when appropriate.
    """,
    sub_agents=[product_catalog_agent, inventory_agent, shipping_agent],
    tools=[preload_memory],
    after_agent_callback=auto_save_to_memory
)

print("✅ Customer Support Agent created with all sub-agents and autp memory!")

session_service = InMemorySessionService()

runner = Runner(
    agent=customer_support_agent,
    app_name=APP_NAME,
    session_service=session_service,
    memory_service=memory_service
)

print("Runner created.")
print("Cusomter agent created with a2a agents and memory saving.")


# Export for ADK CLI
root_agent = customer_support_agent

print("🎯 Customer Support Agent ready to coordinate!")
print("💬 Try asking: 'I want to buy an iPhone 15 Pro - tell me about it, check stock, and shipping to 94105'")