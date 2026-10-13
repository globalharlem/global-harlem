# Global Harlem site

Plain HTML, no build step. Six pages: / , /baron-carr , /trust-audit , /take-audit , /workshops , /contact.

## Deploy
1. Put everything in this folder at the root of your GitHub repo (or drag the folder into Vercel).
2. Vercel: New Project > import the repo > Framework "Other" > Deploy.
3. Settings > Domains > add globalharlem.com.

## Fill in before announcing
- Contact form: in contact.html replace YOUR_CONTACT_FORM_ID with your Formspree form ID.
- Newsletter: in index.html replace YOUR_NEWSLETTER_FORM_ID (Formspree emails you signups until you move to beehiiv).
- Photo: already included (baron.jpg).
- Trust Audit saving (optional): tool/index.html, set SUPABASE_URL and SUPABASE_ANON_KEY.
- Vimeo: for each video, Privacy > allow embedding on globalharlem.com.
- Footer: fiscal sponsor credit line goes at the marked comment in each page footer, after the agreement is signed. No "nonprofit" wording or Donate button until then.
- Confirm peace.globalharlem.com is the right address (used on home and /baron-carr).
- Workshops wording and Trust Audit copy are drafts. Edit the .html files directly.
