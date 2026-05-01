import os
import feedparser
import requests
import json
import datetime

# ── NEWS SOURCES BY CITY ──────────────────────────────────
SOURCES = [
    # DOMESTIC
    {"city": "Harlem", "region": "domestic", "name": "Amsterdam News", "url": "https://amsterdamnews.com/feed/"},
    {"city": "Harlem", "region": "domestic", "name": "Harlem World", "url": "https://www.harlemworldmagazine.com/feed/"},
    {"city": "Atlanta", "region": "domestic", "name": "Atlanta Black Star", "url": "https://atlantablackstar.com/feed/"},
    {"city": "Washington D.C.", "region": "domestic", "name": "The Root", "url": "https://www.theroot.com/rss"},
    {"city": "Chicago", "region": "domestic", "name": "Chicago Defender", "url": "https://chicagodefender.com/feed/"},
    {"city": "Houston", "region": "domestic", "name": "Defender Network", "url": "https://defendernetwork.com/feed/"},
    {"city": "Los Angeles", "region": "domestic", "name": "LA Sentinel", "url": "https://lasentinel.net/feed"},
    {"city": "Detroit", "region": "domestic", "name": "Michigan Chronicle", "url": "https://michiganchronicle.com/feed"},
    {"city": "Philadelphia", "region": "domestic", "name": "Philadelphia Tribune", "url": "https://www.phillytrib.com/feed"},
    {"city": "New Orleans", "region": "domestic", "name": "Louisiana Weekly", "url": "https://www.louisianaweekly.com/feed/"},
    # GLOBAL
    {"city": "London", "region": "global", "name": "Black Ballad", "url": "https://blackballad.co.uk/feed"},
    {"city": "London", "region": "global", "name": "The Voice UK", "url": "https://www.voice-online.co.uk/feed/"},
    {"city": "Accra", "region": "global", "name": "Pulse Ghana", "url": "https://www.pulse.com.gh/rss"},
    {"city": "Lagos", "region": "global", "name": "Pulse Nigeria", "url": "https://www.pulse.ng/rss"},
    {"city": "Lagos", "region": "global", "name": "Guardian Nigeria", "url": "https://guardian.ng/feed/"},
    {"city": "Toronto", "region": "global", "name": "Afro Toronto", "url": "https://afrotoronto.com/feed/"},
    {"city": "Kingston", "region": "global", "name": "Jamaica Gleaner", "url": "https://jamaica-gleaner.com/feed/rss.xml"},
    {"city": "Paris", "region": "global", "name": "Afropean", "url": "https://afropean.com/feed/"},
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
