from google.adk.agents import Agent
import datetime
from zoneinfo import ZoneInfo

# Simple tool: get weather for a city
def get_weather(city: str) -> dict:
    if city.lower() == "new york":
        return {"status": "success", "report": "Sunny, 25°C"}
    else:
        return {"status": "error", "error_message": f"No weather data for {city}"}

# Simple tool: get current time for a city
def get_current_time(city: str) -> dict:
    if city.lower() == "new york":
        tz = ZoneInfo("America/New_York")
        now = datetime.datetime.now(tz)
        return {"status": "success", "report": now.isoformat()}
    else:
        return {"status": "error", "error_message": f"Unknown city {city}"}

# Root agent definition
root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description="Agent that provides weather & time info",
    instruction="I can answer questions about weather or time in a city.",
    tools=[get_weather, get_current_time],
    api_key="env:GOOGLE_API_KEY",
)
