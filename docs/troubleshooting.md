# Troubleshooting Guide

Common issues and solutions for the Timeular to Cosmic Unicorn bridge system.

## 🔍 Diagnostic Steps

### Quick Health Check

Run these commands to verify system status:

```bash
# 1. Test Pico W connectivity
ping 192.168.1.100

# 2. Test HTTP API
curl "http://192.168.1.100/?num=5"

# 3. Test Go bridge compilation
cd go-bridge && go build

# 4. Check Bluetooth status
# macOS: System Settings → Bluetooth
# Linux: systemctl status bluetooth
# Windows: Device Manager → Bluetooth
```

## 🔌 Bluetooth/BLE Issues

### "Device not found" or "Timeular not discovered"

**Symptoms:**
- Go bridge shows "Searching for Timeular tracker..." indefinitely
- No BLE devices detected

**Solutions:**

1. **Verify Timeular is active:**
   ```bash
   # Shake the Timeular device or place it on a different side
   # Look for LED indication or vibration feedback
   ```

2. **Check device name exactly:**
   ```go
   // Try different common names
   TIMEULAR_NAME = "Timeular"
   TIMEULAR_NAME = "Timeular Tra"
   TIMEULAR_NAME = "Timeular Tracker"
   ```

3. **Restart Bluetooth:**
   ```bash
   # macOS
   sudo pkill bluetoothd
   
   # Linux
   sudo systemctl restart bluetooth
   
   # Windows
   # Device Manager → Bluetooth → Disable/Enable
   ```

4. **Check permissions:**
   ```bash
   # macOS: System Settings → Privacy & Security → Bluetooth
   # Add Terminal or your IDE to allowed apps
   
   # Linux: Add user to bluetooth group
   sudo usermod -a -G bluetooth $USER
   ```

### "Connection timeout" or frequent disconnections

**Symptoms:**
- Device connects but drops connection frequently
- Timeouts during BLE communication

**Solutions:**

1. **Reduce distance:**
   - Keep Timeular within 5 meters of computer
   - Remove obstacles between devices

2. **Check for interference:**
   ```bash
   # Turn off other Bluetooth devices temporarily
   # Move away from WiFi routers, microwaves
   # Try different USB ports for Bluetooth adapter
   ```

3. **Adjust polling interval:**
   ```go
   // Reduce frequency to improve stability
   PollInterval: 1000 * time.Millisecond  // 1 second instead of 500ms
   ```

4. **Power management:**
   ```bash
   # Linux: Disable power management for Bluetooth
   echo 'ACTION=="add", SUBSYSTEM=="usb", ATTRS{idVendor}=="1d6b", ATTRS{idProduct}=="0002", TEST=="power/control", ATTR{power/control}="on"' | sudo tee /etc/udev/rules.d/50-usb_power_save.rules
   
   # macOS: Energy Saver → Prevent computer from sleeping
   ```

### "Permission denied" errors

**Symptoms:**
- Go application crashes with permission errors
- Cannot access Bluetooth adapter

**Solutions:**

1. **Run with elevated permissions (temporary):**
   ```bash
   sudo go run main.go  # Not recommended for production
   ```

2. **Fix permissions properly:**
   ```bash
   # Linux
   sudo usermod -a -G bluetooth $USER
   sudo usermod -a -G dialout $USER
   logout  # Log out and back in
   
   # macOS
   # System Settings → Privacy & Security → Bluetooth
   # Add your terminal application
   ```

## 🌐 Network/WiFi Issues

### "WiFi connection failed" on Pico W

**Symptoms:**
- Pico W serial output shows connection failure
- Cannot reach web interface

**Solutions:**

1. **Verify WiFi credentials:**
   ```python
   # Check for typos, case sensitivity
   SSID = "MyWiFi"      # Exact name
   PASSWORD = "pass123"  # Exact password
   ```

