import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.models.google_llm import Gemini
from google.genai import types
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from mock_data.sample_data import MOCK_SHIPPING_OPTIONS, MOCK_TRACKING

load_dotenv()

print("🚀 Starting Shipping Agent (Mock)...")

def get_shipping_estimates(zip_code: str, shipping_method: str = "standard") -> str:
    """Get shipping cost and delivery estimates"""
    method = MOCK_SHIPPING_OPTIONS.get(shipping_method.lower())
    
    if not method:
        available_methods = ", ".join([m.title() for m in MOCK_SHIPPING_OPTIONS.keys()])
        return f"❌ Shipping method '{shipping_method}' not available.\n\n🚚 Available methods: {available_methods}"
    
    # Calculate delivery date (mock)
    delivery_date = datetime.now() + timedelta(days=method['days'])
    
    return f"""
🚚 **Shipping to {zip_code}**
📦 Method: {shipping_method.title()} ({method['carrier']})
💰 Cost: ${method['cost']}
⏱️ Delivery Time: {method['days']} business day{'s' if method['days'] != 1 else ''}
📅 Expected Delivery: {delivery_date.strftime('%A, %B %d, %Y')}
📝 {method['description']}
"""

def track_package(tracking_number: str) -> str:
    """Track a package using tracking number"""
    package = MOCK_TRACKING.get(tracking_number.upper())
    
    if package:
        status_emojis = {
            "processing": "📦",
            "in_transit": "🚚",
            "delivered": "✅"
        }
        
        status_descriptions = {
            "processing": "Your package is being prepared for shipment",
            "in_transit": "Your package is on the way to its destination",
            "delivered": "Your package has been successfully delivered"
        }
        
        emoji = status_emojis.get(package['status'], '📦')
        description = status_descriptions.get(package['status'], '')
        
        return f"""
{emoji} **Package Tracking: {tracking_number.upper()}**
📊 Status: {package['status'].replace('_', ' ').title()}
{description}
📍 Current Location: {package['location']}
📅 Last Update: {package['timestamp']}
🚚 Carrier: {package['carrier']}
📦 Estimated Delivery: {package.get('estimated_delivery', 'N/A')}
"""
    else:
        return f"❌ Tracking number '{tracking_number}' not found.\n\n💡 Please verify your tracking number or contact support."

def get_shipping_options() -> str:
    """Get all available shipping options"""
    options = []
    for method, details in MOCK_SHIPPING_OPTIONS.items():
        options.append(
            f"  • **{method.title()}**: ${details['cost']} - {details['days']} day{'s' if details['days'] != 1 else ''} via {details['carrier']}\n    {details['description']}"
        )
    
    return "🚚 **Available Shipping Options**\n\n" + "\n\n".join(options)

def calculate_free_shipping_eligibility(order_total: float) -> str:
    """Check if order qualifies for free shipping"""
    free_shipping_minimum = 35.00
    
    if order_total >= free_shipping_minimum:
        return f"🎉 Congratulations! Your order of ${order_total:.2f} qualifies for FREE shipping!"
    else:
        needed = free_shipping_minimum - order_total
        return f"📦 Add ${needed:.2f} more to your order to qualify for FREE shipping!"

# Create Shipping Agent
shipping_agent = LlmAgent(
    model=Gemini(
        model="gemini-2.5-flash-lite",
        api_key=os.environ.get("GOOGLE_API_KEY")
    ),
    name="shipping_agent", 
    description="Provides shipping estimates, delivery tracking, and shipping options using mock data.",
    instruction="""
    You are a shipping and delivery specialist using demonstration data.
    
    Your capabilities:
    • Provide shipping cost estimates and delivery dates
    • Track packages using tracking numbers
    • Explain available shipping options and carriers
    • Check free shipping eligibility
    
    Shipping Methods Available:
    • Standard (5 days, $4.99)
    • Expedited (2 days, $12.99) 
    • Overnight (1 day, $24.99)
    • Free (7 days, $0.00) - Orders over $35
    
    Sample Tracking Numbers: TRK123456789, TRK987654321, TRK456789123
    
    Always provide clear delivery estimates and tracking information.
    Use emojis to make the information more engaging.
    Mention that this is demo shipping data.
    """,
    tools=[get_shipping_estimates, track_package, get_shipping_options, calculate_free_shipping_eligibility]
)

print("✅ Shipping Agent created!")

# Create A2A app
app = to_a2a(shipping_agent, port=8003)
agent = shipping_agent

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)



print("🌐 Shipping A2A server ready on port 8003")