const rateLimit = new Map();

export default async function handler(req, res) {
  // Rate limiting: 5 requests per hour per IP
  const ip = req.headers['x-forwarded-for'] || req.headers['x-real-ip'] || 'unknown';
  const now = Date.now();
  const windowMs = 60 * 60 * 1000; // 1 hour
  const maxRequests = 5;

  if (!rateLimit.has(ip)) rateLimit.set(ip, []);
  const timestamps = rateLimit.get(ip).filter(t => now - t < windowMs);
  
  if (timestamps.length >= maxRequests) {
    return res.status(429).json({ error: 'Rate limit exceeded. Try again later.' });
  }
  
  timestamps.push(now);
  rateLimit.set(ip, timestamps);

  // Clean old entries periodically
  if (rateLimit.size > 1000) {
    for (const [key, val] of rateLimit) {
      if (val.filter(t => now - t < windowMs).length === 0) rateLimit.delete(key);
    }
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify(req.body)
    });
    const data = await response.json();
    res.status(200).json(data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to generate report' });
  }
}
