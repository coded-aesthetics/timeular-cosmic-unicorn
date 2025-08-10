# Timeular to Cosmic Unicorn Bridge

A real-time IoT project that connects your Timeular tracker to a Cosmic Unicorn 32x32 LED matrix display via Bluetooth Low Energy and WiFi.

![Project Demo](https://img.shields.io/badge/Status-Working-brightgreen) ![Platform](https://img.shields.io/badge/Platform-Go%20%7C%20MicroPython-blue) ![License](https://img.shields.io/badge/License-MIT-green)

## 🎯 What This Does

Rotate your Timeular tracker → See the side number instantly appear as a large, colorful digit on the LED matrix!

Check this blog post for more info: [https://www.coded-aesthetics.com/posts/control-cosmic-unicorn-with-timeular/](https://www.coded-aesthetics.com/posts/control-cosmic-unicorn-with-timeular/)

## 🏗️ Architecture

```
[Timeular Tracker] --BLE--> [Go Bridge App] --HTTP--> [Pico W Server] --GPIO--> [LED Matrix]
     (Physical)           (Computer)              (WiFi/Web)           (Display)
```

## 🛠️ Hardware Requirements

- **Timeular Tracker** - Any generation of the octagonal time tracker
- **Raspberry Pi Pico W** - Microcontroller with WiFi
- **Pimoroni Cosmic Unicorn** - 32x32 RGB LED matrix display
- **Computer with Bluetooth** - To run the Go bridge application

## 🚀 Quick Start

### 1. Set Up the LED Display Server

1. Flash MicroPython on your Pico W:
   - Download the [latest MicroPython UF2 for Pico W](https://micropython.org/download/rp2-pico-w/)
   - Hold BOOTSEL button while connecting USB, copy UF2 file

2. Install Pimoroni libraries:
   ```bash
   # Using Thonny IDE or your preferred MicroPython tool
   # Install: pimoroni-cosmic-unicorn
   ```

3. Upload the server code:
   ```bash
   # Copy pico-w-server/main.py to your Pico W
   # Update WiFi credentials in the file
   ```

### 2. Run the Go Bridge Application

1. Install dependencies:
   ```bash
   cd go-bridge
   go mod tidy
   ```

2. Update the Pico W IP address in `main.go`:
   ```go
   picoURL := "http://YOUR_PICO_IP"  // Update this line
   ```

3. Run the bridge:
   ```bash
   go run main.go
   ```

4. Turn on your Timeular tracker and start rotating!

## 📁 Project Structure

```
timeular-cosmic-unicorn/
├── README.md                 # This file
├── go-bridge/               # Go application for BLE → HTTP bridge
│   ├── main.go             # Main bridge application
│   ├── go.mod              # Go module dependencies
│   └── README.md           # Go-specific instructions
├── pico-w-server/          # MicroPython server for Pico W
│   ├── main.py             # LED matrix web server
│   ├── README.md           # Pico W setup instructions
│   └── wifi-config.py      # WiFi configuration template
└── docs/                   # Documentation
    ├── setup-guide.md      # Detailed setup instructions
    ├── troubleshooting.md  # Common issues and solutions
    └── architecture.md     # Technical architecture details
```

## 🌟 Features

- **Real-time Response** - Sub-100ms latency from rotation to display
- **Automatic Reconnection** - Handles BLE disconnections gracefully
- **Color Support** - Different colors for different sides
- **Web Interface** - Control the display via web browser
- **Robust Error Handling** - Graceful degradation when components fail
- **Cross-Platform** - Works on Windows, macOS, and Linux

## 🎨 Customization

### Color-Coded Sides

Modify the Go bridge to assign colors based on activity:

```go
var color string
switch side {
case 1, 2, 3:
    color = "green"  // Work tasks
case 4, 5, 6:
    color = "red"    // Break time
default:
    color = "white"  // Other activities
}
```

### Multiple Displays

Scale to control multiple LED matrices:

```go
displays := []string{
    "http://192.168.1.100",  // Kitchen
    "http://192.168.1.101",  // Office
    "http://192.168.1.102",  // Living room
}
```

## 🔧 API Reference

### Pico W Server Endpoints

- `GET /?num=5` - Display white "5"
- `GET /?num=3&color=red` - Display red "3"
- `GET /?num=7&color=green` - Display green "7"

Supported colors: `red`, `green`, `white`

## 🐛 Troubleshooting

### Common Issues

**Bluetooth not connecting:**
- Ensure Timeular is powered on and not connected to other apps
- Check Bluetooth permissions for the Go application
- Try restarting Bluetooth service

**HTTP requests failing:**
- Verify Pico W and computer are on same network
- Check firewall settings on port 80
- Confirm Pico W IP address is correct

**LED display not updating:**
- Check power supply to LED matrix
- Verify MicroPython libraries are installed
- Monitor Pico W serial output for errors

See [docs/troubleshooting.md](docs/troubleshooting.md) for detailed solutions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Bartolome BLE Toolkit](https://github.com/coded-aesthetics/bartolome-ble-toolkit) - Excellent BLE device management
- [Pimoroni](https://pimoroni.com/) - Amazing LED matrix hardware
- [Timeular](https://timeular.com/) - Innovative time tracking device
- [MicroPython](https://micropython.org/) - Python for microcontrollers

## 🔗 Related Projects

- [Bartolome BLE Toolkit](https://github.com/coded-aesthetics/bartolome-ble-toolkit) - Go library for BLE devices
- [Pimoroni Cosmic Unicorn Examples](https://github.com/pimoroni/pimoroni-pico) - Official examples

---

**Built with ❤️ for the maker community**

*Turn your physical interactions into beautiful digital displays!*