2. **Check network requirements:**
   - **2.4GHz only** (Pico W doesn't support 5GHz)
   - **WPA2 security** (avoid WEP/open networks)
   - **No hidden SSID** (or update code to handle)

3. **Network diagnostics:**
   ```bash
   # Test from another device
   iwlist scan | grep "MyWiFi"
   
   # Check signal strength
   iwconfig wlan0
   ```

4. **Router configuration:**
   ```bash
   # Check MAC address filtering is disabled
   # Verify network has DHCP enabled
   # Ensure guest network isolation is off
   ```

### "Cannot reach Pico W server" from Go bridge

**Symptoms:**
- HTTP requests to Pico W fail
- curl commands time out

**Solutions:**

1. **Verify IP address:**
   ```bash
   # Check Pico W serial output for correct IP
   # Or scan network
   nmap -sn 192.168.1.0/24
   ```

2. **Test connectivity:**
   ```bash
   ping 192.168.1.100
   telnet 192.168.1.100 80
   curl -v http://192.168.1.100/
   ```

3. **Check firewall:**
   ```bash
   # Temporarily disable firewall for testing
   # Linux
   sudo ufw disable
   
   # macOS
   # System Settings → Network → Firewall → Off
   ```

4. **Network configuration:**
   ```bash
   # Ensure devices are on same subnet
   ip route show  # Linux/macOS
   route print    # Windows
   ```

### "Connection refused" or timeout errors

**Symptoms:**
- Go bridge cannot connect to Pico W
- HTTP requests fail immediately

**Solutions:**

1. **Verify Pico W server is running:**
   ```python
   # Check serial output for startup messages
   # Look for "Server running on http://..."
   ```

2. **Test with browser:**
   ```bash
   # Open http://192.168.1.100 in web browser
   # Should show web interface
   ```

3. **Check port availability:**
   ```bash
   # Verify nothing else is using port 80
   netstat -tlnp | grep :80
   ```

## 🎨 LED Display Issues

### "Display not responding" or blank screen

**Symptoms:**
- LED matrix remains dark
- No visual response to commands

**Solutions:**

1. **Check power supply:**
   ```python
   # LED matrix requires significant power
   # Use quality USB cable
   # Consider external power supply for full brightness
   ```

2. **Test with simple pattern:**
   ```python
   # Add to main.py for testing
   graphics.set_pen(graphics.create_pen(255, 0, 0))
   graphics.clear()
   cu.update(graphics)  # Should show solid red
   ```

3. **Verify connections:**
   ```bash
   # Check Pico W is properly seated on Cosmic Unicorn
   # Ensure no loose connections
   # Test with known working code
   ```

4. **Library issues:**
   ```python
   # Reinstall Pimoroni libraries
   # Check MicroPython version compatibility
   # Try different examples from Pimoroni
   ```

### "Corrupted display" or strange patterns

**Symptoms:**
- Digits appear garbled
- Random pixels lighting up
- Colors incorrect

**Solutions:**

1. **Power stability:**
   ```python
   # Reduce brightness
   cu.set_brightness(0.2)
   
   # Use external power supply
   # Check USB cable quality
   ```

2. **Timing issues:**
   ```python
   # Add delays between operations
   time.sleep(0.1)
   cu.update(graphics)
   ```

3. **Memory issues:**
   ```python
   # Restart Pico W regularly
   # Simplify display patterns
   # Check available RAM
   import gc
   print(f"Free memory: {gc.mem_free()}")
   ```

### "Colors incorrect" or "Display too dim/bright"

**Symptoms:**
- Colors don't match expectations
- Display too bright or too dim

**Solutions:**

1. **Brightness adjustment:**
   ```python
   # Adjust brightness (0.0 to 1.0)
   cu.set_brightness(0.5)  # 50% brightness
   ```

2. **Color calibration:**
   ```python
   # Test different color values
   RED = graphics.create_pen(255, 0, 0)    # Full red
   GREEN = graphics.create_pen(0, 255, 0)  # Full green
   BLUE = graphics.create_pen(0, 0, 255)   # Full blue
   ```

3. **Power-related color issues:**
   ```python
   # Lower brightness for more accurate colors
   cu.set_brightness(0.3)
   # Use adequate power supply
   ```

## 🔧 Go Application Issues

### "Module not found" or dependency errors

**Symptoms:**
- `go run main.go` fails with import errors
- Cannot find Bartolome BLE toolkit

**Solutions:**

1. **Initialize Go module:**
   ```bash
   cd go-bridge
   go mod init timeular-cosmic-unicorn
   go mod tidy
   ```

2. **Update dependencies:**
   ```bash
   go get github.com/coded-aesthetics/bartolome-ble-toolkit@latest
   go mod download
   ```

3. **Check Go version:**
   ```bash
   go version  # Should be 1.21 or later
   ```

4. **Clear module cache:**
   ```bash
   go clean -modcache
   go mod download
   ```

### "Build errors" or compilation failures

**Symptoms:**
- Go build fails with syntax errors
- Missing symbols or functions

**Solutions:**

1. **Check Go version compatibility:**
   ```bash
   # Ensure Go 1.21+
   go version
   
   # Update if necessary
   # Download from https://golang.org/downloads/
   ```

2. **Verify source code:**
   ```bash
   go fmt ./...  # Format code
   go vet ./...  # Check for issues
   ```

3. **Clean build:**
   ```bash
   go clean
   go build -v
   ```

### "Runtime panic" or crashes

**Symptoms:**
- Go application crashes with panic
- Stack trace errors

**Solutions:**

1. **Check error handling:**
   ```go
   // Add debug logging
   fmt.Printf("Debug: Attempting to connect to %s\n", PICO_W_IP)
   
   // Add error checks
   if err != nil {
       log.Printf("Error: %v", err)
       return
   }
   ```

2. **Timeout configuration:**
   ```go
   // Increase HTTP timeout
   client := &http.Client{
       Timeout: 10 * time.Second,
   }
   ```

3. **Memory issues:**
   ```go
   // Check for memory leaks
   // Ensure proper resource cleanup
   defer response.Body.Close()
   ```

## 📱 Timeular Device Issues

### "Invalid side detected" warnings

**Symptoms:**
- Go bridge shows invalid side warnings
- Inconsistent side detection

**Solutions:**

1. **Calibrate Timeular:**
   ```bash
   # Use official Timeular app to calibrate
   # Ensure device is on flat surface
   # Check for physical damage
   ```

2. **Adjust validation:**
   ```go
   // Relax validation temporarily for debugging
   if side >= 1 && side <= 8 {  // Standard validation
       // Process side
   }
   ```

3. **Check device orientation:**
   ```bash
   # Ensure Timeular is placed correctly
   # Each face should be clearly flat against surface
   # Avoid tilted or unstable surfaces
   ```

### "Battery issues" or device not responding

**Symptoms:**
- Timeular doesn't activate
- Intermittent connectivity
- Device powers off unexpectedly

**Solutions:**

1. **Charge device:**
   ```bash
   # Use original charging cable
   # Charge for at least 2 hours
   # Check charging LED indicator
   ```

2. **Reset device:**
   ```bash
   # Follow Timeular manual for reset procedure
   # Usually involves specific rotation sequence
   # May need to re-pair after reset
   ```

3. **Check for updates:**
   ```bash
   # Use official Timeular app
   # Check for firmware updates
   # Update if available
   ```

## 🔄 System Integration Issues

### "Delayed response" or slow updates

**Symptoms:**
- Display updates slowly after rotation
- Noticeable lag between action and response

**Solutions:**

1. **Optimize polling:**
   ```go
   // Reduce polling interval
   PollInterval: 250 * time.Millisecond
   ```

2. **Network optimization:**
   ```bash
   # Use wired connection for Go bridge computer
   # Ensure strong WiFi signal for Pico W
   # Minimize network hops
   ```

3. **Remove debugging:**
   ```go
   // Comment out excessive logging
   // Remove unnecessary print statements
   ```

### "System becomes unresponsive"

**Symptoms:**
- Go bridge stops responding
- Pico W becomes unreachable
- Need to restart components

**Solutions:**

1. **Add monitoring:**
   ```go
   // Add health checks
   // Implement automatic restart logic
   // Monitor memory usage
   ```

2. **Resource management:**
   ```python
   # Restart Pico W periodically
   # Monitor memory on Pico W
   # Close unused connections
   ```

3. **Graceful shutdown:**
   ```go
   // Implement proper signal handling
   // Clean up resources on exit
   // Save state before shutdown
   ```

## 🐛 Advanced Debugging

### Enable Verbose Logging

1. **Go Bridge Debug Mode:**
   ```go
   // Add debug logging
   func debugLog(message string) {
       if DEBUG {
           log.Printf("[DEBUG] %s", message)
       }
   }
   ```

2. **Pico W Serial Monitoring:**
   ```python
   # Add detailed logging
   print(f"[DEBUG] Received request: {request_str[:100]}")
   print(f"[DEBUG] Parsed params: {params}")
   ```

### Network Packet Capture

```bash
# Capture HTTP traffic
sudo tcpdump -i any port 80 -w capture.pcap

# Analyze with Wireshark
wireshark capture.pcap
```

### BLE Protocol Analysis

```bash
# Linux: Monitor BLE traffic
sudo btmon

# macOS: Use Bluetooth Explorer (from Xcode)
# Windows: Use BLE scanner apps
```

## 📞 Getting Help

If you've tried the above solutions and still have issues:

1. **Gather diagnostic information:**
   - Operating system and version
   - Go version (`go version`)
   - Exact error messages
   - Hardware configuration
   - Network setup details

2. **Create a minimal test case:**
   - Isolate the issue to specific component
   - Test with simple examples
   - Document reproduction steps

3. **Check project resources:**
   - [GitHub Issues](https://github.com/coded-aesthetics/bartolome-ble-toolkit/issues)
   - [Bartolome Documentation](https://github.com/coded-aesthetics/bartolome-ble-toolkit)
   - [Pimoroni Support](https://shop.pimoroni.com/pages/technical-support)

4. **Community support:**
   - Raspberry Pi Foundation forums
   - MicroPython community
   - Go programming communities

Remember: Most issues are related to permissions, network configuration, or hardware connections. Start with the basics and work systematically through each component.
