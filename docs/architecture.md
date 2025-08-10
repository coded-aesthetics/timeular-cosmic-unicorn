# Architecture Documentation

Technical architecture and design decisions for the Timeular to Cosmic Unicorn bridge system.

## 🏗️ System Overview

The system implements a **event-driven, distributed architecture** that bridges physical interactions with digital displays through multiple communication protocols.

```
┌─────────────────┐    BLE     ┌─────────────────┐    HTTP    ┌─────────────────┐
│   Timeular      │◄──────────►│   Go Bridge     │◄──────────►│   Pico W        │
│   Tracker       │  (Notify)  │   Application   │  (GET)     │   Server        │
│   (Physical)    │            │   (Logic)       │            │   (Display)     │
└─────────────────┘            └─────────────────┘            └─────────────────┘
         │                               │                               │
         ▼                               ▼                               ▼
    Orientation                   Side Detection                  LED Matrix
    Detection                   & HTTP Requests                   Rendering
```

## 🔄 Data Flow Architecture

### Event-Driven Processing Pipeline

1. **Physical Event**: User rotates Timeular tracker
2. **Sensor Processing**: Internal accelerometer detects orientation change
3. **BLE Broadcast**: Timeular sends notification with new side data
4. **Event Reception**: Go bridge receives BLE notification
5. **Data Validation**: Bridge validates side number (1-8)
6. **HTTP Translation**: Bridge converts to HTTP GET request
7. **Network Transport**: Request sent over WiFi to Pico W
8. **Request Processing**: Pico W parses query parameters
9. **Display Rendering**: LED matrix displays corresponding digit
10. **Visual Feedback**: User sees immediate visual confirmation

### Timing Characteristics

- **BLE Notification Latency**: 10-50ms
- **Go Processing Time**: 1-5ms
- **Network Transmission**: 5-20ms
- **Pico W Processing**: 10-30ms
- **LED Rendering**: 10-50ms
- **Total System Latency**: 40-150ms (typically <100ms)

## 🧩 Component Architecture

### Timeular Tracker (Physical Layer)

**Technology**: Bluetooth Low Energy (BLE) device with embedded sensors

**Responsibilities**:
- Orientation detection via accelerometer
- Side calculation and validation
- BLE GATT service advertisement
- Low-power operation management

**Technical Details**:
```
Service UUID: c7e70010-c847-11e6-8175-8c89a55d403c
Characteristic UUID: c7e70011-c847-11e6-8175-8c89a55d403c
Data Format: Binary payload with side information
Update Frequency: Event-driven (on orientation change)
Power Profile: Ultra-low power with sleep modes
```

### Go Bridge Application (Logic Layer)

**Technology**: Go with Bartolome BLE Toolkit

**Responsibilities**:
- BLE device discovery and connection management
- Protocol translation (BLE → HTTP)
- Error handling and reconnection logic
- Side change event processing
- HTTP client for API calls

**Key Components**:

```go
// Core Architecture
type BridgeApplication struct {
    bleManager     *ble.Manager
    timeularDevice *timeular.Device
    httpClient     *http.Client
    config         *Config
}

// Event Processing Pipeline
func (app *BridgeApplication) handleSideChange(side byte) error {
    // 1. Validate input
    if !timeular.IsValidSide(side) {
        return ErrInvalidSide
    }
    
    // 2. Transform data
    request := buildHTTPRequest(side, app.config)
    
    // 3. Send to display
    return app.sendDisplayUpdate(request)
}
```

**Concurrency Model**:
- **Main Goroutine**: Event loop and signal handling
- **BLE Goroutine**: Bluetooth communication and callbacks
- **HTTP Goroutines**: Non-blocking HTTP requests (optional)

### Pico W Server (Display Layer)

**Technology**: MicroPython with Pimoroni libraries

**Responsibilities**:
- WiFi connectivity and network services
- HTTP server implementation
- LED matrix control and rendering
- Query parameter parsing
- Web interface serving

**Server Architecture**:

```python
# Request Processing Pipeline
class DisplayServer:
    def handle_request(self, request):
        # 1. Parse HTTP request
        params = self.parse_query_params(request)
        
        # 2. Validate parameters
        if not self.validate_params(params):
            return self.error_response()
        
        # 3. Update display
        self.update_led_display(params)
        
        # 4. Send response
        return self.success_response()
```

**Memory Management**:
- **Heap Usage**: Carefully managed due to Pico W limitations
- **String Processing**: Minimal string manipulation
- **Graphics Buffers**: Efficient pixel buffer management
- **Connection Handling**: Immediate cleanup after requests

