# tools.py
from agents import function_tool
import requests

# (Include get_bible_verse, get_weather, get_currency_rate, random_joke, random_cat as above)



@function_tool
def get_bible_verse(reference: str) -> str:
    url = f"https://bible-api.com/{reference}"
    resp = requests.get(url)
    if resp.status_code != 200:
        return f"❌ Could not fetch verse '{reference}'"
    data = resp.json()
    reference = data.get("reference", reference)
    verse_text = data.get("text", "").strip()
    translation = data.get("translation_id", "WEB")
    return f"{reference} ({translation}): “{verse_text}”"


@function_tool
def get_weather(location: str) -> str:
    # Simple lat/long lookup via Open-Meteo
    # (for production, use geocoding or static mapping)
    import requests
    parts = [p.strip() for p in location.split(',')]
    city = parts[0]
    lat, lon = {"Accra": (5.6037, -0.1870)}.get(city, (0, 0))
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    resp = requests.get(url)
    if resp.status_code != 200:
       return f"❌ Couldn't fetch weather for {location}"
    data = resp.json().get("current_weather", {})
    return f"🌤️ Weather in {city}: {data.get('temperature')}°C, wind {data.get('windspeed')} km/h"

@function_tool
def get_currency_rate(pair: str) -> str:
    base, tgt = pair.upper().split('_')
    import requests
    resp = requests.get(f"https://api.exchangerate.host/convert?from={base}&to={tgt}")
    if resp.status_code != 200:
        return f"❌ Could not fetch rate {base}_{tgt}"
    rate = resp.json().get("result")
    return f"1 {base} = {rate:.4f} {tgt}"

@function_tool
def random_joke() -> str:
    import requests
    resp = requests.get("https://official-joke-api.appspot.com/random_joke")
    if resp.status_code != 200:
        return "❌ Couldn't fetch a joke"
    data = resp.json()
    return f"{data['setup']} … {data['punchline']}"

@function_tool
def random_cat() -> str:
    import requests
    resp = requests.get("https://aws.random.cat/meow")
    if resp.status_code != 200:
        return "❌ Couldn't fetch a cat image"
    return resp.json().get("file", "")


@function_tool
def run_python(code: str) -> str:
    try:
        exec_locals = {}
        exec(code, {}, exec_locals)
        return str(exec_locals.get("result", "Done"))
    except Exception as e:
        return f"Error: {e}"

@function_tool
def encourage(name: str) -> str:
    return f"{name}, never give up — you're chosen to build, lead, and inspire 💡🔥"

# Export them all
all_tools = [get_bible_verse,
    get_weather,
    get_currency_rate,
    random_joke,
    random_cat,run_python, encourage]
