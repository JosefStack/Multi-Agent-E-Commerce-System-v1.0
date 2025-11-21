import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.models.google_llm import Gemini
from google.genai import types

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mock_data.sample_data import find_product, search_products

load_dotenv()

print("🚀 Starting Product Catalog Agent (Mock)...")

def get_product_details(product_name: str) -> str:
    """Get detailed product information from mock data"""
    product = find_product(product_name)
    
    if product:
        features = "\n".join([f"  • {feature}" for feature in product.get('features', [])])
        return f"""
📱 **{product['name']}** - ${product['price']}
🏷️  Brand: {product['brand']}
📂 Category: {product['category']}

📝 Description: {product['description']}

⚙️ Specifications: {product['specifications']}

✨ Features:
{features}

💡 Need stock information? Ask our inventory agent!
"""
    else:
        # Search for similar products
        similar = search_products(product_name)
        if similar:
            suggestions = "\n".join([f"  • {p['name']} - ${p['price']}" for p in similar[:3]])
            return f"❌ Product '{product_name}' not found.\n\n🔍 Similar products:\n{suggestions}"
        else:
            return f"❌ Product '{product_name}' not found in our catalog."

def search_products_tool(query: str, category: str = "") -> str:
    """Search products in mock catalog"""
    results = search_products(query, category)
    
    if results:
        product_list = "\n".join([
            f"  • {p['name']} (${p['price']}) - {p['description'][:80]}..." 
            for p in results[:5]
        ])
        return f"🔍 Found {len(results)} products:\n{product_list}"
    else:
        categories = ", ".join(["electronics", "audio", "tablets"])
        return f"❌ No products found for '{query}'.\n\n📂 Available categories: {categories}"

def list_categories() -> str:
    """List all available product categories"""
    categories = ["📱 Electronics", "🎧 Audio", "📟 Tablets"]
    return "🛍️ Available Categories:\n" + "\n".join([f"  • {cat}" for cat in categories])

# Create Product Catalog Agent
product_catalog_agent = LlmAgent(
    model=Gemini(
        model="gemini-2.5-flash-lite",
        api_key=os.environ.get("GOOGLE_API_KEY")
    ),
    name="product_catalog_agent",
    description="Provides detailed product information, specifications, and search capabilities using mock data.",
    instruction="""
    You are a friendly product catalog specialist using mock demonstration data.
    
    Your capabilities:
    • Get detailed product information with specs and features
    • Search for products by name or category  
    • List available product categories
    
    Available product categories: Electronics, Audio, Tablets
    Example products: iPhone 15 Pro, Samsung Galaxy S24, MacBook Pro, Sony Headphones, iPad Air
    
    Always be helpful and suggest similar products if exact match not found.
    Mention that this is demo data for testing purposes.
    """,
    tools=[get_product_details, search_products_tool, list_categories]
)

print("✅ Product Catalog Agent created!")

# Create A2A app
app = to_a2a(product_catalog_agent, port=8001)
agent = product_catalog_agent


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)


print("🌐 Product Catalog A2A server ready on port 8001")