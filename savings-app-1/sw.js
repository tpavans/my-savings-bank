const C = "savings-v10-live";
const A = [
  "./",
  "index.html",
  "manifest.json",
  "icon-192.png",
  "icon-512.png",
  "icon-maskable-512.png",
  "apple-touch-icon.png",
  "favicon.png",
  "favicon.ico",
  "app-logo.png"
];

self.addEventListener("install", e => {
  self.skipWaiting();
  e.waitUntil(caches.open(C).then(c => c.addAll(A)));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys().then(k => Promise.all(k.map(x => (x !== C ? caches.delete(x) : null)))).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", e => {
  // Network-First for HTML/navigation so code updates appear instantly!
  if (e.request.mode === "navigate" || e.request.destination === "document" || e.request.url.endsWith(".html") || e.request.url.endsWith("/")) {
    e.respondWith(
      fetch(e.request)
        .then(res => {
          if (res && res.status === 200) {
            const clone = res.clone();
            caches.open(C).then(cache => cache.put(e.request, clone));
          }
          return res;
        })
        .catch(() => caches.match(e.request).then(r => r || caches.match("index.html")))
    );
    return;
  }
  // Cache-first for images & static assets with fallback
  e.respondWith(
    caches.match(e.request).then(r => r || fetch(e.request))
  );
});
