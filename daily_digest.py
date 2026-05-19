import json, datetime

STORIES_FILE = "/root/global-harlem/stories.json"

def load_stories():
    with open(STORIES_FILE) as f:
        data = json.load(f)
    return data["stories"]

def build_email(stories):
    today = datetime.date.today().strftime("%B %d, %Y")
    pillars = {"Leadership": [], "Legacy": [], "Ownership": []}
    for s in stories:
        p = s.get("pillar")
        if p in pillars:
            pillars[p].append(s)

    pillar_colors = {"Leadership": "#2D6A4F", "Legacy": "#1B4332", "Ownership": "#0D1B2A"}
    pillar_icons = {"Leadership": "◆", "Legacy": "◉", "Ownership": "▲"}

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&family=Space+Mono&display=swap" rel="stylesheet">
</head>
<body style="margin:0;padding:0;background:#F0EDE6;font-family:'DM Sans',sans-serif;">
<div style="max-width:640px;margin:0 auto;background:#FAF7F0;">

<!-- MASTHEAD -->
<div style="background:#0D1B2A;padding:0;">
  <div style="padding:40px 48px 28px;">
    <p style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:0.25em;color:rgba(250,247,240,0.4);margin:0 0 12px;text-transform:uppercase;">Cultural Intelligence Digest</p>
    <h1 style="font-family:'DM Serif Display',serif;font-size:36px;color:#FAF7F0;margin:0 0 6px;font-weight:400;line-height:1.1;">GLOBAL<br>HARLEM</h1>
    <p style="font-family:'Space Mono',monospace;font-size:10px;color:rgba(250,247,240,0.5);margin:0;letter-spacing:0.1em;">{today.upper()}</p>
  </div>
  <div style="background:#1B4332;padding:12px 48px;display:flex;gap:24px;">
    <span style="font-family:'Space Mono',monospace;font-size:9px;color:rgba(250,247,240,0.7);letter-spacing:0.15em;">◆ LEADERSHIP &nbsp;{len(pillars['Leadership'])}</span>
    <span style="font-family:'Space Mono',monospace;font-size:9px;color:rgba(250,247,240,0.7);letter-spacing:0.15em;">◉ LEGACY &nbsp;{len(pillars['Legacy'])}</span>
    <span style="font-family:'Space Mono',monospace;font-size:9px;color:rgba(250,247,240,0.7);letter-spacing:0.15em;">▲ OWNERSHIP &nbsp;{len(pillars['Ownership'])}</span>
    <span style="font-family:'Space Mono',monospace;font-size:9px;color:rgba(250,247,240,0.5);letter-spacing:0.15em;margin-left:auto;">{len(stories)} STORIES TODAY</span>
  </div>
</div>

"""

    for pillar, items in pillars.items():
        if not items:
            continue
        color = pillar_colors[pillar]
        icon = pillar_icons[pillar]
        html += f"""
<!-- {pillar.upper()} -->
<div style="padding:32px 48px 8px;">
  <div style="border-left:3px solid {color};padding-left:16px;margin-bottom:24px;">
    <p style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:0.2em;color:{color};margin:0 0 2px;text-transform:uppercase;">{icon} {pillar}</p>
    <p style="font-size:11px;color:#888;margin:0;">{len(items)} stories</p>
  </div>
"""
        for s in items[:6]:
            html += f"""
  <div style="margin-bottom:24px;padding-bottom:24px;border-bottom:1px solid #E8E3D8;">
    <p style="font-family:'Space Mono',monospace;font-size:9px;color:#999;margin:0 0 6px;letter-spacing:0.1em;text-transform:uppercase;">{s.get('city','').upper()} &nbsp;·&nbsp; {s.get('source','')}</p>
    <a href="{s.get('link','#')}" style="font-family:'DM Serif Display',serif;font-size:18px;color:#0D1B2A;text-decoration:none;line-height:1.3;display:block;margin-bottom:8px;">{s.get('title','')}</a>
    <p style="font-size:13px;color:#555;margin:0;line-height:1.6;">{s.get('summary','')}</p>
  </div>
"""
        html += "</div>"

    html += f"""
<!-- FOOTER -->
<div style="background:#0D1B2A;padding:32px 48px;margin-top:16px;">
  <p style="font-family:'DM Serif Display',serif;font-size:20px;color:#FAF7F0;margin:0 0 4px;">GLOBAL HARLEM</p>
  <p style="font-family:'Space Mono',monospace;font-size:9px;color:rgba(250,247,240,0.3);margin:0 0 16px;letter-spacing:0.15em;">LOCAL ROOTS. GLOBAL IMPACT.</p>
  <p style="font-size:11px;color:rgba(250,247,240,0.25);margin:0;">Cultural Intelligence Digest · {today} · globalharlem.com</p>
</div>

</div></body></html>"""

    text = f"GLOBAL HARLEM — {today}\n\n"
    for pillar, items in pillars.items():
        text += f"\n── {pillar.upper()} ({len(items)} stories) ──\n"
        for s in items[:6]:
            text += f"\n• [{s.get('city','')}] {s.get('title','')}\n  {s.get('summary','')}\n  {s.get('link','')}\n"

    return text, html
