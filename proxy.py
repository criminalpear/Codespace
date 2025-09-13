import requests
import re
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
from flask import Blueprint, request, Response, jsonify
from flask_cors import CORS

proxy_bp = Blueprint('proxy', __name__)
CORS(proxy_bp)

def rewrite_urls(content, base_url, proxy_base):
    """Rewrite URLs in HTML/CSS content to route through the proxy"""
    if not content:
        return content
    
    # Parse the base URL to get the scheme and netloc
    parsed_base = urlparse(base_url)
    base_scheme_netloc = f"{parsed_base.scheme}://{parsed_base.netloc}"
    
    # Rewrite absolute URLs
    content = re.sub(
        r'(href|src|action)=["\']https?://([^"\']+)["\']',
        lambda m: f'{m.group(1)}="{proxy_base}/proxy?url=https://{m.group(2)}"',
        content
    )
    
    # Rewrite protocol-relative URLs
    content = re.sub(
        r'(href|src|action)=["\']//([^"\']+)["\']',
        lambda m: f'{m.group(1)}="{proxy_base}/proxy?url=https://{m.group(2)}"',
        content
    )
    
    # Rewrite relative URLs
    content = re.sub(
        r'(href|src|action)=["\'](?!https?://|//|#|javascript:|mailto:|data:)([^"\']+)["\']',
        lambda m: f'{m.group(1)}="{proxy_base}/proxy?url={urljoin(base_url, m.group(2))}"',
        content
    )
    
    return content