## 🌐 Network Architecture

### Protocol Stack

```
Application Layer    │ HTTP/1.1 GET Requests
Transport Layer      │ TCP (for HTTP)
Network Layer        │ IPv4
Data Link Layer      │ 802.11 (WiFi) + Ethernet
Physical Layer       │ 2.4GHz Radio + Wired
```

### Network Topology

```
Internet
    │
    ▼
┌─────────────┐     WiFi      ┌─────────────┐     USB/WiFi   ┌─────────────┐
│   Router    │◄─────────────►│  Computer   │◄──────────────►│   Devices   │
│   (Gateway) │               │  (Bridge)   │                │  (Mobile)   │
└─────────────┘               └─────────────┘                └─────────────┘
       ▲                             │
       │                             ▼
       │                      ┌─────────────┐
       │            WiFi      │   Pico W    │
       └─────────────────────►│  (Server)   │
                              └─────────────┘
```

### Communication Patterns

1. **BLE Communication** (Timeular ↔ Go Bridge):
   - **Pattern**: Publish-Subscribe with notifications
   - **Frequency**: Event-driven (0.1-10 Hz typical)
   - **Reliability**: Best-effort with automatic reconnection
   - **Security**: BLE encryption + device pairing

2. **HTTP Communication** (Go Bridge ↔ Pico W):
   - **Pattern**: Request-Response (RESTful)
   - **Frequency**: Matches BLE events (0.1-10 Hz)
   - **Reliability**: TCP with retries
   - **Security**: Unencrypted HTTP (trusted network)

## 🔧 Design Patterns and Principles

### Event-Driven Architecture

**Observer Pattern Implementation**:
```go
// Publisher: Timeular device
type SideChangeHandler func(deviceName string, side byte) error

// Subscriber: Bridge application
device.OnSideChange(func(deviceName string, side byte) error {
    return bridgeApp.handleSideChange(side)
})
```

**Benefits**:
- **Loose Coupling**: Components don't directly depend on each other
- **Scalability**: Easy to add new event handlers
- **Responsiveness**: Events processed immediately
- **Resilience**: Component failures don't cascade

### Protocol Translation Pattern

**Adapter Pattern for Protocol Conversion**:
```go
type ProtocolAdapter interface {
    TranslateBLEToHTTP(bleData []byte) (*http.Request, error)
    TranslateHTTPResponse(*http.Response) error
}

type TimeularAdapter struct {
    picoIP string
    client *http.Client
}

func (a *TimeularAdapter) TranslateBLEToHTTP(side byte) (*http.Request, error) {
    url := fmt.Sprintf("http://%s/?num=%d", a.picoIP, side)
    return http.NewRequest("GET", url, nil)
}
```

### Resource Management Pattern

**RAII (Resource Acquisition Is Initialization)**:
```go
func (m *Manager) ConnectDevices(configs []DeviceConfig) error {
    // Acquire resources
    for _, config := range configs {
        device, err := m.connect(config)
        if err != nil {
            m.cleanup() // Release acquired resources
            return err
        }
        m.devices = append(m.devices, device)
    }
    
    // Set up cleanup on program termination
    signal.Notify(m.sigChan, syscall.SIGTERM, syscall.SIGINT)
    go m.gracefulShutdown()
    
    return nil
}
```

## 🔒 Security Architecture

### Threat Model

**Assets**:
- Network communications
- Device access
- Display content
- System availability

**Threats**:
- Unauthorized network access
- BLE eavesdropping/injection
- HTTP request spoofing
- Denial of service attacks

**Mitigations**:

1. **Network Security**:
   ```python
   # Basic request validation
   def validate_request(self, request):
       # Rate limiting
       if self.is_rate_limited(client_ip):
           return False
       
       # Parameter validation
       if not self.validate_parameters(params):
           return False
       
       return True
   ```

2. **BLE Security**:
   ```go
   // Device authentication
   func (d *Device) authenticate() error {
       // Verify device characteristics
       if !d.verifyServiceUUID() {
           return ErrInvalidDevice
       }
       return nil
   }
   ```

### Security Boundaries

```
Untrusted Network    │ Trusted LAN          │ Device Internal
                     │                      │
External Internet ──→│ Router/Firewall ────→│ Go Bridge
                     │      ↓               │      ↓
                     │ Pico W Server ←──────│ BLE Stack
```

## 📊 Performance Architecture

### Scalability Characteristics

**Horizontal Scaling**:
- **Multiple Displays**: O(n) scaling for additional Pico W servers
- **Multiple Trackers**: O(n) scaling for additional Timeular devices
- **Geographic Distribution**: No inherent limitations

