const express = require('express' );
const { createProxyMiddleware } = require('http-proxy-middleware' );

const app = express();
const PORT = 3000;

// Serve the static files from the 'public' directory
app.use(express.static('public'));

// The proxy middleware
const proxy = createProxyMiddleware({
  // The target will be set dynamically by a router function
  router: (req) => {
    // Extract the target URL from the query parameter
    const targetUrl = req.query.url;
    if (targetUrl) {
      // Ensure the target URL has a protocol
      return targetUrl.startsWith('http' ) ? targetUrl : `https://` + targetUrl;
    }
    return 'https://example.com'; // Default target if no URL is provided
  },
  changeOrigin: true,
  pathRewrite: (path, req ) => {
    // Remove the '/proxy?url=...' part from the path
    return path.replace(/^\/proxy/, '');
  },
  logLevel: 'silent', // Keep the server console clean
  selfHandleResponse: true, // Important: allows us to modify the response
  onProxyRes: (proxyRes, req, res) => {
    let body = [];
    proxyRes.on('data', (chunk) => body.push(chunk));
    proxyRes.on('end', () => {
      let html = Buffer.concat(body).toString();

      // Inject our custom console script into the head of the proxied page
      const injectionScript = `
        <script>
          // Intercept console.log on the proxied page
          const originalLog = console.log;
          console.log = function(...args) {
            window.parent.postMessage({ type: 'console-log', data: args }, '*');
            originalLog.apply(console, args);
          };
          window.addEventListener('error', function(e) {
            window.parent.postMessage({ type: 'console-error', data: e.message }, '*');
          });
        </script>
      `;
      html = html.replace('</head>', `${injectionScript}</head>`);
      
      res.end(html);
    });
  }
});

// Route for proxying requests
app.use('/proxy', proxy);

app.listen(PORT, () => {
  console.log(`Proxy server running on http://localhost:${PORT}` );
});