def inject_console_script(content, proxy_base):
    """Inject the enhanced console script into HTML content"""
    console_script = f'''
    <script>
    // Enhanced Console for Interstellar Proxy
    (function() {{
        let consoleVisible = false;
        let consoleElement = null;
        let commandHistory = [];
        let historyIndex = -1;
        
        function createConsole() {{
            const consoleDiv = document.createElement('div');
            consoleDiv.id = 'interstellar-console';
            consoleDiv.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 50%;
                background: #1e1e1e;
                color: #ffffff;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                z-index: 999999;
                border-bottom: 2px solid #007acc;
                display: none;
                flex-direction: column;
            `;
            
            const header = document.createElement('div');
            header.style.cssText = `
                background: #007acc;
                color: white;
                padding: 8px 16px;
                font-weight: bold;
                display: flex;
                justify-content: space-between;
                align-items: center;
            `;
            header.innerHTML = `
                <span>Interstellar Proxy Console</span>
                <button onclick="window.interstellarConsole.toggle()" style="background: none; border: none; color: white; cursor: pointer; font-size: 16px;">×</button>
            `;
            
            const output = document.createElement('div');
            output.id = 'console-output';
            output.style.cssText = `
                flex: 1;
                padding: 16px;
                overflow-y: auto;
                white-space: pre-wrap;
            `;
            
            const inputContainer = document.createElement('div');
            inputContainer.style.cssText = `
                display: flex;
                padding: 8px 16px;
                background: #2d2d2d;
                border-top: 1px solid #444;
            `;
            
            const prompt = document.createElement('span');
            prompt.textContent = '> ';
            prompt.style.color = '#007acc';
            
            const input = document.createElement('input');
            input.id = 'console-input';
            input.type = 'text';
            input.style.cssText = `
                flex: 1;
                background: transparent;
                border: none;
                color: white;
                outline: none;
                font-family: inherit;
                font-size: inherit;
            `;
            
            inputContainer.appendChild(prompt);
            inputContainer.appendChild(input);
            
            consoleDiv.appendChild(header);
            consoleDiv.appendChild(output);
            consoleDiv.appendChild(inputContainer);
            
            document.body.appendChild(consoleDiv);
            
            // Add event listeners
            input.addEventListener('keydown', handleInput);
            
            return consoleDiv;
        }}
        
        function handleInput(e) {{
            if (e.key === 'Enter') {{
                const command = e.target.value.trim();
                if (command) {{
                    commandHistory.push(command);
                    historyIndex = commandHistory.length;
                    executeCommand(command);
                    e.target.value = '';
                }}
            }} else if (e.key === 'ArrowUp') {{
                e.preventDefault();
                if (historyIndex > 0) {{
                    historyIndex--;
                    e.target.value = commandHistory[historyIndex];
                }}
            }} else if (e.key === 'ArrowDown') {{
                e.preventDefault();
                if (historyIndex < commandHistory.length - 1) {{
                    historyIndex++;
                    e.target.value = commandHistory[historyIndex];
                }} else {{
                    historyIndex = commandHistory.length;
                    e.target.value = '';
                }}
            }}
        }}
        
        function executeCommand(command) {{
            const output = document.getElementById('console-output');
            
            // Add command to output
            const commandLine = document.createElement('div');
            commandLine.style.color = '#007acc';
            commandLine.textContent = '> ' + command;
            output.appendChild(commandLine);
            
            try {{
                // Handle special commands
                if (command.startsWith('help')) {{
                    showHelp();
                }} else if (command.startsWith('clear')) {{
                    output.innerHTML = '';
                }} else if (command.startsWith('inspect ')) {{
                    const selector = command.substring(8);
                    inspectElement(selector);
                }} else if (command.startsWith('network')) {{
                    showNetworkInfo();
                }} else {{
                    // Execute as JavaScript
                    const result = eval(command);
                    const resultLine = document.createElement('div');
                    resultLine.style.color = '#90ee90';
                    resultLine.textContent = result !== undefined ? String(result) : 'undefined';
                    output.appendChild(resultLine);
                }}
            }} catch (error) {{
                const errorLine = document.createElement('div');
                errorLine.style.color = '#ff6b6b';
                errorLine.textContent = 'Error: ' + error.message;
                output.appendChild(errorLine);
            }}
            
            output.scrollTop = output.scrollHeight;
        }}
        
        function showHelp() {{
            const output = document.getElementById('console-output');
            const helpText = `
Available commands:
  help - Show this help message
  clear - Clear the console
  inspect <selector> - Inspect DOM elements
  network - Show network information
  
You can also execute any JavaScript code directly.
            `;
            const helpLine = document.createElement('div');
            helpLine.style.color = '#ffeb3b';
            helpLine.textContent = helpText;
            output.appendChild(helpLine);
        }}
        
        function inspectElement(selector) {{
            const output = document.getElementById('console-output');
            try {{
                const elements = document.querySelectorAll(selector);
                const resultLine = document.createElement('div');
                resultLine.style.color = '#90ee90';
                resultLine.textContent = `Found ${{elements.length}} element(s) matching "${{selector}}"`;
                output.appendChild(resultLine);
                
                elements.forEach((el, index) => {{
                    const elementLine = document.createElement('div');
                    elementLine.style.color = '#87ceeb';
                    elementLine.textContent = `[${{index}}] ${{el.tagName.toLowerCase()}}${{el.id ? '#' + el.id : ''}}${{el.className ? '.' + el.className.split(' ').join('.') : ''}}`;
                    output.appendChild(elementLine);
                }});
            }} catch (error) {{
                const errorLine = document.createElement('div');
                errorLine.style.color = '#ff6b6b';
                errorLine.textContent = 'Error: ' + error.message;
                output.appendChild(errorLine);
            }}
        }}
        
        function showNetworkInfo() {{
            const output = document.getElementById('console-output');
            const infoLine = document.createElement('div');
            infoLine.style.color = '#90ee90';
            infoLine.textContent = `Current URL: ${{window.location.href}}\\nUser Agent: ${{navigator.userAgent}}`;
            output.appendChild(infoLine);
        }}
        
        function toggleConsole() {{
            if (!consoleElement) {{
                consoleElement = createConsole();
            }}
            
            consoleVisible = !consoleVisible;
            consoleElement.style.display = consoleVisible ? 'flex' : 'none';
            
            if (consoleVisible) {{
                document.getElementById('console-input').focus();
            }}
        }}
        
        // Global interface
        window.interstellarConsole = {{
            toggle: toggleConsole,
            show: () => {{ consoleVisible = false; toggleConsole(); }},
            hide: () => {{ consoleVisible = true; toggleConsole(); }}
        }};
        
        // Keyboard shortcut
        document.addEventListener('keydown', function(e) {{
            if (e.ctrlKey && e.shiftKey && e.key === 'J') {{
                e.preventDefault();
                toggleConsole();
            }}
        }});
        
        // Override console methods to capture logs
        const originalLog = console.log;
        const originalError = console.error;
        const originalWarn = console.warn;
        
        function captureLog(type, args) {{
            if (consoleElement) {{
                const output = document.getElementById('console-output');
                const logLine = document.createElement('div');
                logLine.style.color = type === 'error' ? '#ff6b6b' : type === 'warn' ? '#ffeb3b' : '#90ee90';
                logLine.textContent = `[${{type}}] ${{Array.from(args).join(' ')}}`;
                output.appendChild(logLine);
                output.scrollTop = output.scrollHeight;
            }}
        }}
        
        console.log = function(...args) {{
            originalLog.apply(console, args);
            captureLog('log', args);
        }};
        
        console.error = function(...args) {{
            originalError.apply(console, args);
            captureLog('error', args);
        }};
        
        console.warn = function(...args) {{
            originalWarn.apply(console, args);
            captureLog('warn', args);
        }};
    }})();
    </script>
    '''
    
    # Inject before closing body tag
    if '</body>' in content:
        content = content.replace('</body>', console_script + '</body>')
    else:
        content += console_script
    
    return content

