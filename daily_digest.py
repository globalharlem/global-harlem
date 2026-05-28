import json, smtplib, datetime, subprocess, collections
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

YOUR_EMAIL = "baron@globalharlem.com"
YOUR_PASSWORD = "ncemimkznnmevmeh"
TO_EMAIL = "baron@globalharlem.com"
STORIES_FILE = "/Users/barona.carr/Desktop/global-harlem/stories.json"
SCRAPER_FILE = "/Users/barona.carr/Desktop/global-harlem/scraper.py"

def run_scraper():
    print("Running scraper...")
    subprocess.run(["python3", SCRAPER_FILE], check=True)
    print("Scraper done.")

def load_stories():
    with open(STORIES_FILE, "r") as f:
        raw = json.load(f)
    stories = []
    for item in raw:
        if isinstance(item, dict):
            stories.append(item)
        elif isinstance(item, str):
            stories.append({"title": item, "summary": "", "city": "", "source": "", "url": "#", "pillar": "Legacy"})
    return stories

def build_pulse(stories):
    today = datetime.date.today().strftime("%B %d, %Y")
    pillars = {"Legacy": [], "Leadership": [], "Ownership": []}
    cities = collections.Counter()
    for s in stories:
        p = s.get("pillar", "Legacy")
        if p in pillars: pillars[p].append(s)
        else: pillars["Legacy"].append(s)
        if s.get("city"): cities[s["city"]] += 1

    counts = {p: len(v) for p, v in pillars.items()}
    hot_pillar = max(counts, key=counts.get)
    total = sum(counts.values())
    top_city = cities.most_common(1)[0][0] if cities else "New York"
    top_cities = ", ".join([c for c, _ in cities.most_common(3)])

    SIGNALS = {
        "Legacy": "Cultural memory and diaspora identity are dominating the conversation today — arts, heritage, and history stories are surging across sources.",
        "Leadership": "Leadership and civic power are the dominant signal today — Black leaders across politics, business, and community are making moves.",
        "Ownership": "Economic ownership and Black entrepreneurship are surging today — wealth-building and business stories are at a weekly high across all regions.",
    }

    TALKING = {
        "Legacy": [
            "The diaspora is actively preserving and expanding its cultural footprint — this is not nostalgia, it is strategy.",
            f"Today's top cultural activity is concentrated in {top_cities} — three cities, one coordinated narrative.",
            "Brands that want authentic cultural alignment need to be in these conversations now, not after they go mainstream.",
        ],
        "Leadership": [
            f"Black leadership is producing real policy outcomes today — {top_city} is leading the conversation.",
            "This is the moment to position Global Harlem as the intelligence layer between community leadership and brand investment.",
            f"Across {len(cities)} cities today, Black leaders are shaping economic, civic, and cultural outcomes simultaneously.",
        ],
        "Ownership": [
            "The Black wealth-building narrative is accelerating — entrepreneurs are converting visibility into equity at scale.",
            f"Today's ownership stories span {len(cities)} cities — this is a coordinated diaspora economic movement.",
            "Any brand not actively investing in Black ownership narratives right now is already behind.",
        ],
    }

    pulse_signal = SIGNALS[hot_pillar]
    talking_points = TALKING[hot_pillar]

    pulse_html = f"""
    <tr><td style="background:#0A3D2B;padding:44px 36px 36px;border-radius:12px 12px 0 0;">
      <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td><span style="font-size:10px;letter-spacing:3px;text-transform:uppercase;color:#5DDB8A;background:rgba(93,219,138,0.12);padding:5px 12px;border-radius:20px;border:0.5px solid rgba(93,219,138,0.3);">Daily Intelligence</span></td>
          <td align="right" style="font-size:11px;color:rgba(255,255,255,0.35);letter-spacing:2px;">{today}</td>
        </tr>
      </table>
      <h1 style="font-size:38px;font-weight:400;color:#fff;letter-spacing:0.5px;margin:20px 0 6px;font-family:Georgia,serif;">Global Harlem</h1>
      <p style="font-size:13px;color:rgba(255,255,255,0.5);margin:0 0 28px;">What the diaspora is building, saying, and owning — today.</p>
      <table width="100%" cellpadding="0" cellspacing="0" style="background:rgba(0,0,0,0.2);border-radius:8px;"><tr>
        <td align="center" style="padding:14px;border-right:0.5px solid rgba(255,255,255,0.08);"><p style="font-size:24px;font-weight:500;color:#5DDB8A;margin:0;">{total}</p><p style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin:4px 0 0;">Stories</p></td>
        <td align="center" style="padding:14px;border-right:0.5px solid rgba(255,255,255,0.08);"><p style="font-size:24px;font-weight:500;color:#5DDB8A;margin:0;">{len(cities)}</p><p style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin:4px 0 0;">Cities</p></td>
        <td align="center" style="padding:14px;"><p style="font-size:24px;font-weight:500;color:#5DDB8A;margin:0;">{hot_pillar}</p><p style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin:4px 0 0;">Signal</p></td>
      </tr></table>
    </td></tr>

    <tr><td style="padding:0;">
      <table width="100%" cellpadding="0" cellspacing="0">
        <tr><td style="background:#F0FFF6;border-left:4px solid #5DDB8A;padding:22px 36px;">
          <p style="font-size:9px;letter-spacing:3px;text-transform:uppercase;color:#0A7A45;font-weight:700;margin:0 0 8px;">Today's pulse signal</p>
          <p style="font-size:15px;color:#1a3a28;line-height:1.7;margin:0;font-style:italic;">"{pulse_signal}"</p>
        </td></tr>
      </table>
    </td></tr>

    <tr><td style="background:#fff;padding:22px 36px;border-left:0.5px solid #e0e0e0;border-right:0.5px solid #e0e0e0;">
      <p style="font-size:9px;letter-spacing:3px;text-transform:uppercase;color:#999;font-weight:700;margin:0 0 12px;">Say this today — your authority talking points</p>
      <table width="100%" cellpadding="0" cellspacing="0">
        {"".join(f'<tr><td style="padding:6px 0;border-bottom:0.5px solid #f5f5f5;"><table cellpadding="0" cellspacing="0"><tr><td style="padding-right:10px;vertical-align:top;padding-top:2px;"><span style="color:#5DDB8A;font-size:14px;">&#8594;</span></td><td style="font-size:13px;color:#333;line-height:1.6;">{pt}</td></tr></table></td></tr>' for pt in talking_points)}
      </table>
    </td></tr>
    """

    return pulse_html, counts, total, len(cities)

