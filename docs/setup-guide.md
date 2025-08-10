# Setup Guide

This comprehensive guide walks you through setting up the complete Timeular to Cosmic Unicorn bridge system.

## 📋 Prerequisites

### Hardware
- **Timeular Tracker** (any generation)
- **Raspberry Pi Pico W** 
- **Pimoroni Cosmic Unicorn 32x32 LED Matrix**
- **Computer with Bluetooth** (Windows, macOS, or Linux)
- **USB-C cable** for Pico W programming
- **Adequate power supply** for LED matrix

### Software
- **Go 1.21+** for the bridge application
- **MicroPython** for Pico W
- **Thonny IDE** or similar for MicroPython development
- **Git** for cloning the repository

## 🔧 Step-by-Step Setup

### Step 1: Prepare the Hardware

1. **Assemble Cosmic Unicorn:**
   - Attach the Pico W to the Cosmic Unicorn board
   - Ensure all connections are secure
   - Connect power supply if using external power

2. **Test Timeular Tracker:**
   - Ensure Timeular is charged
   - Test basic functionality (shake to activate)
   - Note the exact device name (usually "Timeular Tra" or similar)

### Step 2: Set Up the Pico W Server

1. **Flash MicroPython:**
   ```bash
   # Download from https://micropython.org/download/rp2-pico-w/
   # Hold BOOTSEL while connecting USB, then copy UF2 file
   ```

2. **Install Pimoroni Libraries:**
   - Open Thonny IDE
   - Connect to Pico W
   - Tools → Manage packages → Install `pimoroni-cosmic-unicorn`

3. **Configure WiFi:**
   ```python
   # In main.py, update these lines:
   SSID = "YourWiFiName"
   PASSWORD = "YourWiFiPassword"
   ```

4. **Upload Server Code:**
   - Copy `pico-w-server/main.py` to Pico W
   - Save as `main.py` on the device
   - Reset Pico W and note the IP address

### Step 3: Set Up the Go Bridge

1. **Install Go:**
   ```bash
   # Download from https://golang.org/downloads/
   # Follow installation instructions for your platform
   ```

2. **Clone and Build:**
   ```bash
   cd /Users/jan/dev/timeular-cosmic-unicorn/go-bridge
   go mod tidy
   ```

3. **Configure Bridge:**
   ```go
   // In main.go, update:
   const PICO_W_IP = "192.168.1.100"  // Your Pico W's IP
   const TIMEULAR_NAME = "Timeular Tra"  // Your device name
   ```

### Step 4: Test the System

1. **Test Pico W Server:**
   ```bash
   # Visit web interface
   curl http://192.168.1.100/
   
   # Test API
   curl "http://192.168.1.100/?num=5&color=red"
   ```

2. **Test Timeular Connection:**
   ```bash
   cd go-bridge
   go run main.go
   # Should show "Searching for Timeular tracker..."
   ```

3. **Test Full Integration:**
   - Run the Go bridge application
   - Rotate Timeular to different sides
   - Verify numbers appear on LED display

## 🔍 Platform-Specific Setup

### macOS Setup

1. **Bluetooth Permissions:**
   - System Settings → Privacy & Security → Bluetooth
   - Add Terminal (or your IDE) to allowed apps

2. **Go Installation:**
   ```bash
   # Using Homebrew
   brew install go
   
   # Or download from golang.org
   ```

3. **Common Issues:**
   - Bluetooth may need to be restarted: System Settings → Bluetooth → Turn off/on
   - Some IDE permissions may be needed for Bluetooth access

### Windows Setup

1. **Bluetooth Permissions:**
   - Ensure Bluetooth is enabled
   - Allow apps to access Bluetooth in Privacy settings
   - May need to run as Administrator for Bluetooth access

2. **Go Installation:**
   - Download installer from golang.org
   - Add Go to PATH if not automatic

3. **Common Issues:**
   - Windows Defender may block Bluetooth access
   - Some antivirus software interferes with BLE

### Linux Setup

1. **Bluetooth Permissions:**
   ```bash
   # Add user to bluetooth group
   sudo usermod -a -G bluetooth $USER
   
   # Or run with sudo (not recommended for production)
   sudo go run main.go
   ```

2. **Dependencies:**
   ```bash
   # Ubuntu/Debian
   sudo apt install bluetooth bluez libbluetooth-dev
   
   # Fedora
   sudo dnf install bluez bluez-libs bluez-libs-devel
   ```

## 🌐 Network Configuration

### WiFi Network Requirements