**Vertical Scaling**:
- **CPU**: Single-threaded BLE, multi-threaded HTTP
- **Memory**: Constant memory usage per device
- **Network**: Bandwidth scales with update frequency

### Performance Metrics

**Latency Requirements**:
- **Target**: <100ms end-to-end
- **Acceptable**: <200ms
- **Poor Experience**: >500ms

**Throughput Characteristics**:
- **BLE Events**: 0.1-10 Hz (user-dependent)
- **HTTP Requests**: Matches BLE frequency
- **Network Bandwidth**: <1 KB/s typical

**Resource Utilization**:
```go
// Memory usage patterns
type ResourceMetrics struct {
    GoHeapSize      int64  // ~10-50 MB typical
    PicoWRAM        int32  // ~100-200 KB typical
    NetworkSockets  int    // 1-2 active connections
    BLEConnections  int    // 1 per Timeular device
}
```

### Optimization Strategies

1. **Polling Optimization**:
   ```go
   // Adaptive polling based on activity
   func (d *Device) adjustPollInterval(activity ActivityLevel) {
       switch activity {
       case HighActivity:
           d.pollInterval = 250 * time.Millisecond
       case MediumActivity:
           d.pollInterval = 500 * time.Millisecond
       case LowActivity:
           d.pollInterval = 1000 * time.Millisecond
       }
   }
   ```

2. **Connection Pooling**:
   ```go
   // Reuse HTTP connections
   client := &http.Client{
       Transport: &http.Transport{
           MaxIdleConns:        10,
           IdleConnTimeout:     30 * time.Second,
           DisableCompression:  true,
       },
   }
   ```

3. **Memory Optimization**:
   ```python
   # Pico W memory management
   def cleanup_resources(self):
       gc.collect()  # Force garbage collection
       self.close_unused_connections()
       self.clear_display_cache()
   ```

## 🔄 Reliability Architecture

### Fault Tolerance Patterns

**Circuit Breaker Pattern**:
```go
type CircuitBreaker struct {
    failures    int
    maxFailures int
    timeout     time.Duration
    lastFailure time.Time
    state       CircuitState
}

func (cb *CircuitBreaker) Call(fn func() error) error {
    if cb.state == Open && time.Since(cb.lastFailure) < cb.timeout {
        return ErrCircuitOpen
    }
    
    err := fn()
    if err != nil {
        cb.recordFailure()
        return err
    }
    
    cb.reset()
    return nil
}
```

**Retry with Exponential Backoff**:
```go
func (app *BridgeApplication) sendWithRetry(request *http.Request) error {
    backoff := time.Second
    for attempt := 0; attempt < MaxRetries; attempt++ {
        if err := app.sendRequest(request); err == nil {
            return nil
        }
        
        time.Sleep(backoff)
        backoff *= 2 // Exponential backoff
    }
    return ErrMaxRetriesExceeded
}
```

### Recovery Mechanisms

1. **Automatic Reconnection**:
   ```go
   func (m *Manager) handleDisconnection(device *Device) {
       go func() {
           for {
               if err := m.reconnect(device); err == nil {
                   break
               }
               time.Sleep(ReconnectInterval)
           }
       }()
   }
   ```

2. **Health Monitoring**:
   ```python
   # Pico W health checks
   def monitor_system_health(self):
       while True:
           self.check_memory_usage()
           self.check_network_connectivity()
           self.check_display_functionality()
           time.sleep(HealthCheckInterval)
   ```

## 🔮 Future Architecture Considerations

### Extensibility Points

1. **Plugin Architecture**:
   ```go
   type DisplayPlugin interface {
       Name() string
       HandleEvent(event Event) error
       Configure(config map[string]interface{}) error
   }
   
   // Support for multiple display types
   plugins := []DisplayPlugin{
       NewCosmicUnicornPlugin(),
       NewE-InkPlugin(),
       NewLCDPlugin(),
   }
   ```

2. **Message Bus Integration**:
   ```go
   // MQTT/Event streaming support
   type EventBus interface {
       Publish(topic string, event Event) error
       Subscribe(topic string, handler EventHandler) error
   }
   ```

3. **Cloud Integration**:
   ```go
   // IoT platform integration
   type CloudConnector interface {
       SendTelemetry(data TelemetryData) error
       ReceiveCommands() (<-chan Command, error)
   }
   ```

This architecture provides a solid foundation for a responsive, scalable, and maintainable IoT system that bridges physical interactions with digital displays.
