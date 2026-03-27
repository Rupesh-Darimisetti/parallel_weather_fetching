# setup of the application
- Python 3.8+
- pip installation tool
- create a venv using ``` python -m venv .venv```
- activate it using ``` source .venv/Script/activate```
- install dependencies present in **requirement.txt** using
  - ``` pip install -r requirements.txt```
- copy the **.env.example** as **.env** using cmd
  - ```cp .env.example .env```
- place your open weather api key in **.env** file under the name **OPENWEATHER_API_KEY**.
- Place the country and details in a folder called **orders.json** in the following format
- after running the script an updated file of order get displayed in the **order_updated.json** file.

# The code outline
- Its run prallel so that all the response gets at once without much delay using asynio http method in python


# APIs Used: OpenWeatherMap API (Free Tier)
1. The Data Sample (Save as orders.json)
"Please use this JSON as your local database. Your script must process these specific cities."
```JSON
[
  {
    "order_id": "1001",
    "customer": "Alice Smith",
    "city": "New York",
    "status": "Pending"
  },
  {
    "order_id": "1002",
    "customer": "Bob Jones",
    "city": "Mumbai",
    "status": "Pending"
  },
  {
    "order_id": "1003",
    "customer": "Charlie Green",
    "city": "London",
    "status": "Pending"
  },
  {
    "order_id": "1004",
    "customer": "InvalidCity123",
    "city": "InvalidCity123",
    "status": "Pending"
  }
]
```

The Mission
Build a script that checks the weather for each order's city and flags potential delivery delays.

- Parallel Fetching: Loop through the orders.json and fetch the current weather for each city using the OpenWeatherMap API.
- Used asyncio.gather in Python.

The "Golden Flow" Logic:
- If the weather "main" status is Rain, Snow, or Extreme, update the order status to Delayed in the JSON.
- AI Challenge: Use an AI tool to write a "Weather-Aware Apology" function. The script should generate a personalized message like: "Hi Alice, your order to New York is delayed due to heavy rain. We appreciate your patience!"

- Resilience:
Error Handling: Your script must handle the InvalidCity123 case. The error for that city should be logged, but the script must not crash—it should finish processing the other valid cities.
