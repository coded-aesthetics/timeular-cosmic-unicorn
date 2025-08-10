# Pico W Server Setup

This directory contains the MicroPython server code for the Raspberry Pi Pico W that controls the Cosmic Unicorn LED matrix display.

## 🚀 Quick Setup

### 1. Flash MicroPython

1. Download the latest MicroPython UF2 file for Pico W:
   - Visit [micropython.org/download/rp2-pico-w/](https://micropython.org/download/rp2-pico-w/)
   - Download the latest stable release

2. Flash to Pico W:
   - Hold the BOOTSEL button while connecting Pico W via USB
   - Copy the UF2 file to the RPI-RP2 drive that appears
   - Pico W will reboot automatically

### 2. Install Pimoroni Libraries

Using **Thonny IDE** (recommended):
1. Install Thonny from [thonny.org](https://thonny.org/)
2. Open Thonny and connect to your Pico W
3. Go to Tools → Manage packages
4. Search and install: `pimoroni-cosmic-unicorn`

Using **mpremote**:
```bash
pip install mpremote
mpremote mip install github:pimoroni/pimoroni-pico/micropython/modules/cosmic.py
mpremote mip install github:pimoroni/pimoroni-pico/micropython/modules/picographics.py
```

### 3. Configure WiFi

1. Open `main.py` in your editor
2. Find these lines:
   ```python
   # TODO: Update these with your WiFi credentials
   SSID = "YOUR_WIFI_SSID"
   PASSWORD = "YOUR_WIFI_PASSWORD"
   ```
3. Replace with your actual WiFi credentials:
   ```python
   SSID = "MyHomeWiFi"
   PASSWORD = "myactualpassword"
   ```

### 4. Upload and Run

1. Copy `main.py` to your Pico W (save as `main.py` on the device)
2. Reset the Pico W or run the code
3. Watch the serial output for the IP address:
   ```
   WiFi connected!
   IP address: 192.168.1.100
   🌐 Cosmic Unicorn Server running!
   🔗 Web interface: http://192.168.1.100
   ```

## 🎯 Features

### LED Display Control

The server displays large, colorful digits (0-9) that fill the entire 32x32 matrix:

- **High visibility** - Thick, bold digits optimized for the LED matrix
- **Multiple colors** - Support for red, green, blue, white, yellow, cyan, magenta
- **Real-time updates** - Sub-100ms response to HTTP requests
- **Robust rendering** - Carefully designed digit patterns for maximum readability

### Web Interface

Access `http://[pico-ip]` for a full web control interface:

- **Interactive digit buttons** - Click any number 0-9 to display instantly
- **Color controls** - Test different colors with preset combinations
- **Real-time status** - See current display state and server uptime
- **API documentation** - Built-in reference for programmatic control
- **Responsive design** - Works on desktop, tablet, and mobile

### HTTP API

Simple GET requests to control the display:

```bash
# Display white "5"
curl "http://192.168.1.100/?num=5"

# Display red "3"
curl "http://192.168.1.100/?num=3&color=red"

# Display green "7"
curl "http://192.168.1.100/?num=7&color=green"
```

**Supported colors:** red, green, blue, white, yellow, cyan, magenta

## 🔧 Configuration

### WiFi Settings

Update WiFi credentials in `main.py`:

```python
# Single network
SSID = "MyWiFi"
PASSWORD = "mypassword"
```

For multiple networks, use the template in `wifi-config.py`.

### Display Settings

Customize display behavior:

```python
# Brightness (0.0 to 1.0)
cu.set_brightness(0.5)

# Default thickness for digits
thickness = 3

# Default color
color = WHITE
```

### Server Settings

```python
# HTTP port (default: 80)
SERVER_PORT = 80

# Connection timeout
WIFI_TIMEOUT = 20  # seconds
```

## 🐛 Troubleshooting

### WiFi Connection Issues

**"WiFi connection failed":**
- Double-check SSID and password (case-sensitive)
- Ensure 2.4GHz network (Pico W doesn't support 5GHz)
- Check WiFi signal strength
- Try restarting your router

**"Network connection failed":**
- Verify network allows new device connections
- Check for MAC address filtering
- Try a mobile hotspot for testing

### Display Issues

**"Cosmic Unicorn not responding":**
- Check physical connections between Pico W and LED matrix
- Verify power supply is adequate (LED matrix needs significant power)
- Test with a simple color fill to isolate the issue

**"Digits appear corrupted":**
- Check for electrical interference
- Verify all solder joints are solid
- Try reducing brightness to test power issues

### Server Issues

**"Cannot access web interface":**
- Verify IP address is correct (check serial output)
- Ensure devices are on same network
- Try ping test: `ping 192.168.1.100`
- Check firewall settings

**"API calls timing out":**
- Test with simple curl command
- Check for network congestion
- Verify Pico W isn't overloaded

### Memory Issues

**"Out of memory" errors:**
- Restart the Pico W periodically for long-running deployments
- Monitor memory usage in serial output
- Consider simplifying the web interface for memory-constrained scenarios

## 📊 Monitoring

The server provides detailed logging via serial output:

```
🚀 Starting Cosmic Unicorn Display Server...
📝 Remember to update WiFi credentials in this file!
Connecting to WiFi: MyWiFi
WiFi connected!
IP address: 192.168.1.100
🌐 Cosmic Unicorn Server running!
🔗 Web interface: http://192.168.1.100
🎯 API endpoint: http://192.168.1.100/?num=5&color=red
🎲 Ready for Timeular tracker input!
==================================================
📱 Client connected from 192.168.1.50
🎨 Displaying digit 5 in red
📱 Client connected from 192.168.1.50
🌐 Serving web interface
```

### Log Levels

- `🚀` Startup messages
- `🌐` Web interface requests
- `📱` Client connections
- `🎨` Display updates
- `❌` Error conditions
- `⚠️` Warnings

## 🚀 Advanced Features

### Multiple Color Support

Extend color support by adding to the color map:

```python
def get_color_pen(color_name):
    color_map = {
        'red': RED,
        'green': GREEN,
        'blue': BLUE,
        'white': WHITE,
        'yellow': YELLOW,
        'cyan': CYAN,
        'magenta': MAGENTA,
        'purple': graphics.create_pen(128, 0, 128),
        'orange': graphics.create_pen(255, 165, 0),
    }
    return color_map.get(color_name.lower(), WHITE)
```

### Custom Digit Patterns

Modify `draw_thick_digit()` to create custom digit styles:

```python
# Add custom patterns for digits
elif digit == 1:
    # Custom "1" with decorative elements
    x = 16 - thickness // 2
    graphics.rectangle(x, top, thickness, height)
    # Add decorative top
    graphics.rectangle(x - 4, top, 8, thickness)
    # Add decorative base
    graphics.rectangle(x - 4, bottom - thickness, 8, thickness)
```

### Animation Support

Add simple animations:

```python
def animate_digit_entrance(digit, color=WHITE):
    """Animate digit appearing with fade-in effect"""
    for brightness in range(10, 100, 10):
        cu.set_brightness(brightness / 100.0)
        draw_thick_digit(digit, color, 3)
        time.sleep(0.05)
```

### API Rate Limiting

Add basic rate limiting for API calls:

```python
last_request_time = 0
MIN_REQUEST_INTERVAL = 100  # milliseconds

def handle_api_request():
    global last_request_time
    current_time = time.ticks_ms()
    
    if time.ticks_diff(current_time, last_request_time) < MIN_REQUEST_INTERVAL:
        return "Rate limited", 429
    
    last_request_time = current_time
    # Handle request normally
```

## 🔗 Integration Examples

### Home Assistant

Add to Home Assistant configuration:

```yaml
# configuration.yaml
rest_command:
  cosmic_unicorn_display:
    url: "http://192.168.1.100/"
    method: GET
    payload: "num={{ num }}&color={{ color }}"

# automation.yaml
automation:
  - alias: "Display current hour"
    trigger:
      platform: time_pattern
      minutes: 0
    action:
      service: rest_command.cosmic_unicorn_display
      data:
        num: "{{ now().hour % 10 }}"
        color: "blue"
```

### Node-RED

Create HTTP request node:

```json
{
    "url": "http://192.168.1.100/?num={{payload.digit}}&color={{payload.color}}",
    "method": "GET"
}
```

### Python Script

```python
import requests
import time

def update_display(digit, color="white"):
    url = f"http://192.168.1.100/?num={digit}&color={color}"
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Example: Count down from 9 to 0
for i in range(9, -1, -1):
    update_display(i, "red" if i <= 3 else "green")
    time.sleep(1)
```

## 📁 File Structure

```
pico-w-server/
├── main.py              # Main server application
├── wifi-config.py       # WiFi configuration template
└── README.md           # This file
```

## 🤝 Contributing

To contribute improvements:

1. Test thoroughly on actual hardware
2. Ensure memory efficiency (Pico W has limited RAM)
3. Maintain compatibility with MicroPython
4. Add appropriate error handling
5. Update documentation

## 📜 License

This server code is part of the Timeular-Cosmic-Unicorn project and follows the same MIT license terms.
