import os
import feedparser
import requests
import json
import datetime

# ── NEWS SOURCES BY CITY ──────────────────────────────────
SOURCES = [
    # ── US NATIONAL ──────────────────────────────────────
    {"city": "National", "region": "domestic", "name": "Black Enterprise", "url": "https://www.blackenterprise.com/feed/"},
    {"city": "National", "region": "domestic", "name": "TheGrio", "url": "https://thegrio.com/feed/"},
    {"city": "National", "region": "domestic", "name": "Essence", "url": "https://www.essence.com/feed/"},
    {"city": "National", "region": "domestic", "name": "Ebony", "url": "https://www.ebony.com/feed/"},
    {"city": "National", "region": "domestic", "name": "Blavity", "url": "https://blavity.com/feed/"},
    {"city": "National", "region": "domestic", "name": "AfroTech", "url": "https://afrotech.com/feed/"},
    {"city": "National", "region": "domestic", "name": "NewsOne", "url": "https://newsone.com/feed/"},
    {"city": "National", "region": "domestic", "name": "Shadow & Act", "url": "https://shadowandact.com/feed/"},
    {"city": "National", "region": "domestic", "name": "EURweb", "url": "https://eurweb.com/feed/"},
    {"city": "National", "region": "domestic", "name": "BlackPressUSA", "url": "https://blackpressusa.com/feed/"},
    {"city": "National", "region": "domestic", "name": "UrbanGeekz", "url": "https://urbangeekz.com/feed/"},
    {"city": "National", "region": "domestic", "name": "OkayPlayer", "url": "https://www.okayplayer.com/feed/"},
    # ── US CITIES ─────────────────────────────────────────
    {"city": "Harlem", "region": "domestic", "name": "Amsterdam News", "url": "https://amsterdamnews.com/feed/"},
    {"city": "Harlem", "region": "domestic", "name": "Harlem World", "url": "https://www.harlemworldmagazine.com/feed/"},
    {"city": "Atlanta", "region": "domestic", "name": "Atlanta Black Star", "url": "https://atlantablackstar.com/feed/"},
    {"city": "Atlanta", "region": "domestic", "name": "Atlanta Tribune", "url": "https://atlantatribune.com/feed/"},
    {"city": "Washington D.C.", "region": "domestic", "name": "The Root", "url": "https://www.theroot.com/rss"},
    {"city": "Washington D.C.", "region": "domestic", "name": "Washington Informer", "url": "https://washingtoninformer.com/feed/"},
    {"city": "Chicago", "region": "domestic", "name": "Chicago Defender", "url": "https://chicagodefender.com/feed/"},
    {"city": "Houston", "region": "domestic", "name": "Defender Network", "url": "https://defendernetwork.com/feed/"},
    {"city": "Houston", "region": "domestic", "name": "Afro American News", "url": "https://aframnews.com/feed/"},
    {"city": "Los Angeles", "region": "domestic", "name": "LA Sentinel", "url": "https://lasentinel.net/feed/"},
    {"city": "Baltimore", "region": "domestic", "name": "Afro American", "url": "https://afro.com/feed/"},
    {"city": "Detroit", "region": "domestic", "name": "Michigan Chronicle", "url": "https://michiganchronicle.com/feed/"},
    {"city": "Philadelphia", "region": "domestic", "name": "Philadelphia Tribune", "url": "https://www.phillytrib.com/feed/"},
    {"city": "New Orleans", "region": "domestic", "name": "Louisiana Weekly", "url": "https://louisianaweekly.com/feed/"},
    {"city": "Memphis", "region": "domestic", "name": "Tri-State Defender", "url": "https://tri-statedefender.com/feed/"},
    {"city": "Cleveland", "region": "domestic", "name": "Call & Post", "url": "https://callandpost.com/feed/"},
    {"city": "Oakland", "region": "domestic", "name": "Oakland Post", "url": "https://oaklandpost.org/feed/"},
    # ── CARIBBEAN ─────────────────────────────────────────
    {"city": "Kingston", "region": "caribbean", "name": "Jamaica Gleaner", "url": "https://jamaica-gleaner.com/feed/rss.xml"},
    {"city": "Trinidad", "region": "caribbean", "name": "Trinidad Express", "url": "https://trinidadexpress.com/feed/"},
    {"city": "Barbados", "region": "caribbean", "name": "Barbados Today", "url": "https://barbadostoday.bb/feed/"},
    {"city": "Guyana", "region": "caribbean", "name": "Stabroek News", "url": "https://www.stabroeknews.com/feed/"},
    # ── AFRICA ────────────────────────────────────────────
    {"city": "Lagos", "region": "africa", "name": "Pulse Nigeria", "url": "https://www.pulse.ng/rss"},
    {"city": "Lagos", "region": "africa", "name": "Guardian Nigeria", "url": "https://guardian.ng/feed/"},
    {"city": "Lagos", "region": "africa", "name": "Vanguard Nigeria", "url": "https://www.vanguardngr.com/feed/"},
    {"city": "Accra", "region": "africa", "name": "Pulse Ghana", "url": "https://www.pulse.com.gh/rss"},
    {"city": "Accra", "region": "africa", "name": "Ghana Web", "url": "https://www.ghanaweb.com/GhanaHomePage/rss/index.xml"},
    {"city": "Nairobi", "region": "africa", "name": "Daily Nation Kenya", "url": "https://nation.africa/kenya/rss.xml"},
    {"city": "Johannesburg", "region": "africa", "name": "Daily Maverick", "url": "https://www.dailymaverick.co.za/feed/"},
    {"city": "Pan-Africa", "region": "africa", "name": "OkayAfrica", "url": "https://www.okayafrica.com/feeds/feed.rss"},
    {"city": "Pan-Africa", "region": "africa", "name": "Afrocritik", "url": "https://afrocritik.com/feed/"},
    {"city": "Pan-Africa", "region": "africa", "name": "Africa Is A Country", "url": "https://africasacountry.com/feed/"},
    {"city": "Pan-Africa", "region": "africa", "name": "AllAfrica", "url": "https://allafrica.com/tools/headlines/rdf/latest/headlines.rdf"},
    # ── UK & EUROPE ───────────────────────────────────────
    {"city": "London", "region": "europe", "name": "Black Ballad", "url": "https://blackballad.co.uk/feed"},
    {"city": "London", "region": "europe", "name": "The Voice UK", "url": "https://www.voice-online.co.uk/feed/"},
    {"city": "Paris", "region": "europe", "name": "Afropean", "url": "https://afropean.com/feed/"},
    # ── CANADA ────────────────────────────────────────────
    {"city": "Toronto", "region": "canada", "name": "Afro Toronto", "url": "https://afrotoronto.com/feed/"},
    # ── BRAZIL ────────────────────────────────────────────
    {"city": "São Paulo", "region": "latam", "name": "Alma Preta", "url": "https://almapreta.com.br/feed/"},
]

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

