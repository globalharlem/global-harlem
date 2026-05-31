export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  
  const { email } = req.body;
  if (!email || !email.includes('@') || !email.includes('.')) {
    return res.status(400).json({ error: 'Valid email required' });
  }

  // Store email on your DigitalOcean server
  try {
    await fetch('http://167.99.3.176/subscribe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, date: new Date().toISOString() })
    });
  } catch(e) {}

  // Also log to Vercel (backup)
  console.log('SUBSCRIBER:', email, new Date().toISOString());
  
  res.status(200).json({ success: true });
}
