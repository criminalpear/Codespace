const express = require('express' );
const { createProxyMiddleware } = require('http-proxy-middleware' );
const { URL } = require('url'); // Import the URL module

const app = express();
const PORT = 3000;

// Serve the static files from the 'public' directory
app.use(express.static('public'));

// The proxy middleware
const proxy = createProxyMiddleware({
  router: (req) => {
    const targetUrl = req.query.url;
    if (!targetUrl) {
      return 'https://example.com'; // Default target
    }
    // Use the URL constructor for robust parsing
    const target = new URL(targetUrl.startsWith('http' ) ? targetUrl : `https://${targetUrl}` );
    return target;
  },
  changeOrigin: true,
  pathRewrite: (path, req) => {
    // This function now needs to return just the path and search part of the target URL
    const targetUrl = req.query.url;
    const target = new URL(targetUrl.startsWith('http' ) ? targetUrl : `https://${targetUrl}` );
    // Return the pathname and search from the original target URL
    // This prevents the proxy from appending our own query string (/proxy?url=...) to the target request
    return target.pathname + target.search;
  },
  logLevel: 'info', // Changed to 'info' for better debugging during setup
  selfHandleResponse: true,
  
  // --- FIXES ADDED HERE ---
  followRedirects: true, // Crucial: Tells the proxy to follow redirects on the server-side
  onProxyReq: (proxyReq, req, res) => {
    // Some websites check the 'host' header. We need to set it correctly.
    const targetUrl = req.query.url;
    const target = new URL(targetUrl.startsWith('http' ) ? targetUrl : `https://${targetUrl}` );
    proxyReq.setHeader('host', target.hostname);
  },
  // --- END OF FIXES ---

  onProxyRes: (proxyRes, req, res) => {
    // We need to prevent the browser from caching a 301/302 response
    delete proxyRes.headers['location'];

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
            try {
              const formattedArgs = args.map(arg => typeof arg === 'object' ? JSON.stringify(arg) : arg);
              window.parent.postMessage({ type: 'console-log', data: formattedArgs }, '*');
            } catch (e) {
              // Fallback for circular structures
              window.parent.postMessage({ type: 'console-log', data: ['[Unserializable Object]'] }, '*');
            }
            originalLog.apply(console, args);
          };
          window.addEventListener('error', function(e) {
            window.parent.postMessage({ type: 'console-error', data: e.message }, '*');
          });

          // Listen for commands from the parent window
          window.addEventListener('message', (event) => {
            if (event.data && event.data.type === 'execute-script') {
              try {
                eval(event.data.script);
              } catch (e) {
                console.log('Execution Error:', e.message);
              }
            }
          });
        </script>
      `;
      
      // A more robust way to inject the script
      if (proxyRes.headers['content-type'] && proxyRes.headers['content-type'].includes('text/html')) {
        html = html.replace('</head>', `${injectionScript}</head>`);
      }
      
      res.writeHead(proxyRes.statusCode, proxyRes.headers);
      res.end(html);
    });
  }
});

// Route for proxying requests
app.use('/proxy', proxy);

app.listen(PORT, () => {
  console.log(`Proxy server running on http://localhost:${PORT}` );
});
