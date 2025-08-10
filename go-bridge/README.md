# Go Bridge Application

This Go application serves as the bridge between your Timeular tracker (via Bluetooth Low Energy) and the Pico W server (via HTTP).

## 🚀 Quick Start

1. **Install Go** (version 1.21 or later)
   - Download from [golang.org](https://golang.org/downloads/)

2. **Install dependencies:**
   ```bash
   go mod tidy
   ```

3. **Configure the application:**
   - Open `main.go`
   - Update `PICO_W_IP` with your Pico W's IP address
   - Update `TIMEULAR_NAME` if your device has a different name

4. **Run the bridge:**
   ```bash
   go run main.go
   ```

## ⚙️ Configuration

### Key Constants in `main.go`:

```go
const (
    // Update this with your Pico W's IP address
    PICO_W_IP = "192.168.0.185"
    
    // Timeular device name - check your device's exact name
    TIMEULAR_NAME = "Timeular Tra"
    
    // Polling interval for responsiveness
    POLL_INTERVAL = 500 * time.Millisecond
)
```

### Color Mapping

The `getColorForSide()` function maps Timeular sides to LED colors:

```go
func getColorForSide(side byte) string {
    switch side {
    case 1, 2, 3:
        return "green" // Work/Focus time
    case 4, 5, 6:
        return "red"   // Break/Personal time
    case 7, 8:
        return "white" // Meetings/Other
    default:
        return "white" // Default color
    }
}
```

Customize this mapping to match your workflow!

## 🔧 Troubleshooting

### Bluetooth Issues

**"Device not found":**
- Ensure Timeular is powered on (shake it or place on side)
- Check that Timeular isn't connected to other apps
- Verify the device name matches exactly

**"Permission denied":**
- On macOS: System Settings → Privacy & Security → Bluetooth
- On Linux: Run with `sudo` or add user to `bluetooth` group
- On Windows: Ensure Bluetooth permissions are granted

### Network Issues

**"Connection refused":**
- Verify Pico W IP address is correct
- Ensure both devices are on the same WiFi network
- Check that Pico W server is running

**"Timeout":**
- Check WiFi signal strength
- Verify firewall isn't blocking port 80

### Device Discovery

**Finding your Timeular device name:**
```bash
# Run the app and look for device discovery messages
go run main.go

# Or use a BLE scanner app on your phone to find the exact name
```

## 📊 Monitoring

The application provides detailed logging:

- `🔍` Device discovery
- `🎲` Side changes detected
- `✅` Successful LED updates
- `❌` Error conditions
- `⚠️` Warnings and reconnections

## 🔄 Auto-Reconnection

The bridge automatically handles:
- Bluetooth disconnections
- Network timeouts
- Device going to sleep
- WiFi interruptions

No manual intervention needed - just leave it running!

## 🚀 Advanced Usage

### Multiple Pico W Displays

To control multiple LED displays, modify the side change handler:

```go
timeularDevice.OnSideChange(func(deviceName string, side byte) error {
    displays := []string{
        "192.168.1.100", // Kitchen
        "192.168.1.101", // Office
        "192.168.1.102", // Living room
    }
    
    for _, ip := range displays {
        go func(displayIP string) {
            url := fmt.Sprintf("http://%s/?num=%d", displayIP, side)
            http.Get(url)
        }(ip)
    }
    
    return nil
})
```

### Logging to File

Add file logging for debugging:

```go
logFile, err := os.OpenFile("timeular-bridge.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
if err == nil {
    log.SetOutput(logFile)
    defer logFile.Close()
}
```

### Integration with Other Services

Send side changes to multiple services:

```go
timeularDevice.OnSideChange(func(deviceName string, side byte) error {
    // Update LED display
    http.Get(fmt.Sprintf("http://%s/?num=%d", PICO_W_IP, side))
    
    // Log to analytics service
    http.Post("https://api.analytics.com/events", "application/json", body)
    
    // Update Slack status
    updateSlackStatus(side)
    
    return nil
})
```

## 📚 Dependencies

- **[Bartolome BLE Toolkit](https://github.com/coded-aesthetics/bartolome-ble-toolkit)** - Handles all BLE communication
- **Go standard library** - HTTP client and signal handling