@proxy_bp.route('/proxy')
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({'error': 'URL parameter is required'}), 400
    
    # Ensure the URL has a scheme
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url
    
    try:
        # Forward the request
        headers = dict(request.headers)
        # Remove problematic headers
        headers.pop('Host', None)
        headers.pop('Origin', None)
        headers.pop('Referer', None)
        
        # Add user agent if not present
        if 'User-Agent' not in headers:
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        
        # Make the request
        response = requests.get(
            target_url,
            headers=headers,
            params=request.args.to_dict(flat=False),
            allow_redirects=True,
            timeout=30
        )
        
        # Get the content
        content = response.content
        content_type = response.headers.get('Content-Type', '')
        
        # Process HTML content
        if 'text/html' in content_type:
            try:
                content = content.decode('utf-8', errors='ignore')
                proxy_base = request.url_root.rstrip('/')
                content = rewrite_urls(content, target_url, proxy_base)
                content = inject_console_script(content, proxy_base)
                content = content.encode('utf-8')
            except Exception as e:
                print(f"Error processing HTML: {e}")
        
        # Create response
        response_headers = {}
        for key, value in response.headers.items():
            # Skip problematic headers
            if key.lower() not in ['content-encoding', 'content-length', 'transfer-encoding', 'connection']:
                response_headers[key] = value
        
        # Add CORS headers
        response_headers['Access-Control-Allow-Origin'] = '*'
        response_headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response_headers['Access-Control-Allow-Headers'] = '*'
        
        return Response(
            content,
            status=response.status_code,
            headers=response_headers
        )
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Proxy error: {str(e)}'}), 500

@proxy_bp.route('/proxy', methods=['POST'])
def proxy_post():
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({'error': 'URL parameter is required'}), 400
    
    # Ensure the URL has a scheme
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url
    
    try:
        # Forward the POST request
        headers = dict(request.headers)
        # Remove problematic headers
        headers.pop('Host', None)
        headers.pop('Origin', None)
        headers.pop('Referer', None)
        
        # Make the POST request
        response = requests.post(
            target_url,
            headers=headers,
            data=request.get_data(),
            allow_redirects=True,
            timeout=30
        )
        
        # Get the content
        content = response.content
        content_type = response.headers.get('Content-Type', '')
        
        # Process HTML content
        if 'text/html' in content_type:
            try:
                content = content.decode('utf-8', errors='ignore')
                proxy_base = request.url_root.rstrip('/')
                content = rewrite_urls(content, target_url, proxy_base)
                content = inject_console_script(content, proxy_base)
                content = content.encode('utf-8')
            except Exception as e:
                print(f"Error processing HTML: {e}")
        
        # Create response
        response_headers = {}
        for key, value in response.headers.items():
            # Skip problematic headers
            if key.lower() not in ['content-encoding', 'content-length', 'transfer-encoding', 'connection']:
                response_headers[key] = value
        
        # Add CORS headers
        response_headers['Access-Control-Allow-Origin'] = '*'
        response_headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response_headers['Access-Control-Allow-Headers'] = '*'
        
        return Response(
            content,
            status=response.status_code,
            headers=response_headers
        )
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Proxy error: {str(e)}'}), 500

