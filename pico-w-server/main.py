from cosmic import CosmicUnicorn
from picographics import PicoGraphics, DISPLAY_COSMIC_UNICORN
import time
import network
import socket

cu = CosmicUnicorn()
graphics = PicoGraphics(display=DISPLAY_COSMIC_UNICORN)
cu.set_brightness(0.5)

# Colors
WHITE = graphics.create_pen(255, 255, 255)
RED = graphics.create_pen(255, 0, 0)
GREEN = graphics.create_pen(0, 255, 0)
BLUE = graphics.create_pen(0, 0, 255)
YELLOW = graphics.create_pen(255, 255, 0)
CYAN = graphics.create_pen(0, 255, 255)
MAGENTA = graphics.create_pen(255, 0, 255)
BLACK = graphics.create_pen(0, 0, 0)

def draw_thick_digit(digit, color=WHITE, thickness=3):
    """Draw digits with adjustable thickness filling the 32x32 display"""
    
    graphics.set_pen(BLACK)
    graphics.clear()
    graphics.set_pen(color)
    
    # Coordinates for a well-proportioned digit
    left = 6
    right = 26
    top = 2
    middle = 14
    bottom = 30
    width = right - left
    height = bottom - top
    
    if digit == 0:
        # Rounded rectangle approach for 0
        for i in range(thickness):
            # Outer border
            graphics.rectangle(left + i, top + i, width - 2*i, thickness)      # Top
            graphics.rectangle(left + i, bottom - thickness - i, width - 2*i, thickness)  # Bottom
            graphics.rectangle(left + i, top + thickness + i, thickness, height - 2*thickness - 2*i)  # Left
            graphics.rectangle(right - thickness - i, top + thickness + i, thickness, height - 2*thickness - 2*i)  # Right
            
    elif digit == 1:
        # Centered vertical line
        x = 16 - thickness // 2
        graphics.rectangle(x, top, thickness, height)
        # Small diagonal at top
        graphics.rectangle(x - 3, top + 2, 3, thickness)
        
    elif digit == 2:
        graphics.rectangle(left, top, width, thickness)           # Top
        graphics.rectangle(right - thickness, top, thickness, middle - top)  # Right upper
        graphics.rectangle(left, middle - thickness//2, width, thickness)    # Middle
        graphics.rectangle(left, middle, thickness, bottom - middle)         # Left lower
        graphics.rectangle(left, bottom - thickness, width, thickness)       # Bottom
        
    elif digit == 3:
        graphics.rectangle(left, top, width, thickness)           # Top
        graphics.rectangle(right - thickness, top, thickness, height)        # Right
        graphics.rectangle(left + width//3, middle - thickness//2, width*2//3, thickness)  # Middle
        graphics.rectangle(left, bottom - thickness, width, thickness)       # Bottom
        
    elif digit == 4:
        graphics.rectangle(left, top, thickness, middle - top + thickness//2)  # Left upper
        graphics.rectangle(right - thickness, top, thickness, height)          # Right
        graphics.rectangle(left, middle - thickness//2, width, thickness)      # Horizontal
        
    elif digit == 5:
        graphics.rectangle(left, top, width, thickness)           # Top
        graphics.rectangle(left, top, thickness, middle - top + thickness//2)   # Left upper
        graphics.rectangle(left, middle - thickness//2, width*2//3, thickness)  # Middle
        graphics.rectangle(right - thickness, middle, thickness, bottom - middle)  # Right lower
        graphics.rectangle(left, bottom - thickness, width, thickness)          # Bottom
        
    elif digit == 6:
        graphics.rectangle(left, top, width, thickness)           # Top
        graphics.rectangle(left, top, thickness, height)          # Left
        graphics.rectangle(left, middle - thickness//2, width, thickness)      # Middle
        graphics.rectangle(right - thickness, middle, thickness, bottom - middle)  # Right lower
        graphics.rectangle(left, bottom - thickness, width, thickness)          # Bottom
        
    elif digit == 7:
        graphics.rectangle(left, top, width, thickness)           # Top
        graphics.rectangle(right - thickness, top, thickness, height)          # Right
        
    elif digit == 8:
        graphics.rectangle(left, top, width, thickness)           # Top
        graphics.rectangle(left, top, thickness, middle - top)    # Left upper
        graphics.rectangle(right - thickness, top, thickness, middle - top)   # Right upper
        graphics.rectangle(left, middle - thickness//2, width, thickness)     # Middle
        graphics.rectangle(left, middle, thickness, bottom - middle)          # Left lower
        graphics.rectangle(right - thickness, middle, thickness, bottom - middle)  # Right lower
        graphics.rectangle(left, bottom - thickness, width, thickness)        # Bottom
        
    elif digit == 9:
        graphics.rectangle(left, top, width, thickness)           # Top
        graphics.rectangle(left, top, thickness, middle - top + thickness//2)   # Left upper
        graphics.rectangle(right - thickness, top, thickness, height)          # Right
        graphics.rectangle(left, middle - thickness//2, width, thickness)      # Middle
        graphics.rectangle(left, bottom - thickness, width, thickness)         # Bottom
    
    cu.update(graphics)

def connect_wifi():
    """Connect to Wi-Fi network - UPDATE YOUR CREDENTIALS!"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # TODO: Update these with your WiFi credentials
    SSID = "YOUR_WIFI_SSID"
    PASSWORD = "YOUR_WIFI_PASSWORD"
    
    print(f"Connecting to WiFi: {SSID}")
    wlan.connect(SSID, PASSWORD)
    
    # Wait for connection with timeout
    max_wait = 20
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('Waiting for WiFi connection...')
        time.sleep(1)
    
    # Handle connection result
    if wlan.status() != 3:
        print(f"WiFi connection failed. Status: {wlan.status()}")
        print("Please check your WiFi credentials in main.py")
        raise RuntimeError('Network connection failed')
    else:
        print('WiFi connected!')
        status = wlan.ifconfig()
        ip = status[0]
        print(f'IP address: {ip}')
        return ip

def url_decode(text):
    """Basic URL decoding for common cases"""
    text = text.replace('+', ' ')
    
    # Handle %XX encoding for common characters
    replacements = {
        '%20': ' ', '%21': '!', '%22': '"', '%23': '#', '%24': '$',
        '%25': '%', '%26': '&', '%27': "'", '%28': '(', '%29': ')',
        '%2A': '*', '%2B': '+', '%2C': ',', '%2D': '-', '%2E': '.',
        '%2F': '/', '%3A': ':', '%3B': ';', '%3C': '<', '%3D': '=',
        '%3E': '>', '%3F': '?', '%40': '@', '%5B': '[', '%5C': '\\',
        '%5D': ']', '%5E': '^', '%5F': '_', '%60': '`', '%7B': '{',
        '%7C': '|', '%7D': '}', '%7E': '~'
    }
    
    for encoded, decoded in replacements.items():
        text = text.replace(encoded, decoded)
    
    return text

def parse_query_params(request):
    """Parse query parameters from HTTP request"""
    params = {}
    
    try:
        # Extract the first line from the HTTP request
        lines = request.split('\n')
        if not lines:
            return params
            
        first_line = lines[0].strip()
        
        # Parse the request line: "GET /path?param=value HTTP/1.1"
        parts = first_line.split(' ')
        if len(parts) < 2:
            return params
            
        url = parts[1]
        
        # Check if there are query parameters
        if '?' not in url:
            return params
        
        # Split URL and query string
        path, query_string = url.split('?', 1)
        
        # Parse each parameter
        if query_string:
            pairs = query_string.split('&')
            for pair in pairs:
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    # URL decode
                    key = url_decode(key)
                    value = url_decode(value)
                    params[key] = value
                else:
                    # Parameter without value
                    params[url_decode(pair)] = ''
        
    except Exception as e:
        print(f"Error parsing query params: {e}")
    
    return params

def safe_string_to_int(value, default=0):
    """Safely convert string to integer"""
    try:
        return int(value)
    except (ValueError, TypeError):
        print(f"Could not convert '{value}' to integer, using default: {default}")
        return default

def get_color_pen(color_name):
    """Get color pen based on name"""
    color_map = {
        'red': RED,
        'green': GREEN,
        'blue': BLUE,
        'white': WHITE,
        'yellow': YELLOW,
        'cyan': CYAN,
        'magenta': MAGENTA,
    }
    return color_map.get(color_name.lower(), WHITE)

def create_web_interface(last_number="None"):
    """Create HTML web interface"""
    html_template = """<!DOCTYPE html>
<html>
<head>
    <title>Cosmic Unicorn Display Control</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 20px; 
            background-color: #1a1a1a; 
            color: white; 
        }
        .container { max-width: 800px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .status { 
            background: #333; 
            padding: 15px; 
            border-radius: 8px; 
            margin: 20px 0; 
        }
        .controls { margin: 20px 0; }
        .digit-grid { 
            display: grid; 
            grid-template-columns: repeat(5, 1fr); 
            gap: 10px; 
            margin: 20px 0; 
        }
        .digit-btn { 
            padding: 20px; 
            font-size: 24px; 
            font-weight: bold; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            text-decoration: none;
            display: block;
            text-align: center;
            background-color: #4CAF50;
            color: white;
            transition: background-color 0.3s;
        }
        .digit-btn:hover { background-color: #45a049; }
        .color-btn { 
            padding: 15px; 
            margin: 5px; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer; 
            text-decoration: none; 
            display: inline-block; 
            color: white; 
            font-weight: bold;
        }
        .red { background-color: #f44336; }
        .green { background-color: #4CAF50; }
        .blue { background-color: #2196F3; }
        .white { background-color: #757575; }
        h1 { color: #4CAF50; }
        h3 { color: #81C784; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 Cosmic Unicorn 32x32 Display</h1>
            <p>Real-time LED matrix control via Timeular tracker or web interface</p>
        </div>
        
        <div class="status">
            <h3>📊 Status</h3>
            <p><strong>Last Number Displayed:</strong> %s</p>
            <p><strong>Server Uptime:</strong> %s ms</p>
            <p><strong>Ready for Timeular input!</strong></p>
        </div>
        
        <div class="controls">
            <h3>🎲 Manual Control - Click any number:</h3>
            <div class="digit-grid">
                <a href="/?num=0" class="digit-btn">0</a>
                <a href="/?num=1" class="digit-btn">1</a>
                <a href="/?num=2" class="digit-btn">2</a>
                <a href="/?num=3" class="digit-btn">3</a>
                <a href="/?num=4" class="digit-btn">4</a>
                <a href="/?num=5" class="digit-btn">5</a>
                <a href="/?num=6" class="digit-btn">6</a>
                <a href="/?num=7" class="digit-btn">7</a>
                <a href="/?num=8" class="digit-btn">8</a>
                <a href="/?num=9" class="digit-btn">9</a>
            </div>
        </div>
        
        <div class="controls">
            <h3>🌈 Color Examples:</h3>
            <a href="/?num=5&color=red" class="color-btn red">Red 5</a>
            <a href="/?num=3&color=green" class="color-btn green">Green 3</a>
            <a href="/?num=7&color=blue" class="color-btn blue">Blue 7</a>
            <a href="/?num=1&color=white" class="color-btn white">White 1</a>
        </div>
        
        <div class="controls">
            <h3>🔗 API Usage:</h3>
            <p>Send HTTP GET requests to control the display:</p>
            <ul>
                <li><code>/?num=5</code> - Display white "5"</li>
                <li><code>/?num=3&color=red</code> - Display red "3"</li>
                <li><code>/?num=7&color=green</code> - Display green "7"</li>
            </ul>
            <p><strong>Supported colors:</strong> red, green, blue, white, yellow, cyan, magenta</p>
        </div>
        
        <div class="controls">
            <h3>🎯 Timeular Integration:</h3>
            <p>This server is designed to work with the Timeular tracker bridge application.</p>
            <p>When you rotate your Timeular device, the corresponding number will appear on this display!</p>
        </div>
    </div>
</body>
</html>"""
    
    return html_template % (last_number, time.ticks_ms())

def web_server():
    """Main web server function"""
    # Connect to Wi-Fi
    ip = connect_wifi()
    
    # Create socket
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    
    print(f'🌐 Cosmic Unicorn Server running!')
    print(f'🔗 Web interface: http://{ip}')
    print(f'🎯 API endpoint: http://{ip}/?num=5&color=red')
    print(f'🎲 Ready for Timeular tracker input!')
    print('=' * 50)
    
    # Keep track of last displayed number
    last_number = "None"
    
    while True:
        try:
            cl, addr = s.accept()
            print(f'📱 Client connected from {addr[0]}')
            
            request = cl.recv(1024)
            request_str = request.decode('utf-8')
            
            # Parse query parameters
            params = parse_query_params(request_str)
            
            response_sent = False
            
            # Handle the 'num' parameter
            if 'num' in params:
                num_str = params['num']
                num_int = safe_string_to_int(num_str)
                
                # Validate digit range (0-9)
                if 0 <= num_int <= 9:
                    last_number = str(num_int)
                    
                    # Handle color parameter
                    color = WHITE  # Default color
                    color_name = "white"
                    if 'color' in params:
                        color_name = params['color'].lower()
                        color = get_color_pen(color_name)
                    
                    print(f'🎨 Displaying digit {num_int} in {color_name}')
                    
                    # Display the digit on the LED matrix
                    draw_thick_digit(num_int, color, 3)
                    
                    # Send simple OK response for API calls
                    response = 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nOK'
                    cl.send(response.encode('utf-8'))
                    response_sent = True
                else:
                    print(f'❌ Invalid digit: {num_int} (must be 0-9)')
                    last_number = f"Invalid: {num_int}"
            
            # If no API call, send web interface
            if not response_sent:
                print(f'🌐 Serving web interface')
                response_body = create_web_interface(last_number)
                
                response_headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n'
                
                cl.send(response_headers.encode('utf-8'))
                cl.send(response_body.encode('utf-8'))
            
            cl.close()
            
        except OSError as e:
            cl.close()
            print(f'💥 Connection error: {e}')
        except Exception as e:
            cl.close()
            print(f'💥 Unexpected error: {e}')

# Initialize display with startup message
print("🚀 Starting Cosmic Unicorn Display Server...")
print("📝 Remember to update WiFi credentials in this file!")

# Show startup pattern
draw_thick_digit(0, GREEN, 3)  # Show green "0" on startup
time.sleep(2)

# Run the server
try:
    web_server()
except KeyboardInterrupt:
    print("\n🛑 Server stopped by user")
except Exception as e:
    print(f"💥 Server error: {e}")
finally:
    # Clear display on exit
    graphics.set_pen(BLACK)
    graphics.clear()
    cu.update(graphics)
    print("👋 Cosmic Unicorn server shutdown complete")