- **2.4GHz network** (Pico W doesn't support 5GHz)
- **WPA2 security** (WEP and open networks need code modifications)
- **Same subnet** for Go bridge and Pico W
- **No client isolation** enabled on router

### Firewall Configuration

1. **Allow HTTP traffic on port 80:**
   ```bash
   # Linux (ufw)
   sudo ufw allow 80
   
   # macOS/Windows - usually no changes needed for outgoing HTTP
   ```

2. **Router settings:**
   - Ensure AP isolation is disabled
   - Consider setting static IP for Pico W
   - Open port forwarding if accessing from outside network

### Network Troubleshooting

1. **Find Pico W IP:**
   ```bash
   # Network scan
   nmap -sn 192.168.1.0/24
   
   # Or check router admin panel
   ```

2. **Test connectivity:**
   ```bash
   ping 192.168.1.100
   curl http://192.168.1.100/
   ```

## 🎯 Device Discovery

### Finding Your Timeular Device Name

1. **Using the Go app:**
   ```bash
   go run main.go
   # Look for discovery messages in output
   ```

2. **Using smartphone BLE scanner:**
   - Install "BLE Scanner" app
   - Look for devices starting with "Timeular"
   - Note exact name including spaces/capitalization

3. **Common device names:**
   - "Timeular Tra"
   - "Timeular Tracker"
   - "Timeular" (older devices)

### Bluetooth Troubleshooting

1. **Device not found:**
   - Ensure Timeular is active (shake it)
   - Check it's not connected to other apps
   - Restart Bluetooth service
   - Move closer to computer

2. **Connection drops:**
   - Check power management settings
   - Ensure consistent power to Timeular
   - Avoid interference from other devices

## ⚙️ Performance Optimization

### Response Time Optimization

1. **Polling Interval:**
   ```go
   // Faster response (uses more battery)
   PollInterval: 250 * time.Millisecond
   
   // Balanced (default)
   PollInterval: 500 * time.Millisecond
   
   // Power saving
   PollInterval: 1000 * time.Millisecond
   ```

2. **Network Optimization:**
   - Use 5GHz network for Go bridge computer
   - Keep Pico W on 2.4GHz (required)
   - Minimize network hops between devices

### Power Management

1. **LED Matrix:**
   ```python
   # Reduce brightness to save power
   cu.set_brightness(0.3)  # 30% brightness
   ```

2. **Timeular Battery:**
   - Longer polling intervals extend battery life
   - Automatic sleep when not rotated for extended periods

## 🔒 Security Considerations

### Network Security

1. **HTTP vs HTTPS:**
   - Current implementation uses HTTP for simplicity
   - Consider HTTPS for production deployments
   - Network should be trusted (home/office)

2. **Access Control:**
   - No authentication on Pico W server
   - Consider adding basic auth for public networks
   - Use VPN for remote access

### Device Security

1. **Bluetooth Security:**
   - BLE uses encryption by default
   - Timeular doesn't expose sensitive data
   - Consider pairing if supported

2. **WiFi Security:**
   - Use WPA2 or WPA3 networks
   - Avoid open/public WiFi for production use

## 📈 Scaling and Extensions

### Multiple Displays

Configure multiple Pico W servers:

```go
displays := []string{
    "http://192.168.1.100", // Kitchen
    "http://192.168.1.101", // Office  
    "http://192.168.1.102", // Living room
}

for _, display := range displays {
    go updateDisplay(display, side, color)
}
```

### Multiple Timeular Devices

Support multiple trackers:

```go
devices := []timeular.Config{
    {Name: "Timeular Tra", PollInterval: 500 * time.Millisecond},
    {Name: "Timeular Pro", PollInterval: 500 * time.Millisecond},
}

for _, config := range devices {
    device := timeular.NewDeviceWithConfig(config)
    // Set up handlers...
}
```

### Integration Services

1. **Home Automation:**
   - Home Assistant integration
   - OpenHAB support
   - Node-RED flows

2. **Cloud Services:**
   - AWS IoT integration
   - Azure IoT Hub
   - Google Cloud IoT

3. **Productivity Tools:**
   - Slack status updates
   - Toggl time tracking
   - Calendar integration

## 🎓 Next Steps

After successful setup:

1. **Customize color mapping** for your workflow
2. **Add logging and analytics** for usage patterns
3. **Integrate with other services** (Slack, calendar, etc.)
4. **Create automation rules** based on activity patterns
5. **Extend to multiple displays** for different rooms
6. **Build additional features** like timers or alerts

## 📚 Additional Resources

- [Bartolome BLE Toolkit Documentation](https://github.com/coded-aesthetics/bartolome-ble-toolkit)
- [Pimoroni Cosmic Unicorn Guide](https://shop.pimoroni.com/products/space-unicorns?variant=40842626236499)
- [MicroPython Documentation](https://docs.micropython.org/)
- [Timeular API Documentation](https://developers.timeular.com/)
- [Go Bluetooth Libraries](https://github.com/tinygo-org/bluetooth)

Your physical-digital bridge is now ready to provide real-time visual feedback for your daily activities!
