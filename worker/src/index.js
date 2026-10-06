const ORIGIN = 'https://contensi.github.io';

export default {
  async fetch(request) {
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return new Response('Method Not Allowed', { status: 405, headers: { allow: 'GET, HEAD' } });
    }
    const url = new URL(request.url);
    const upstream = await fetch(new URL(url.pathname + url.search, ORIGIN), {
      method: request.method,
      headers: { 'accept-encoding': request.headers.get('accept-encoding') ?? '' },
      redirect: 'manual',
      cf: { cacheEverything: true, cacheTtl: 300 },
    });
    const headers = new Headers(upstream.headers);
    const location = headers.get('location');
    if (location?.startsWith(ORIGIN)) {
      headers.set('location', url.origin + location.slice(ORIGIN.length));
    }
    for (const name of ['x-github-request-id', 'x-proxy-cache', 'x-fastly-request-id', 'x-served-by', 'x-cache', 'x-cache-hits', 'x-timer', 'via']) {
      headers.delete(name);
    }
    return new Response(upstream.body, { status: upstream.status, headers });
  },
};
