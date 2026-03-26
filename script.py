import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

load_dotenv()
# .strip() removes accidental spaces or newline characters from the .env file
API_KEY = os.getenv("OPENWEATHER_API_KEY", "").strip()
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def generate_apology(customer, city, condition):
    messages = {
        "Rain": f"Hi {customer}, the rain in {city} is a bit heavier than expected! Your order is slightly delayed.",
        "Snow": f"Hi {customer}, snowy tracks in {city} are slowing us down. Your order is delayed.",
        "Extreme": f"Hi {customer}, extreme weather in {city} has paused deliveries for safety."
    }
    return messages.get(condition, f"Hi {customer}, due to weather in {city}, your delivery is delayed.")

async def fetch_weather(session, order):
    city = order['city']
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    
    try:
        async with session.get(BASE_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                # logs data in the CLI in a formatted way
                print(json.dumps(data,indent=2))
                main_condition = data['weather'][0]['main']
                
                if main_condition in ["Rain", "Snow", "Extreme","Clouds","Smoke"]:
                    order['status'] = "Delayed"
                    order['apology'] = generate_apology(order['customer'], city, main_condition)
                return order
            else:
                print(f"❌ API Error for {city}: Status {response.status}")
                return order
    except Exception as e:
        print(f"🔥 Error processing {city}: {e}")
        return order

async def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_path, "orders.json")
    output_path = os.path.join(base_path, "orders_updated.json")

    if not os.path.exists(input_path):
        print(f"❌ Error: Cannot find {input_path}")
        return

    with open(input_path, 'r') as f:
        orders = json.load(f)

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_weather(session, order) for order in orders]
        updated_orders = await asyncio.gather(*tasks)

    with open(output_path, 'w') as f:
        json.dump(updated_orders, f, indent=2)
    
    print(f"\n✅ Done! Check results in: {output_path}")

if __name__ == "__main__":
    asyncio.run(main())