def build_email(stories):
    today = datetime.date.today().strftime("%B %d, %Y")
    pillars = {"Legacy": [], "Leadership": [], "Ownership": []}
    for story in stories:
        p = story.get("pillar", "Legacy")
        if p in pillars: pillars[p].append(story)
        else: pillars["Legacy"].append(story)

    pulse_html, counts, total, city_count = build_pulse(stories)

    COLORS = {
        "Legacy":     {"chip_bg":"#E8F5E9","chip_txt":"#2E7D32","city":"#2E7D32","link":"#4CAF50","tp_dot":"#4CAF50","tp_bg":"#F1FBF3"},
        "Leadership": {"chip_bg":"#E3F2FD","chip_txt":"#1565C0","city":"#1565C0","link":"#2196F3","tp_dot":"#2196F3","tp_bg":"#F0F7FF"},
        "Ownership":  {"chip_bg":"#FFF8E1","chip_txt":"#E65100","city":"#E65100","link":"#FF9800","tp_dot":"#FF9800","tp_bg":"#FFFBF0"},
    }

    TALKING_POINTS = {
        "Legacy": [
            "Black cultural institutions are going global — London, Lagos, Kingston and Paris all had major moves this week.",
            "Anniversary moments are being converted into community infrastructure, not just commemoration.",
            "The pipeline from Black storytelling to mainstream cultural canon is alive and accelerating.",
        ],
        "Leadership": [
            "Black-led municipal leadership is producing measurable economic outcomes.",
            "The digital divide is the new civil rights issue — diaspora leaders are demanding tech infrastructure now.",
            "Community civic organizations are running real operations, not just rhetoric — this is what organized power looks like.",
        ],
        "Ownership": [
            "Black entrepreneurs are converting personal narratives into scalable businesses — the creator-to-owner pipeline is real.",
            "Community infrastructure is being rebuilt and funded by the community, not outside institutions.",
            "Education investment across the diaspora is building a new generation positioned for economic participation from day one.",
        ],
    }

    pillar_sections = ""
    for pillar, items in pillars.items():
        if not items: continue
        c = COLORS[pillar]
        tp_html = "".join(f'<li style="font-size:12px;color:#444;line-height:1.6;padding:3px 0 3px 16px;position:relative;"><span style="position:absolute;left:0;color:{c["tp_dot"]};font-weight:700;">•</span>{pt}</li>' for pt in TALKING_POINTS[pillar])
        story_rows = ""
        for i, s in enumerate(items[:5], 1):
            story_rows += f"""
            <tr><td style="padding:12px 0;border-bottom:0.5px solid #f5f5f5;">
              <table width="100%" cellpadding="0" cellspacing="0"><tr>
                <td width="24" valign="top" style="font-size:12px;color:#ccc;font-weight:600;padding-top:2px;">0{i}</td>
                <td>
                  <p style="margin:0 0 4px;"><span style="font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:{c['city']};">{s.get('city','')}</span><span style="font-size:10px;color:#bbb;"> &middot; {s.get('source','')}</span></p>
                  <p style="font-size:14px;font-weight:600;color:#1a1a1a;margin:0 0 4px;line-height:1.45;">{s.get('title','')}</p>
                  <p style="font-size:12px;color:#666;font-style:italic;margin:0 0 6px;line-height:1.55;">{s.get('summary','No summary available.')}</p>
                  <a href="{s.get('url','#')}" style="font-size:10px;color:{c['link']};text-decoration:none;letter-spacing:1px;text-transform:uppercase;font-weight:700;">Read more &rarr;</a>
                </td>
              </tr></table>
            </td></tr>"""

        pillar_sections += f"""
        <tr><td style="border-bottom:0.5px solid #f0f0f0;">
          <table width="100%" cellpadding="0" cellspacing="0">
            <tr><td style="padding:22px 36px 0;">
              <table cellpadding="0" cellspacing="0"><tr>
                <td><span style="font-size:10px;letter-spacing:2px;text-transform:uppercase;font-weight:700;color:{c['chip_txt']};background:{c['chip_bg']};padding:5px 14px;border-radius:20px;">{pillar}</span></td>
                <td style="padding-left:12px;font-size:11px;color:#ccc;">{len(items)} stories today</td>
              </tr></table>
            </td></tr>
            <tr><td style="padding:14px 36px 0;">
              <div style="background:{c['tp_bg']};border-radius:8px;padding:14px 16px;">
                <p style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:#999;font-weight:700;margin:0 0 8px;">Talking points</p>
                <ul style="list-style:none;margin:0;padding:0;">{tp_html}</ul>
              </div>
            </td></tr>
            <tr><td style="padding:4px 36px 24px;">
              <table width="100%" cellpadding="0" cellspacing="0">{story_rows}</table>
            </td></tr>
          </table>
        </td></tr>"""

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Global Harlem Intelligence Digest</title></head>
<body style="margin:0;padding:20px;background:#f0f0ec;font-family:Georgia,serif;">
<table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center">
<table width="660" cellpadding="0" cellspacing="0" style="max-width:660px;">
  {pulse_html}
  <tr><td style="background:#ffffff;border:0.5px solid #e0e0e0;border-top:none;">
    <table width="100%" cellpadding="0" cellspacing="0">{pillar_sections}</table>
  </td></tr>
  <tr><td style="background:#0A3D2B;padding:28px 36px;border-radius:0 0 12px 12px;">
    <table width="100%" cellpadding="0" cellspacing="0"><tr>
      <td><p style="font-size:14px;color:#fff;font-weight:500;margin:0 0 2px;">Global Harlem</p><p style="font-size:10px;color:rgba(255,255,255,0.3);letter-spacing:2px;text-transform:uppercase;margin:0;">Cultural Intelligence Platform</p></td>
      <td align="right" style="font-size:10px;color:rgba(255,255,255,0.25);letter-spacing:1px;line-height:1.8;">Scraped daily &middot; Powered by AI<br>{TO_EMAIL}</td>
    </tr></table>
  </td></tr>
</table>
</td></tr></table>
</body></html>"""

    text = f"GLOBAL HARLEM PULSE — {today}\n{total} stories · {city_count} cities\n\n"
    for pillar, items in pillars.items():
        if not items: continue
        text += f"── {pillar.upper()} ({len(items)}) ──\n"
        for s in items[:5]:
            text += f"• [{s.get('city','')}] {s.get('title','')}\n  {s.get('url','')}\n\n"
    return text, html

def send_email(text, html):
    today = datetime.date.today().strftime("%B %d, %Y")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Global Harlem Pulse — {today}"
    msg["From"] = YOUR_EMAIL
    msg["To"] = TO_EMAIL
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(YOUR_EMAIL, YOUR_PASSWORD)
        server.sendmail(YOUR_EMAIL, TO_EMAIL, msg.as_string())
    print(f"Digest sent to {TO_EMAIL}")

if __name__ == "__main__":
    run_scraper()
    stories = load_stories()
    print(f"Loaded {len(stories)} stories")
    text, html = build_email(stories)
    send_email(text, html)