def categorize_story(title, summary, city):
    """Send story to Claude to categorize by pillar and summarize."""
    prompt = f"""You are the editorial AI for Global Harlem, a cultural intelligence platform for the Black diaspora.

Analyze this news story and respond with ONLY a JSON object, no other text:

Title: {title}
Summary: {summary}
City: {city}

Respond with exactly this JSON format:
{{
  "pillar": "Legacy" or "Leadership" or "Ownership",
  "summary": "One sentence summary in 20 words or less that captures the cultural significance",
  "relevant": true or false
}}

Pillar definitions:
- Legacy: History, culture, arts, music, community memory, cultural preservation, diaspora identity
- Leadership: Business leaders, community organizers, political figures, entrepreneurs building something
- Ownership: Economic power, property, financial literacy, Black-owned businesses, wealth building

Set relevant to false if the story has no connection to Black culture or the diaspora."""

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 200,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        if response.status_code != 200:
            print(f"  API error {response.status_code}: {response.text[:100]}")
            return None
        result = response.json()
        if "content" not in result:
            print(f"  Unexpected response: {str(result)[:100]}")
            return None
        text = result["content"][0]["text"].strip()
        import re
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"  JSON parse error: {e}")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None

def scrape_source(source):
    """Fetch and parse RSS feed from one source."""
    print(f"Scraping {source['name']} ({source['city']})...")
    stories = []
    try:
        feed = feedparser.parse(source["url"])
        entries = feed.entries[:5]  # Max 5 stories per source
        for entry in entries:
            title = entry.get("title", "").strip()
            summary = entry.get("summary", entry.get("description", "")).strip()
            link = entry.get("link", "")
            published = entry.get("published", str(datetime.date.today()))
            # Clean HTML from summary
            import re
            summary = re.sub('<[^<]+?>', '', summary)[:500]
            if not title or not link:
                continue
            print(f"  Categorizing: {title[:60]}...")
            categorized = categorize_story(title, summary, source["city"])
            if categorized and categorized.get("relevant"):
                stories.append({
                    "title": title,
                    "summary": categorized.get("summary", summary[:100]),
                    "pillar": categorized.get("pillar", "Legacy"),
                    "city": source["city"],
                    "region": source["region"],
                    "source": source["name"],
                    "link": link,
                    "published": published,
                    "scraped": str(datetime.datetime.now())
                })
    except Exception as e:
        print(f"  Error scraping {source['name']}: {e}")
    return stories

