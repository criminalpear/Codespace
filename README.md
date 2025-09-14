# 🌟 Interstellar Proxy

A modern web proxy application with an enhanced developer console, designed to provide unblocked internet browsing with advanced JavaScript execution capabilities.

## ✨ Features

- **🚀 Fast & Secure**: Lightning-fast browsing with secure connections
- **🔓 Unblock Everything**: Access any website without restrictions
- **🛠️ Enhanced Console**: Advanced developer tools with JavaScript execution
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices
- **🎨 Modern UI**: Clean and intuitive interface with glassmorphism design

## 🚀 Quick Start with GitHub Codespaces

1. **Open in Codespaces**: Click the "Code" button on this repository and select "Create codespace on main"
2. **Wait for Setup**: The devcontainer will automatically install dependencies
3. **Start the Server**: Run the following commands in the terminal:
   ```bash
   source venv/bin/activate
   python src/main.py
   ```
4. **Access the Proxy**: Open the forwarded port (5000) in your browser

## 🛠️ Local Development Setup

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd interstellar-proxy
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python src/main.py
   ```

5. **Open your browser** and navigate to `http://localhost:5000`

## 🎮 How to Use

### Basic Browsing

1. Enter any URL in the input field (e.g., `google.com`, `youtube.com`)
2. Click the "Go" button or press Enter
3. Browse the web through the proxy interface

### Enhanced Console

The enhanced console provides advanced debugging and JavaScript execution capabilities:

1. **Activate**: Press `Ctrl+Shift+J` on any proxied page
2. **Execute JavaScript**: Type any JavaScript code and press Enter
3. **Inspect Elements**: Use `inspect <selector>` to examine DOM elements
4. **View Network Info**: Use `network` command to see connection details
5. **Clear Console**: Use `clear` command to clear the output
6. **Get Help**: Use `help` command to see all available commands

### Navigation Controls

- **🏠 Home**: Return to the main proxy interface
- **← Back**: Navigate to the previous page
- **Forward →**: Navigate to the next page (if available)
- **🔄 Refresh**: Reload the current page
- **✕ Close**: Close the proxy frame and return home

### Keyboard Shortcuts

- `Ctrl+H`: Go home
- `Alt+←`: Go back
- `Alt+→`: Go forward
- `F5` or `Ctrl+R`: Refresh current page
- `Ctrl+Shift+J`: Toggle enhanced console

## 🏗️ Architecture

### Backend (Flask)

- **Proxy Engine**: Handles HTTP/HTTPS request forwarding
- **URL Rewriting**: Automatically rewrites URLs to route through the proxy
- **Header Management**: Manages request/response headers for compatibility
- **CORS Support**: Enables cross-origin requests for frontend communication

### Frontend (HTML/CSS/JavaScript)

- **Modern UI**: Glassmorphism design with responsive layout
- **Enhanced Console**: Custom developer console with JavaScript execution
- **Navigation System**: Browser-like navigation with history support
- **Frame Management**: Seamless iframe-based browsing experience

### Enhanced Console Features

- **JavaScript Execution**: Run arbitrary JavaScript in the proxied page context
- **DOM Inspection**: Examine and interact with page elements
- **Network Monitoring**: View request/response information
- **Console Logging**: Capture and display console messages
- **Command History**: Navigate through previous commands with arrow keys

## 📁 Project Structure

```
interstellar-proxy/
├── .devcontainer/
│   └── devcontainer.json     # GitHub Codespaces configuration
├── src/
│   ├── models/               # Database models
│   ├── routes/
│   │   ├── proxy.py         # Main proxy logic
│   │   └── user.py          # User management (template)
│   ├── static/
│   │   └── index.html       # Frontend interface
│   ├── database/
│   │   └── app.db          # SQLite database
│   └── main.py             # Flask application entry point
├── venv/                   # Python virtual environment
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .gitignore            # Git ignore rules
```

## 🔧 Configuration

### Environment Variables

The application uses the following environment variables (optional):

- `FLASK_ENV`: Set to `development` for debug mode
- `SECRET_KEY`: Flask secret key (auto-generated if not provided)

### Proxy Settings

The proxy is configured to:

- Listen on all interfaces (`0.0.0.0:5000`)
- Handle both HTTP and HTTPS requests
- Automatically rewrite URLs for proper routing
- Inject the enhanced console into all HTML pages

## 🛡️ Security Considerations

- **HTTPS Support**: The proxy handles HTTPS traffic through request forwarding
- **Header Sanitization**: Removes potentially problematic headers
- **CORS Protection**: Implements proper CORS headers
- **Input Validation**: Validates and sanitizes user input

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This proxy is intended for educational and legitimate use cases only. Users are responsible for complying with all applicable laws and regulations. The developers are not responsible for any misuse of this software.

## 🆘 Troubleshooting

### Common Issues

1. **Port 5000 already in use**:
   ```bash
   # Kill any process using port 5000
   sudo lsof -ti:5000 | xargs kill -9
   ```

2. **Virtual environment issues**:
   ```bash
   # Remove and recreate virtual environment
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Console not appearing**:
   - Ensure you're pressing `Ctrl+Shift+J` on a proxied page (not the home page)
   - Check browser console for JavaScript errors

### Getting Help

If you encounter any issues:

1. Check the [Issues](../../issues) page for existing solutions
2. Create a new issue with detailed information about your problem
3. Include your operating system, Python version, and error messages

---

Made with ❤️ for unrestricted web browsing

