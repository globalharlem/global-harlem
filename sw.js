const CACHE = 'gh-v1';
const URLS = ['/', '/intelligence.html', '/pulse.html', '/trust.html', '/about.html'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(URLS)));
});

self.addEventListener('fetch', e => {
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});
