# WiFi Configuration Template
# Copy this to your main.py and update the credentials

# WiFi Configuration
WIFI_SSID = "YOUR_WIFI_NETWORK_NAME"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

# Alternative configuration for multiple networks
WIFI_NETWORKS = [
    {"ssid": "Home_WiFi", "password": "home_password"},
    {"ssid": "Office_WiFi", "password": "office_password"},
    {"ssid": "Mobile_Hotspot", "password": "mobile_password"},
]

# Network Settings
WIFI_TIMEOUT = 20  # seconds to wait for connection
SERVER_PORT = 80   # HTTP server port

# Display Settings  
DEFAULT_BRIGHTNESS = 0.5  # 0.0 to 1.0
DEFAULT_COLOR = "white"    # Default digit color
DIGIT_THICKNESS = 3        # Thickness of digit lines

# Server Configuration
ENABLE_WEB_INTERFACE = True  # Set to False for API-only mode
ENABLE_CORS = True          # Enable Cross-Origin Resource Sharing