def run_scraper():
    """Main scraper function."""
    print(f"\nGlobal Harlem Cultural Intelligence Scraper")
    print(f"Running at {datetime.datetime.now()}")
    print("=" * 50)
    all_stories = []
    for source in SOURCES:
        stories = scrape_source(source)
        all_stories.extend(stories)
        print(f"  Found {len(stories)} relevant stories")
    # Sort by city then pillar
    all_stories.sort(key=lambda x: (x["pillar"], x["city"]))
    # Save to JSON
    output = {
        "last_updated": str(datetime.datetime.now()),
        "total_stories": len(all_stories),
        "stories": all_stories
    }
    output_path = "/Users/barona.carr/Desktop/global-harlem/stories.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nDone. {len(all_stories)} stories saved to stories.json")
    print("=" * 50)

if __name__ == "__main__":
    run_scraper()
# --- appended sources ---
EXTRA_SOURCES = [
    # ── US NATIONAL ──────────────────────────────────────
    {"city": "National", "region": "domestic", "name": "Black Enterprise", "url": "https://www.blackenterprise.com/feed/"},
    {"city": "National", "region": "domestic", "name": "TheGrio", "url": "https://thegrio.com/feed/"},
    {"city": "National", "region": "domestic", "name": "Essence", "url": "https://www.essence.com/feed/"},
    {"city": "National", "region": "domestic", "name": "Ebony", "url": "https://www.ebony.com/feed/"},
    {"city": "National", "region": "domestic", "name": "Blavity", "url": "https://blavity.com/feed/"},
    {"city": "National", "region": "domestic", "name": "AfroTech", "url": "https://afrotech.com/feed/"},
    {"city": "National", "region": "domestic", "name": "NewsOne", "url": "https://newsone.com/feed/"},
    {"city": "National", "region": "domestic", "name": "Shadow & Act", "url": "https://shadowandact.com/feed/"},
    {"city": "National", "region": "domestic", "name": "EURweb", "url": "https://eurweb.com/feed/"},
    {"city": "National", "region": "domestic", "name": "BlackPressUSA", "url": "https://blackpressusa.com/feed/"},
    {"city": "National", "region": "domestic", "name": "UrbanGeekz", "url": "https://urbangeekz.com/feed/"},
    {"city": "National", "region": "domestic", "name": "OkayPlayer", "url": "https://www.okayplayer.com/feed/"},
    # ── US CITIES ─────────────────────────────────────────
    {"city": "Harlem", "region": "domestic", "name": "Amsterdam News", "url": "https://amsterdamnews.com/feed/"},
    {"city": "Harlem", "region": "domestic", "name": "Harlem World", "url": "https://www.harlemworldmagazine.com/feed/"},
    {"city": "Atlanta", "region": "domestic", "name": "Atlanta Black Star", "url": "https://atlantablackstar.com/feed/"},
    {"city": "Atlanta", "region": "domestic", "name": "Atlanta Tribune", "url": "https://atlantatribune.com/feed/"},
    {"city": "Washington D.C.", "region": "domestic", "name": "The Root", "url": "https://www.theroot.com/rss"},
    {"city": "Washington D.C.", "region": "domestic", "name": "Washington Informer", "url": "https://washingtoninformer.com/feed/"},
    {"city": "Chicago", "region": "domestic", "name": "Chicago Defender", "url": "https://chicagodefender.com/feed/"},
    {"city": "Houston", "region": "domestic", "name": "Defender Network", "url": "https://defendernetwork.com/feed/"},
    {"city": "Houston", "region": "domestic", "name": "Afro American News", "url": "https://aframnews.com/feed/"},
    {"city": "Los Angeles", "region": "domestic", "name": "LA Sentinel", "url": "https://lasentinel.net/feed/"},
    {"city": "Baltimore", "region": "domestic", "name": "Afro American", "url": "https://afro.com/feed/"},
    {"city": "Detroit", "region": "domestic", "name": "Michigan Chronicle", "url": "https://michiganchronicle.com/feed/"},
    {"city": "Philadelphia", "region": "domestic", "name": "Philadelphia Tribune", "url": "https://www.phillytrib.com/feed/"},
    {"city": "New Orleans", "region": "domestic", "name": "Louisiana Weekly", "url": "https://louisianaweekly.com/feed/"},
    {"city": "Memphis", "region": "domestic", "name": "Tri-State Defender", "url": "https://tri-statedefender.com/feed/"},
    {"city": "Cleveland", "region": "domestic", "name": "Call & Post", "url": "https://callandpost.com/feed/"},
    {"city": "Oakland", "region": "domestic", "name": "Oakland Post", "url": "https://oaklandpost.org/feed/"},
    # ── CARIBBEAN ─────────────────────────────────────────
    {"city": "Kingston", "region": "caribbean", "name": "Jamaica Gleaner", "url": "https://jamaica-gleaner.com/feed/rss.xml"},
    {"city": "Trinidad", "region": "caribbean", "name": "Trinidad Express", "url": "https://trinidadexpress.com/feed/"},
    {"city": "Barbados", "region": "caribbean", "name": "Barbados Today", "url": "https://barbadostoday.bb/feed/"},
    {"city": "Guyana", "region": "caribbean", "name": "Stabroek News", "url": "https://www.stabroeknews.com/feed/"},
    # ── AFRICA ────────────────────────────────────────────
    {"city": "Lagos", "region": "africa", "name": "Pulse Nigeria", "url": "https://www.pulse.ng/rss"},
    {"city": "Lagos", "region": "africa", "name": "Guardian Nigeria", "url": "https://guardian.ng/feed/"},
    {"city": "Lagos", "region": "africa", "name": "Vanguard Nigeria", "url": "https://www.vanguardngr.com/feed/"},
    {"city": "Accra", "region": "africa", "name": "Pulse Ghana", "url": "https://www.pulse.com.gh/rss"},
    {"city": "Accra", "region": "africa", "name": "Ghana Web", "url": "https://www.ghanaweb.com/GhanaHomePage/rss/index.xml"},
    {"city": "Nairobi", "region": "africa", "name": "Daily Nation Kenya", "url": "https://nation.africa/kenya/rss.xml"},
    {"city": "Johannesburg", "region": "africa", "name": "Daily Maverick", "url": "https://www.dailymaverick.co.za/feed/"},
    {"city": "Pan-Africa", "region": "africa", "name": "OkayAfrica", "url": "https://www.okayafrica.com/feeds/feed.rss"},
    {"city": "Pan-Africa", "region": "africa", "name": "Afrocritik", "url": "https://afrocritik.com/feed/"},
    {"city": "Pan-Africa", "region": "africa", "name": "Africa Is A Country", "url": "https://africasacountry.com/feed/"},
    {"city": "Pan-Africa", "region": "africa", "name": "AllAfrica", "url": "https://allafrica.com/tools/headlines/rdf/latest/headlines.rdf"},
    # ── UK & EUROPE ───────────────────────────────────────
    {"city": "London", "region": "europe", "name": "Black Ballad", "url": "https://blackballad.co.uk/feed"},
    {"city": "London", "region": "europe", "name": "The Voice UK", "url": "https://www.voice-online.co.uk/feed/"},
    {"city": "Paris", "region": "europe", "name": "Afropean", "url": "https://afropean.com/feed/"},
    # ── CANADA ────────────────────────────────────────────
    {"city": "Toronto", "region": "canada", "name": "Afro Toronto", "url": "https://afrotoronto.com/feed/"},
    # ── BRAZIL ────────────────────────────────────────────
    {"city": "São Paulo", "region": "latam", "name": "Alma Preta", "url": "https://almapreta.com.br/feed/"},
]
SOURCES.extend(EXTRA_SOURCES)
